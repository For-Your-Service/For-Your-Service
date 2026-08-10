"""Unit tests for neural network matching engine"""
import pytest
import numpy as np
from src.matching import encode_veteran_profile, encode_job_posting, calculate_similarity


def test_embedding_dimensions():
    """Test that embeddings have correct dimensions (384)"""
    sample_text = "DevOps Engineer with AWS and Kubernetes experience"
    embedding = encode_veteran_profile(sample_text)
    
    assert isinstance(embedding, np.ndarray)
    assert embedding.shape == (384,)


def test_similarity_score_range():
    """Test that similarity scores are between 0 and 1"""
    vec1 = np.random.rand(384)
    vec2 = np.random.rand(384)
    
    score = calculate_similarity(vec1, vec2)
    
    assert 0.0 <= score <= 1.0
    assert isinstance(score, float)


def test_identical_vectors_similarity():
    """Test that identical vectors have similarity = 1.0"""
    vec = np.random.rand(384)
    
    score = calculate_similarity(vec, vec)
    
    assert abs(score - 1.0) < 0.0001  # Allow tiny floating point error


def test_orthogonal_vectors_similarity():
    """Test that orthogonal vectors have similarity close to 0"""
    vec1 = np.zeros(384)
    vec1[0] = 1.0
    
    vec2 = np.zeros(384)
    vec2[1] = 1.0
    
    score = calculate_similarity(vec1, vec2)
    
    assert abs(score) < 0.0001


def test_embedding_consistency():
    """Test that same input produces same embedding"""
    text = "Cloud Architect with 10 years experience"
    
    embedding1 = encode_veteran_profile(text)
    embedding2 = encode_veteran_profile(text)
    
    assert np.array_equal(embedding1, embedding2)
