"""
Generate 384-dimensional embeddings for jobs and veterans
"""

from typing import List, Dict
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EmbeddingGenerator:
    """Generates feature embeddings for neural matching"""

    def __init__(self):
        """Initialize embedding generator"""
        # TODO: Load sentence-transformers model
        # self.model = SentenceTransformer('all-MiniLM-L6-v2')

    def generate_job_embedding(self, job: Dict) -> np.ndarray:
        """
        Generate 384-dim embedding for a job posting

        Args:
            job: Job dictionary with title, description, skills

        Returns:
            384-dimensional numpy array
        """
        # Combine job features into text
        text = f"{job.get('title', '')} {job.get('description', '')} "
        text += " ".join(job.get("skills", []))

        # TODO: Generate actual embedding
        # embedding = self.model.encode(text)

        # Placeholder: random 384-dim vector
        embedding = np.random.rand(384)

        return embedding

    def generate_veteran_embedding(self, veteran: Dict) -> np.ndarray:
        """
        Generate 384-dim embedding for a veteran profile

        Args:
            veteran: Veteran dict with MOS, skills, experience

        Returns:
            384-dimensional numpy array
        """
        # Combine veteran features
        text = f"MOS: {veteran.get('mos', '')} "
        text += f"Skills: {' '.join(veteran.get('skills', []))} "
        text += f"Experience: {veteran.get('years_of_service', 0)} years"

        # TODO: Generate actual embedding
        # embedding = self.model.encode(text)

        # Placeholder
        embedding = np.random.rand(384)

        return embedding

    def batch_generate(self, items: List[Dict]) -> np.ndarray:
        """
        Generate embeddings for multiple items

        Args:
            items: List of job or veteran dicts

        Returns:
            Matrix of shape (n_items, 384)
        """
        embeddings = []
        for item in items:
            if "mos" in item:
                emb = self.generate_veteran_embedding(item)
            else:
                emb = self.generate_job_embedding(item)
            embeddings.append(emb)

        return np.array(embeddings)
