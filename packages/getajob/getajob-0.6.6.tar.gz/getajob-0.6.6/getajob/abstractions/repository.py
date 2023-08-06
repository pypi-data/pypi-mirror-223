import typing as t
from datetime import datetime
from functools import wraps
from pydantic import BaseModel

from getajob.abstractions.models import BaseDataModel
from getajob.utils import generate_random_short_code, get_value_from_enum, update_dict
from getajob.exceptions import (
    KafkaEventTopicNotProvidedError,
    EntityNotFound,
    MissingParentKeyError,
)
from getajob.vendor.firestore.models import (
    FirestoreDocument,
    FirestorePagination,
    FirestoreFilters,
    FirestoreOrderBy,
    FirestorePaginatedResponse,
    FirestoreBatchAction,
    FirestoreBatchActionType,
    JoinAttribute,
    GetWithJoins,
    QueryWithJoins,
)
from getajob.vendor.firestore.repository import FirestoreDB
from getajob.vendor.kafka.models import (
    KafkaEventType,
    BaseKafkaMessage,
)
from .models import (
    PaginatedResponse,
    BaseDataModel,
    RepositoryDependencies,
)


def format_to_schema(
    document: FirestoreDocument, entity_model: t.Type[BaseModel]
) -> BaseDataModel:
    id_included_dict = {
        "id": document.id,
        **document.data,
    }
    return t.cast(BaseDataModel, entity_model(**id_included_dict))


def format_paginated_response(
    res: FirestorePaginatedResponse, entity_model: t.Optional[t.Type[BaseModel]] = None
):
    if entity_model is None:
        data = [
            {
                "id": doc.id,
                **doc.data,
            }
            for doc in res.results
        ]
    else:
        data = [format_to_schema(doc, entity_model) for doc in res.results]  # type: ignore
    return PaginatedResponse(data=data, next=res.start_after)  # type: ignore


