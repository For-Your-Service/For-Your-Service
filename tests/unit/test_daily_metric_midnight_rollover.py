import pytest
from app.app import get_platform_metrics

def test_daily_metrics_structure():
    metrics = get_platform_metrics()
    assert "total_visitors" in metrics
    assert "total_matches_run" in metrics
    assert "veterans_connected" in metrics
    assert "metric_date" in metrics
