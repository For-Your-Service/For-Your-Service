"""
Canonical skill name normalization.

Handles variations: "Kubernetes", "k8s", "K8S" → "kubernetes"
"""

from typing import Dict, Optional, Set
import re


class SkillNormalizer:
    """Normalize skill names to canonical forms."""
    
    # Canonical skill mappings
    SKILL_SYNONYMS = {
        # Kubernetes variants
        'k8s': 'kubernetes',
        'k8': 'kubernetes',
        'kube': 'kubernetes',
        
        # Docker variants
        'containerization': 'docker',
        'containers': 'docker',
        
        # Cloud platforms
        'amazon web services': 'aws',
        'google cloud platform': 'gcp',
        'microsoft azure': 'azure',
        
        # IaC
        'infrastructure as code': 'terraform',
        'iac': 'terraform',
        
        # CI/CD
        'continuous integration': 'ci/cd',
        'continuous delivery': 'ci/cd',
        'continuous deployment': 'ci/cd',
        
        # Programming languages
        'python3': 'python',
        'python 3': 'python',
        'golang': 'go',
        
        # Databases
        'postgres': 'postgresql',
        'mongo': 'mongodb',
        
        # Monitoring
        'prom': 'prometheus',
    }
    
    def __init__(self):
        """Initialize normalizer with synonym mappings."""
        self.synonyms = {k.lower(): v.lower() for k, v in self.SKILL_SYNONYMS.items()}
    
    def normalize(self, skill_text: str) -> str:
        """
        Normalize skill to canonical form.
        
        Args:
            skill_text: Raw skill string
            
        Returns:
            Canonical skill name
        """
        skill_lower = skill_text.lower().strip()
        
        # Remove special characters
        skill_lower = re.sub(r'[^\w\s/-]', '', skill_lower)
        
        # Check synonym mapping
        if skill_lower in self.synonyms:
            return self.synonyms[skill_lower]
        
        return skill_lower
    
    def normalize_list(self, skills: list[str]) -> Set[str]:
        """Normalize a list of skills and deduplicate."""
        return {self.normalize(skill) for skill in skills}
