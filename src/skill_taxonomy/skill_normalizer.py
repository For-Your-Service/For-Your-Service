"""
Skill Normalizer

Canonicalizes raw skills to standardized O*NET taxonomy.
Handles variations, abbreviations, and synonyms.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import List, Dict, Optional
from difflib import SequenceMatcher

from .onet_client import ONetClient


class SkillNormalizer:
    """Normalizes skills to standard taxonomy"""

    def __init__(self, onet_client: Optional[ONetClient] = None):
        """
        Initialize skill normalizer

        Args:
            onet_client: Optional ONetClient instance (creates default if None)
        """
        self.onet = onet_client or ONetClient()

        # Common skill variations and canonical forms
        self.skill_aliases = {
            # Cloud platforms
            "aws": "Amazon Web Services",
            "amazon web services": "Amazon Web Services",
            "azure": "Microsoft Azure",
            "gcp": "Google Cloud Platform",
            "google cloud": "Google Cloud Platform",
            # Containers
            "k8s": "Kubernetes",
            "kube": "Kubernetes",
            "docker": "Docker",
            "containerization": "Docker",
            # CI/CD
            "jenkins": "Jenkins",
            "gitlab ci": "GitLab CI/CD",
            "github actions": "GitHub Actions",
            "cicd": "CI/CD",
            "ci/cd": "CI/CD",
            # IaC
            "terraform": "Terraform",
            "tf": "Terraform",
            "iac": "Infrastructure as Code",
            "cloudformation": "AWS CloudFormation",
            # Programming
            "py": "Python",
            "python3": "Python",
            "js": "JavaScript",
            "javascript": "JavaScript",
            "ts": "TypeScript",
            "golang": "Go",
            # Databases
            "postgres": "PostgreSQL",
            "postgresql": "PostgreSQL",
            "mysql": "MySQL",
            "mongodb": "MongoDB",
            "mongo": "MongoDB",
            # Operating Systems
            "linux": "Linux",
            "unix": "Unix",
            "ubuntu": "Linux",
            "rhel": "Red Hat Enterprise Linux",
            # Version Control
            "git": "Git",
            "github": "GitHub",
            "gitlab": "GitLab",
            "bitbucket": "Bitbucket",
        }

        # Skill categories
        self.skill_categories = {
            "Amazon Web Services": "Cloud",
            "Microsoft Azure": "Cloud",
            "Google Cloud Platform": "Cloud",
            "Kubernetes": "DevOps",
            "Docker": "DevOps",
            "Terraform": "DevOps",
            "Jenkins": "DevOps",
            "CI/CD": "DevOps",
            "Python": "Programming",
            "JavaScript": "Programming",
            "Go": "Programming",
            "PostgreSQL": "Database",
            "MongoDB": "Database",
            "Linux": "Operating System",
            "Git": "Version Control",
        }

    def normalize_skill(self, raw_skill: str) -> Dict[str, str]:
        """
        Normalize a single skill to canonical form

        Args:
            raw_skill: Raw skill name from resume

        Returns:
            Dict with canonical_name, category, original
        """
        # Clean and lowercase
        cleaned = raw_skill.strip().lower()

        # Check aliases first
        canonical = self.skill_aliases.get(cleaned, raw_skill.title())

        # Get category
        category = self.skill_categories.get(canonical, "Other")

        return {
            "original": raw_skill,
            "canonical_name": canonical,
            "category": category,
            "confidence": 1.0 if cleaned in self.skill_aliases else 0.8,
        }

    def normalize_skills(self, raw_skills: List[str]) -> List[Dict]:
        """
        Normalize a list of skills

        Args:
            raw_skills: List of raw skill names

        Returns:
            List of normalized skill dicts
        """
        normalized = []
        seen_canonical = set()

        for skill in raw_skills:
            norm = self.normalize_skill(skill)

            # Deduplicate by canonical name
            if norm["canonical_name"] not in seen_canonical:
                normalized.append(norm)
                seen_canonical.add(norm["canonical_name"])

        return normalized

    def fuzzy_match_skill(
        self, skill: str, candidates: List[str], threshold: float = 0.8
    ) -> Optional[str]:
        """
        Find best fuzzy match for skill in candidate list

        Args:
            skill: Skill to match
            candidates: List of canonical skills
            threshold: Minimum similarity score (0-1)

        Returns:
            Best matching canonical skill or None
        """
        skill_lower = skill.lower()
        best_match = None
        best_score = threshold

        for candidate in candidates:
            score = SequenceMatcher(None, skill_lower, candidate.lower()).ratio()
            if score > best_score:
                best_score = score
                best_match = candidate

        return best_match

    def extract_tech_stack(self, normalized_skills: List[Dict]) -> Dict[str, List[str]]:
        """
        Group normalized skills by category

        Args:
            normalized_skills: List of normalized skill dicts

        Returns:
            Dict mapping category to list of skills
        """
        tech_stack = {}

        for skill in normalized_skills:
            category = skill["category"]
            name = skill["canonical_name"]

            if category not in tech_stack:
                tech_stack[category] = []

            tech_stack[category].append(name)

        return tech_stack

    def add_skill_alias(self, alias: str, canonical: str, category: Optional[str] = None):
        """
        Add new skill alias mapping

        Args:
            alias: Alternate name/abbreviation
            canonical: Standard form
            category: Optional skill category
        """
        self.skill_aliases[alias.lower()] = canonical

        if category:
            self.skill_categories[canonical] = category

    def get_skill_suggestions(self, partial_skill: str, limit: int = 5) -> List[str]:
        """
        Get skill name suggestions based on partial input

        Args:
            partial_skill: Partial skill name
            limit: Max suggestions to return

        Returns:
            List of suggested canonical skill names
        """
        partial_lower = partial_skill.lower()
        suggestions = []

        for alias, canonical in self.skill_aliases.items():
            if partial_lower in alias or partial_lower in canonical.lower():
                if canonical not in suggestions:
                    suggestions.append(canonical)
                    if len(suggestions) >= limit:
                        break

        return suggestions
