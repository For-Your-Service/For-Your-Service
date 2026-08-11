"""
Text extraction from various resume formats.

Handles PDF, DOCX, and plain text conversion to clean, parseable strings.
"""

import re
from pathlib import Path
from typing import Union, Optional
import logging

logger = logging.getLogger(__name__)


class TextExtractor:
    """Extract clean text from resume files."""
    
    @staticmethod
    def extract_from_pdf(file_path: Union[str, Path]) -> str:
        """
        Extract text from PDF resume.
        
        Uses PyPDF2 or pdfplumber for text extraction.
        Falls back to OCR (pytesseract) for scanned PDFs.
        """
        try:
            import pdfplumber
            
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            
            if not text.strip():
                # Empty text suggests scanned PDF
                logger.warning(f"No text extracted from {file_path}, attempting OCR")
                return TextExtractor._ocr_pdf(file_path)
            
            return TextExtractor._clean_text(text)
            
        except ImportError:
            logger.error("pdfplumber not installed. Install: pip install pdfplumber")
            raise
        except Exception as e:
            logger.error(f"Failed to extract PDF text: {e}")
            raise
    
    @staticmethod
    def extract_from_docx(file_path: Union[str, Path]) -> str:
        """Extract text from DOCX resume."""
        try:
            from docx import Document
            
            doc = Document(file_path)
            paragraphs = [para.text for para in doc.paragraphs]
            text = "\n".join(paragraphs)
            
            return TextExtractor._clean_text(text)
            
        except ImportError:
            logger.error("python-docx not installed. Install: pip install python-docx")
            raise
        except Exception as e:
            logger.error(f"Failed to extract DOCX text: {e}")
            raise
    
    @staticmethod
    def _ocr_pdf(file_path: Union[str, Path]) -> str:
        """OCR fallback for scanned PDFs."""
        try:
            from pdf2image import convert_from_path
            import pytesseract
            
            images = convert_from_path(file_path)
            text_parts = []
            
            for img in images:
                text_parts.append(pytesseract.image_to_string(img))
            
            return TextExtractor._clean_text("\n".join(text_parts))
            
        except ImportError:
            logger.error("OCR dependencies missing. Install: pip install pdf2image pytesseract")
            return ""
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""
    
    @staticmethod
    def _clean_text(text: str) -> str:
        """Clean extracted text: normalize whitespace, remove artifacts."""
        # Remove excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove page numbers
        text = re.sub(r'Page \d+ of \d+', '', text, flags=re.IGNORECASE)
        
        # Normalize whitespace
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Remove common PDF artifacts
        text = re.sub(r'\x0c', '', text)  # Form feed
        
        return text.strip()
    
    @classmethod
    def extract(cls, file_path: Union[str, Path]) -> str:
        """
        Auto-detect format and extract text.
        
        Args:
            file_path: Path to resume file
            
        Returns:
            Cleaned text content
        """
        path = Path(file_path)
        extension = path.suffix.lower()
        
        if extension == '.pdf':
            return cls.extract_from_pdf(path)
        elif extension in ['.docx', '.doc']:
            return cls.extract_from_docx(path)
        elif extension == '.txt':
            return path.read_text(encoding='utf-8')
        else:
            raise ValueError(f"Unsupported file format: {extension}")
