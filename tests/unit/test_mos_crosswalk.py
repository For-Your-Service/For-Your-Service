"""Unit tests for MOS crosswalk."""
import pytest
from src.taxonomy.mos_crosswalk import MOSCrosswalk

def test_get_civilian_skills():
    """Test MOS to civilian skill mapping."""
    skills = MOSCrosswalk.get_civilian_skills('25B')
    assert 'network administration' in skills
    assert 'cisco' in skills

def test_special_forces_mapping():
    """Test Special Forces MOS mapping."""
    skills = MOSCrosswalk.get_civilian_skills('18A')
    assert 'leadership' in skills
    assert 'strategic planning' in skills

def test_enrich_veteran_profile():
    """Test skill enrichment from multiple MOS."""
    skills = MOSCrosswalk.enrich_veteran_profile(['25B', '18C'])
    assert 'network administration' in skills
    assert 'communications' in skills
    assert len(skills) > 5
