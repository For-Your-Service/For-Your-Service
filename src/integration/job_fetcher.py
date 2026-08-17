"""
Job Fetcher for Real-Time Data

Fetches live job postings from USAJobs API (free tier).
Filters for veteran-friendly and Greenville, SC area positions.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class JobFetcher:
    """Fetches real job data from USAJobs API"""

    BASE_URL = "https://data.usajobs.gov/api/search"

    def __init__(self, user_email: str = "whall4.wh@gmail.com"):
        """
        Initialize job fetcher

        Args:
            user_email: Email for API user-agent (required by USAJobs)
        """
        self.user_email = user_email
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Host": "data.usajobs.gov",
                "User-Agent": user_email,
            }
        )

    def fetch_veteran_jobs(
        self,
        location: str = "Greenville, SC",
        keywords: Optional[List[str]] = None,
        limit: int = 50,
    ) -> List[Dict]:
        """
        Fetch veteran-friendly federal jobs

        Args:
            location: Target location
            keywords: Job search keywords (DevOps, Cloud, etc.)
            limit: Maximum number of jobs to return

        Returns:
            List of job dictionaries with standardized format
        """
        if keywords is None:
            keywords = ["DevOps", "Cloud", "Kubernetes", "AWS", "Engineer"]

        all_jobs = []

        for keyword in keywords[:3]:  # Limit API calls
            try:
                jobs = self._fetch_by_keyword(keyword, location, limit // len(keywords))
                all_jobs.extend(jobs)
            except Exception as e:
                logger.error(f"Error fetching jobs for '{keyword}': {e}")

        # Deduplicate by job ID
        seen_ids = set()
        unique_jobs = []
        for job in all_jobs:
            job_id = job.get("job_id")
            if job_id not in seen_ids:
                seen_ids.add(job_id)
                unique_jobs.append(job)

        return unique_jobs[:limit]

    def _fetch_by_keyword(self, keyword: str, location: str, limit: int) -> List[Dict]:
        """
        Fetch jobs by single keyword

        Args:
            keyword: Search keyword
            location: Location filter
            limit: Max results

        Returns:
            List of job dictionaries
        """
        params = {
            "Keyword": keyword,
            "LocationName": location,
            "ResultsPerPage": min(limit, 500),  # API max
            "HiringPath": "veterans",  # Veteran preference only
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = data.get("SearchResult", {}).get("SearchResultItems", [])

            logger.info(f"Fetched {len(results)} jobs for keyword '{keyword}'")

            return [self._normalize_job(item) for item in results]

        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed for '{keyword}': {e}")
            return []

    def _normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize USAJobs API response to standard format

        Args:
            raw_job: Raw API response item

        Returns:
            Standardized job dictionary
        """
        matched_obj = raw_job.get("MatchedObjectDescriptor", {})

        # Extract salary
        salary_info = matched_obj.get("PositionRemuneration", [{}])[0]
        salary_min_str = salary_info.get("MinimumRange", "0")
        salary_max_str = salary_info.get("MaximumRange", "0")

        try:
            salary_min = int(salary_min_str.replace(",", ""))
            salary_max = int(salary_max_str.replace(",", ""))
        except (ValueError, AttributeError):
            salary_min = 0
            salary_max = 0

        # Extract location
        locations = matched_obj.get("PositionLocation", [])
        location_str = locations[0].get("LocationName", "Unknown") if locations else "Unknown"

        # Extract skills from qualifications summary
        qualifications = matched_obj.get("QualificationSummary", "")

        return {
            "job_id": matched_obj.get("PositionID", ""),
            "title": matched_obj.get("PositionTitle", "Unknown"),
            "company": matched_obj.get("OrganizationName", "Federal Government"),
            "location": location_str,
            "description": matched_obj.get("UserArea", {}).get("Details", {}).get("JobSummary", ""),
            "qualifications": qualifications,
            "required_skills": self._extract_skills(qualifications),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_range": (
                f"${salary_min:,}-${salary_max:,}" if salary_max > 0 else "Not specified"
            ),
            "remote": "Onsite",  # Federal jobs typically onsite
            "clearance_required": self._check_clearance(qualifications),
            "veteran_friendly": True,  # All from veteran hiring path
            "posted_date": matched_obj.get("PublicationStartDate", datetime.now().isoformat()),
            "data_source": "usajobs",
            "url": matched_obj.get("PositionURI", ""),
        }

    def _extract_skills(self, text: str) -> List[str]:
        """
        Extract technical skills from job description

        Args:
            text: Job description or qualifications text

        Returns:
            List of identified skills
        """
        if not text:
            return []

        text_lower = text.lower()

        # Common technical skills to look for
        skill_keywords = {
            "aws",
            "azure",
            "gcp",
            "kubernetes",
            "k8s",
            "docker",
            "terraform",
            "ansible",
            "jenkins",
            "python",
            "java",
            "linux",
            "windows",
            "networking",
            "security",
            "ci/cd",
            "devops",
            "cloud",
            "scripting",
            "automation",
            "monitoring",
        }

        found_skills = []
        for skill in skill_keywords:
            if skill in text_lower:
                # Capitalize properly
                if skill == "aws":
                    found_skills.append("AWS")
                elif skill == "gcp":
                    found_skills.append("GCP")
                elif skill == "k8s":
                    found_skills.append("Kubernetes")
                elif skill == "ci/cd":
                    found_skills.append("CI/CD")
                else:
                    found_skills.append(skill.title())

        return found_skills

    def _check_clearance(self, text: str) -> Optional[str]:
        """
        Check if security clearance is required

        Args:
            text: Job description text

        Returns:
            Clearance level or None
        """
        if not text:
            return None

        text_lower = text.lower()

        if "top secret" in text_lower or "ts/sci" in text_lower:
            return "TS/SCI"
        elif "secret" in text_lower:
            return "Secret"
        elif "clearance" in text_lower:
            return "Required"

        return None

    def fetch_and_cache(
        self, cache_path: str = "data/jobs_cache/usajobs_latest.json", **kwargs
    ) -> List[Dict]:
        """
        Fetch jobs and cache to file

        Args:
            cache_path: Path to save cached jobs
            **kwargs: Arguments for fetch_veteran_jobs

        Returns:
            List of fetched jobs
        """
        jobs = self.fetch_veteran_jobs(**kwargs)

        # Save to cache
        cache_data = {"fetched_at": datetime.now().isoformat(), "count": len(jobs), "jobs": jobs}

        with open(cache_path, "w") as f:
            json.dump(cache_data, f, indent=2)

        logger.info(f"Cached {len(jobs)} jobs to {cache_path}")

        return jobs
