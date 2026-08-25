# Helm & Istio Integration Checklist for *For Your Service*

- [x] **Step 1: Helm Migration** — Convert raw Kubernetes manifests into a parameterized Helm chart (`charts/for-your-service`).
- [x] **Step 2: Pipeline Update** — Update GitHub Actions CI/CD workflow to deploy using `helm upgrade --install`.
- [x] **Step 3: Istio Mesh Injection** — Enable automatic sidecar injection on your target Kubernetes namespace (`kubectl label namespace default istio-injection=enabled`).
- [x] **Step 4: Zero-Trust Policy** — Apply a PeerAuthentication resource enforcing strict mTLS across services.
- [x] **Step 5: Routing Rules** — Configure Istio Gateway and VirtualService for ingress traffic management.

---

## 🚀 Mission Overview

- **Objective:** Seamlessly integrate Helm (for modular Kubernetes packaging) and Istio (for zero-trust service mesh routing and security) into the *For Your Service* data pipeline and SaaS architecture.
- **Strategic Focus:** Elevate the open-source repository from standard Kubernetes deployments to an enterprise-grade, service-meshed microservice architecture.

---

## 📁 Repository Chart & Manifest Architecture

```
For-Your-Service/
├── charts/
│   └── for-your-service/
│       ├── Chart.yaml                  # Helm chart metadata
│       ├── values.yaml                 # Configurable defaults (replicas, image tags, mesh params)
│       ├── .helmignore                 # Helm build packaging rules
│       └── templates/                  # Parameterized Kubernetes & Istio templates
│           ├── _helpers.tpl            # Template named helpers & label generators
│           ├── deployment.yaml         # Multi-replica workload deployment template
│           ├── service.yaml            # ClusterIP service definition
│           ├── gateway.yaml            # Istio Ingress Gateway
│           ├── virtualservice.yaml     # Istio VirtualService (with Canary support)
│           ├── peerauthentication.yaml # Zero-Trust Strict mTLS Policy
│           ├── destinationrule.yaml    # Istio DestinationRule & TLS settings
│           ├── serviceaccount.yaml     # Workload ServiceAccount
│           ├── configmap.yaml          # Dynamic environment configuration
│           └── hpa.yaml                # Horizontal Pod Autoscaler
├── deployment/
│   └── kubernetes/
│       ├── deployment.yaml             # Raw manifest
│       ├── service.yaml                # Raw manifest
│       └── istio/                      # Standalone Istio CRD manifests
│           ├── gateway.yaml
│           ├── virtualservice.yaml
│           ├── peer-authentication.yaml
│           ├── destination-rule.yaml
│           └── canary-virtualservice.yaml
└── .github/workflows/
    └── deploy-helm-istio.yml           # Automated Helm & Istio CI/CD deployment
```

---

## 🛠️ Step-by-Step Execution Guide

### 1. Helm Chart Linting & Dry Run
To validate chart syntax and template expansion locally:
```bash
# Validate chart syntax
helm lint charts/for-your-service

# Render templates locally to verify output
helm template fys-release charts/for-your-service --debug

# Dry-run installation on cluster
helm upgrade --install fys-release charts/for-your-service \
  --namespace default \
  --dry-run
```

### 2. Deploying Workloads with Helm
Deploy or upgrade with atomic rollbacks:
```bash
helm upgrade --install for-your-service ./charts/for-your-service \
  --namespace default \
  --create-namespace \
  --set image.tag="latest" \
  --set replicaCount=2 \
  --atomic \
  --timeout 5m
```

### 3. Enabling Istio Service Mesh Sidecar Injection
Enable automatic sidecar injection on your namespace:
```bash
kubectl label namespace default istio-injection=enabled --overwrite
```

### 4. Zero-Trust Security with Strict mTLS
Enforce strict mutual TLS across all microservice pods:
```bash
kubectl apply -f deployment/kubernetes/istio/peer-authentication.yaml
```

### 5. Ingress Traffic Routing & Canary Deployments
Apply Istio Gateway and VirtualService:
```bash
kubectl apply -f deployment/kubernetes/istio/gateway.yaml
kubectl apply -f deployment/kubernetes/istio/virtualservice.yaml

# For gradual canary rollouts (90% v1 / 10% v2):
kubectl apply -f deployment/kubernetes/istio/destination-rule.yaml
kubectl apply -f deployment/kubernetes/istio/canary-virtualservice.yaml
```

---

## 🔍 Verification & Troubleshooting Commands

```bash
# Verify sidecar injection
kubectl get pods -n default -l app=for-your-service -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{range .spec.containers[*]}{.name}{" "}{end}{"\n"}{end}'

# Check Istio proxy sync status
istioctl proxy-status

# Verify mTLS encryption between services
istioctl authn tls-check $(kubectl get pods -n default -l app=for-your-service -o jsonpath='{.items[0].metadata.name}')
```
