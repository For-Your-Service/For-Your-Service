# Enterprise Kubernetes Deployment Guide

## Overview

*For Your Service* supports enterprise-grade microservice deployments leveraging **Helm** for modular workload packaging and **Istio** for Zero-Trust Service Mesh security, mutual TLS (mTLS), and intelligent traffic management.

---

## Architecture: Enterprise Service Mesh

```
┌─────────────────────────────────────────────────────────────┐
│                    Istio Ingress Gateway                    │
│                 (Edge Ingress on Port 80/443)               │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                    Istio VirtualService                     │
│               (Intelligent / Canary Routing)                │
└──────────────┬──────────────────────────────┬───────────────┘
               │ (90% Traffic)                │ (10% Traffic)
               ▼                              ▼
┌──────────────────────────────┐ ┌──────────────────────────────┐
│  Streamlit Frontend / API v1 │ │ Streamlit Frontend / API v2  │
│  ┌────────────────────────┐  │ │  ┌────────────────────────┐  │
│  │   Envoy Sidecar Proxy  │  │ │  │   Envoy Sidecar Proxy  │  │
│  └───────────┬────────────┘  │ │  └───────────┬────────────┘  │
│              ▼               │ │              ▼               │
│  ┌────────────────────────┐  │ │  ┌────────────────────────┐  │
│  │   Workload Application │  │ │  │   Workload Application │  │
│  └────────────────────────┘  │ │  └────────────────────────┘  │
└──────────────────────────────┘ └──────────────────────────────┘
               ▲                              ▲
               └──────────────┬───────────────┘
                              │
               [ Strict Mutual TLS: mTLS STRICT ]
               (PeerAuthentication Zero-Trust Mesh)
```

---

## 1. Modular Helm Chart Packaging

Instead of managing raw manifests, use the parameterized Helm chart in `charts/for-your-service`:

### Structure
```
charts/for-your-service/
├── Chart.yaml                  # Chart metadata & versioning
├── values.yaml                 # Configurable defaults
├── .helmignore                 # Packaging filters
└── templates/                  # Parameterized Kubernetes & Istio templates
    ├── _helpers.tpl            # Template helper macros
    ├── deployment.yaml         # Multi-replica workload deployment
    ├── service.yaml            # ClusterIP service
    ├── gateway.yaml            # Istio Ingress Gateway
    ├── virtualservice.yaml     # Istio VirtualService (Canary routing)
    ├── peerauthentication.yaml # Zero-Trust Strict mTLS
    ├── destinationrule.yaml    # Istio DestinationRule
    ├── serviceaccount.yaml     # RBAC Workload identity
    ├── configmap.yaml          # Environment config
    └── hpa.yaml                # Horizontal Pod Autoscaler
```

### Installation & Atomic Upgrades
```bash
# Validate chart
helm lint charts/for-your-service

# Deploy or Upgrade with automated rollback on failure
helm upgrade --install for-your-service ./charts/for-your-service \
  --namespace default \
  --create-namespace \
  --set image.tag="latest" \
  --set istio.enabled=true \
  --atomic \
  --timeout 5m
```

---

## 2. Zero-Trust Security with Istio Service Mesh

### Automatic Sidecar Injection
Enable automatic Envoy proxy injection across your target namespace:
```bash
kubectl label namespace default istio-injection=enabled --overwrite
```

### Strict mTLS PeerAuthentication
Enforce cryptographically verified mutual TLS across all microservice pods:
```yaml
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: default
spec:
  mtls:
    mode: STRICT
```

---

## 3. Ingress Traffic & Canary Deployments

Manage ingress traffic via Istio Gateway and VirtualService:

```yaml
apiVersion: networking.istio.io/v1beta1
kind: VirtualService
metadata:
  name: for-your-service-route
spec:
  hosts:
  - "foryourservice.internal"
  gateways:
  - for-your-service-gateway
  http:
  - route:
    - destination:
        host: streamlit-frontend.default.svc.cluster.local
        port:
          number: 8501
```

For gradual rollouts, configure weighted routing (e.g. 90% v1 / 10% v2) using `deployment/kubernetes/istio/canary-virtualservice.yaml`.

---

## 4. GitHub Actions CI/CD Automation

Continuous deployment is managed via [`.github/workflows/deploy-helm-istio.yml`](file:///.github/workflows/deploy-helm-istio.yml):
- Automated `helm lint` and template dry-run validation on every PR.
- Atomic `helm upgrade --install` deployment on merge to `main`.
