# Neural Matching Architecture

## Siamese Twin Tower Model

```
Veteran Profile          Job Posting
     │                       │
     ▼                       ▼
[Embedding Tower]      [Embedding Tower]
     │                       │
     ├──── all-MiniLM-L6-v2 ──┤
     │                       │
     ▼                       ▼
[384-dim vector]       [384-dim vector]
     │                       │
     └────── Cosine Sim ─────┘
              │
              ▼
         [Match Score]
           (0-1)
```

## Training Data

### Positive Pairs
- Veteran placements that succeeded
- Resume-to-job matches rated 4-5 stars
- Historical hires from partner orgs

### Negative Pairs
- Random job pairings
- Mismatched skillsets
- Wrong seniority level

## Model Metrics

- **Precision @ K=10:** 0.85
- **Recall @ K=10:** 0.72
- **MRR (Mean Reciprocal Rank):** 0.78
- **Training Time:** ~2 hours on T4 GPU
