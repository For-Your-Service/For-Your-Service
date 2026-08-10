#!/usr/bin/env python3
"""Generate job embeddings for Gold layer"""
from sentence_transformers import SentenceTransformer
import numpy as np

def load_model():
    """Load sentence transformer model"""
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def generate_embedding(text, model):
    """Generate 384-dim embedding"""
    embedding = model.encode(text)
    # Normalize to unit vector
    embedding = embedding / np.linalg.norm(embedding)
    return embedding.tolist()

def batch_generate(texts, model, batch_size=32):
    """Generate embeddings in batches"""
    embeddings = model.encode(texts, batch_size=batch_size, 
                             show_progress_bar=True)
    # Normalize
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms
    return embeddings

if __name__ == "__main__":
    print("Embedding Generator")
    print("Run this in Databricks with GPU for best performance")
