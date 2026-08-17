"""
CareerOneStop API Client
DOL veteran employment services and training
API Docs: https://www.careeronestop.org/Developers/WebAPI/
"""

import requests
from typing import Dict


class CareerOneStopClient:
    """Client for CareerOneStop API (DOL)"""

    BASE_URL = "https://api.careeronestop.org/v1"

    def __init__(self, user_id: str, authorization_token: str):
        """
        Initialize CareerOneStop API client

        Args:
            user_id: User ID from registration
            authorization_token: API token from registration
        """
        self.user_id = user_id
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {authorization_token}"})

    def get_veteran_employers(self, city: str, state: str, radius: int = 25) -> Dict:
        """
        Find veteran-friendly employers

        Args:
            city: City name
            state: 2-letter state code
            radius: Search radius in miles

        Returns:
            Dict containing veteran-friendly employers
        """
        response = self.session.get(
            f"{self.BASE_URL}/veteranemployer/{self.user_id}/{city}/{state}/{radius}", timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_training_programs(self, keyword: str, city: str, state: str, radius: int = 25) -> Dict:
        """
        Find training programs

        Args:
            keyword: Program keyword (e.g., "CYBERSECURITY")
            city: City name
            state: 2-letter state code
            radius: Search radius in miles

        Returns:
            Dict containing training programs
        """
        response = self.session.get(
            f"{self.BASE_URL}/training/{self.user_id}/{keyword}/{city}/{state}/0/0/0/{radius}",
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

    def get_certifications(self, keyword: str) -> Dict:
        """
        Find industry certifications

        Args:
            keyword: Certification keyword

        Returns:
            Dict containing certification information
        """
        response = self.session.get(
            f"{self.BASE_URL}/certificationfinder/{self.user_id}/{keyword}", timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_american_job_centers(self, city: str, state: str, radius: int = 25) -> Dict:
        """
        Find local American Job Centers

        Args:
            city: City name
            state: 2-letter state code
            radius: Search radius in miles

        Returns:
            Dict containing job center locations
        """
        response = self.session.get(
            f"{self.BASE_URL}/jobcenter/{self.user_id}/{city}/{state}/{radius}", timeout=30
        )
        response.raise_for_status()
        return response.json()
