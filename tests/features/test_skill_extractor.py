"""
Tests for skill extraction
"""
import pytest
from src.features.skill_extractor import SkillExtractor


def test_extract_technical_skills():
    """Test technical skill extraction"""
    extractor = SkillExtractor()
    
    text = "Looking for Python developer with AWS and Docker experience"
    skills = extractor.extract_skills(text)
    
    assert "python" in skills["technical"]
    assert "aws" in skills["technical"]
    assert "docker" in skills["technical"]


def test_normalize_skill_name():
    """Test skill name normalization"""
    extractor = SkillExtractor()
    
    assert extractor.normalize_skill_name("K8s") == "kubernetes"
    assert extractor.normalize_skill_name("EKS") == "kubernetes"
