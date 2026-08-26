"""
Extract and normalize skills from job descriptions
"""

from typing import List, Dict
import re
import logging

logger = logging.getLogger(__name__)


class SkillExtractor:
    """Extracts technical and soft skills from text"""

    # Common technical skills
    TECHNICAL_SKILLS = {
        # Programming
        "python",
        "java",
        "javascript",
        "c++",
        "c#",
        "sql",
        "go",
        "rust",
        # Cloud
        "aws",
        "azure",
        "gcp",
        "kubernetes",
        "docker",
        "terraform",
        # Cybersecurity
        "cissp",
        "security+",
        "ceh",
        "penetration testing",
        "siem",
        # Networking
        "cisco",
        "ccna",
        "ccnp",
        "tcp/ip",
        "bgp",
        "ospf",
        # Data
        "spark",
        "hadoop",
        "kafka",
        "airflow",
        "databricks",
    }

    # Soft skills
    SOFT_SKILLS = {
        "leadership",
        "teamwork",
        "communication",
        "problem-solving",
        "critical thinking",
        "adaptability",
        "time management",
    }

    def extract_skills(self, text: str) -> Dict[str, List[str]]:
        """
        Extract skills from job description

        Args:
            text: Job description text

        Returns:
            Dict with 'technical' and 'soft' skill lists
        """
        text_lower = text.lower()

        technical = []
        for skill in self.TECHNICAL_SKILLS:
            if skill in text_lower:
                technical.append(skill)

        soft = []
        for skill in self.SOFT_SKILLS:
            if skill in text_lower:
                soft.append(skill)

        return {"technical": technical, "soft": soft}

    def normalize_skill_name(self, skill: str) -> str:
        """
        Normalize skill variations to canonical form

        Args:
            skill: Raw skill string

        Returns:
            Normalized skill name
        """
        # Remove special characters, lowercase
        normalized = re.sub(r"[^\w\s]", "", skill.lower())

        # Map variations to canonical names
        mappings = {
            "k8s": "kubernetes",
            "eks": "kubernetes",
            "aws lambda": "lambda",
            "azure functions": "serverless",
        }

        return mappings.get(normalized, normalized)
