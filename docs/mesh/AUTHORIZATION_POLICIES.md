# Istio Authorization Policy & Role-Based Access Control (RBAC)

## 1. Overview
Istio AuthorizationPolicies govern ingress and east-west traffic permissions across *For Your Service* services.

## 2. Policy Enforcement Rules

### Public Endpoints (Health Probes & Metrics)
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: fys-allow-health-probes
  namespace: default
spec:
  action: ALLOW
  rules:
  - to:
    - operation:
        paths: ["/_stcore/health", "/healthz", "/metrics"]
```

### Internal Microservice Communication
```yaml
apiVersion: security.istio.io/v1beta1
kind: AuthorizationPolicy
metadata:
  name: fys-internal-matching-api
  namespace: default
spec:
  selector:
    matchLabels:
      app: fys-matching-service
  action: ALLOW
  rules:
  - from:
    - source:
        principals: ["cluster.local/ns/default/sa/for-your-service-sa"]
```
