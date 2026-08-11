"""
Live Integration Module

Real-time job data fetching and matching for veterans.
Connects API scrapers to the matching pipeline.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

__version__ = "0.1.0"

from .job_fetcher import JobFetcher
from .live_matcher import LiveMatcher
from .data_store import JobDataStore

__all__ = [
    "JobFetcher",
    "LiveMatcher",
    "JobDataStore",
]
