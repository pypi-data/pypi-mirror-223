from pydantic import BaseModel


class CompanyDashboard(BaseModel):
    num_live_jobs: int
    num_applicants: int
