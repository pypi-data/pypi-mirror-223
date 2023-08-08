from getajob.abstractions.models import Entity, EntityModels
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import UserAndDatabaseConnection

from .models import UserCreateChatMessage, UpdateChatMessage, ChatMessage


entity_models = EntityModels(
    entity=ChatMessage, create=UserCreateChatMessage, update=UpdateChatMessage
)


class ChatMessageRepository(MultipleChildrenRepository):
    def __init__(self, *, request_scope: UserAndDatabaseConnection):
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.CHAT_MESSAGES.value,
                entity_models=entity_models,
            ),
            required_parent_keys=[Entity.CHAT.value],
        )
