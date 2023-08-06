import json
from algoliasearch.search_client import SearchClient

from .client_factory import AlgoliaClientFactory
from .models import AlgoliaIndex, AlgoliaSearchParams, AlgoliaSearchResults


class AlgoliaSearchRepository:
    def __init__(
        self,
        index_name: AlgoliaIndex,
        client: SearchClient = AlgoliaClientFactory().get_client(),
    ):
        self.index = client.init_index(index_name.value)

    def search(self, query: AlgoliaSearchParams | str = ""):
        if not query:
            return AlgoliaSearchResults(**self.index.search(query))
        raise NotImplementedError("This is not implemented yet")
        search_params = {
            "query": query.query,
            "filters": query.filters,
            "page": query.page,
            "hitsPerPage": query.hits_per_page,
        }
        if query.filters:
            search_params["filters"] = query.filters
        if query.facet_filters:
            search_params["facetFilters"] = query.facet_filters
        if query.attributes_to_retrieve:
            search_params["attributesToRetrieve"] = query.attributes_to_retrieve
        res = self.index.search(query.query, search_params)
        return AlgoliaSearchResults(**res)

    def get_object(self, object_id: str):
        return self.index.get_object(object_id)

    def create_object(self, object_id: str, object_data: dict):
        object_data["objectID"] = object_id
        object_data = json.loads(json.dumps(object_data, default=str))
        return self.index.save_object(object_data)

    def update_object(self, object_id: str, object_data: dict):
        object_data["objectID"] = object_id
        object_data = json.loads(json.dumps(object_data, default=str))
        return self.index.partial_update_object(object_data)

    def partial_update_based_on_attribute(
        self, objects_to_update: list[dict], filter_attribute: str
    ):
        """
        Provide a dictionary of partials updates for objects.
        These objects must have an attribute that matches the filter_attribute.
        The filter attribute will be used to filter objects in the database and then
        the partial update will be applied to the filtered objects.
        """
        return self.index.partial_update_objects(objects_to_update, request_options=[filter_attribute])  # type: ignore

    def replace_all_objects(self, objects: list[dict]):
        return self.index.replace_all_objects(objects)

    # For now we are using soft delete for these search databases so this method is unavailable
    # def delete_object(self, object_id: str):
    #     return self.index.delete_object(object_id)