def ensure_parent_keys(method):
    """
    This decorator ensures that the parent_collections parameter is provided
    when querying a sub-collection.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if not self.required_parent_keys:
            return method(self, *args, **kwargs)
        kwarg_parent_collections = kwargs.get("parent_collections", {})
        potential_arg_parent_collections = [
            arg for arg in args if isinstance(arg, dict)
        ]
        for key in self.required_parent_keys:
            if key not in kwarg_parent_collections and not any(
                key in arg for arg in potential_arg_parent_collections
            ):
                raise MissingParentKeyError(f"Missing parent key: {key}")
        return method(self, *args, **kwargs)

    return wrapper


def query_collection(
    db: FirestoreDB,
    collection_name: str,
    parent_collections: dict = {},
    entity_model: t.Optional[t.Type[BaseModel]] = None,
    filters: t.Optional[t.List[FirestoreFilters]] = None,
    order_by: t.Optional[FirestoreOrderBy] = None,
    pagination: FirestorePagination = FirestorePagination(),
):
    """
    This query method is kept outside of the base repository to allow for it to be used
    with any collection name. Otherwise, you would have to instantiantiate a repository
    to perform a query which confines broader queries across multiple collections.
    """
    res = db.query(
        parent_collections=parent_collections,
        collection_name=collection_name,
        filters=filters,
        order_by=order_by,
        pagination=pagination,
    )
    return format_paginated_response(res, entity_model)


def get_count_from_collection(
    db: FirestoreDB,
    collection_name: str,
    parent_collections: dict = {},
    filters: t.Optional[t.List[FirestoreFilters]] = None,
):
    return db.get_count_from_collection(parent_collections, collection_name, filters)


def query_subcollection(
    db: FirestoreDB,
    collection_name: str,
    entity_model: t.Optional[t.Type[BaseModel]] = None,
    filters: t.Optional[t.List[FirestoreFilters]] = None,
    order_by: t.Optional[FirestoreOrderBy] = None,
    pagination: FirestorePagination = FirestorePagination(),
):
    res = db.query_subcollection(
        collection_name=collection_name,
        filters=filters,
        order_by=order_by,
        pagination=pagination,
    )
    return format_paginated_response(res, entity_model)


def get_count_from_subcollection(
    db: FirestoreDB,
    collection_name: str,
    filters: t.Optional[t.List[FirestoreFilters]] = None,
):
    return db.get_count_from_subcollection_query(collection_name, filters)


class BaseRepository:
    """
    This is the base repository layer that sites between a context's repository and the database.
    It's purpose is to provide basic query function with a conversion to pydantic models.

    It also handles the relationship between collections and sub-collections and can
    be given a Kafka client and configuration to create event streams based on CRUD operations.

    A Collection is a root level document in firestore, such as a company or a user.
    A Sub-Collection is a document that is a child of a root level document, such as a company's recruiters.

    The parent_collections parameter is a dictionary of the parent collections and their ids.
    For example, if you are querying a company's recruiters, the parent_collections would be:
    {
        "companies": "company_id"
    }

    The required_parent_keys parameter is a list of the keys that must be in the parent_collections
    dictionary. This is used to ensure that the parent_collections are provided when querying a sub-collection.

    This class should not be used directly, but should be extended by the
    parent, multiple children, and single child repositories defined below.

    These 3 repository classes are then meant to be used by the context layer of the application.

    """

    def __init__(
        self,
        dependencies: RepositoryDependencies,
        required_parent_keys: t.Optional[t.List[str]] = None,
    ):
        self.db = dependencies.db
        self.collection_name = dependencies.collection_name
        self.entity_models = dependencies.entity_models
        self.kafka = dependencies.kafka
        self.kafka_event_config = dependencies.kafka_event_config
        self.required_parent_keys = required_parent_keys
        self.requesting_user_id = dependencies.user_id

        # If kafka client given but with no configuration, complain about it
        if self.kafka and not self.kafka_event_config:
            raise KafkaEventTopicNotProvidedError()

    def _produce_repository_kafka_event(
        self,
        event_type: KafkaEventType,
        object_id: str,
        parent_collections: dict = {},
        data: dict | None = None,
    ):
        if not self.kafka or not self.kafka_event_config:
            return
        event_enum = get_value_from_enum(
            value=event_type.value,
            enumeration=self.kafka_event_config.message_type_enum,
        )
        if not event_enum:
            return
        self.kafka.publish(
            topic=self.kafka_event_config.topic,
            message=BaseKafkaMessage(
                message_type=event_enum.value,
                requesting_user_id=self.requesting_user_id,
                object_id=object_id,
                parent_collections=parent_collections,
                data=data if data else None,
            ),
        )

    @ensure_parent_keys
    def get(
        self,
        doc_id: str,
        parent_collections: dict = {},
        internal_get_request: bool = False,
    ) -> BaseDataModel:
        res = self.db.get(parent_collections, self.collection_name, doc_id)
        if not internal_get_request:
            self._produce_repository_kafka_event(
                KafkaEventType.get, doc_id, parent_collections
            )
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def get_with_filters(
        self,
        doc_id: str,
        filters: t.List[FirestoreFilters],
        parent_collections: dict = {},
    ) -> BaseDataModel:
        res = self.db.get_with_filters(
            parent_collections, self.collection_name, doc_id, filters
        )
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def get_all(
        self,
        items_to_get: list[str],
        parent_collections: dict = {},
    ) -> t.Any:
        res = self.db.query(
            parent_collections=parent_collections,
            collection_name=self.collection_name,
            filters=[FirestoreFilters(field="id", operator="in", value=items_to_get)],
        )
        return format_paginated_response(res, self.entity_models.entity)

    @ensure_parent_keys
    def create(
        self,
        data: BaseModel,
        parent_collections: dict = {},
        provided_id: t.Optional[str] = None,
    ) -> BaseDataModel:
        data_dict = data.dict()
        data_dict.update(
            {
                "created": datetime.now(),
                "updated": datetime.now(),
            }
        )
        document_id = provided_id or generate_random_short_code()
        res = self.db.create(
            parent_collections=parent_collections,
            collection_name=self.collection_name,
            document_id=document_id,
            document_data=data_dict,
        )
        formatted_res = format_to_schema(res, self.entity_models.entity)
        self._produce_repository_kafka_event(
            KafkaEventType.create, res.id, parent_collections, formatted_res.dict()
        )
        return formatted_res

    @ensure_parent_keys
    def update(
        self,
        doc_id: str,
        data: BaseModel,
        parent_collections: dict = {},
    ) -> BaseDataModel:
        original_item = self.get(doc_id, parent_collections, True).dict()
        updated_item = update_dict(original_item, data.dict())
        updated_item["updated"] = datetime.now()
        res = self.db.update(
            parent_collections, self.collection_name, doc_id, updated_item
        )
        self._produce_repository_kafka_event(
            KafkaEventType.update, doc_id, parent_collections, updated_item
        )
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def delete(
        self,
        doc_id: str,
        parent_collections: dict = {},
    ) -> bool:
        deleted_object = self.get(doc_id, parent_collections, True)
        self._produce_repository_kafka_event(
            KafkaEventType.delete,
            doc_id,
            parent_collections,
            deleted_object.dict(),
        )
        return self.db.delete(parent_collections, self.collection_name, doc_id)

    @ensure_parent_keys
    def get_one_by_attribute(
        self,
        attribute: str,
        value: t.Any,
        parent_collections: dict = {},
    ) -> t.Union[BaseDataModel, None]:
        res = self.db.get_one_by_attribute(
            parent_collections, self.collection_name, attribute, value
        )
        return format_to_schema(res, self.entity_models.entity)

    @ensure_parent_keys
    def query(
        self,
        parent_collections: dict = {},
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
    ) -> t.Any:
        return query_collection(
            db=self.db,
            collection_name=self.collection_name,
            entity_model=self.entity_models.entity,
            parent_collections=parent_collections,
            filters=filters,
            order_by=order_by,
            pagination=pagination,
        )

    @ensure_parent_keys
    def get_count_from_collection(
        self,
        parent_collections: dict = {},
        filters: t.Optional[t.List[FirestoreFilters]] = None
    ) -> int:
        return get_count_from_collection(
            db=self.db,
            collection_name=self.collection_name,
            parent_collections=parent_collections,
            filters=filters,
        )

    @ensure_parent_keys
    def batch_action(
        self,
        data: t.List[BaseDataModel | BaseModel],
        action: FirestoreBatchActionType,
        parent_collections: dict = {},
    ):
        batch_action = [
            FirestoreBatchAction(
                action=action,
                parent_collections=parent_collections,
                collection_name=self.collection_name,
                document_data=item.dict(),
                document_id=item.id  # type: ignore
                if action != FirestoreBatchActionType.CREATE
                else generate_random_short_code(),
            )
            for item in data
        ]
        return self.db.batch_action(batch_action)

    @ensure_parent_keys
    def batch_create(
        self,
        data: t.List[BaseModel],
        parent_collections: dict = {},
    ):
        return self.batch_action(
            data, FirestoreBatchActionType.CREATE, parent_collections
        )

    @ensure_parent_keys
    def batch_update(
        self,
        data: t.List[BaseDataModel],
        parent_collections: dict = {},
    ):
        return self.batch_action(data, FirestoreBatchActionType.UPDATE, parent_collections)  # type: ignore

    @ensure_parent_keys
    def batch_delete(
        self,
        data: t.List[BaseDataModel],
        parent_collections: dict = {},
    ):
        return self.batch_action(data, FirestoreBatchActionType.DELETE, parent_collections)  # type: ignore

    @ensure_parent_keys
    def get_with_joins(
        self,
        doc_id: str,
        parent_collections: dict = {},
        joins: t.List[JoinAttribute] = [],
    ) -> dict:
        """
        TODO - the repo layer is supposed to always return pydantic models
        The current models don't support joins so we need to figure out how to do this

        For now, these will just return the dictionary results
        """
        res = self.db.get_with_joins(
            join_model=GetWithJoins(
                parent_collections=parent_collections,
                get_id=doc_id,
                get_collection=self.collection_name,
                joins=joins,
            )
        )
        return res.data

    @ensure_parent_keys
    def query_with_joins(
        self,
        parent_collections: dict = {},
        filters: t.Optional[t.List[FirestoreFilters]] = None,
        order_by: t.Optional[FirestoreOrderBy] = None,
        pagination: FirestorePagination = FirestorePagination(),
        joins: t.List[JoinAttribute] = [],
    ):
        res = self.db.query_with_joins(
            join_query=QueryWithJoins(
                parent_collections=parent_collections,
                collection_name=self.collection_name,
                filters=filters,
                order_by=order_by,
                pagination=pagination,
                joins=joins,
            )
        )
        return format_paginated_response(res, None)


class ParentRepository(BaseRepository):
    """
    This class extends the base repository and is meant for
    interacting with root level documents.

    An example is a company, this is a root level object
    """

    def __init__(
        self,
        dependencies: RepositoryDependencies,
    ):
        super().__init__(dependencies)


class MultipleChildrenRepository(BaseRepository):
    """
    This class extends the base repository is meant for interacting with a
    sub-collection of a root level document where there can be many
    sub collections of the same type.

    An example is a company's recruiters, which there may be many of directly under the company
    """

    def __init__(
        self, dependencies: RepositoryDependencies, required_parent_keys: t.List[str]
    ):
        super().__init__(dependencies)
        self.required_parent_keys = required_parent_keys


class SingleChildRepository:
    """
    This class extends the base repository is meant for interacting with a
    sub-collection of a root level document where there can be only one sub
    collection of the same type.

    An example is a company's details, which there can only be one of
    directly under the company

    This repository includes additional handling for cacheing data. I expect
    that this type of data is better suited for cacheing that the multiple
    child or parent classes above.
    """

    def __init__(
        self, dependencies: RepositoryDependencies, required_parent_keys: t.List[str]
    ):
        self.dependencies = dependencies
        self.repo = BaseRepository(dependencies)
        self.required_parent_keys = required_parent_keys
        self.redis = dependencies.redis

    def _get_cached_data(self, parent_collections: dict):
        if not self.redis:
            return None
        return self.redis.get(
            entity_type=self.dependencies.collection_name,
            entity_id=self.dependencies.collection_name,
            parent_collections=parent_collections,
            model=self.dependencies.entity_models.entity,
        )

    def _set_cached_data(self, parent_collections: dict, data: BaseModel):
        if not self.redis:
            return None
        self.redis.set(
            entity_type=self.dependencies.collection_name,
            entity_id=self.dependencies.collection_name,
            parent_collections=parent_collections,
            data=data,
        )

    @ensure_parent_keys
    def get_sub_entity(self, parent_collections: dict):
        cached_result = self._get_cached_data(parent_collections)
        if cached_result:
            return cached_result
        result = self.repo.get(self.dependencies.collection_name, parent_collections)
        if result:
            self._set_cached_data(parent_collections, result)
        return result

    @ensure_parent_keys
    def set_sub_entity(self, data: BaseModel, parent_collections: dict):
        try:
            result = self.repo.update(
                self.dependencies.collection_name, data, parent_collections
            )
        except EntityNotFound:
            result = self.repo.create(
                data, parent_collections, self.dependencies.collection_name
            )
        self._set_cached_data(parent_collections, result)
        return result
