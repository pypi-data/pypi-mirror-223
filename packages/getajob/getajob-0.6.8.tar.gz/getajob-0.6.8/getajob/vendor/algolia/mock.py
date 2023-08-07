from algoliasearch.search_client import SearchClient, SearchIndex
from .models import AlgoliaSearchResults


class MockAlgoliaIndex(SearchIndex):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        self.local_items = {}

    def search(self, *args, **kwargs):
        return AlgoliaSearchResults(
            hits=list(self.local_items.values()),
            nbHits=0,
            page=0,
            nbPages=0,
            hitsPerPage=0,
            processingTimeMS=0,
            exhaustiveNbHits=False,
            query="",
            params="",
        ).dict()

    def get_object(self, object_id: str, request_options=None):
        return self.local_items[object_id]

    def save_object(self, obj: dict, request_options=None):
        self.local_items[obj["objectID"]] = obj

    def partial_update_object(self, obj: dict, request_options=None):
        self.local_items[obj["objectID"]] = obj

    def partial_update_objects(self, objects: list[dict], request_options=[]):
        # Using a set for efficient look-up
        request_options_set = set(request_options)

        # Iterate over the local_items and find objects that need to be altered
        objects_to_alter = {
            key: object_dict
            for key, object_dict in self.local_items.items()
            if any(
                object_key == matching_key and object_value == update_dict[matching_key]
                for object_key, object_value in object_dict.items()
                for matching_key in request_options_set
                for update_dict in objects
            )
        }

        # Prepare update by aggregating all the updates into one dictionary
        aggregated_update = {
            key: value
            for update_object in objects
            for key, value in update_object.items()
        }

        # Update the objects that match the provided attribute
        for key in objects_to_alter:
            self.local_items[key].update(aggregated_update)

    def delete_object(self, object_id: str, request_options=None):
        del self.local_items[object_id]


class MockAlgoliaClient(SearchClient):
    # pylint: disable=super-init-not-called
    def __init__(self, *args, **kwargs):
        self.index = MockAlgoliaIndex()

    def init_index(self, *args, **kwargs):
        return self.index
