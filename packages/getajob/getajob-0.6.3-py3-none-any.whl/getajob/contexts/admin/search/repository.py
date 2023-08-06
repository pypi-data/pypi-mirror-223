from getajob.abstractions.repository import query_collection
from getajob.abstractions.models import UserAndDatabaseConnection

from .models import AdminEntitySearch


class AdminSearchRepository:
    def __init__(self, request_scope: UserAndDatabaseConnection):
        self.db = request_scope.db

    def admin_collection_search(self, search: AdminEntitySearch):
        return query_collection(db=self.db, collection_name=search.entity_type.value)

    def admin_subcollection_search(self, search: AdminEntitySearch):
        return query_collection(db=self.db, collection_name=search.entity_type.value)
