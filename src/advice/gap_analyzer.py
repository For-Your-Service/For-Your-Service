"""
Gap analysis engine.

Performs set difference analysis: Job Requirements ∖ Candidate Skills
"""

from typing import List, Set
from .models import GapAnalysis, SkillGap, ExperienceGap, SkillGap
from ..resume_parsing.models import ParsedResume


class GapAnalyzer:
    """Analyze gaps between candidate and job requirements."""
    
    def analyze(
        self,
        candidate: ParsedResume,
        job_skills: List[str],
        job_required_years: int = None,
        job_certifications: List[str] = None,
        job_clearance: str = None,
        match_score: float = 0.0
    ) -> GapAnalysis:
        """
        Perform complete gap analysis.
        
        Args:
            candidate: Parsed resume
            job_skills: Required skills from job posting
            job_required_years: Years experience required
            job_certifications: Required certifications
            job_clearance: Required clearance level
            match_score: Neural network match score (0-1)
            
        Returns:
            Complete gap analysis with recommendations
        """
        candidate_skills = set(candidate.get_skill_names())
        job_skills_set = set(s.lower() for s in job_skills)
        
        # Calculate skill gaps
        missing = job_skills_set - candidate_skills
        matching = job_skills_set & candidate_skills
        
        missing_skills = [
            SkillGap(
                skill_name=skill,
                required_by_job=True,
                candidate_has=False,
                importance=self._estimate_importance(skill, job_skills)
            )
            for skill in missing
        ]
        
        # Experience gap
        experience_gaps = []
        if job_required_years and candidate.total_years_experience:
            if candidate.total_years_experience < job_required_years:
                gap = job_required_years - candidate.total_years_experience
                experience_gaps.append(ExperienceGap(
                    required_years=job_required_years,
                    candidate_years=candidate.total_years_experience,
                    role_type="general",
                    gap_description=f"Need {gap} more years of experience"
                ))
        
        # Certification gaps
        candidate_certs = set(c.lower() for c in candidate.certifications)
        job_certs_set = set(c.lower() for c in (job_certifications or []))
        missing_certs = list(job_certs_set - candidate_certs)
        
        # Clearance mismatch
        clearance_mismatch = False
        if job_clearance and not candidate.clearance_level:
            clearance_mismatch = True
        
        return GapAnalysis(
            job_id="unknown",
            candidate_id=candidate.candidate_id or "unknown",
            match_score=match_score,
            missing_skills=missing_skills,
            matching_skills=list(matching),
            experience_gaps=experience_gaps,
            missing_certifications=missing_certs,
            clearance_mismatch=clearance_mismatch
        )
    
    @staticmethod
    def _estimate_importance(skill: str, all_job_skills: List[str]) -> int:
        """
        Estimate skill importance (1-5) based on context.
        
        Heuristic: Skills mentioned early or in uppercase are more important.
        """
        skill_lower = skill.lower()
        
        # Critical infrastructure skills
        if skill_lower in ['kubernetes', 'aws', 'terraform', 'docker']:
            return 1
        
        # Important but not critical
        if skill_lower in ['python', 'bash', 'jenkins', 'ansible']:
            return 2
        
        # Standard skills
        return 3
