# Two-Stage Matching Architecture

## Stage 1: Fast Retrieval (Bi-Encoder)
- Encode all jobs once (offline)
- Encode candidate resume (online)
- Vector similarity search → Top 50 matches
- Latency: ~10ms

## Stage 2: Deep Analysis (Cross-Encoder)
- Joint encoding of candidate-job pairs
- Precise similarity scores
- Rerank top 10
- Latency: ~100ms

## Total Pipeline
- Search 10,000 jobs in <200ms
- High precision from cross-encoder
- Scalable to millions of jobs
