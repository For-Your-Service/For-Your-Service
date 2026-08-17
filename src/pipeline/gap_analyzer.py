"""
Gap Analyzer

Analyzes skill gaps between candidate resume and job requirements.
Provides actionable recommendations for closing gaps.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class SkillGap:
    """Represents a missing or weak skill"""

    skill_name: str
    importance: str  # "Critical", "Important", "Nice-to-have"
    current_level: Optional[str] = None  # None if missing, else proficiency
    target_level: str = "Proficient"
    learning_resources: List[str] = None
    estimated_time: str = None  # e.g., "2-4 weeks"

    def __post_init__(self):
        if self.learning_resources is None:
            self.learning_resources = []


@dataclass
class GapAnalysis:
    """Complete gap analysis result"""

    matching_skills: List[str]
    missing_skills: List[SkillGap]
    weak_skills: List[SkillGap]
    match_score: float  # 0.0-1.0
    recommendations: List[str]
    certification_suggestions: List[str]
    estimated_readiness: str  # "Ready Now", "1-2 months", "3-6 months"


class GapAnalyzer:
    """Analyzes skills gaps between candidates and jobs"""

    def __init__(self):
        """Initialize gap analyzer"""

        # Learning resources for common skills
        self.learning_resources = {
            "AWS": [
                "AWS Certified Solutions Architect - Associate",
                "A Cloud Guru AWS Courses",
                "AWS Free Tier Hands-on Labs",
            ],
            "Kubernetes": [
                "Certified Kubernetes Administrator (CKA)",
                "Kubernetes.io Official Tutorials",
                "KodeKloud Kubernetes Courses",
            ],
            "Terraform": [
                "HashiCorp Terraform Associate Certification",
                "Terraform Up & Running (Book)",
                "HashiCorp Learn Platform",
            ],
            "Python": [
                "Python.org Official Tutorial",
                "Automate the Boring Stuff with Python",
                "Real Python Tutorials",
            ],
            "Docker": [
                "Docker Official Documentation",
                "Docker Deep Dive (Book)",
                "Play with Docker Labs",
            ],
        }

        # Estimated learning time for skills
        self.learning_time = {
            "AWS": "4-8 weeks",
            "Kubernetes": "6-10 weeks",
            "Terraform": "2-4 weeks",
            "Python": "8-12 weeks",
            "Docker": "2-4 weeks",
            "Jenkins": "2-3 weeks",
            "Git": "1-2 weeks",
        }

    def analyze(
        self,
        candidate_skills: List[str],
        job_requirements: List[Dict],
        candidate_experience_years: float = 0,
    ) -> GapAnalysis:
        """
        Perform gap analysis between candidate and job

        Args:
            candidate_skills: List of candidate skill names
            job_requirements: List of dicts with {skill, importance, required_level}
            candidate_experience_years: Total years of experience

        Returns:
            GapAnalysis with matching/missing skills and recommendations
        """
        # Normalize skill names for comparison
        candidate_set = {s.lower().strip() for s in candidate_skills}

        matching_skills = []
        missing_skills = []
        weak_skills = []

        # Analyze each job requirement
        for req in job_requirements:
            skill_name = req.get("skill", "")
            importance = req.get("importance", "Important")
            required_level = req.get("required_level", "Proficient")

            skill_lower = skill_name.lower().strip()

            if skill_lower in candidate_set:
                matching_skills.append(skill_name)
            else:
                # Missing skill
                gap = SkillGap(
                    skill_name=skill_name,
                    importance=importance,
                    current_level=None,
                    target_level=required_level,
                    learning_resources=self.learning_resources.get(skill_name, []),
                    estimated_time=self.learning_time.get(skill_name, "4-6 weeks"),
                )
                missing_skills.append(gap)

        # Calculate match score
        total_skills = len(job_requirements)
        if total_skills > 0:
            # Weight by importance
            importance_weights = {"Critical": 3.0, "Important": 2.0, "Nice-to-have": 1.0}

            max_score = sum(
                importance_weights.get(req.get("importance", "Important"), 2.0)
                for req in job_requirements
            )

            earned_score = sum(
                importance_weights.get(req.get("importance", "Important"), 2.0)
                for req in job_requirements
                if req.get("skill", "").lower().strip() in candidate_set
            )

            match_score = earned_score / max_score if max_score > 0 else 0.0
        else:
            match_score = 1.0

        # Generate recommendations
        recommendations = self._generate_recommendations(
            matching_skills, missing_skills, candidate_experience_years
        )

        # Certification suggestions
        cert_suggestions = self._suggest_certifications(missing_skills)

        # Estimate readiness
        readiness = self._estimate_readiness(match_score, missing_skills)

        return GapAnalysis(
            matching_skills=matching_skills,
            missing_skills=missing_skills,
            weak_skills=weak_skills,
            match_score=match_score,
            recommendations=recommendations,
            certification_suggestions=cert_suggestions,
            estimated_readiness=readiness,
        )

    def _generate_recommendations(
        self, matching_skills: List[str], missing_skills: List[SkillGap], experience_years: float
    ) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []

        # Highlight strengths
        if matching_skills:
            recommendations.append(
                f"✓ Strong foundation: You already have {len(matching_skills)} "
                f"of the required skills including {', '.join(matching_skills[:3])}"
            )

        # Prioritize critical gaps
        critical_gaps = [g for g in missing_skills if g.importance == "Critical"]
        if critical_gaps:
            recommendations.append(
                f"⚠ Priority: Focus on critical skills first - "
                f"{', '.join([g.skill_name for g in critical_gaps[:3]])}"
            )

        # Experience-based advice
        if experience_years < 3:
            recommendations.append(
                "💡 Build hands-on projects to demonstrate missing skills - "
                "GitHub portfolio highly valuable"
            )
        elif experience_years >= 10:
            recommendations.append(
                "💡 Leverage your extensive experience - highlight transferable "
                "skills and leadership in applications"
            )

        # Learning path
        if missing_skills:
            top_gap = missing_skills[0]
            recommendations.append(
                f"📚 Start with {top_gap.skill_name} - " f"estimated time: {top_gap.estimated_time}"
            )

        return recommendations

    def _suggest_certifications(self, missing_skills: List[SkillGap]) -> List[str]:
        """Suggest relevant certifications"""
        cert_map = {
            "aws": "AWS Certified Solutions Architect - Associate",
            "azure": "Microsoft Azure Administrator Associate",
            "kubernetes": "Certified Kubernetes Administrator (CKA)",
            "terraform": "HashiCorp Certified: Terraform Associate",
            "docker": "Docker Certified Associate",
            "jenkins": "CloudBees Jenkins Certification",
        }

        suggestions = []
        for gap in missing_skills:
            skill_lower = gap.skill_name.lower()
            for key, cert in cert_map.items():
                if key in skill_lower and cert not in suggestions:
                    suggestions.append(cert)

        return suggestions

    def _estimate_readiness(self, match_score: float, missing_skills: List[SkillGap]) -> str:
        """Estimate time to job readiness"""
        if match_score >= 0.8:
            return "Ready Now - Apply immediately"

        critical_missing = sum(1 for g in missing_skills if g.importance == "Critical")

        if critical_missing == 0 and match_score >= 0.6:
            return "1-2 months - Upskill on nice-to-haves"
        elif critical_missing <= 2:
            return "2-4 months - Focus on critical gaps"
        else:
            return "4-6 months - Significant skill development needed"

    def get_skill_priority_order(self, gaps: List[SkillGap]) -> List[SkillGap]:
        """
        Sort gaps by learning priority

        Args:
            gaps: List of skill gaps

        Returns:
            Sorted list (highest priority first)
        """
        importance_order = {"Critical": 0, "Important": 1, "Nice-to-have": 2}

        return sorted(gaps, key=lambda g: (importance_order.get(g.importance, 3), g.skill_name))
