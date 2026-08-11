"""
Live Integration Module

Real-time job data fetching and matching for veterans.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

__version__ = "0.1.0"

from .job_fetcher import JobFetcher
from .indeed_scraper import IndeedScraper
from .adzuna_client import AdzunaClient

__all__ = [
    "JobFetcher",
    "IndeedScraper",
    "AdzunaClient",
]
