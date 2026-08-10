# Kubernetes Deployment (Production Option)

## Overview

For production workloads requiring:
- Custom domains
- Higher throughput
- Advanced monitoring
- Private deployment

## Architecture

```
┌─────────────────┐
│   Ingress       │
│   (NGINX)       │
└────────┬────────┘
         │
    ┌────▼────┐
    │ Service │
    └────┬────┘
         │
    ┌────▼────────────┐
    │  Deployment     │
    │  (3 replicas)   │
    │                 │
    │  FastAPI Pod x3 │
    └─────────────────┘
```

## GKE Configuration

### Cluster Setup
```bash
gcloud container clusters create fys-cluster \
  --zone us-east1-b \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 5
```

### Deployment YAML
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: fys-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: fys-api
  template:
    metadata:
      labels:
        app: fys-api
    spec:
      containers:
      - name: api
        image: gcr.io/7eaglegroup/for-your-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABRICKS_TOKEN
          valueFrom:
            secretKeyRef:
              name: fys-secrets
              key: databricks-token
```

## Cost Estimate
- GKE cluster: $95/month
- Load balancer: $18/month
- Storage: $5/month
- **Total: ~$120/month**

## When to Use
- >1000 requests/day
- Custom domain required
- Advanced monitoring needs
- Multi-region deployment
