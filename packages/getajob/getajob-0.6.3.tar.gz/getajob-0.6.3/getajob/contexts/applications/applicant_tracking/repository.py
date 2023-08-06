"""Single child repository under an application, only visibile to the company"""


from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaTopic,
    KafkaApplicationATSEnum,
)
from getajob.abstractions.models import Entity, EntityModels, UserAndDatabaseConnection
from getajob.vendor.firestore.models import FirestoreFilters, JoinAttribute

from .models import SetATSDetails, ATSDetails, ApplicantQueryWithCompanyID


entity_models = EntityModels(
    create=SetATSDetails,
    update=SetATSDetails,
    entity=ATSDetails,
)


class ATSRepository(SingleChildRepository):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.applications, message_type_enum=KafkaApplicationATSEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.APPLICATION_TRACKING.value,
                entity_models=entity_models,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            ),
            required_parent_keys=[Entity.APPLICATIONS.value],
        )

    def get_all_applicants(self, query: ApplicantQueryWithCompanyID):
        filters = [
            FirestoreFilters(
                field="company_id",
                operator="==",
                value=query.company_id,
            )
        ]
        for _query_field in [
            "job_id",
            "quick_action",
            "ats_status",
            "tags",
            "is_viewed",
        ]:
            if _query_value := getattr(query, _query_field):
                filters.append(
                    FirestoreFilters(
                        field=_query_field,
                        operator="==",
                        value=_query_value,
                    )
                )
        return self.repo.query_with_joins(
            filters=filters,
            joins=[
                JoinAttribute(
                    attribute="user_id",
                    collection=Entity.USERS.value,
                    parent_collections={},
                )
            ],
        )
