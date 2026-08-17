"""
Adzuna Response Parser
"""

from typing import Dict
from datetime import datetime


class AdzunaParser:
    """Parser for Adzuna API responses"""

    @staticmethod
    def parse_job(raw_job: Dict) -> Dict:
        """Parse Adzuna job to normalized format"""
        return {
            "source": "adzuna",
            "job_id": str(raw_job.get("id")),
            "title": raw_job.get("title", ""),
            "company": raw_job.get("company", {}).get("display_name", "Unknown"),
            "description": raw_job.get("description", ""),
            "url": raw_job.get("redirect_url", ""),
            "locations": [
                {
                    "display_name": raw_job.get("location", {}).get("display_name", ""),
                    "area": raw_job.get("location", {}).get("area", []),
                }
            ],
            "min_salary": raw_job.get("salary_min"),
            "max_salary": raw_job.get("salary_max"),
            "contract_time": raw_job.get("contract_time"),
            "contract_type": raw_job.get("contract_type"),
            "category": raw_job.get("category", {}).get("label"),
            "posted_date": raw_job.get("created"),
            "fetched_at": datetime.utcnow().isoformat(),
        }
