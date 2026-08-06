"""
API Keys Configuration
Store your API keys as environment variables in production
This file is a template - DO NOT commit actual keys to Git
"""

import os
from typing import Optional


class APIConfig:
    """Centralized API configuration management"""
    
    # USAJobs API (https://developer.usajobs.gov/)
    USAJOBS_API_KEY: str = os.getenv("USAJOBS_API_KEY", "")
    USAJOBS_USER_AGENT: str = os.getenv("USAJOBS_USER_AGENT", "whall4.wh@gmail.com")
    
    # BLS API (https://data.bls.gov/registrationEngine/)
    BLS_API_KEY: str = os.getenv("BLS_API_KEY", "d2d7521b04c2411e9f16e639e617cd7a")
    
    # Adzuna API (https://developer.adzuna.com/)
    ADZUNA_APP_ID: str = os.getenv("ADZUNA_APP_ID", "")
    ADZUNA_API_KEY: str = os.getenv("ADZUNA_API_KEY", "")
    
    # O*NET API (No key required - use email as username)
    ONET_USERNAME: str = os.getenv("ONET_USERNAME", "whall4.wh@gmail.com")
    
    # CareerOneStop API (https://www.careeronestop.org/Developers/)
    CAREERONESTOP_USER_ID: str = os.getenv("CAREERONESTOP_USER_ID", "")
    CAREERONESTOP_TOKEN: str = os.getenv("CAREERONESTOP_TOKEN", "")
    
    @classmethod
    def validate(cls) -> dict:
        """Check which API keys are configured"""
        return {
            "usajobs": bool(cls.USAJOBS_API_KEY),
            "bls": bool(cls.BLS_API_KEY),
            "adzuna": bool(cls.ADZUNA_APP_ID and cls.ADZUNA_API_KEY),
            "onet": bool(cls.ONET_USERNAME),
            "careeronestop": bool(cls.CAREERONESTOP_USER_ID and cls.CAREERONESTOP_TOKEN)
        }
    
    @classmethod
    def get_missing_keys(cls) -> list:
        """Return list of APIs with missing keys"""
        validation = cls.validate()
        return [api for api, configured in validation.items() if not configured]


# Usage example:
if __name__ == "__main__":
    print("API Configuration Status:")
    for api, status in APIConfig.validate().items():
        print(f"  {api}: {'✅ Configured' if status else '❌ Missing'}")
    
    missing = APIConfig.get_missing_keys()
    if missing:
        print(f"\nMissing API keys: {', '.join(missing)}")
