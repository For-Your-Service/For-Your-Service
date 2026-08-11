"""
O*NET Web Services Client

Free tier API client for O*NET occupational database.
Provides skill taxonomies, occupation details, and competency mappings.

API: https://services.onetcenter.org/
Free tier: No authentication required for basic queries

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import requests
from typing import List, Dict, Optional
import time
from functools import lru_cache


class ONetClient:
    """Client for O*NET Web Services API (free tier)"""
    
    BASE_URL = "https://services.onetcenter.org/ws"
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize O*NET client
        
        Args:
            username: Optional O*NET Web Services username
            password: Optional O*NET Web Services password
            
        Note: Free tier works without credentials for basic queries
        """
        self.username = username
        self.password = password
        self.session = requests.Session()
        
        if username and password:
            self.session.auth = (username, password)
        
        # Rate limiting (free tier: 10 requests/minute)
        self.last_request_time = 0
        self.min_request_interval = 6.0  # seconds
    
    def _rate_limit(self):
        """Enforce rate limiting for free tier"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        Make API request with rate limiting
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response as dict
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.get(url, params=params or {})
        response.raise_for_status()
        
        return response.json()
    
    @lru_cache(maxsize=1000)
    def search_occupations(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Search occupations by keyword
        
        Args:
            keyword: Search term (e.g., "software engineer")
            limit: Max results to return
            
        Returns:
            List of occupation matches with code, title, tags
        """
        try:
            result = self._make_request(
                f"online/search",
                params={"keyword": keyword, "end": limit}
            )
            return result.get("occupation", [])
        except Exception as e:
            print(f"O*NET search error: {e}")
            return []
    
    @lru_cache(maxsize=500)
    def get_occupation_details(self, onet_code: str) -> Dict:
        """
        Get detailed occupation information
        
        Args:
            onet_code: O*NET-SOC code (e.g., "15-1252.00")
            
        Returns:
            Occupation details including skills, knowledge, abilities
        """
        try:
            return self._make_request(f"online/occupations/{onet_code}")
        except Exception as e:
            print(f"O*NET occupation details error: {e}")
            return {}
    
    @lru_cache(maxsize=500)
    def get_skills(self, onet_code: str) -> List[Dict]:
        """
        Get skills for an occupation
        
        Args:
            onet_code: O*NET-SOC code
            
        Returns:
            List of skills with names, descriptions, importance levels
        """
        try:
            result = self._make_request(
                f"online/occupations/{onet_code}/skills"
            )
            return result.get("skill", [])
        except Exception as e:
            print(f"O*NET skills error: {e}")
            return []
    
    @lru_cache(maxsize=500)
    def get_knowledge(self, onet_code: str) -> List[Dict]:
        """
        Get knowledge areas for an occupation
        
        Args:
            onet_code: O*NET-SOC code
            
        Returns:
            List of knowledge areas with importance levels
        """
        try:
            result = self._make_request(
                f"online/occupations/{onet_code}/knowledge"
            )
            return result.get("knowledge", [])
        except Exception as e:
            print(f"O*NET knowledge error: {e}")
            return []
    
    @lru_cache(maxsize=500)
    def get_abilities(self, onet_code: str) -> List[Dict]:
        """
        Get abilities for an occupation
        
        Args:
            onet_code: O*NET-SOC code
            
        Returns:
            List of abilities with importance levels
        """
        try:
            result = self._make_request(
                f"online/occupations/{onet_code}/abilities"
            )
            return result.get("ability", [])
        except Exception as e:
            print(f"O*NET abilities error: {e}")
            return []
    
    def get_occupation_profile(self, onet_code: str) -> Dict:
        """
        Get complete occupation profile (skills + knowledge + abilities)
        
        Args:
            onet_code: O*NET-SOC code
            
        Returns:
            Complete profile dictionary
        """
        return {
            "code": onet_code,
            "details": self.get_occupation_details(onet_code),
            "skills": self.get_skills(onet_code),
            "knowledge": self.get_knowledge(onet_code),
            "abilities": self.get_abilities(onet_code)
        }
