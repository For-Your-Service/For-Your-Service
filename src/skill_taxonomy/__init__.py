"""
Skill Taxonomy Module

Normalizes and canonicalizes skills using O*NET taxonomy.
Maps military occupational specialties to civilian skills.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

__version__ = "0.1.0"

from .onet_client import ONetClient
from .skill_normalizer import SkillNormalizer
from .military_mapper import MilitarySkillMapper
from .taxonomy_cache import TaxonomyCache

__all__ = [
    "ONetClient",
    "SkillNormalizer",
    "MilitarySkillMapper",
    "TaxonomyCache",
]
