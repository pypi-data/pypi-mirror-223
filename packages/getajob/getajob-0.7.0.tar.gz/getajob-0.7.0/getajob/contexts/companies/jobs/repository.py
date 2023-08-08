import typing as t
from getajob.vendor.kafka.repository import KafkaProducerRepository
from getajob.vendor.kafka.models import KafkaEventConfig, KafkaTopic, KafkaJobsEnum
from getajob.abstractions.repository import (
    MultipleChildrenRepository,
    RepositoryDependencies,
)
from getajob.abstractions.models import Entity, EntityModels, UserAndDatabaseConnection

from .models import CreateJob, UpdateJob, Job, UserCreateJob
from .unit_of_work import JobsUnitOfWork


entity_models = EntityModels(entity=Job, create=CreateJob, update=UpdateJob)


class JobsRepository(MultipleChildrenRepository):
    def __init__(
        self,
        *,
        request_scope: UserAndDatabaseConnection,
        kafka: KafkaProducerRepository | None,
    ):
        kafka_event_config = KafkaEventConfig(
            topic=KafkaTopic.jobs, message_type_enum=KafkaJobsEnum
        )
        super().__init__(
            RepositoryDependencies(
                user_id=request_scope.initiating_user_id,
                db=request_scope.db,
                collection_name=Entity.JOBS.value,
                entity_models=entity_models,
                kafka=kafka,
                kafka_event_config=kafka_event_config,
            ),
            required_parent_keys=[Entity.COMPANIES.value],
        )

    def create_job(self, company_id: str, job: UserCreateJob):
        return JobsUnitOfWork(self).create_job(company_id, job)
