"""
Career Advice & Gap Analysis Module

Deterministic feedback generation explaining match scores and providing
actionable recommendations for resume improvement and skill development.
"""

from .gap_analyzer import GapAnalyzer
from .resume_advisor import ResumeAdvisor
from .skill_advisor import SkillAdvisor
from .models import GapAnalysis, Recommendation, RecommendationType

__all__ = [
    'GapAnalyzer',
    'ResumeAdvisor',
    'SkillAdvisor',
    'GapAnalysis',
    'Recommendation',
    'RecommendationType'
]
