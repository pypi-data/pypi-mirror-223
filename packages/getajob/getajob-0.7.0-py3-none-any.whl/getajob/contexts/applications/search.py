"""
Search from algolia
"""

from .models import (
    CompanyQueryApplications,
    UserQueryApplications,
)
from getajob.vendor.algolia.repository import AlgoliaSearchRepository
from getajob.vendor.algolia.models import AlgoliaSearchParams, AlgoliaSearchResults


class ApplicationSearchRepository:
    def __init__(self, algolia_applications: AlgoliaSearchRepository):
        self.algolia_applications = algolia_applications

    def get_company_view_applications(
        self, query: CompanyQueryApplications
    ) -> AlgoliaSearchResults:
        filter_string = f"company_id:{query.company_id}"
        if query.job_id:
            filter_string += f" AND job_id:{query.job_id}"
        if query.is_viewed:
            filter_string += f" AND is_viewed:{query.is_viewed}"
        if query.quick_action_status:
            filter_string += f" AND quick_action_status:{query.quick_action_status}"
        if query.tags:
            filter_string += f" AND tags:{query.tags}"
        search_params = AlgoliaSearchParams(
            filters=filter_string,
            page=query.page,
            hits_per_page=query.hits_per_page,
        )
        return self.algolia_applications.search(search_params)

    def get_user_view_applications(
        self, query: UserQueryApplications
    ) -> AlgoliaSearchResults:
        filter_string = f"user_id:{query.user_id}"
        if query.company_id:
            filter_string += f" AND company_id:{query.company_id}"
        if query.job_id:
            filter_string += f" AND job_id:{query.job_id}"
        search_params = AlgoliaSearchParams(
            filters=filter_string,
            page=query.page,
            hits_per_page=query.hits_per_page,
        )
        return self.algolia_applications.search(search_params)
