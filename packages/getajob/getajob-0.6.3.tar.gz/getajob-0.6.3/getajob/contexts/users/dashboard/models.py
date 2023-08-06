from pydantic import BaseModel


class UserDashboard(BaseModel):
    num_applications: int
