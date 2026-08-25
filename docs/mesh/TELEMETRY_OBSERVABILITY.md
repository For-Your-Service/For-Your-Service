# Service Mesh Telemetry, Tracing & Monitoring Guide

## 1. Observability Stack
The *For Your Service* mesh integrates three pillars of observability:
1. **Metrics:** Prometheus scrapes Envoy proxy metrics on port `15090` using Prometheus Operator `ServiceMonitor`.
2. **Access Logs:** Envoy logs all HTTP/TCP transactions in JSON format to stdout.
3. **Distributed Tracing:** OpenTelemetry & Jaeger propagate B3/W3C trace context across Streamlit, FastAPI, and Spark nodes.

## 2. Access Log Format
```json
{
  "start_time": "%START_TIME%",
  "method": "%REQ(:METHOD)%",
  "path": "%REQ(X-ENVOY-ORIGINAL-PATH?:PATH)%",
  "protocol": "%PROTOCOL%",
  "response_code": "%RESPONSE_CODE%",
  "duration_ms": "%DURATION%",
  "upstream_cluster": "%UPSTREAM_CLUSTER%",
  "upstream_host": "%UPSTREAM_HOST%",
  "client_ip": "%DOWNSTREAM_REMOTE_ADDRESS_WITHOUT_PORT%"
}
```
