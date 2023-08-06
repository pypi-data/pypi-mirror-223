from typing import cast, Any
from pydantic import BaseModel

from getajob.contexts.users.models import User
from getajob.contexts.users.resumes.models import Resume
from getajob.contexts.companies.models import Company
from getajob.contexts.companies.jobs.models import Job
from getajob.contexts.applications.repository import ApplicationRepository
from getajob.contexts.applications.models import (
    UserCreatedApplication,
    Application,
)

from .users import UserFixtures
from .company import CompanyFixture
from .job import JobFixture


class ApplicationWithDependencies(BaseModel):
    application: Any
    company: Any
    job: Any
    resume: Any
    user: Any


class ApplicationFixture:
    @staticmethod
    def create_application(request_scope, user, resume, company, job):
        application_repo = ApplicationRepository(
            request_scope=request_scope, kafka=None
        )
        new_application = application_repo.user_creates_application(
            user_id=user.id,
            application=UserCreatedApplication(
                company_id=company.id, job_id=job.id, resume_id=resume.id
            ),
        )
        new_application = cast(Application, new_application)
        return new_application

    @staticmethod
    def create_application_with_dependencies(request_scope):
        user = cast(User, UserFixtures.create_user_from_webhook(request_scope))
        resume = cast(Resume, UserFixtures.create_user_resume(request_scope, user.id))
        company = cast(
            Company, CompanyFixture.create_company_from_webhook(request_scope)
        )
        job = cast(Job, JobFixture.create_job(request_scope, company.id))
        application_repo = ApplicationRepository(
            request_scope=request_scope, kafka=None
        )
        new_application = application_repo.user_creates_application(
            user_id=user.id,
            application=UserCreatedApplication(
                company_id=company.id, job_id=job.id, resume_id=resume.id
            ),
        )
        new_application = cast(Application, new_application)
        return ApplicationWithDependencies(
            application=new_application,
            company=company,
            job=job,
            resume=resume,
            user=user,
        )
