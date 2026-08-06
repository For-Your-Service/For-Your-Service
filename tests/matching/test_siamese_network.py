"""
Tests for Siamese network
"""
import pytest
import numpy as np
from src.matching.siamese_network import SiameseNetwork


def test_compute_similarity():
    """Test similarity computation"""
    network = SiameseNetwork(embedding_dim=384)
    
    # Identical vectors should have similarity = 1
    vec = np.ones(384)
    similarity = network.compute_similarity(vec, vec)
    
    assert 0.99 < similarity <= 1.0


def test_batch_predict():
    """Test batch similarity prediction"""
    network = SiameseNetwork(embedding_dim=384)
    
    veteran_emb = np.random.rand(384)
    job_embs = np.random.rand(10, 384)
    
    similarities = network.batch_predict(veteran_emb, job_embs)
    
    assert len(similarities) == 10
    assert all(0 <= s <= 1 for s in similarities)
