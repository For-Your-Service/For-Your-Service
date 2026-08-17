"""
Base Resume Parser

Abstract base class for all resume parsers.
Defines common interface and shared utilities.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Optional
import re
from datetime import datetime

from .schema import ResumeSchema


class BaseResumeParser(ABC):
    """Abstract base class for resume parsers"""

    def __init__(self):
        self.supported_formats = []

    @abstractmethod
    def extract_text(self, file_path: Union[str, Path]) -> str:
        """
        Extract raw text from resume file

        Args:
            file_path: Path to resume file

        Returns:
            Raw text content
        """

    @abstractmethod
    def parse(self, file_path: Union[str, Path]) -> ResumeSchema:
        """
        Parse resume file into structured schema

        Args:
            file_path: Path to resume file

        Returns:
            ResumeSchema with extracted data
        """

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email address from text"""
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        matches = re.findall(email_pattern, text)
        return matches[0] if matches else None

    def extract_phone(self, text: str) -> Optional[str]:
        """Extract phone number from text"""
        # Match various phone formats
        phone_pattern = r"\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b"
        matches = re.findall(phone_pattern, text)
        if matches:
            # Format as (XXX) XXX-XXXX
            area, prefix, line = matches[0]
            return f"({area}) {prefix}-{line}"
        return None

    def extract_urls(self, text: str, domain: str) -> Optional[str]:
        """
        Extract URL for specific domain (e.g., linkedin.com, github.com)

        Args:
            text: Text to search
            domain: Domain to match (e.g., "linkedin.com")

        Returns:
            First matching URL or None
        """
        url_pattern = rf"https?://(?:www\.)?{re.escape(domain)}/[A-Za-z0-9/_.-]+"
        matches = re.findall(url_pattern, text, re.IGNORECASE)
        return matches[0] if matches else None

    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove null bytes
        text = text.replace("\x00", "")
        return text.strip()

    def get_timestamp(self) -> str:
        """Get ISO format timestamp"""
        return datetime.utcnow().isoformat() + "Z"

    def is_supported(self, file_path: Union[str, Path]) -> bool:
        """Check if file format is supported"""
        path = Path(file_path)
        return path.suffix.lower() in self.supported_formats
