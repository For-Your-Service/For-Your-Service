"""
siamese_network.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np


class SiameseNetwork(nn.Module):
    def __init__(self, input_dim: int = 384, hidden_dim: int = 64, embedding_dim: int = None):
        super(SiameseNetwork, self).__init__()
        if embedding_dim is not None:
            input_dim = embedding_dim
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.fc = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

    def forward_one(self, x):
        return self.fc(x)

    def forward(self, input1, input2):
        out1 = self.forward_one(input1)
        out2 = self.forward_one(input2)
        return out1, out2

    def compute_similarity(self, vec1, vec2) -> float:
        """Compute cosine similarity between two embedding vectors."""
        t1 = torch.as_tensor(vec1, dtype=torch.float32)
        t2 = torch.as_tensor(vec2, dtype=torch.float32)
        if t1.ndim == 1:
            t1 = t1.unsqueeze(0)
        if t2.ndim == 1:
            t2 = t2.unsqueeze(0)

        with torch.no_grad():
            sim = F.cosine_similarity(t1, t2)
            score = float(sim.item())
            # Normalize cosine similarity [-1, 1] to [0, 1] if needed or preserve positive similarity
            return float(np.clip(score, 0.0, 1.0))

    def batch_predict(self, veteran_emb, job_embs) -> np.ndarray:
        """Compute similarities between one veteran embedding and a matrix of job embeddings."""
        v = torch.as_tensor(veteran_emb, dtype=torch.float32)
        jobs = torch.as_tensor(job_embs, dtype=torch.float32)
        if v.ndim == 1:
            v = v.unsqueeze(0)

        with torch.no_grad():
            sims = F.cosine_similarity(v, jobs)
            scores = sims.cpu().numpy()
            return np.clip(scores, 0.0, 1.0)
