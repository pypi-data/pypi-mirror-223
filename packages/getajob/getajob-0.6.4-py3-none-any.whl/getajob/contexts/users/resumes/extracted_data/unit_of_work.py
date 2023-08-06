from typing import cast
import pdfplumber
import io
import urllib3

from getajob.abstractions.models import Entity
from getajob.abstractions.repository import (
    SingleChildRepository,
    MultipleChildrenRepository,
)
from getajob.contexts.users.resumes.models import Resume

from .extractor import ResumeExtractor


class ResumeExtractorUnitOfWork:
    def __init__(
        self,
        resume_repo: MultipleChildrenRepository,
        resume_extraction_repo: SingleChildRepository,
    ):
        self.resume_repo = resume_repo
        self.resume_extraction_repo = resume_extraction_repo

    def _extract_pdf_text_by_url(self, url):
        http = urllib3.PoolManager()
        temp = io.BytesIO()
        temp.write(http.request("GET", url).data)
        all_text = ""
        with pdfplumber.open(temp) as pdf:
            for pdf_page in pdf.pages:
                single_page_text = pdf_page.extract_text()
                all_text = all_text + "\n" + single_page_text
        return all_text

    async def create_resume_extraction(self, user_id: str, resume_id: str):
        resume = cast(
            Resume,
            self.resume_repo.get(
                resume_id, parent_collections={Entity.USERS.value: user_id}
            ),
        )
        resume_text = self._extract_pdf_text_by_url(resume.resume_url)
        extractor = ResumeExtractor(resume_text)
        extracted_data = await extractor.extract_all()
        return self.resume_extraction_repo.set_sub_entity(
            extracted_data,
            parent_collections={
                Entity.USERS.value: user_id,
                Entity.RESUMES.value: resume_id,
            },
        )
