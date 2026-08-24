"""Manhattan distance scorer."""
import numpy as np

def manhattan_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    return np.sum(np.abs(vec1 - vec2))
