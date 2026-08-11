"""
Data models for gap analysis and recommendations.
"""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class RecommendationType(Enum):
    """Type of career recommendation."""
    RESUME_TAILORING = "resume_tailoring"
    SKILL_GAP = "skill_gap"
    CERTIFICATION = "certification"
    EXPERIENCE_GAP = "experience_gap"
    LOCATION_MISMATCH = "location_mismatch"
    SALARY_EXPECTATION = "salary_expectation"


@dataclass
class Recommendation:
    """Single actionable recommendation."""
    type: RecommendationType
    title: str
    description: str
    impact: int  # Estimated match score improvement (0-100)
    priority: int  # 1 (high) to 5 (low)
    effort: str  # "low", "medium", "high"
    
    # Specific guidance
    action_items: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)


@dataclass
class SkillGap:
    """Missing or weak skill relative to job requirements."""
    skill_name: str
    required_by_job: bool
    candidate_has: bool
    proficiency_gap: Optional[int] = None  # 0-100 if both have skill
    importance: int = 3  # 1 (critical) to 5 (nice-to-have)


@dataclass
class ExperienceGap:
    """Experience requirement mismatch."""
    required_years: Optional[int]
    candidate_years: Optional[int]
    role_type: str
    gap_description: str


@dataclass
class GapAnalysis:
    """
    Complete gap analysis between candidate and job.
    
    Set difference analysis: Job Requirements ∖ Candidate Profile
    """
    job_id: str
    candidate_id: str
    match_score: float  # 0.0 - 1.0 from Siamese network
    
    # Skill analysis
    missing_skills: List[SkillGap] = field(default_factory=list)
    weak_skills: List[SkillGap] = field(default_factory=list)
    matching_skills: List[str] = field(default_factory=list)
    
    # Experience gaps
    experience_gaps: List[ExperienceGap] = field(default_factory=list)
    
    # Certifications
    missing_certifications: List[str] = field(default_factory=list)
    
    # Other factors
    clearance_mismatch: bool = False
    location_distance_miles: Optional[float] = None
    salary_gap: Optional[int] = None
    
    # Recommendations
    recommendations: List[Recommendation] = field(default_factory=list)
    
    def get_critical_gaps(self) -> List[SkillGap]:
        """Return only critical (importance 1-2) skill gaps."""
        return [gap for gap in self.missing_skills if gap.importance <= 2]
    
    def get_high_priority_recommendations(self) -> List[Recommendation]:
        """Return recommendations with priority 1-2."""
        return sorted(
            [r for r in self.recommendations if r.priority <= 2],
            key=lambda r: (r.priority, -r.impact)
        )
