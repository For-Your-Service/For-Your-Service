"""
Matching Orchestrator

End-to-end pipeline orchestration for veteran job matching.
Coordinates: Resume → Parse → Normalize → Match → Recommend

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import Dict, List, Optional, Union
from pathlib import Path
import logging

from src.resume_parser import PDFResumeParser, DOCXResumeParser, ResumeSchema
from src.skill_taxonomy import SkillNormalizer, MilitarySkillMapper
from .gap_analyzer import GapAnalyzer
from .job_matcher import JobMatcher
from .recommendation_engine import RecommendationEngine

logger = logging.getLogger(__name__)


class MatchingOrchestrator:
    """Orchestrates end-to-end job matching pipeline"""

    def __init__(self, similarity_threshold: float = 0.6, enable_military_mapping: bool = True):
        """
        Initialize orchestrator with all pipeline components

        Args:
            similarity_threshold: Min similarity for job matches
            enable_military_mapping: Whether to enrich with military skills
        """
        # Initialize parsers
        self.pdf_parser = PDFResumeParser()
        self.docx_parser = DOCXResumeParser()

        # Initialize skill processors
        self.skill_normalizer = SkillNormalizer()
        self.military_mapper = MilitarySkillMapper()
        self.enable_military_mapping = enable_military_mapping

        # Initialize matching components
        self.gap_analyzer = GapAnalyzer()
        self.job_matcher = JobMatcher(similarity_threshold=similarity_threshold)
        self.recommendation_engine = RecommendationEngine()

        logger.info("MatchingOrchestrator initialized")

    def process_resume(self, resume_path: Union[str, Path]) -> ResumeSchema:
        """
        Parse and normalize resume

        Args:
            resume_path: Path to resume file (PDF or DOCX)

        Returns:
            Parsed and enriched ResumeSchema
        """
        path = Path(resume_path)

        # Select appropriate parser
        if path.suffix.lower() == ".pdf":
            resume = self.pdf_parser.parse(path)
        elif path.suffix.lower() == ".docx":
            resume = self.docx_parser.parse(path)
        else:
            raise ValueError(f"Unsupported file format: {path.suffix}")

        logger.info(f"Parsed resume for {resume.full_name}")

        # Normalize skills
        if resume.skills:
            skill_names = [s.name for s in resume.skills]
            normalized = self.skill_normalizer.normalize_skills(skill_names)

            # Update with canonical names
            for i, norm in enumerate(normalized):
                if i < len(resume.skills):
                    resume.skills[i].name = norm["canonical_name"]
                    resume.skills[i].category = norm["category"]

        # Enrich with military skills if applicable
        if self.enable_military_mapping and resume.military_mos and resume.military_branch:
            resume_dict = resume.to_dict()
            enriched = self.military_mapper.enrich_resume_with_military_skills(resume_dict)

            # Add military-derived skills
            military_skills = enriched.get("skills", [])
            existing_skill_names = {s.name for s in resume.skills}

            for skill_name in military_skills:
                if skill_name not in existing_skill_names:
                    from src.resume_parser.schema import SkillEntry

                    resume.skills.append(SkillEntry(name=skill_name, category="Military-Derived"))

            logger.info(f"Enriched with {len(military_skills)} military skills")

        return resume

    def match_jobs(
        self,
        resume: ResumeSchema,
        job_requirements: List[Dict],
        location_filter: Optional[str] = None,
        salary_min: Optional[int] = None,
    ) -> Dict:
        """
        Complete matching pipeline: analyze gaps and find job matches

        Args:
            resume: Parsed resume
            job_requirements: List of job requirement dicts
            location_filter: Optional location preference
            salary_min: Optional minimum salary

        Returns:
            Complete matching results with gaps and recommendations
        """
        # Extract candidate skills
        candidate_skills = [s.name for s in resume.skills]

        # Perform gap analysis for each job
        gap_analyses = []
        for job in job_requirements:
            gap = self.gap_analyzer.analyze(
                candidate_skills=candidate_skills,
                job_requirements=job.get("required_skills", []),
                candidate_experience_years=resume.total_years_experience,
            )
            gap_analyses.append(
                {"job_id": job.get("id"), "job_title": job.get("title"), "gap_analysis": gap}
            )

        # Generate recommendations
        if gap_analyses:
            best_gap = max(gap_analyses, key=lambda x: x["gap_analysis"].match_score)
            recommendations = self.recommendation_engine.generate_recommendations(
                resume_data=resume.to_dict(),
                gap_analysis=best_gap["gap_analysis"].__dict__,
                target_jobs=job_requirements,
            )
        else:
            recommendations = None

        return {
            "candidate": {
                "name": resume.full_name,
                "email": resume.email,
                "location": resume.location,
                "skills": candidate_skills,
                "experience_years": resume.total_years_experience,
                "military_background": {
                    "branch": resume.military_branch,
                    "mos": resume.military_mos,
                    "clearance": resume.security_clearance,
                },
            },
            "gap_analyses": gap_analyses,
            "recommendations": recommendations,
            "summary": {
                "total_jobs_analyzed": len(job_requirements),
                "best_match_score": best_gap["gap_analysis"].match_score if gap_analyses else 0.0,
                "average_match_score": (
                    sum(g["gap_analysis"].match_score for g in gap_analyses) / len(gap_analyses)
                    if gap_analyses
                    else 0.0
                ),
            },
        }

    def end_to_end_match(
        self,
        resume_path: Union[str, Path],
        job_requirements: List[Dict],
        location_filter: Optional[str] = None,
        salary_min: Optional[int] = None,
    ) -> Dict:
        """
        Complete end-to-end matching pipeline

        Args:
            resume_path: Path to resume file
            job_requirements: List of job requirement dicts
            location_filter: Optional location preference
            salary_min: Optional minimum salary

        Returns:
            Complete matching results
        """
        # Step 1: Parse resume
        resume = self.process_resume(resume_path)

        # Step 2: Match jobs
        results = self.match_jobs(
            resume=resume,
            job_requirements=job_requirements,
            location_filter=location_filter,
            salary_min=salary_min,
        )

        logger.info(
            f"Matching complete: {results['summary']['total_jobs_analyzed']} jobs, "
            f"best match: {results['summary']['best_match_score']:.2f}"
        )

        return results

    def batch_process(
        self, resume_paths: List[Union[str, Path]], job_requirements: List[Dict]
    ) -> Dict[str, Dict]:
        """
        Process multiple resumes against job requirements

        Args:
            resume_paths: List of resume file paths
            job_requirements: List of job requirement dicts

        Returns:
            Dict mapping resume path to results
        """
        results = {}

        for resume_path in resume_paths:
            try:
                result = self.end_to_end_match(resume_path, job_requirements)
                results[str(resume_path)] = result
            except Exception as e:
                logger.error(f"Error processing {resume_path}: {e}")
                results[str(resume_path)] = {"error": str(e)}

        return results
