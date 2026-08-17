"""
Job matching service using the Siamese network
"""

from typing import List, Dict, Tuple
import numpy as np
import logging

from .siamese_network import SiameseNetwork

logger = logging.getLogger(__name__)


class JobMatcher:
    """Matches veterans to jobs using neural similarity"""

    def __init__(self):
        """Initialize job matcher"""
        self.network = SiameseNetwork(embedding_dim=384)

    def find_matches(
        self,
        veteran_embedding: np.ndarray,
        job_embeddings: np.ndarray,
        job_metadata: List[Dict],
        top_k: int = 10,
        min_similarity: float = 0.5,
    ) -> List[Tuple[Dict, float]]:
        """
        Find top job matches for a veteran

        Args:
            veteran_embedding: Veteran's 384-dim embedding
            job_embeddings: Matrix of job embeddings (n_jobs, 384)
            job_metadata: List of job dictionaries
            top_k: Number of top matches to return
            min_similarity: Minimum similarity threshold

        Returns:
            List of (job_dict, similarity_score) tuples
        """
        # Compute similarities
        similarities = self.network.batch_predict(veteran_embedding, job_embeddings)

        # Filter by minimum threshold
        valid_indices = np.where(similarities >= min_similarity)[0]

        if len(valid_indices) == 0:
            logger.warning("No jobs meet minimum similarity threshold")
            return []

        # Get top K
        sorted_indices = valid_indices[np.argsort(similarities[valid_indices])[::-1]][:top_k]

        # Build results
        matches = []
        for idx in sorted_indices:
            job = job_metadata[idx]
            score = float(similarities[idx])
            matches.append((job, score))

        logger.info(f"Found {len(matches)} matches (min_sim={min_similarity})")
        return matches

    def explain_match(self, veteran: Dict, job: Dict) -> Dict[str, any]:
        """
        Explain why a veteran-job pair was matched

        Args:
            veteran: Veteran profile dict
            job: Job posting dict

        Returns:
            Dict with explanation details
        """
        explanation = {
            "mos_match": veteran.get("mos") in job.get("preferred_mos", []),
            "skill_overlap": len(
                set(veteran.get("skills", [])) & set(job.get("required_skills", []))
            ),
            "location_match": veteran.get("location") == job.get("location"),
            "clearance_match": veteran.get("clearance") >= job.get("clearance_required", ""),
        }

        return explanation
