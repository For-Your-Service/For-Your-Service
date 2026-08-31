"""
config.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
import os


class Config:
    ONET_USERNAME: str = os.getenv("ONET_USERNAME", "")
    ONET_PASSWORD: str = os.getenv("ONET_PASSWORD", "")
    ONET_API_KEY: str = os.getenv("ONET_API_KEY", "")
    USAJOBS_API_KEY: str = os.getenv("USAJOBS_API_KEY", "")
    USAJOBS_EMAIL: str = os.getenv("USAJOBS_EMAIL", "")
    USAJOBS_USER_AGENT: str = os.getenv("USAJOBS_USER_AGENT", "For-Your-Service/1.0")
    ADZUNA_APP_ID: str = os.getenv("ADZUNA_APP_ID", "")
    ADZUNA_API_KEY: str = os.getenv("ADZUNA_API_KEY", "")
    BLS_API_KEY: str = os.getenv("BLS_API_KEY", "")
    CAREERONESTOP_USER_ID: str = os.getenv("CAREERONESTOP_USER_ID", "")
    CAREERONESTOP_TOKEN: str = os.getenv("CAREERONESTOP_TOKEN", "")
    ENV: str = os.getenv("APP_ENV", "development")

    @classmethod
    def validate_secrets(cls) -> None:
        if cls.ENV.lower() in ("production", "prod", "staging"):
            missing = [
                k
                for k in ["ONET_USERNAME", "ONET_PASSWORD", "USAJOBS_API_KEY", "USAJOBS_EMAIL"]
                if not getattr(cls, k)
            ]
            if missing:
                raise ValueError(f"Missing required production credentials: {', '.join(missing)}")
