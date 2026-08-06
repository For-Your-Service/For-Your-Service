"""
Siamese Twin Tower Neural Network for job matching
"""
import numpy as np
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class SiameseNetwork:
    """Siamese network for computing veteran-job similarity"""
    
    def __init__(self, embedding_dim: int = 384):
        """
        Initialize Siamese network
        
        Args:
            embedding_dim: Dimension of input embeddings (384 by default)
        """
        self.embedding_dim = embedding_dim
        # TODO: Initialize actual neural network layers
        
    def compute_similarity(
        self,
        veteran_embedding: np.ndarray,
        job_embedding: np.ndarray
    ) -> float:
        """
        Compute similarity score between veteran and job
        
        Args:
            veteran_embedding: 384-dim veteran vector
            job_embedding: 384-dim job vector
            
        Returns:
            Similarity score between 0 and 1
        """
        # Cosine similarity
        dot_product = np.dot(veteran_embedding, job_embedding)
        norm_product = np.linalg.norm(veteran_embedding) * np.linalg.norm(job_embedding)
        
        if norm_product == 0:
            return 0.0
        
        similarity = dot_product / norm_product
        
        # Normalize to [0, 1]
        return (similarity + 1) / 2
    
    def batch_predict(
        self,
        veteran_embedding: np.ndarray,
        job_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Compute similarities for one veteran against multiple jobs
        
        Args:
            veteran_embedding: Single 384-dim vector
            job_embeddings: Matrix of shape (n_jobs, 384)
            
        Returns:
            Array of similarity scores of shape (n_jobs,)
        """
        similarities = []
        for job_emb in job_embeddings:
            sim = self.compute_similarity(veteran_embedding, job_emb)
            similarities.append(sim)
        
        return np.array(similarities)
