"""
__init__.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
from .indeed_scraper import fetch_indeed_jobs, parse_job_response, normalize_location

__all__ = ['fetch_indeed_jobs', 'parse_job_response', 'normalize_location']
