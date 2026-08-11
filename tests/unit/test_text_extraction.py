"""Unit tests for text extraction."""
import pytest
from src.resume_parsing.text_extraction import TextExtractor

def test_clean_text():
    """Test text cleaning."""
    dirty = "Page 1 of 2\n\n\nTest   text"
    clean = TextExtractor._clean_text(dirty)
    assert "Page 1 of 2" not in clean
    assert "Test text" in clean

def test_extract_unsupported_format():
    """Test error on unsupported format."""
    with pytest.raises(ValueError):
        TextExtractor.extract("test.xyz")
