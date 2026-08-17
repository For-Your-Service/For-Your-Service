"""
Resume Parser Module

Extracts structured data from unstructured resume formats (PDF, DOCX).
Part of For Your Service veteran job matching platform.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

__version__ = "0.1.0"

from .base_parser import BaseResumeParser
from .pdf_parser import PDFResumeParser
from .docx_parser import DOCXResumeParser
from .schema import ResumeSchema, SkillEntry, ExperienceEntry, EducationEntry

__all__ = [
    "BaseResumeParser",
    "PDFResumeParser",
    "DOCXResumeParser",
    "ResumeSchema",
    "SkillEntry",
    "ExperienceEntry",
    "EducationEntry",
]
