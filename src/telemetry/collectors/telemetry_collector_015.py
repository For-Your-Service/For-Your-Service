"""
Telemetry Collector 015 - For Your Service
Observability, Performance Metrics and Pipeline Health Monitor
"""

import time
from typing import Dict, Any

class TelemetryCollector_015:
    def __init__(self, collector_id: int = 15):
        self.collector_id = collector_id
        self.start_time = time.time()
        self.metrics_buffer = []

    def record_event(self, event_name: str, duration_ms: float, status: str = "success") -> Dict[str, Any]:
        """Records granular stage latency and execution health status"""
        payload = {
            "collector": self.collector_id,
            "event": event_name,
            "latency_ms": round(duration_ms, 2),
            "status": status,
            "timestamp": time.time()
        }
        self.metrics_buffer.append(payload)
        return payload

    def get_summary(self) -> Dict[str, Any]:
        """Returns aggregated telemetry summary"""
        return {
            "collector_id": self.collector_id,
            "total_events": len(self.metrics_buffer),
            "uptime_sec": round(time.time() - self.start_time, 2)
        }
