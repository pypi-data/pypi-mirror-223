from getajob.contexts.applications.repository import ApplicationRepository

from .models import UserDashboard
from .unit_of_work import UserDashboardUnitOfWork


class UserDashboardRepository:
    def __init__(self, *, request_scope):
        self.request_scope = request_scope

    def get_user_dashboard(self, company_id: str) -> UserDashboard:
        return UserDashboardUnitOfWork(
            ApplicationRepository(request_scope=self.request_scope, kafka=None),
        ).get_user_dashboard(company_id)
