"""
Cross-encoder for deep match analysis.

Jointly encodes candidate-job pairs for precise scoring.
"""
from typing import List, Tuple

class CrossEncoder:
    """Deep matching with cross-encoder."""
    
    def __init__(self, model_name: str = 'cross-encoder/ms-marco-MiniLM-L-6-v2'):
        """Initialize cross-encoder model."""
        try:
            from sentence_transformers import CrossEncoder as CE
            self.model = CE(model_name)
        except ImportError:
            raise ImportError("Install: pip install sentence-transformers")
    
    def score_pair(self, resume_text: str, job_description: str) -> float:
        """Score candidate-job pair (0-1)."""
        score = self.model.predict([(resume_text, job_description)])[0]
        # Normalize to 0-1
        return (score + 1) / 2
    
    def score_pairs(self, pairs: List[Tuple[str, str]]) -> List[float]:
        """Score multiple pairs efficiently."""
        scores = self.model.predict(pairs)
        return [(s + 1) / 2 for s in scores]
