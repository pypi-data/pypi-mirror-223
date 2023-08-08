from typing import cast

from getajob.utils import extract_pdf_text_by_url
from getajob.abstractions.models import Entity
from getajob.abstractions.repository import (
    SingleChildRepository,
    MultipleChildrenRepository,
)
from getajob.contexts.users.resumes.models import Resume

from .suggestor import ResumeSuggestor


class ResumeSuggestorUnitOfWork:
    def __init__(
        self,
        resume_repo: MultipleChildrenRepository,
    ):
        self.resume_repo = resume_repo

    def create_resume_suggestion(self, user_id: str, resume_id: str) -> str:
        resume = cast(
            Resume,
            self.resume_repo.get(
                resume_id, parent_collections={Entity.USERS.value: user_id}
            ),
        )
        resume_text = extract_pdf_text_by_url(resume.resume_url)
        return ResumeSuggestor(resume_text).provide_suggestion()
