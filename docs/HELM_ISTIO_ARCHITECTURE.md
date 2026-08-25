# Enterprise Helm & Istio Architecture Specification

## 1. Executive Summary

This architecture integrates **Helm** (modular Kubernetes application packaging) and **Istio** (zero-trust service mesh routing, mTLS security, and traffic engineering) into the **For Your Service** veteran career matching platform.

```
                  ┌────────────────────────────────────────┐
                  │          Internet / Ingress            │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       Istio Ingress Gateway            │
                  │    (Port 80 / 443, Gateway CRD)        │
                  └───────────────────┬────────────────────┘
                                      │
                                      ▼
                  ┌────────────────────────────────────────┐
                  │       Istio VirtualService             │
                  │  (Traffic Splitting & Path Routing)    │
                  └───────┬────────────────────────┬───────┘
                          │ (90% v1)               │ (10% Canary v2)
                          ▼                        ▼
                ┌──────────────────┐     ┌──────────────────┐
                │ Streamlit / API  │     │ Streamlit / API  │
                │ Pod (v1)         │     │ Canary Pod (v2)  │
                │ ┌──────────────┐ │     │ ┌──────────────┐ │
                │ │ Envoy Proxy  │ │     │ │ Envoy Proxy  │ │
                │ └──────────────┘ │     │ └──────────────┘ │
                │ ┌──────────────┐ │     │ ┌──────────────┐ │
                │ │ App Engine   │ │     │ │ App Engine   │ │
                │ └──────────────┘ │     │ └──────────────┘ │
                └──────────────────┘     └──────────────────┘
                          ▲                        ▲
                          └──────────┬─────────────┘
                                     │
                                     ▼
                        [ Strict mTLS Zero-Trust ]
                        PeerAuthentication: STRICT
```

---

## 2. Key Architecture Components

### A. Helm Packaging (`charts/for-your-service`)
- **Single Source of Truth:** Manages deployments, services, autoscalers, and mesh resources through parameterized `values.yaml`.
- **Environment Agnostic:** Readily scales across local minikube/k3s, prototyping clusters, and production Google Kubernetes Engine (GKE).
- **Atomic Operations:** Integrates with CI/CD via `helm upgrade --install --atomic` with automatic rollbacks upon health probe failures.

### B. Istio Zero-Trust Security
- **Strict PeerAuthentication:** Enforces encrypted TLS 1.3 tunnels with mutual authentication across all service-to-service communication.
- **Sidecar Injection:** Automated Envoy sidecar proxy injection (`istio-injection=enabled`) intercepts all TCP/HTTP traffic transparently without code changes.

### C. Traffic Management & Canary Deployments
- **Istio Gateway:** Manages edge routing for external traffic.
- **VirtualService & DestinationRule:** Enables weighted routing (canary deployments) for safe rolling updates of machine learning matching algorithms and Streamlit frontends.

---

## 3. Configuration Reference

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `replicaCount` | `int` | `2` | Number of pod replicas |
| `image.repository` | `string` | `gcr.io/7eaglegroup/for-your-service` | Container image repository |
| `image.tag` | `string` | `latest` | Container image tag |
| `istio.enabled` | `bool` | `true` | Enables Istio mesh integration templates |
| `istio.mtls.mode` | `string` | `STRICT` | Mutual TLS mode (`STRICT` or `PERMISSIVE`) |
| `istio.virtualService.canary.enabled` | `bool` | `false` | Enables traffic splitting canary |
| `istio.virtualService.canary.weightPrimary` | `int` | `90` | Percentage of traffic routed to primary |
| `istio.virtualService.canary.weightCanary` | `int` | `10` | Percentage of traffic routed to canary |
