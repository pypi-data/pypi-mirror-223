from typing import cast
from datetime import datetime

from getajob.abstractions.models import (
    Entity,
    ProcessedKafkaMessage,
)
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.contexts.search.models import JobSearch

from .models import Job, InternalUpdateJob
from .repository import JobsRepository


class AsyncronousJobService:
    def __init__(
        self,
        algolia_jobs: AlgoliaSearchRepository,
        algolia_applications: AlgoliaSearchRepository,
    ):
        self.algolia_jobs = algolia_jobs
        self.algolia_applications = algolia_applications

    async def create_job(self, processed_message: ProcessedKafkaMessage):
        job_data = cast(Job, processed_message.data)
        self.algolia_jobs.create_object(
            object_id=job_data.id,
            object_data=JobSearch(
                id=job_data.id,
                created=datetime.now(),
                updated=datetime.now(),
                job=job_data,
                company_id=processed_message.parent_collections[Entity.COMPANIES.value],
            ).dict(),
        )

    async def _update_all_applications_with_job(self, job: Job):
        # TODO improve patch modelling for algolia updates
        objects_to_update = [
            {
                "job_id": job.id,
                "job": job.dict(),
                "updated": datetime.now(),
            }
        ]
        self.algolia_applications.partial_update_based_on_attribute(
            objects_to_update, "job_id"
        )

    async def _delete_all_applications_with_job(self, job_id: str):
        # TODO improve patch modelling for algolia updates
        objects_to_update = [
            {
                "job_id": job_id,
                "is_deleted": True,
                "updated": datetime.now(),
            }
        ]
        self.algolia_applications.partial_update_based_on_attribute(
            objects_to_update, "job_id"
        )

    async def _handle_job_is_now_filled(self):
        # TODO add handling here for when a job is now filled
        # Set all applications with job ID to is deleted?
        # Remove all applications with job id?
        ...

    async def update_job(self, processed_message: ProcessedKafkaMessage):
        original_data = JobSearch(
            **self.algolia_jobs.get_object(object_id=processed_message.object_id)
        )
        job_updates = cast(Job, processed_message.data)
        if job_updates.position_filled:
            await self._handle_job_is_now_filled()
        original_data.job = job_updates
        original_data.updated = datetime.now()
        self.algolia_jobs.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._update_all_applications_with_job(original_data.job)

    async def delete_job(self, processed_message: ProcessedKafkaMessage):
        original_data = JobSearch(
            **self.algolia_jobs.get_object(object_id=processed_message.object_id)
        )
        original_data.is_deleted = True
        original_data.updated = datetime.now()
        self.algolia_jobs.update_object(
            object_id=original_data.id, object_data=original_data.dict()
        )
        await self._delete_all_applications_with_job(original_data.id)
