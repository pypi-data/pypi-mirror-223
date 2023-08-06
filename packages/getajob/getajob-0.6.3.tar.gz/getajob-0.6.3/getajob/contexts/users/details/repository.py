from getajob.abstractions.repository import (
    SingleChildRepository,
    RepositoryDependencies,
)
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import (
    KafkaEventConfig,
    KafkaTopic,
    KafkaUsersDetailsEnum,
)
from getajob.abstractions.models import Entity, EntityModels, UserAndDatabaseConnection
from getajob.vendor.redis.repository import RedisRepository

from .models import SetUserDetails, UserDetails


entity_models = EntityModels(
    entity=UserDetails,
    create=SetUserDetails,
    update=SetUserDetails,
)


class UserDetailsRepository(SingleChildRepository):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        redis: RedisRepository | None,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.users, message_type_enum=KafkaUsersDetailsEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.USER_DETAILS.value,
                entity_models=entity_models,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
                redis=redis,
            ),
            required_parent_keys=[Entity.USERS.value],
        )
