"""
O*NET OnLine API Client
Occupational skills and MOS-to-civilian crosswalk
API Docs: https://services.onetcenter.org/ws/online-help/
"""

import requests
from typing import Dict, List, Optional


class ONetClient:
    """Client for O*NET OnLine Web Services"""
    
    BASE_URL = "https://services.onetcenter.org/ws/online"
    
    def __init__(self, username: str):
        """
        Initialize O*NET API client
        
        Args:
            username: Your email address (no password required)
        """
        self.username = username
        self.session = requests.Session()
        self.session.auth = (username, "")  # No password needed
    
    def get_occupation(self, onet_code: str) -> Dict:
        """Get occupation details by O*NET code"""
        response = self.session.get(
            f"{self.BASE_URL}/occupations/{onet_code}",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_skills(self, onet_code: str) -> Dict:
        """Get skills required for occupation"""
        response = self.session.get(
            f"{self.BASE_URL}/occupations/{onet_code}/skills",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_abilities(self, onet_code: str) -> Dict:
        """Get abilities required for occupation"""
        response = self.session.get(
            f"{self.BASE_URL}/occupations/{onet_code}/abilities",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def get_knowledge(self, onet_code: str) -> Dict:
        """Get knowledge domains for occupation"""
        response = self.session.get(
            f"{self.BASE_URL}/occupations/{onet_code}/knowledge",
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    
    def search_occupations(self, keyword: str) -> Dict:
        """Search for occupations by keyword"""
        response = self.session.get(
            f"{self.BASE_URL}/search",
            params={"keyword": keyword},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
