"""
Pipeline Orchestration Module

End-to-end pipeline for veteran job matching:
Resume Upload → Parsing → Skill Normalization → Gap Analysis → Job Matching → Recommendations

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

__version__ = "0.1.0"

from .gap_analyzer import GapAnalyzer
from .job_matcher import JobMatcher
from .recommendation_engine import RecommendationEngine
from .orchestrator import MatchingOrchestrator

__all__ = [
    "GapAnalyzer",
    "JobMatcher",
    "RecommendationEngine",
    "MatchingOrchestrator",
]
