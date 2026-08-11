"""Two-stage matching orchestrator."""
from typing import List, Tuple
from .bi_encoder import BiEncoder
from .cross_encoder import CrossEncoder

class TwoStageMatcher:
    """Orchestrate two-stage matching pipeline."""
    
    def __init__(self):
        self.bi_encoder = BiEncoder()
        self.cross_encoder = CrossEncoder()
    
    def match(
        self,
        resume_text: str,
        job_candidates: List[str],
        top_k: int = 50,
        rerank_k: int = 10
    ) -> List[Tuple[int, float]]:
        """
        Two-stage matching.
        
        Stage 1: Bi-encoder retrieves top_k candidates (fast)
        Stage 2: Cross-encoder reranks top rerank_k (accurate)
        
        Returns:
            List of (job_index, score) tuples
        """
        # Stage 1: Fast retrieval
        resume_vec = self.bi_encoder.encode_candidate(resume_text)
        job_vecs = self.bi_encoder.encode_batch(job_candidates)
        
        # Cosine similarity
        from numpy.linalg import norm
        similarities = job_vecs @ resume_vec / (norm(job_vecs, axis=1) * norm(resume_vec))
        
        # Get top_k
        top_indices = similarities.argsort()[-top_k:][::-1]
        
        # Stage 2: Deep reranking
        pairs = [(resume_text, job_candidates[i]) for i in top_indices[:rerank_k]]
        deep_scores = self.cross_encoder.score_pairs(pairs)
        
        # Combine results
        results = list(zip(top_indices[:rerank_k], deep_scores))
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results
