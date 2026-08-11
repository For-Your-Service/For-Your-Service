"""
Manual Job Upload Utility

Quickly add jobs from Indeed/LinkedIn/ClearanceJobs by copying job postings.
No API required - paste job text and get instant matches.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group

Usage:
    python scripts/manual_job_upload.py
    
Or import and use programmatically:
    from scripts.manual_job_upload import add_job
    
    job = add_job(
        title="Senior DevOps Engineer",
        company="Michelin",
        location="Greenville, SC",
        description="...",
        salary_range="$125K-$155K",
        url="https://indeed.com/...",
        remote="Hybrid"
    )
"""

import json
import re
from datetime import datetime
from typing import Optional, List, Dict
from pathlib import Path


class ManualJobUploader:
    """Upload jobs manually from any source"""
    
    def __init__(self, cache_dir: str = "data/jobs_cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "manual_jobs.json"
        
        # Load existing jobs
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                self.jobs = json.load(f)
        else:
            self.jobs = []
    
    def add_job(
        self,
        title: str,
        company: str,
        location: str,
        description: str,
        salary_range: str = "Not specified",
        url: str = "",
        remote: str = "Onsite",
        source: str = "manual"
    ) -> Dict:
        """
        Add a single job manually
        
        Args:
            title: Job title
            company: Company name
            location: Location string
            description: Full job description
            salary_range: Salary (e.g., "$120K-$150K")
            url: Job posting URL
            remote: "Remote", "Hybrid", or "Onsite"
            source: Data source (e.g., "indeed", "linkedin")
            
        Returns:
            Normalized job dictionary
        """
        job = {
            "job_id": f"manual_{len(self.jobs) + 1}_{hash(title + company)}",
            "title": title,
            "company": company,
            "location": location,
            "description": description,
            "required_skills": self._extract_skills(description),
            "salary_min": self._parse_salary_min(salary_range),
            "salary_max": self._parse_salary_max(salary_range),
            "salary_range": salary_range,
            "remote": remote,
            "clearance_required": self._check_clearance(description),
            "veteran_friendly": self._check_veteran_friendly(description),
            "posted_date": datetime.now().isoformat(),
            "data_source": source,
            "url": url
        }
        
        self.jobs.append(job)
        self._save()
        
        return job
    
    def add_from_text(self, job_text: str, source: str = "manual") -> Dict:
        """
        Parse and add job from copy-pasted text
        
        Args:
            job_text: Full job posting text
            source: Data source
            
        Returns:
            Normalized job dictionary
        """
        # Basic parsing (can be enhanced)
        lines = [l.strip() for l in job_text.split('\n') if l.strip()]
        
        title = lines[0] if lines else "Unknown"
        company = lines[1] if len(lines) > 1 else "Unknown"
        
        # Try to find location
        location = "Unknown"
        for line in lines[:5]:
            if any(state in line for state in ["SC", "Remote", "Greenville"]):
                location = line
                break
        
        # Try to find salary
        salary_range = "Not specified"
        for line in lines:
            if '$' in line and any(c.isdigit() for c in line):
                salary_range = line
                break
        
        # Remote detection
        remote = "Onsite"
        text_lower = job_text.lower()
        if "remote" in text_lower:
            if "hybrid" in text_lower:
                remote = "Hybrid"
            else:
                remote = "Remote"
        
        return self.add_job(
            title=title,
            company=company,
            location=location,
            description=job_text,
            salary_range=salary_range,
            remote=remote,
            source=source
        )
    
    def get_all_jobs(self) -> List[Dict]:
        """Get all manually uploaded jobs"""
        return self.jobs
    
    def clear_all(self):
        """Clear all jobs"""
        self.jobs = []
        self._save()
    
    def _save(self):
        """Save jobs to cache file"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.jobs, f, indent=2)
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills"""
        if not text:
            return []
        
        text_lower = text.lower()
        
        skills = {
            "aws", "azure", "gcp", "kubernetes", "k8s", "docker",
            "terraform", "ansible", "jenkins", "python", "java",
            "linux", "windows", "ci/cd", "devops", "cloud",
            "databricks", "spark", "pyspark", "sql", "git",
            "bash", "shell", "monitoring", "grafana", "prometheus"
        }
        
        found = []
        for skill in skills:
            if skill in text_lower:
                if skill == "aws":
                    found.append("AWS")
                elif skill == "k8s":
                    found.append("Kubernetes")
                else:
                    found.append(skill.title())
        
        return found
    
    def _parse_salary_min(self, salary_text: str) -> int:
        """Extract minimum salary"""
        numbers = re.findall(r'(\d{1,3}(?:,\d{3})*)', salary_text)
        if numbers:
            try:
                return int(numbers[0].replace(',', '')) * 1000
            except:
                pass
        return 0
    
    def _parse_salary_max(self, salary_text: str) -> int:
        """Extract maximum salary"""
        numbers = re.findall(r'(\d{1,3}(?:,\d{3})*)', salary_text)
        if len(numbers) >= 2:
            try:
                return int(numbers[-1].replace(',', '')) * 1000
            except:
                pass
        elif numbers:
            try:
                return int(numbers[0].replace(',', '')) * 1000
            except:
                pass
        return 0
    
    def _check_clearance(self, text: str) -> Optional[str]:
        """Check for security clearance"""
        if not text:
            return None
        
        text_lower = text.lower()
        
        if "ts/sci" in text_lower or "top secret" in text_lower:
            return "TS/SCI"
        elif "secret clearance" in text_lower:
            return "Secret"
        elif "clearance" in text_lower:
            return "Required"
        
        return None
    
    def _check_veteran_friendly(self, text: str) -> bool:
        """Check for veteran-friendly"""
        if not text:
            return False
        
        text_lower = text.lower()
        keywords = ["veteran", "military", "vets", "gi bill"]
        
        return any(kw in text_lower for kw in keywords)


def quick_demo():
    """Quick demo of manual upload"""
    uploader = ManualJobUploader()
    
    # Example job
    job = uploader.add_job(
        title="Senior DevOps Engineer",
        company="Michelin North America",
        location="Greenville, SC",
        description="""
        We are seeking a Senior DevOps Engineer with strong Kubernetes and AWS experience.
        Work with our hybrid cloud infrastructure supporting manufacturing operations.
        
        Requirements:
        - 5+ years DevOps experience
        - Kubernetes, Docker, AWS
        - Terraform, Python, CI/CD
        - Strong automation skills
        
        Veterans encouraged to apply!
        """,
        salary_range="$125K-$155K",
        url="https://example.com/job",
        remote="Hybrid"
    )
    
    print("✅ Added job:")
    print(f"   {job['title']} - {job['company']}")
    print(f"   Skills: {', '.join(job['required_skills'])}")
    print(f"   Veteran-Friendly: {job['veteran_friendly']}")
    
    return uploader


if __name__ == "__main__":
    quick_demo()
