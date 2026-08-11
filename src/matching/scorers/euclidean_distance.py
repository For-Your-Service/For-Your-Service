"""Euclidean distance scorer."""
import numpy as np

def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return np.linalg.norm(vec1 - vec2)
