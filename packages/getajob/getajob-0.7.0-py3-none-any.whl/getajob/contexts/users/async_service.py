from typing import cast
from datetime import datetime

from getajob.abstractions.models import (
    Entity,
    ProcessedKafkaMessage,
)
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.contexts.search.models import CandidateSearch

from .details.repository import UserDetailsRepository
from .models import User
from .details.models import UserDetails


class AsyncronousUserService:
    def __init__(
        self,
        algolia_users: AlgoliaSearchRepository,
        algolia_applications: AlgoliaSearchRepository,
    ):
        self.algolia_users = algolia_users
        self.algolia_applications = algolia_applications

    async def user_is_created(self, processed_message: ProcessedKafkaMessage):
        data = cast(User, processed_message.data)
        candidate_data = CandidateSearch(
            user=data,
            id=data.id,
            created=datetime.now(),
            updated=datetime.now(),
            thumbnail=data.image_url,
        )
        self.algolia_users.create_object(
            object_id=data.id, object_data=candidate_data.dict()
        )

    async def _update_all_user_in_applications(self, user_id: str, new_user: User):
        # TODO improve patch modelling for algolia updates
        objects_to_update = [
            {
                "user_id": user_id,
                "user": new_user.dict(),
                "updated": datetime.now(),
            }
        ]
        self.algolia_applications.partial_update_based_on_attribute(
            objects_to_update, "user_id"
        )

    async def _update_all_user_details_in_applications(
        self, user_id: str, new_user_details: UserDetails
    ):
        # TODO improve patch modelling for algolia updates
        objects_to_update = [
            {
                "user_id": user_id,
                "user_details": new_user_details.dict(),
                "updated": datetime.now(),
            }
        ]
        self.algolia_applications.partial_update_based_on_attribute(
            objects_to_update, "user_id"
        )

    async def _delete_all_user_applications(self, user_id: str):
        # TODO improve patch modelling for algolia updates
        objects_to_update = [
            {
                "user_id": user_id,
                "is_deleted": True,
                "updated": datetime.now(),
            }
        ]
        self.algolia_applications.partial_update_based_on_attribute(
            objects_to_update, "user_id"
        )

    async def user_is_updated(self, processed_message: ProcessedKafkaMessage):
        data = cast(User, processed_message.data)
        original_data = CandidateSearch(
            **self.algolia_users.get_object(object_id=data.id)
        )
        original_data.user = data
        original_data.updated = datetime.now()
        original_data.thumbnail = data.image_url
        self.algolia_users.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._update_all_user_in_applications(data.id, data)

    async def user_is_deleted(self, processed_message: ProcessedKafkaMessage):
        original_data = CandidateSearch(
            **self.algolia_users.get_object(object_id=processed_message.object_id)
        )
        original_data.is_deleted = True
        original_data.updated = datetime.now()
        self.algolia_users.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._delete_all_user_applications(processed_message.object_id)

    async def user_details_are_created_or_updated(
        self, processed_message: ProcessedKafkaMessage
    ):
        user_id = processed_message.parent_collections[Entity.USERS.value]
        data = cast(UserDetails, processed_message.data)

        # """Update the user details for the candidate and the application"""
        original_data = CandidateSearch(
            **self.algolia_users.get_object(object_id=user_id)
        )
        original_data.user_details = data
        original_data.updated = datetime.now()
        self.algolia_users.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        # await self._update_all_user_details_in_applications(user_id, data)
