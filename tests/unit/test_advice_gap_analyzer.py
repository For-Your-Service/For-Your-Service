"""Unit tests for gap analysis."""
import pytest
from src.advice.gap_analyzer import GapAnalyzer
from src.advice.models import GapAnalysis
from src.resume_parsing.models import ParsedResume, Skill

def test_analyze_skill_gaps():
    """Test skill gap detection."""
    analyzer = GapAnalyzer()
    
    candidate = ParsedResume()
    candidate.hard_skills = [
        Skill(raw_text='python', normalized_name='python'),
        Skill(raw_text='docker', normalized_name='docker')
    ]
    
    job_skills = ['python', 'kubernetes', 'terraform']
    
    analysis = analyzer.analyze(candidate, job_skills, match_score=0.75)
    
    assert analysis.match_score == 0.75
    missing_names = {s.skill_name for s in analysis.missing_skills}
    assert 'kubernetes' in missing_names
    assert 'terraform' in missing_names
    assert 'python' in analysis.matching_skills

def test_experience_gap_detection():
    """Test experience gap calculation."""
    analyzer = GapAnalyzer()
    
    candidate = ParsedResume()
    candidate.total_years_experience = 3
    
    analysis = analyzer.analyze(
        candidate, 
        job_skills=[],
        job_required_years=5
    )
    
    assert len(analysis.experience_gaps) > 0
    assert analysis.experience_gaps[0].required_years == 5
    assert analysis.experience_gaps[0].candidate_years == 3
