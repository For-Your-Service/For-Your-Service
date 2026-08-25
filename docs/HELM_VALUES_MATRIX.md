# Helm Chart Parameter Reference

Comprehensive configuration matrix for the `charts/for-your-service` Helm chart.

---

## Workload & Container Configuration

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `replicaCount` | integer | `2` | Number of pod replicas for the primary deployment |
| `image.repository` | string | `gcr.io/7eaglegroup/for-your-service` | Container image repository URL |
| `image.tag` | string | `latest` | Image tag / version |
| `image.pullPolicy` | string | `IfNotPresent` | Kubernetes image pull policy (`Always`, `IfNotPresent`, `Never`) |
| `serviceAccount.create` | boolean | `true` | Creates dedicated ServiceAccount |
| `serviceAccount.name` | string | `for-your-service-sa` | ServiceAccount identifier |

---

## Istio Service Mesh & Zero-Trust Security

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `istio.enabled` | boolean | `true` | Enables Istio CRD manifest templates |
| `istio.mtls.enabled` | boolean | `true` | Enforces PeerAuthentication resource |
| `istio.mtls.mode` | string | `STRICT` | Mutual TLS mode (`STRICT` for zero-trust, `PERMISSIVE` for migration) |
| `istio.gateway.enabled` | boolean | `true` | Deploys Istio Ingress Gateway |
| `istio.gateway.host` | string | `foryourservice.internal` | Ingress hostname |
| `istio.gateway.port` | integer | `80` | Gateway listening port |
| `istio.virtualService.enabled` | boolean | `true` | Deploys VirtualService routing rules |
| `istio.virtualService.canary.enabled` | boolean | `false` | Enables traffic splitting for canary releases |
| `istio.virtualService.canary.weightPrimary` | integer | `90` | Percentage of traffic sent to primary revision (v1) |
| `istio.virtualService.canary.weightCanary` | integer | `10` | Percentage of traffic sent to canary revision (v2) |
| `istio.destinationRule.enabled` | boolean | `true` | Deploys DestinationRule with mutual TLS policy |

---

## Resource Management & High Availability

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `resources.limits.cpu` | string | `1000m` | Pod CPU hard ceiling |
| `resources.limits.memory` | string | `2Gi` | Pod memory hard ceiling |
| `resources.requests.cpu` | string | `250m` | Guaranteed CPU request |
| `resources.requests.memory` | string | `512Mi` | Guaranteed memory request |
| `autoscaling.enabled` | boolean | `true` | Enables HorizontalPodAutoscaler (HPA v2) |
| `autoscaling.minReplicas` | integer | `2` | Minimum pod count |
| `autoscaling.maxReplicas` | integer | `10` | Maximum pod count |
| `autoscaling.targetCPUUtilizationPercentage` | integer | `75` | Target CPU utilization threshold |
| `podDisruptionBudget.enabled` | boolean | `true` | Protects quorum during node drain / upgrades |
| `podDisruptionBudget.minAvailable` | integer | `1` | Minimum available pods during disruptions |
| `networkPolicy.enabled` | boolean | `true` | Isolates pod network traffic to mesh members |
