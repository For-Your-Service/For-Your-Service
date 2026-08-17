import os


class Config:
    ONET_USERNAME: str = os.getenv("ONET_USERNAME", "")
    ONET_PASSWORD: str = os.getenv("ONET_PASSWORD", "")
    USAJOBS_API_KEY: str = os.getenv("USAJOBS_API_KEY", "")
    USAJOBS_EMAIL: str = os.getenv("USAJOBS_EMAIL", "")
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
