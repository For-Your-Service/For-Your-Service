"""
Data models for parsed resume components.

Structured representations of resume entities extracted from unstructured text.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional, Dict
from enum import Enum


class SkillCategory(Enum):
    """Skill categorization for taxonomy mapping."""
    HARD_SKILL = "hard_skill"
    SOFT_SKILL = "soft_skill"
    TOOL = "tool"
    FRAMEWORK = "framework"
    LANGUAGE = "language"
    CERTIFICATION = "certification"
    CLEARANCE = "clearance"


class ExperienceType(Enum):
    """Type of work experience."""
    MILITARY = "military"
    CIVILIAN = "civilian"
    CONTRACT = "contract"
    VOLUNTEER = "volunteer"


@dataclass
class Skill:
    """Extracted skill with normalization metadata."""
    raw_text: str  # Original text from resume
    normalized_name: Optional[str] = None  # Canonical skill name
    onet_code: Optional[str] = None  # O*NET skill taxonomy ID
    category: Optional[SkillCategory] = None
    confidence: float = 0.0  # Extraction confidence (0-1)
    
    def __hash__(self):
        return hash(self.normalized_name or self.raw_text)


@dataclass
class WorkExperience:
    """Structured work history entry."""
    role_title: str
    organization: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None  # None = current position
    duration_months: Optional[int] = None
    location: Optional[str] = None
    description: Optional[str] = None
    skills_used: List[Skill] = field(default_factory=list)
    experience_type: ExperienceType = ExperienceType.CIVILIAN
    
    # Military-specific fields
    mos_code: Optional[str] = None
    rank: Optional[str] = None
    clearance_level: Optional[str] = None


@dataclass
class Education:
    """Education and certification entry."""
    degree: str
    institution: str
    field_of_study: Optional[str] = None
    graduation_date: Optional[date] = None
    gpa: Optional[float] = None


@dataclass
class ContactInfo:
    """Contact information extracted from resume."""
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None  # City, State
    zip_code: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None


@dataclass
class ParsedResume:
    """
    Complete structured resume representation.
    
    This is the normalized output that feeds into the Siamese network
    for vector embedding generation.
    """
    # Identification
    candidate_id: Optional[str] = None
    raw_text: str = ""
    
    # Contact
    contact: Optional[ContactInfo] = None
    
    # Experience
    work_history: List[WorkExperience] = field(default_factory=list)
    
    # Education
    education: List[Education] = field(default_factory=list)
    
    # Skills
    hard_skills: List[Skill] = field(default_factory=list)
    soft_skills: List[Skill] = field(default_factory=list)
    certifications: List[str] = field(default_factory=list)
    
    # Military context
    is_veteran: bool = False
    military_branch: Optional[str] = None
    years_of_service: Optional[int] = None
    mos_codes: List[str] = field(default_factory=list)
    clearance_level: Optional[str] = None
    
    # Metadata
    total_years_experience: Optional[int] = None
    target_location: Optional[str] = None
    salary_expectation: Optional[int] = None
    
    def get_all_skills(self) -> List[Skill]:
        """Return all skills regardless of category."""
        return self.hard_skills + self.soft_skills
    
    def get_skill_names(self) -> List[str]:
        """Return list of normalized skill names."""
        return [s.normalized_name or s.raw_text for s in self.get_all_skills()]
    
    def get_years_in_role(self, role_title: str) -> int:
        """Calculate total years experience in a specific role."""
        months = sum(
            exp.duration_months or 0
            for exp in self.work_history
            if role_title.lower() in exp.role_title.lower()
        )
        return months // 12
