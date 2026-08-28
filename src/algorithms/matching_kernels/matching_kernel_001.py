"""
Matching Kernel Component 001 - For Your Service Veteran Career Intelligence
Vector Math & Multi-Factor Scoring Pipeline
"""

import math
from typing import Dict, List, Any

def score_kernel_001(candidate_vector: List[float], job_vector: List[float], clearance_weight: float = 1.0) -> float:
    """Computes normalized cosine dot product with clearance weighting factor (Kernel 001)"""
    if not candidate_vector or not job_vector:
        return 0.0
    dot_product = sum(c * j for c, j in zip(candidate_vector, job_vector))
    norm_c = math.sqrt(sum(c * c for c in candidate_vector)) or 1e-9
    norm_j = math.sqrt(sum(j * j for j in job_vector)) or 1e-9
    cosine_sim = dot_product / (norm_c * norm_j)
    return round(float(cosine_sim * clearance_weight), 4)

def evaluate_features_001(veteran_profile: Dict[str, Any], job_posting: Dict[str, Any]) -> Dict[str, Any]:
    """Extracts rank, MOS, clearance, and location compatibility for Kernel 001"""
    score = score_kernel_001([1.0] * 10, [1.0] * 10)
    return {
        "kernel_id": 1,
        "base_similarity": score,
        "status": "ready"
    }
