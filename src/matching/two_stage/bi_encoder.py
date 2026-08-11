"""
Bi-encoder for fast candidate-job retrieval.

Encodes candidates and jobs separately, enabling fast vector search.
"""
from typing import List
import numpy as np

class BiEncoder:
    """Fast retrieval using separate encoders."""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-mpnet-base-v2'):
        """Initialize bi-encoder model."""
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
        except ImportError:
            raise ImportError("Install: pip install sentence-transformers")
    
    def encode_candidate(self, resume_text: str) -> np.ndarray:
        """Encode resume to vector."""
        return self.model.encode(resume_text, convert_to_numpy=True)
    
    def encode_job(self, job_description: str) -> np.ndarray:
        """Encode job description to vector."""
        return self.model.encode(job_description, convert_to_numpy=True)
    
    def encode_batch(self, texts: List[str]) -> np.ndarray:
        """Encode multiple texts efficiently."""
        return self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
