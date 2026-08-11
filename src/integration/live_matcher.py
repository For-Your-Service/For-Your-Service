"""
Live Matcher

Connects real-time job data to the matching pipeline.
End-to-end veteran job matching with live data.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import Dict, List, Optional, Union
from pathlib import Path
import logging

from src.pipeline import MatchingOrchestrator
from src.integration.job_fetcher import JobFetcher


logger = logging.getLogger(__name__)


class LiveMatcher:
    """Live job matching with real-time data"""
    
    def __init__(
        self,
        user_email: str = "whall4.wh@gmail.com",
        similarity_threshold: float = 0.6,
        enable_military_mapping: bool = True
    ):
        """
        Initialize live matcher
        
        Args:
            user_email: Email for API requests
            similarity_threshold: Min similarity for matches
            enable_military_mapping: Enable military skill enrichment
        """
        self.job_fetcher = JobFetcher(user_email=user_email)
        self.orchestrator = MatchingOrchestrator(
            similarity_threshold=similarity_threshold,
            enable_military_mapping=enable_military_mapping
        )
        
        logger.info("LiveMatcher initialized")
    
    def match_veteran_to_live_jobs(
        self,
        resume_path: Union[str, Path],
        location: str = "Greenville, SC",
        keywords: Optional[List[str]] = None,
        job_limit: int = 50,
        salary_min: Optional[int] = None
    ) -> Dict:
        """
        Complete live matching pipeline
        
        Args:
            resume_path: Path to veteran's resume
            location: Target job location
            keywords: Job search keywords
            job_limit: Max number of jobs to fetch
            salary_min: Minimum salary requirement
            
        Returns:
            Complete matching results with live jobs
        """
        logger.info(f"Starting live match for resume: {resume_path}")
        
        # Step 1: Fetch real jobs
        logger.info(f"Fetching live jobs from USAJobs (location: {location})...")
        jobs = self.job_fetcher.fetch_veteran_jobs(
            location=location,
            keywords=keywords,
            limit=job_limit
        )
        
        if not jobs:
            return {
                "error": "No jobs found matching criteria",
                "location": location,
                "keywords": keywords
            }
        
        logger.info(f"✓ Fetched {len(jobs)} veteran-friendly jobs")
        
        # Step 2: Convert to job requirements format
        job_requirements = self._convert_to_requirements(jobs)
        
        # Step 3: Run matching pipeline
        logger.info("Running matching pipeline...")
        results = self.orchestrator.end_to_end_match(
            resume_path=resume_path,
            job_requirements=job_requirements,
            location_filter=location,
            salary_min=salary_min
        )
        
        # Step 4: Enrich with original job data
        results["live_jobs"] = jobs
        results["data_source"] = "USAJobs API (live)"
        results["fetch_timestamp"] = self.job_fetcher._get_timestamp()
        
        logger.info("✓ Matching complete")
        
        return results
    
    def _convert_to_requirements(self, jobs: List[Dict]) -> List[Dict]:
        """
        Convert fetched jobs to pipeline format
        
        Args:
            jobs: List of normalized job dicts
            
        Returns:
            List of job requirement dicts for pipeline
        """
        requirements = []
        
        for job in jobs:
            req = {
                "id": job.get("job_id"),
                "title": job.get("title"),
                "company": job.get("company"),
                "location": job.get("location"),
                "salary_range": job.get("salary_range"),
                "required_skills": [
                    {
                        "skill": skill,
                        "importance": self._infer_importance(skill),
                        "required_level": "Proficient"
                    }
                    for skill in job.get("required_skills", [])
                ]
            }
            requirements.append(req)
        
        return requirements
    
    def _infer_importance(self, skill: str) -> str:
        """
        Infer skill importance based on skill type
        
        Args:
            skill: Skill name
            
        Returns:
            Importance level
        """
        critical_skills = {"AWS", "Azure", "Kubernetes", "Security", "Clearance"}
        important_skills = {"Python", "Docker", "Linux", "Terraform", "CI/CD"}
        
        if skill in critical_skills:
            return "Critical"
        elif skill in important_skills:
            return "Important"
        else:
            return "Nice-to-have"
    
    def match_and_display(
        self,
        resume_path: Union[str, Path],
        **kwargs
    ) -> None:
        """
        Run matching and display results
        
        Args:
            resume_path: Path to resume
            **kwargs: Arguments for match_veteran_to_live_jobs
        """
        results = self.match_veteran_to_live_jobs(resume_path, **kwargs)
        
        if "error" in results:
            print(f"Error: {results['error']}")
            return
        
        # Display results
        self._display_results(results)
    
    def _display_results(self, results: Dict) -> None:
        """
        Pretty print matching results
        
        Args:
            results: Matching results dictionary
        """
        print("=" * 80)
        print("LIVE JOB MATCHING RESULTS")
        print("=" * 80)
        print()
        
        # Candidate info
        candidate = results.get("candidate", {})
        print(f"📋 CANDIDATE: {candidate.get('name', 'Unknown')}")
        print(f"   Email: {candidate.get('email', 'N/A')}")
        print(f"   Location: {candidate.get('location', 'N/A')}")
        print(f"   Experience: {candidate.get('experience_years', 0)} years")
        
        military = candidate.get("military_background", {})
        if military.get("branch"):
            print(f"   🎖️  {military.get('branch')} - {military.get('mos', 'N/A')}")
            if military.get("clearance"):
                print(f"   🔒 Clearance: {military.get('clearance')}")
        print()
        
        # Gap analyses
        gap_analyses = results.get("gap_analyses", [])
        print(f"🎯 TOP MATCHES ({len(gap_analyses)} jobs analyzed)")
        print("-" * 80)
        
        for i, gap_data in enumerate(gap_analyses[:5], 1):
            gap = gap_data.get("gap_analysis")
            print(f"
{i}. {gap_data.get('job_title')} - {gap_data.get('job_id')}")
            print(f"   Match Score: {gap.match_score:.1%}")
            print(f"   ✓ Matching Skills ({len(gap.matching_skills)}): {', '.join(gap.matching_skills[:5])}")
            
            if gap.missing_skills:
                missing_names = [g.skill_name for g in gap.missing_skills[:3]]
                print(f"   ⚠ Missing Skills ({len(gap.missing_skills)}): {', '.join(missing_names)}")
            
            print(f"   🎯 Readiness: {gap.estimated_readiness}")
        
        print()
        print("=" * 80)
        print(f"✓ Analysis complete | Data source: {results.get('data_source')}")
        print("=" * 80)
