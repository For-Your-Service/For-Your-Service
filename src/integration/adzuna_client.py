"""
Adzuna API Client

Real job data from Adzuna (free tier: 1000 calls/month).
Aggregates jobs from multiple sources.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import requests
from typing import List, Dict, Optional
from datetime import datetime
import logging


logger = logging.getLogger(__name__)


class AdzunaClient:
    """Client for Adzuna Job Search API (free tier)"""
    
    BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search"
    
    def __init__(self, app_id: str = None, app_key: str = None):
        """
        Initialize Adzuna client
        
        Args:
            app_id: Adzuna App ID (get free at https://developer.adzuna.com)
            app_key: Adzuna App Key
        """
        # Using demo credentials for now (limited but works)
        self.app_id = app_id or "test"
        self.app_key = app_key or "test"
        self.session = requests.Session()
    
    def search_jobs(
        self,
        keywords: str = "DevOps Engineer",
        location: str = "Greenville, SC",
        max_days_old: int = 30,
        results_per_page: int = 50,
        page: int = 1,
        salary_min: Optional[int] = None,
        full_time: bool = True
    ) -> List[Dict]:
        """
        Search for jobs on Adzuna
        
        Args:
            keywords: Job search keywords
            location: Location (city, state)
            max_days_old: Only jobs posted in last N days
            results_per_page: Number of results (max 50)
            page: Page number for pagination
            salary_min: Minimum salary filter
            full_time: Full-time positions only
            
        Returns:
            List of normalized job dictionaries
        """
        params = {
            "app_id": self.app_id,
            "app_key": self.app_key,
            "what": keywords,
            "where": location,
            "max_days_old": max_days_old,
            "results_per_page": min(results_per_page, 50),
            "page": page,
            "content-type": "application/json"
        }
        
        if salary_min:
            params["salary_min"] = salary_min
        
        if full_time:
            params["full_time"] = 1
        
        try:
            url = f"{self.BASE_URL}/{page}"
            response = self.session.get(url, params=params, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            results = data.get("results", [])
            
            logger.info(f"Fetched {len(results)} jobs from Adzuna")
            
            return [self._normalize_job(job) for job in results]
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Adzuna API request failed: {e}")
            return []
    
    def search_veteran_jobs(
        self,
        location: str = "Greenville, SC",
        keywords: List[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """
        Search for veteran-relevant tech jobs
        
        Args:
            location: Target location
            keywords: List of job keywords
            limit: Max number of jobs
            
        Returns:
            Deduplicated list of jobs
        """
        if keywords is None:
            keywords = [
                "DevOps Engineer",
                "Cloud Engineer", 
                "Solutions Architect",
                "Platform Engineer",
                "Site Reliability Engineer"
            ]
        
        all_jobs = []
        
        for keyword in keywords[:3]:  # Top 3 to stay under rate limit
            try:
                jobs = self.search_jobs(
                    keywords=keyword,
                    location=location,
                    results_per_page=20,
                    salary_min=100000
                )
                all_jobs.extend(jobs)
            except Exception as e:
                logger.error(f"Error fetching '{keyword}': {e}")
        
        # Deduplicate by job ID
        seen_ids = set()
        unique_jobs = []
        for job in all_jobs:
            job_id = job.get("job_id")
            if job_id not in seen_ids:
                seen_ids.add(job_id)
                unique_jobs.append(job)
        
        return unique_jobs[:limit]
    
    def _normalize_job(self, raw_job: Dict) -> Dict:
        """
        Normalize Adzuna response to standard format
        
        Args:
            raw_job: Raw API response
            
        Returns:
            Standardized job dictionary
        """
        # Extract location
        location_parts = []
        if raw_job.get("location", {}).get("display_name"):
            location_parts.append(raw_job["location"]["display_name"])
        
        location_str = ", ".join(location_parts) if location_parts else "Remote"
        
        # Extract salary
        salary_min = int(raw_job.get("salary_min", 0))
        salary_max = int(raw_job.get("salary_max", 0))
        
        # Extract skills from description
        description = raw_job.get("description", "")
        
        return {
            "job_id": raw_job.get("id", ""),
            "title": raw_job.get("title", "Unknown"),
            "company": raw_job.get("company", {}).get("display_name", "Unknown"),
            "location": location_str,
            "description": description,
            "required_skills": self._extract_skills(description),
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_range": f"${salary_min:,}-${salary_max:,}" if salary_max > 0 else "Not specified",
            "remote": self._detect_remote(description, raw_job.get("title", "")),
            "clearance_required": self._check_clearance(description),
            "veteran_friendly": self._check_veteran_friendly(description),
            "posted_date": raw_job.get("created", datetime.now().isoformat()),
            "data_source": "adzuna",
            "url": raw_job.get("redirect_url", "")
        }
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from job description"""
        if not text:
            return []
        
        text_lower = text.lower()
        
        skill_keywords = {
            "aws", "azure", "gcp", "kubernetes", "k8s", "docker",
            "terraform", "ansible", "jenkins", "python", "java",
            "linux", "windows", "networking", "security", "ci/cd",
            "devops", "cloud", "scripting", "automation", "monitoring",
            "databricks", "spark", "pyspark", "sql", "postgresql",
            "git", "github", "gitlab", "helm", "grafana", "prometheus"
        }
        
        found_skills = []
        for skill in skill_keywords:
            if skill in text_lower:
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
    
    def _detect_remote(self, description: str, title: str) -> str:
        """Detect if job is remote/hybrid/onsite"""
        text = (description + " " + title).lower()
        
        if "remote" in text or "work from home" in text:
            if "hybrid" in text:
                return "Hybrid"
            return "Remote"
        return "Onsite"
    
    def _check_clearance(self, text: str) -> Optional[str]:
        """Check if security clearance required"""
        if not text:
            return None
        
        text_lower = text.lower()
        
        if "top secret" in text_lower or "ts/sci" in text_lower:
            return "TS/SCI"
        elif "secret" in text_lower and "clearance" in text_lower:
            return "Secret"
        elif "clearance" in text_lower:
            return "Required"
        
        return None
    
    def _check_veteran_friendly(self, text: str) -> bool:
        """Check if employer is veteran-friendly"""
        if not text:
            return False
        
        text_lower = text.lower()
        veteran_keywords = ["veteran", "military", "vets", "gi bill"]
        
        return any(keyword in text_lower for keyword in veteran_keywords)
