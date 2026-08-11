"""Unit tests for skill normalization."""
import pytest
from src.taxonomy.skill_normalizer import SkillNormalizer

def test_normalize_synonyms():
    """Test skill synonym normalization."""
    normalizer = SkillNormalizer()
    
    assert normalizer.normalize('k8s') == 'kubernetes'
    assert normalizer.normalize('K8S') == 'kubernetes'
    assert normalizer.normalize('kube') == 'kubernetes'
    
def test_normalize_list():
    """Test batch normalization."""
    normalizer = SkillNormalizer()
    skills = ['k8s', 'Kubernetes', 'Docker']
    normalized = normalizer.normalize_list(skills)
    
    assert 'kubernetes' in normalized
    assert 'docker' in normalized
    assert len(normalized) == 2  # k8s and Kubernetes deduplicated
