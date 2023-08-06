from getajob.vendor.firestore.models import FirestoreFilters
from getajob.abstractions.repository import ParentRepository

from .models import UserDashboard


class UserDashboardUnitOfWork:
    
    def __init__(
        self,
        application_repo: ParentRepository
    ):
        self.application_repo = application_repo

    def _get_user_application_count(self, user_id: str) -> int:
        return self.application_repo.get_count_from_query(
            parent_collections={},
            filters=[
                FirestoreFilters(
                    field="user_id",
                    operator="==",
                    value=user_id
                )
            ]
        )

    def get_user_dashboard(self, user_id: str) -> UserDashboard:
        return UserDashboard(
            num_applications=self._get_user_application_count(user_id)
        )
