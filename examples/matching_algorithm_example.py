#!/usr/bin/env python3
"""Example: Job matching algorithm workflow"""
import numpy as np
from typing import List, Dict

def load_veteran_profile(veteran_id: str) -> Dict:
    """Load veteran profile from database"""
    return {
        "veteran_id": veteran_id,
        "skills": ["AWS", "Kubernetes", "Python"],
        "mos": "18Z",
        "years_experience": 18
    }

def generate_veteran_embedding(profile: Dict) -> np.ndarray:
    """Generate embedding for veteran profile"""
    # Concat skills + experience
    text = f"{profile['mos']} {' '.join(profile['skills'])}"
    # In production: use sentence-transformers
    # embedding = model.encode(text)
    return np.random.rand(384)  # Placeholder

def load_job_embeddings(location: str, radius: int) -> List[Dict]:
    """Load job embeddings from Gold table"""
    # Query: SELECT * FROM workspace.fys_gold.job_embeddings
    #        WHERE location NEAR (lat, lon) RADIUS radius
    return [
        {"job_id": "job_1", "embedding": np.random.rand(384)},
        {"job_id": "job_2", "embedding": np.random.rand(384)}
    ]

def calculate_matches(veteran_emb: np.ndarray, 
                     job_embs: List[Dict], 
                     threshold: float = 0.7) -> List[Dict]:
    """Calculate match scores"""
    matches = []
    for job in job_embs:
        score = np.dot(veteran_emb, job["embedding"])
        if score >= threshold:
            matches.append({
                "job_id": job["job_id"],
                "score": float(score)
            })
    
    # Sort by score descending
    matches.sort(key=lambda x: x["score"], reverse=True)
    return matches

def main():
    """Run matching workflow"""
    # Step 1: Load veteran profile
    veteran = load_veteran_profile("vet_12345")
    print(f"Loaded veteran: {veteran['veteran_id']}")
    
    # Step 2: Generate veteran embedding
    veteran_emb = generate_veteran_embedding(veteran)
    print(f"Generated embedding: {veteran_emb.shape}")
    
    # Step 3: Load job embeddings (regional)
    jobs = load_job_embeddings("Greenville, SC", radius=50)
    print(f"Loaded {len(jobs)} job embeddings")
    
    # Step 4: Calculate matches
    matches = calculate_matches(veteran_emb, jobs, threshold=0.7)
    print(f"Found {len(matches)} matches")
    
    # Step 5: Return top 10
    top_matches = matches[:10]
    for i, match in enumerate(top_matches):
        print(f"  {i+1}. Job {match['job_id']}: {match['score']:.2f}")

if __name__ == "__main__":
    main()
