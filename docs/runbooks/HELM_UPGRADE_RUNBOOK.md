# Helm Upgrade and Rollback Standard Operating Procedure (SOP)

## 1. Pre-Deployment Validation
```bash
# 1. Lint the chart
helm lint charts/for-your-service

# 2. Render templates and inspect output
helm template fys-release charts/for-your-service -f charts/for-your-service/values-prod.yaml --debug

# 3. Perform dry-run against cluster
helm upgrade --install for-your-service ./charts/for-your-service   --namespace default   -f charts/for-your-service/values-prod.yaml   --dry-run
```

## 2. Production Deployment
```bash
helm upgrade --install for-your-service ./charts/for-your-service   --namespace default   -f charts/for-your-service/values-prod.yaml   --atomic   --timeout 5m
```

## 3. Automated & Manual Rollback
```bash
# Inspect revision history
helm history for-your-service -n default

# Rollback to previous known good revision
helm rollback for-your-service 1 -n default --wait
```
