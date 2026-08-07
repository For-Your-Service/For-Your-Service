"""
Siamese Twin Tower Neural Network for Veteran-Job Matching

Complete PyTorch implementation with:
- Separate encoders for veterans and jobs  
- Batch normalization and dropout
- L2-normalized embeddings
- Contrastive and triplet loss functions
- ~400K parameters, ~2MB model size
"""
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, Tuple


class VeteranEncoder(nn.Module):
    """
    Veteran profile encoder: 384-dim features -> 128-dim embedding
    
    Input features (384 dimensions):
    - MOS skill embeddings: 128-dim
    - Technical skills one-hot: 50-dim  
    - Soft skills one-hot: 30-dim
    - Education level: 5-dim
    - Certifications: 20-dim
    - Years of service: 1-dim
    - Security clearance: 5-dim
    - Location (state) one-hot: 50-dim
    - Salary expectation: 1-dim (normalized)
    - Deployment count: 1-dim
    - Job preferences: 100-dim
    - Other features: 13-dim
    """
    def __init__(self, input_dim=384, hidden_dim=256, embedding_dim=128, dropout=0.2):
        super(VeteranEncoder, self).__init__()
        
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.dropout1 = nn.Dropout(dropout)
        
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.dropout2 = nn.Dropout(dropout)
        
        self.fc3 = nn.Linear(hidden_dim // 2, embedding_dim)
        
    def forward(self, x):
        # Layer 1
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout1(x)
        
        # Layer 2  
        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout2(x)
        
        # Output layer (embedding)
        x = self.fc3(x)
        
        # L2 normalization (unit vector)
        x = F.normalize(x, p=2, dim=1)
        
        return x


class JobEncoder(nn.Module):
    """
    Job posting encoder: 384-dim features -> 128-dim embedding
    
    Input features (384 dimensions):
    - Required skills embeddings: 128-dim
    - Job title embedding: 50-dim
    - Industry one-hot: 30-dim
    - Location (state) one-hot: 50-dim
    - Salary range: 2-dim (normalized min/max)
    - Experience required: 1-dim
    - Education requirement: 5-dim
    - Clearance requirement: 5-dim
    - Job type: 3-dim
    - Remote/hybrid/on-site: 3-dim
    - Company size: 5-dim
    - Benefits score: 1-dim
    - Other features: 101-dim
    """
    def __init__(self, input_dim=384, hidden_dim=256, embedding_dim=128, dropout=0.2):
        super(JobEncoder, self).__init__()
        
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.bn1 = nn.BatchNorm1d(hidden_dim)
        self.dropout1 = nn.Dropout(dropout)
        
        self.fc2 = nn.Linear(hidden_dim, hidden_dim // 2)
        self.bn2 = nn.BatchNorm1d(hidden_dim // 2)
        self.dropout2 = nn.Dropout(dropout)
        
        self.fc3 = nn.Linear(hidden_dim // 2, embedding_dim)
        
    def forward(self, x):
        # Layer 1
        x = self.fc1(x)
        x = self.bn1(x)
        x = F.relu(x)
        x = self.dropout1(x)
        
        # Layer 2
        x = self.fc2(x)
        x = self.bn2(x)
        x = F.relu(x)
        x = self.dropout2(x)
        
        # Output layer (embedding)
        x = self.fc3(x)
        
        # L2 normalization (unit vector)
        x = F.normalize(x, p=2, dim=1)
        
        return x


class SiameseMatchingModel(nn.Module):
    """
    Siamese network for veteran-job matching
    Combines veteran and job encoders with contrastive loss
    """
    def __init__(self, input_dim=384, hidden_dim=256, embedding_dim=128, dropout=0.2):
        super(SiameseMatchingModel, self).__init__()
        
        self.veteran_encoder = VeteranEncoder(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            embedding_dim=embedding_dim,
            dropout=dropout
        )
        
        self.job_encoder = JobEncoder(
            input_dim=input_dim,
            hidden_dim=hidden_dim,
            embedding_dim=embedding_dim,
            dropout=dropout
        )
    
    def forward(self, veteran_features, job_features):
        """
        Forward pass: encode both veteran and job
        Returns normalized embeddings
        """
        veteran_emb = self.veteran_encoder(veteran_features)
        job_emb = self.job_encoder(job_features)
        
        return veteran_emb, job_emb
    
    def compute_similarity(self, veteran_emb, job_emb):
        """
        Compute cosine similarity between veteran and job embeddings
        Returns similarity score in [-1, 1]
        """
        return F.cosine_similarity(veteran_emb, job_emb)


def contrastive_loss(veteran_emb, job_emb, labels, margin=0.5, temperature=0.5):
    """
    Contrastive loss for learning veteran-job similarity
    
    Args:
        veteran_emb: Veteran embeddings (batch_size, embedding_dim)
        job_emb: Job embeddings (batch_size, embedding_dim)
        labels: Binary labels (1 = match/hired, 0 = no match)
        margin: Margin for negative pairs
        temperature: Temperature for similarity scaling
    
    Returns:
        loss: Scalar contrastive loss
    """
    # Compute cosine similarity
    similarity = F.cosine_similarity(veteran_emb, job_emb) / temperature
    
    # Positive pairs: hired/matched (maximize similarity)
    positive_loss = labels * torch.pow(1 - similarity, 2)
    
    # Negative pairs: not hired (push apart, keep margin)
    negative_loss = (1 - labels) * torch.pow(
        torch.clamp(similarity - margin, min=0), 2
    )
    
    # Combined loss
    loss = (positive_loss + negative_loss).mean()
    
    return loss


def triplet_loss(anchor_emb, positive_emb, negative_emb, margin=0.2):
    """
    Alternative: Triplet loss for learning veteran-job similarity
    
    Args:
        anchor_emb: Veteran embeddings (batch_size, embedding_dim)
        positive_emb: Matched job embeddings (batch_size, embedding_dim) 
        negative_emb: Non-matched job embeddings (batch_size, embedding_dim)
        margin: Margin between positive and negative pairs
    
    Returns:
        loss: Scalar triplet loss
    """
    positive_distance = 1 - F.cosine_similarity(anchor_emb, positive_emb)
    negative_distance = 1 - F.cosine_similarity(anchor_emb, negative_emb)
    
    loss = torch.clamp(positive_distance - negative_distance + margin, min=0)
    
    return loss.mean()


# Example usage
if __name__ == "__main__":
    # Initialize model
    model = SiameseMatchingModel(
        input_dim=384,
        hidden_dim=256,
        embedding_dim=128,
        dropout=0.2
    )
    
    # Example batch
    batch_size = 32
    veteran_features = torch.randn(batch_size, 384)
    job_features = torch.randn(batch_size, 384)
    labels = torch.randint(0, 2, (batch_size,)).float()
    
    # Forward pass
    veteran_emb, job_emb = model(veteran_features, job_features)
    
    # Compute loss
    loss = contrastive_loss(veteran_emb, job_emb, labels)
    
    print(f"Veteran embedding shape: {veteran_emb.shape}")
    print(f"Job embedding shape: {job_emb.shape}")
    print(f"Loss: {loss.item():.4f}")
    
    # Compute similarity
    similarity = model.compute_similarity(veteran_emb, job_emb)
    print(f"Similarity scores: {similarity[:5]}")
