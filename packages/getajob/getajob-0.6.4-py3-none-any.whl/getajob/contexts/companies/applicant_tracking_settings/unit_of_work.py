from .models import SetATSConfig, ATSConfig


class ATSUnitOfWork:
    ...

    def update_company_ats(self, company_id: str, new_ats: SetATSConfig) -> ATSConfig:
        ...
