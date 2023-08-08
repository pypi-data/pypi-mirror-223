from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels, UserAndDatabaseConnection

from .models import CoverLetter, CreateCoverLetter, UpdateCoverLetter

entity_models = EntityModels(
    entity=CoverLetter,
    create=CreateCoverLetter,
    update=UpdateCoverLetter,
)


class CoverLetterRepository(MultipleChildrenRepository):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.COVER_LETTERS.value,
                entity_models=entity_models,
            ),
            required_parent_keys=[Entity.USERS.value],
        )
