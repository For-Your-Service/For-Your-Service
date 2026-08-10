# Hugging Face Spaces Deployment

## Overview

Deploy For Your Service API on Hugging Face Spaces (FREE tier).

## Benefits
- **$0/month** hosting
- Auto-scaling
- Built-in GPU support
- HTTPS endpoint
- Git-based deployment

## Setup Steps

### 1. Create Space
1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Name: "for-your-service"
4. SDK: "Docker"
5. Hardware: CPU Basic (FREE)

### 2. Add Files
```
for-your-service/
├── Dockerfile
├── app.py
├── requirements.txt
└── README.md
```

### 3. Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

### 4. Deploy
```bash
git clone https://huggingface.co/spaces/7eaglegroup/for-your-service
cd for-your-service
cp ../huggingface/* .
git add .
git commit -m "Deploy For Your Service API"
git push
```

### 5. Configure Secrets
In Space settings:
- `DATABRICKS_TOKEN`
- `DATABRICKS_HOST`
- `DATABRICKS_HTTP_PATH`

## Endpoint
https://huggingface.co/spaces/7eaglegroup/for-your-service
