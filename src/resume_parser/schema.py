"""
Resume Schema Definitions

Structured data models for parsed resume information.
Uses dataclasses for type safety and serialization.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from dataclasses import dataclass, field
from typing import List, Optional
from datetime import date


@dataclass
class SkillEntry:
    """Individual skill extracted from resume"""
    name: str
    category: Optional[str] = None  # e.g., "Technical", "Leadership"
    proficiency: Optional[str] = None  # e.g., "Expert", "Intermediate"
    years_experience: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "name": self.name,
            "category": self.category,
            "proficiency": self.proficiency,
            "years_experience": self.years_experience
        }


@dataclass
class ExperienceEntry:
    """Work experience entry"""
    title: str
    company: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None  # None indicates current position
    location: Optional[str] = None
    description: Optional[str] = None
    achievements: List[str] = field(default_factory=list)
    
    @property
    def duration_years(self) -> Optional[float]:
        """Calculate experience duration in years"""
        if not self.start_date:
            return None
        end = self.end_date or date.today()
        delta = end - self.start_date
        return round(delta.days / 365.25, 1)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "title": self.title,
            "company": self.company,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "location": self.location,
            "description": self.description,
            "achievements": self.achievements,
            "duration_years": self.duration_years
        }


@dataclass
class EducationEntry:
    """Education entry"""
    degree: str
    institution: str
    field_of_study: Optional[str] = None
    graduation_date: Optional[date] = None
    gpa: Optional[float] = None
    honors: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "degree": self.degree,
            "institution": self.institution,
            "field_of_study": self.field_of_study,
            "graduation_date": self.graduation_date.isoformat() if self.graduation_date else None,
            "gpa": self.gpa,
            "honors": self.honors
        }


@dataclass
class ResumeSchema:
    """Complete structured resume data"""
    # Contact Information
    full_name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    
    # Professional Summary
    summary: Optional[str] = None
    
    # Core Data
    skills: List[SkillEntry] = field(default_factory=list)
    experience: List[ExperienceEntry] = field(default_factory=list)
    education: List[EducationEntry] = field(default_factory=list)
    
    # Veteran-Specific Fields
    military_branch: Optional[str] = None
    military_mos: Optional[str] = None  # Military Occupational Specialty
    security_clearance: Optional[str] = None
    years_of_service: Optional[float] = None
    
    # Certifications
    certifications: List[str] = field(default_factory=list)
    
    # Metadata
    raw_text: Optional[str] = None  # Full extracted text
    parse_timestamp: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "location": self.location,
            "linkedin_url": self.linkedin_url,
            "github_url": self.github_url,
            "summary": self.summary,
            "skills": [s.to_dict() for s in self.skills],
            "experience": [e.to_dict() for e in self.experience],
            "education": [e.to_dict() for e in self.education],
            "military_branch": self.military_branch,
            "military_mos": self.military_mos,
            "security_clearance": self.security_clearance,
            "years_of_service": self.years_of_service,
            "certifications": self.certifications,
            "raw_text": self.raw_text,
            "parse_timestamp": self.parse_timestamp
        }
    
    @property
    def total_years_experience(self) -> float:
        """Calculate total years of professional experience"""
        total = sum(
            exp.duration_years for exp in self.experience 
            if exp.duration_years is not None
        )
        if self.years_of_service:
            total += self.years_of_service
        return round(total, 1)
