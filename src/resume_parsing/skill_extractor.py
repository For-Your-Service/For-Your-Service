"""
Skill extraction from resume text using NER and pattern matching.
"""

import re
from typing import List, Set
from .models import Skill, SkillCategory
import logging

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extract skills from resume text."""
    
    # Common tech skills patterns
    TECH_SKILLS = {
        # Cloud
        'aws', 'azure', 'gcp', 'google cloud', 'cloud computing',
        # Containers & Orchestration
        'docker', 'kubernetes', 'k8s', 'openshift', 'rancher',
        # IaC
        'terraform', 'ansible', 'chef', 'puppet', 'cloudformation',
        # CI/CD
        'jenkins', 'github actions', 'gitlab ci', 'circleci', 'travis ci',
        # Languages
        'python', 'java', 'javascript', 'typescript', 'go', 'rust', 'c++',
        'bash', 'shell scripting', 'powershell',
        # Databases
        'postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch',
        # Monitoring
        'prometheus', 'grafana', 'datadog', 'new relic', 'splunk',
    }
    
    # Military-specific clearances
    CLEARANCES = {
        'top secret', 'ts', 'ts/sci', 'secret', 'confidential',
        'public trust', 'q clearance', 'l clearance'
    }
    
    # Certifications
    CERTIFICATIONS = {
        'security+', 'sec+', 'cissp', 'ceh', 'cism', 'cisa',
        'aws certified', 'azure certified', 'gcp certified',
        'cka', 'ckad', 'cks',  # Kubernetes
        'pmp', 'csm', 'psm',  # Project management
    }
    
    def __init__(self):
        """Initialize skill extractor."""
        self.tech_skills_lower = {s.lower() for s in self.TECH_SKILLS}
        self.clearances_lower = {c.lower() for c in self.CLEARANCES}
        self.certs_lower = {c.lower() for c in self.CERTIFICATIONS}
    
    def extract(self, text: str) -> List[Skill]:
        """
        Extract all skills from resume text.
        
        Args:
            text: Cleaned resume text
            
        Returns:
            List of extracted skills with categories
        """
        text_lower = text.lower()
        skills = []
        
        # Extract technical skills
        for skill_name in self.tech_skills_lower:
            if re.search(r'\b' + re.escape(skill_name) + r'\b', text_lower):
                skills.append(Skill(
                    raw_text=skill_name,
                    normalized_name=skill_name,
                    category=SkillCategory.HARD_SKILL,
                    confidence=0.9
                ))
        
        # Extract clearances
        for clearance in self.clearances_lower:
            if re.search(r'\b' + re.escape(clearance) + r'\b', text_lower):
                skills.append(Skill(
                    raw_text=clearance,
                    normalized_name=clearance,
                    category=SkillCategory.CLEARANCE,
                    confidence=0.95
                ))
        
        # Extract certifications
        for cert in self.certs_lower:
            if re.search(r'\b' + re.escape(cert) + r'\b', text_lower):
                skills.append(Skill(
                    raw_text=cert,
                    normalized_name=cert,
                    category=SkillCategory.CERTIFICATION,
                    confidence=0.95
                ))
        
        return self._deduplicate(skills)
    
    @staticmethod
    def _deduplicate(skills: List[Skill]) -> List[Skill]:
        """Remove duplicate skills, keeping highest confidence."""
        seen = {}
        for skill in skills:
            key = skill.normalized_name or skill.raw_text
            if key not in seen or skill.confidence > seen[key].confidence:
                seen[key] = skill
        
        return list(seen.values())
