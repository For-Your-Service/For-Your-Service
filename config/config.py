"""
Configuration settings for For Your Service platform
Author: William Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class DatabaseConfig:
    """Unity Catalog configuration"""
    catalog: str = "veteran_intake"
    bronze_schema: str = "bronze"
    silver_schema: str = "silver"
    gold_schema: str = "gold"

    @property
    def bronze_jobs_table(self) -> str:
        return f"{self.catalog}.{self.bronze_schema}.jobs"

    @property
    def silver_jobs_table(self) -> str:
        return f"{self.catalog}.{self.silver_schema}.jobs"

    @property
    def silver_veterans_table(self) -> str:
        return f"{self.catalog}.{self.silver_schema}.veterans"

    @property
    def gold_matches_table(self) -> str:
        return f"{self.catalog}.{self.gold_schema}.job_matches"


@dataclass
class ModelConfig:
    """ML model configuration"""
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    embedding_dim: int = 384
    max_sequence_length: int = 256
    batch_size: int = 100
    device: str = "cpu"  # cpu or cuda

    # Similarity thresholds
    exceptional_threshold: int = 85
    strong_threshold: int = 70
    good_threshold: int = 60
    fair_threshold: int = 50


@dataclass
class ScraperConfig:
    """Job scraper API configuration"""

    # USAJobs
    usajobs_api_url: str = "https://data.usajobs.gov/api/search"
    usajobs_rate_limit: int = 250  # per day
    usajobs_user_agent: str = "whall4.wh@gmail.com"

    # Adzuna
    adzuna_api_url: str = "https://api.adzuna.com/v1/api/jobs/us/search"
    adzuna_rate_limit: int = 250  # per month (free tier)

    # Search parameters
    results_per_page: int = 100
    max_pages: int = 5
    posted_within_days: int = 14

    # Target locations
    target_locations: List[str] = None

    def __post_init__(self):
        if self.target_locations is None:
            self.target_locations = [
                "Greenville, SC",
                "Spartanburg, SC",
                "Anderson, SC",
                "Remote",
                "Charlotte, NC",
                "Atlanta, GA"
            ]

    # Target keywords
    target_keywords: List[str] = None

    def __post_init__(self):
        if self.target_keywords is None:
            self.target_keywords = [
                "DevOps Engineer",
                "Solutions Architect",
                "Cloud Engineer",
                "Site Reliability Engineer",
                "Platform Engineer",
                "AWS Architect",
                "Kubernetes Engineer",
                "Terraform Engineer",
                "Infrastructure Engineer"
            ]


@dataclass
class VeteranConfig:
    """Default veteran profile configuration"""

    # William Free Hall's profile as default
    name: str = "William Free Hall"
    email: str = "whall4.wh@gmail.com"
    location: str = "Greenville, SC"

    # Military background
    military_branch: str = "Army"
    mos: str = "18F"
    rank: str = "Team Sergeant"
    years_of_service: int = 18
    clearance_level: str = "TS/SCI"
    clearance_status: str = "expired"

    # Professional
    total_years: int = 28
    seniority_level: str = "executive"

    # Skills
    skills: List[str] = None

    def __post_init__(self):
        if self.skills is None:
            self.skills = [
                "AWS", "Azure", "GCP",
                "Kubernetes", "Docker", "Terraform",
                "Python", "Bash", "SQL",
                "Databricks", "PySpark",
                "GitHub Actions", "Jenkins"
            ]

    # Preferences
    salary_min: int = 120000
    salary_max: int = 180000
    remote_preference: str = "preferred"


@dataclass
class DeploymentConfig:
    """Deployment configuration"""

    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")

    # Hugging Face Spaces (FREE tier)
    hf_space_name: str = "for-your-service"
    hf_sdk: str = "streamlit"

    # Production (GKE)
    gke_cluster_name: str = "fys-production"
    gke_region: str = "us-central1"
    gke_node_count: int = 2
    gke_machine_type: str = "n1-standard-1"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@dataclass
class Config:
    """Main configuration class"""

    database: DatabaseConfig = DatabaseConfig()
    model: ModelConfig = ModelConfig()
    scraper: ScraperConfig = ScraperConfig()
    veteran: VeteranConfig = VeteranConfig()
    deployment: DeploymentConfig = DeploymentConfig()

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Feature flags
    enable_vector_search: bool = False  # Future: Databricks Vector Search
    enable_caching: bool = True
    enable_telemetry: bool = True


# Singleton instance
config = Config()


# Environment-specific overrides
def load_config(env: str = None):
    """
    Load environment-specific configuration

    Args:
        env: Environment name (development, staging, production)
    """
    global config

    if env:
        config.deployment.environment = env

    if config.deployment.is_production:
        # Production overrides
        config.model.batch_size = 500
        config.scraper.results_per_page = 100
        config.scraper.max_pages = 10
        config.enable_vector_search = True

    return config


if __name__ == "__main__":
    # Test configuration
    cfg = load_config("development")

    print("=== Configuration ===")
    print(f"Environment: {cfg.deployment.environment}")
    print(f"\nDatabase:")
    print(f"  Bronze jobs: {cfg.database.bronze_jobs_table}")
    print(f"  Silver veterans: {cfg.database.silver_veterans_table}")
    print(f"  Gold matches: {cfg.database.gold_matches_table}")
    print(f"\nModel:")
    print(f"  Embedding model: {cfg.model.embedding_model}")
    print(f"  Embedding dim: {cfg.model.embedding_dim}")
    print(f"  Batch size: {cfg.model.batch_size}")
    print(f"\nVeteran Profile:")
    print(f"  Name: {cfg.veteran.name}")
    print(f"  Location: {cfg.veteran.location}")
    print(f"  Salary range: ${cfg.veteran.salary_min:,} - ${cfg.veteran.salary_max:,}")
    print(f"  Skills: {', '.join(cfg.veteran.skills[:5])}...")
