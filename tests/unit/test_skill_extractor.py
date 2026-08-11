"""Unit tests for skill extraction."""
import pytest
from src.resume_parsing.skill_extractor import SkillExtractor
from src.resume_parsing.models import SkillCategory

def test_extract_tech_skills():
    """Test technical skill extraction."""
    text = "Experience with Kubernetes, Docker, and AWS"
    extractor = SkillExtractor()
    skills = extractor.extract(text)
    
    skill_names = {s.normalized_name for s in skills}
    assert 'kubernetes' in skill_names
    assert 'docker' in skill_names
    assert 'aws' in skill_names

def test_extract_clearances():
    """Test clearance detection."""
    text = "Hold active TS/SCI clearance"
    extractor = SkillExtractor()
    skills = extractor.extract(text)
    
    clearances = [s for s in skills if s.category == SkillCategory.CLEARANCE]
    assert len(clearances) > 0
    assert any('ts/sci' in s.normalized_name for s in clearances)
