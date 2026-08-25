# Canary Traffic Engineering & Deployment Runbook

## 1. Objective
Enable zero-downtime, progressive rollout of matching algorithm updates and frontend UI features through weighted traffic splitting.

## 2. Traffic Splitting Configuration
Traffic weights are managed via the `for-your-service-route` VirtualService:

- **Stage 1 (Internal Testing):** 100% Primary (v1) / 0% Canary (v2) with HTTP Header routing (`X-Beta-Tester: true`).
- **Stage 2 (Canary Rollout):** 90% Primary (v1) / 10% Canary (v2).
- **Stage 3 (General Availability):** 100% Canary (promoted to v1).

## 3. Circuit Breaking & Outlier Detection
DestinationRule defines automatic pod ejection upon consecutive errors:
- `consecutive5xxErrors: 3`
- `interval: 10s`
- `baseEjectionTime: 30s`
- `maxEjectionPercent: 50%`
