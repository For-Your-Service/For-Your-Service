"""
Tests for data orchestrator
"""

from src.ingestion.orchestrator import DataOrchestrator


def test_orchestrator_initialization():
    """Test orchestrator can be initialized"""
    orchestrator = DataOrchestrator()
    assert orchestrator.config is not None
    assert orchestrator.clients is not None
