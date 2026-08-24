#!/bin/bash
# Train custom Siamese network

echo "Training Siamese network..."

python src/matching/train.py \
  --data data/veteran_job_pairs.csv \
  --epochs 10 \
  --batch-size 32 \
  --output models/siamese_v1.pth

echo "✅ Training complete!"
