"""
Adzuna API Client
Job aggregator with 1M+ listings from Indeed, CareerBuilder, etc.
API Docs: https://api.adzuna.com/v1/doc/
"""

import requests
from typing import Dict, Optional


class AdzunaClient:
    """Client for Adzuna job search API"""

    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def __init__(self, app_id: str, api_key: str, country: str = "us"):
        """
        Initialize Adzuna API client

        Args:
            app_id: Application ID from developer.adzuna.com
            api_key: API key from developer.adzuna.com
            country: Country code (default: "us")
        """
        self.app_id = app_id
        self.api_key = api_key
        self.country = country
        self.session = requests.Session()

    def search_jobs(
        self,
        what: Optional[str] = None,
        where: Optional[str] = None,
        results_per_page: int = 50,
        page: int = 1,
        salary_min: Optional[int] = None,
        salary_max: Optional[int] = None,
        distance: Optional[int] = None,
        full_time: Optional[bool] = None,
        part_time: Optional[bool] = None,
        contract: Optional[bool] = None,
        permanent: Optional[bool] = None,
        category: Optional[str] = None,
    ) -> Dict:
        """
        Search for jobs on Adzuna

        Args:
            what: Keywords (e.g., "python developer")
            where: Location (e.g., "San Diego, CA")
            results_per_page: Results per page (max 50)
            page: Page number
            salary_min: Minimum salary filter
            salary_max: Maximum salary filter
            distance: Search radius in miles
            full_time: Filter for full-time positions
            part_time: Filter for part-time positions
            contract: Filter for contract positions
            permanent: Filter for permanent positions
            category: Job category tag

        Returns:
            Dict containing search results
        """
        params = {
            "app_id": self.app_id,
            "app_key": self.api_key,
            "results_per_page": min(results_per_page, 50),
        }

        if what:
            params["what"] = what
        if where:
            params["where"] = where
        if salary_min:
            params["salary_min"] = salary_min
        if salary_max:
            params["salary_max"] = salary_max
        if distance:
            params["distance"] = distance
        if full_time is not None:
            params["full_time"] = 1 if full_time else 0
        if part_time is not None:
            params["part_time"] = 1 if part_time else 0
        if contract is not None:
            params["contract"] = 1 if contract else 0
        if permanent is not None:
            params["permanent"] = 1 if permanent else 0
        if category:
            params["category"] = category

        response = self.session.get(
            f"{self.BASE_URL}/{self.country}/search/{page}", params=params, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_job_details(self, job_id: str) -> Dict:
        """
        Get detailed information for a specific job

        Args:
            job_id: Adzuna job ID

        Returns:
            Dict containing full job details
        """
        params = {"app_id": self.app_id, "app_key": self.api_key}

        response = self.session.get(
            f"{self.BASE_URL}/{self.country}/jobs/{job_id}", params=params, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_salary_history(
        self, location: Optional[str] = None, category: Optional[str] = None
    ) -> Dict:
        """
        Get historical salary data

        Args:
            location: Location filter (e.g., "California")
            category: Job category (e.g., "it-jobs")

        Returns:
            Dict containing salary trend data
        """
        params = {"app_id": self.app_id, "app_key": self.api_key}

        if location:
            params["location0"] = "US"
            params["location1"] = location
        if category:
            params["category"] = category

        response = self.session.get(
            f"{self.BASE_URL}/{self.country}/history", params=params, timeout=30
        )
        response.raise_for_status()
        return response.json()
