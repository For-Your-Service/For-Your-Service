# Zero-Trust Mutual TLS (mTLS) Security Specification

## 1. Overview
This document specifies the cryptographic zero-trust baseline implemented across the *For Your Service* microservice mesh on Kubernetes. All inter-pod communication is encrypted in transit with mutual authentication using SPIFFE/SPIRE workload identities and Envoy sidecar proxies.

## 2. PeerAuthentication Architecture
The cluster enforces `mode: STRICT` at the namespace root:

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

### Key Security Properties:
- **Mutual Authentication:** Both client and server Envoy proxies exchange and verify x509 certificates.
- **Automatic Key & Certificate Rotation:** Managed via Istio CA / cert-manager with 24-hour rotation windows.
- **Cipher Suite Hardening:** Enforces TLS 1.3 with ECDHE-ECDSA-AES256-GCM-SHA384 and TLS_AES_128_GCM_SHA256.
- **Zero Plaintext Fallback:** Any non-mTLS TCP or HTTP connection attempt is immediately dropped at the Envoy filter chain.
