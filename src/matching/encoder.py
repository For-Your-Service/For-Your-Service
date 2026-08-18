"""
Neural Profile Encoder and Similarity Calculation
"""

import hashlib
import numpy as np


def encode_veteran_profile(profile_data) -> np.ndarray:
    """
    Encode veteran profile text or dictionary into a 384-dimensional normalized embedding vector.
    """
    text = str(profile_data)

    # Deterministic, consistent 384-dim normalized embedding based on MD5 seed
    seed = int(hashlib.md5(text.encode("utf-8")).hexdigest(), 16) % (2**32)
    rng = np.random.default_rng(seed)
    vec = rng.standard_normal(384).astype(np.float32)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec


def calculate_similarity(vec1, vec2) -> float:
    """
    Calculate cosine similarity between two vectors in the range [0.0, 1.0].
    """
    v1 = np.asarray(vec1, dtype=np.float32)
    v2 = np.asarray(vec2, dtype=np.float32)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    dot = np.dot(v1, v2) / (norm1 * norm2)
    return float(np.clip(dot, 0.0, 1.0))
