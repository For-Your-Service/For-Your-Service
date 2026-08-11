"""
PDF Resume Parser

Extracts structured data from PDF resume files.
Uses PyPDF2 for text extraction (free, no API costs).

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from pathlib import Path
from typing import Union, List
import re

try:
    from PyPDF2 import PdfReader
except ImportError:
    raise ImportError(
        "PyPDF2 is required for PDF parsing. "
        "Install with: pip install PyPDF2"
    )

from .base_parser import BaseResumeParser
from .schema import (
    ResumeSchema, 
    SkillEntry, 
    ExperienceEntry, 
    EducationEntry
)


class PDFResumeParser(BaseResumeParser):
    """Parser for PDF resume files"""
    
    def __init__(self):
        super().__init__()
        self.supported_formats = ['.pdf']
    
    def extract_text(self, file_path: Union[str, Path]) -> str:
        """
        Extract all text from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Raw text content
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if not self.is_supported(path):
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        try:
            reader = PdfReader(str(path))
            text_parts = []
            
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            full_text = '\n'.join(text_parts)
            return self.clean_text(full_text)
            
        except Exception as e:
            raise RuntimeError(f"Failed to extract PDF text: {str(e)}")
    
    def parse(self, file_path: Union[str, Path]) -> ResumeSchema:
        """
        Parse PDF resume into structured schema
        
        Args:
            file_path: Path to PDF resume file
            
        Returns:
            ResumeSchema with extracted data
        """
        raw_text = self.extract_text(file_path)
        
        # Extract contact information
        full_name = self._extract_name(raw_text)
        email = self.extract_email(raw_text)
        phone = self.extract_phone(raw_text)
        location = self._extract_location(raw_text)
        linkedin = self.extract_urls(raw_text, "linkedin.com")
        github = self.extract_urls(raw_text, "github.com")
        
        # Extract sections
        skills = self._extract_skills(raw_text)
        experience = self._extract_experience(raw_text)
        education = self._extract_education(raw_text)
        certifications = self._extract_certifications(raw_text)
        
        # Extract veteran-specific info
        military_info = self._extract_military_info(raw_text)
        
        return ResumeSchema(
            full_name=full_name,
            email=email,
            phone=phone,
            location=location,
            linkedin_url=linkedin,
            github_url=github,
            skills=skills,
            experience=experience,
            education=education,
            certifications=certifications,
            military_branch=military_info.get('branch'),
            military_mos=military_info.get('mos'),
            security_clearance=military_info.get('clearance'),
            years_of_service=military_info.get('years'),
            raw_text=raw_text,
            parse_timestamp=self.get_timestamp()
        )
    
    def _extract_name(self, text: str) -> str:
        """Extract candidate name (typically first line)"""
        lines = text.split('\n')
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            # Name is usually short, capitalized, no special chars
            if len(line) < 50 and re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', line):
                return line
        return "Unknown"
    
    def _extract_location(self, text: str) -> str:
        """Extract location (city, state)"""
        # Match patterns like "City, ST" or "City, State"
        location_pattern = r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)*),\s*([A-Z]{2}|[A-Z][a-z]+)'
        matches = re.findall(location_pattern, text)
        if matches:
            city, state = matches[0]
            return f"{city}, {state}"
        return None
    
    def _extract_skills(self, text: str) -> List[SkillEntry]:
        """Extract skills section"""
        skills = []
        
        # Common tech skills to look for
        tech_skills = [
            'Python', 'AWS', 'Azure', 'GCP', 'Kubernetes', 'Docker', 
            'Terraform', 'Jenkins', 'GitHub', 'GitLab', 'CI/CD',
            'Linux', 'Bash', 'SQL', 'PostgreSQL', 'MongoDB',
            'React', 'Node.js', 'Java', 'Go', 'Rust'
        ]
        
        text_lower = text.lower()
        for skill in tech_skills:
            if skill.lower() in text_lower:
                skills.append(SkillEntry(
                    name=skill,
                    category="Technical"
                ))
        
        return skills
    
    def _extract_experience(self, text: str) -> List[ExperienceEntry]:
        """Extract work experience entries"""
        # This is a placeholder - real implementation would use NLP
        # to identify experience sections and parse dates/companies
        return []
    
    def _extract_education(self, text: str) -> List[EducationEntry]:
        """Extract education entries"""
        # Placeholder for education extraction
        return []
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certs = []
        common_certs = [
            'AWS Certified', 'Azure Certified', 'GCP Certified',
            'CISSP', 'Security+', 'CEH', 'OSCP',
            'PMP', 'Scrum Master', 'Six Sigma'
        ]
        
        for cert in common_certs:
            if cert.lower() in text.lower():
                certs.append(cert)
        
        return certs
    
    def _extract_military_info(self, text: str) -> dict:
        """Extract military service information"""
        info = {}
        
        # Branch detection
        branches = ['Army', 'Navy', 'Air Force', 'Marines', 'Coast Guard', 'Space Force']
        for branch in branches:
            if branch.lower() in text.lower():
                info['branch'] = branch
                break
        
        # Clearance detection
        clearances = ['TS/SCI', 'Top Secret', 'Secret', 'Confidential']
        for clearance in clearances:
            if clearance.lower() in text.lower():
                info['clearance'] = clearance
                break
        
        # MOS/AFSC detection (e.g., "18B", "25B")
        mos_pattern = r'\b\d{2}[A-Z]\b'
        mos_matches = re.findall(mos_pattern, text)
        if mos_matches:
            info['mos'] = mos_matches[0]
        
        return info
