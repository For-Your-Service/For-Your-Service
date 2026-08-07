"""
Tests for MOS mapping
"""
import pytest
from src.features.mos_mapper import MOSMapper


def test_get_civilian_occupations():
    """Test MOS to O*NET mapping"""
    mapper = MOSMapper()
    
    # Army IT Specialist
    onet_codes = mapper.get_civilian_occupations("25B")
    assert len(onet_codes) > 0
    assert "15-1231.00" in onet_codes or "15-1232.00" in onet_codes


def test_get_skills_from_mos():
    """Test skill extraction from MOS"""
    mapper = MOSMapper()
    
    skills = mapper.get_skills_from_mos("25B")
    assert "networking" in skills or "cisco" in skills
