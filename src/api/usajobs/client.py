"""
USAJobs API Client
Federal government job postings with veteran preferences
API Docs: https://developer.usajobs.gov/API-Reference
"""

import requests
from typing import Dict, Optional


class USAJobsClient:
    """Client for USAJobs.gov API - Federal government job postings"""

    BASE_URL = "https://data.usajobs.gov/api"

    def __init__(self, api_key: str, user_agent: str):
        """
        Initialize USAJobs API client

        Args:
            api_key: Authorization key from developer.usajobs.gov
            user_agent: Your email address (required by API)
        """
        self.api_key = api_key
        self.user_agent = user_agent
        self.session = requests.Session()
        self.session.headers.update(
            {"Host": "data.usajobs.gov", "User-Agent": user_agent, "Authorization-Key": api_key}
        )

    def search_jobs(
        self,
        keyword: Optional[str] = None,
        location: Optional[str] = None,
        results_per_page: int = 100,
        page: int = 1,
        veteran_preference: bool = False,
        security_clearance: Optional[str] = None,
    ) -> Dict:
        """
        Search for federal job postings

        Args:
            keyword: Job title or keywords (e.g., "cybersecurity")
            location: Location name (e.g., "California", "San Diego, CA")
            results_per_page: Number of results per page (max 500)
            page: Page number for pagination
            veteran_preference: Filter for veteran preference jobs only
            security_clearance: Security clearance level filter

        Returns:
            Dict containing search results and metadata
        """
        params = {"ResultsPerPage": min(results_per_page, 500), "Page": page}

        if keyword:
            params["Keyword"] = keyword
        if location:
            params["LocationName"] = location
        if veteran_preference:
            params["VeteranPreference"] = "true"
        if security_clearance:
            params["SecurityClearance"] = security_clearance

        response = self.session.get(f"{self.BASE_URL}/Search", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_job_details(self, control_number: str) -> Dict:
        """
        Get detailed information for a specific job posting

        Args:
            control_number: USAJobs control number for the position

        Returns:
            Dict containing full job details
        """
        response = self.session.get(
            f"{self.BASE_URL}/Search", params={"ControlNumber": control_number}, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def search_by_occupation_series(
        self, series_code: str, location: Optional[str] = None, page: int = 1
    ) -> Dict:
        """
        Search jobs by federal occupation series code

        Args:
            series_code: Federal series code (e.g., "2210" for IT)
            location: Location filter
            page: Page number

        Returns:
            Dict containing matching jobs
        """
        params = {"JobCategoryCode": series_code, "Page": page, "ResultsPerPage": 100}

        if location:
            params["LocationName"] = location

        response = self.session.get(f"{self.BASE_URL}/Search", params=params, timeout=30)
        response.raise_for_status()
        return response.json()

    def _build_search_params(
        self,
        keyword: Optional[str] = None,
        location: Optional[str] = None,
        results_per_page: int = 100,
        page: int = 1,
        veteran_preference: bool = False,
        security_clearance: Optional[str] = None,
    ) -> Dict:
        params = {"ResultsPerPage": min(results_per_page, 500), "Page": page}

        if keyword:
            params["Keyword"] = keyword
        if location:
            params["LocationName"] = location
        if veteran_preference:
            params["VeteranPreference"] = "true"
        if security_clearance:
            params["SecurityClearance"] = security_clearance

        return params
