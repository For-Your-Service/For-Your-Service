"""
Manual Real Job Data Uploader

For when API credentials are unavailable - allows manual entry of REAL jobs
from Indeed, LinkedIn, Glassdoor, etc.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import json
import os
from datetime import datetime
from typing import Dict, List


class ManualRealJobUploader:
    """Upload REAL job data manually scraped from job boards"""
    
    def __init__(self, volume_path: str = "/Volumes/workspace/for_your_service/job_data"):
        self.volume_path = volume_path
        self.raw_path = f"{volume_path}/raw"
        os.makedirs(self.raw_path, exist_ok=True)
    
    def add_real_job_from_indeed(
        self,
        job_url: str,
        title: str,
        company: str,
        location: str,
        description: str,
        salary_text: str = None,
        posted_date: str = None
    ) -> Dict:
        """
        Add a REAL job manually scraped from Indeed
        
        Args:
            job_url: Indeed job URL
            title: Job title
            company: Company name
            location: Job location
            description: Full job description
            salary_text: Salary (e.g., "$120K-$150K")
            posted_date: Posted date (e.g., "2 days ago")
        
        Returns:
            Job record
        """
        job = {
            "id": f"indeed_{hash(job_url)}",
            "source": "indeed",
            "title": title,
            "company": {"display_name": company},
            "location": {"display_name": location},
            "description": description,
            "salary_text": salary_text,
            "posted_date": posted_date,
            "url": job_url,
            "fetched_at": datetime.now().isoformat()
        }
        
        return job
    
    def add_real_job_from_linkedin(
        self,
        job_url: str,
        title: str,
        company: str,
        location: str,
        description: str,
        salary_range: str = None,
        posted_date: str = None
    ) -> Dict:
        """
        Add a REAL job manually scraped from LinkedIn
        """
        job = {
            "id": f"linkedin_{hash(job_url)}",
            "source": "linkedin",
            "title": title,
            "company": {"display_name": company},
            "location": {"display_name": location},
            "description": description,
            "salary_range": salary_range,
            "posted_date": posted_date,
            "url": job_url,
            "fetched_at": datetime.now().isoformat()
        }
        
        return job
    
    def save_jobs_to_volume(self, jobs: List[Dict], source_name: str = "manual"):
        """
        Save REAL job list to UC Volume
        
        Args:
            jobs: List of real job dictionaries
            source_name: Source identifier (e.g., "indeed", "linkedin")
        
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"jobs_{source_name}_{timestamp}.json"
        filepath = f"{self.raw_path}/{filename}"
        
        payload = {
            "fetched_at": datetime.now().isoformat(),
            "source": source_name,
            "count": len(jobs),
            "results": jobs
        }
        
        with open(filepath, 'w') as f:
            json.dump(payload, f, indent=2)
        
        print(f"✅ Saved {len(jobs)} REAL jobs to: {filepath}")
        
        return filepath


# ====================================================================================
# DEMO: Add REAL jobs manually
# ====================================================================================

def demo_manual_upload():
    """
    Demo: Manually add REAL jobs scraped from Indeed/LinkedIn
    
    INSTRUCTION: Replace these with ACTUAL job postings
    """
    uploader = ManualRealJobUploader()
    
    real_jobs = []
    
    # REAL JOB 1: Indeed (example - replace with actual data)
    real_jobs.append(uploader.add_real_job_from_indeed(
        job_url="https://www.indeed.com/viewjob?jk=ACTUAL_JOB_ID",
        title="Senior DevOps Engineer",
        company="ACTUAL COMPANY NAME",
        location="Greenville, SC",
        description="ACTUAL FULL JOB DESCRIPTION FROM INDEED",
        salary_text="$130,000 - $160,000 per year",
        posted_date="3 days ago"
    ))
    
    # REAL JOB 2: LinkedIn (example - replace with actual data)
    real_jobs.append(uploader.add_real_job_from_linkedin(
        job_url="https://www.linkedin.com/jobs/view/ACTUAL_JOB_ID",
        title="Cloud Solutions Architect",
        company="ACTUAL COMPANY NAME",
        location="Remote",
        description="ACTUAL FULL JOB DESCRIPTION FROM LINKEDIN",
        salary_range="$140K - $180K",
        posted_date="1 week ago"
    ))
    
    # Save to UC Volume
    filepath = uploader.save_jobs_to_volume(real_jobs, source_name="manual_scrape")
    
    return filepath


if __name__ == "__main__":
    demo_manual_upload()
