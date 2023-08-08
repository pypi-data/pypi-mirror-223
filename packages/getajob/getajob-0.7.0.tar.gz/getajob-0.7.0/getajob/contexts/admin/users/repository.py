from getajob.abstractions.repository import ParentRepository, RepositoryDependencies
from getajob.abstractions.models import Entity, EntityModels, UserAndDatabaseConnection

from .models import AdminUser, CreateAdminUser, UpdateAdminUser


entity_models = EntityModels(
    entity=AdminUser, create=CreateAdminUser, update=UpdateAdminUser
)


class AdminUserRepository(ParentRepository):
    def __init__(self, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.ADMIN_USERS.value,
                entity_models=entity_models,
            )
        )

    def get_by_user_id(self, user_id: str):
        return self.get_one_by_attribute("user_id", user_id)
