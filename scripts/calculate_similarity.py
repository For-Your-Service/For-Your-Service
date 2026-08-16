#!/usr/bin/env python3
"""Calculate cosine similarity between both veteran and jobs"""
import numpy as np

def cosine_similarity(vec1, vec2):
    """Calculate cosine similarity between two vectors"""
    return np.dot(vec1, vec2) / (
        np.linalg.norm(vec1) * np.linalg.norm(vec2)
    )

def batch_similarity(veteran_emb, job_embs):
    """Calculate similarity against multiple job embeddings"""
    # Assumes embeddings are already normalized
    similarities = np.dot(job_embs, veteran_emb)
    return similarities

def rank_jobs(veteran_emb, job_embs, threshold=0.7):
    """Rank jobs by similarity score"""
    scores = batch_similarity(veteran_emb, job_embs)
    
    # Filter by threshold
    matches = [(idx, score) for idx, score in enumerate(scores) 
               if score >= threshold]
    
    # Sort descending
    matches.sort(key=lambda x: x[1], reverse=True)
    
    return matches

if __name__ == "__main__":
    print("Similarity Calculator")
    print("Calculate veteran-to-job matching scores")
