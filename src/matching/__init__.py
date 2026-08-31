"""
__init__.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
from .siamese_network import SiameseNetwork
from .encoder import encode_veteran_profile, calculate_similarity

__all__ = ['SiameseNetwork', 'encode_veteran_profile', 'calculate_similarity']
