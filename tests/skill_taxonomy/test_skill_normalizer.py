"""
Tests for Skill Normalizer

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import unittest
from src.skill_taxonomy.skill_normalizer import SkillNormalizer


class TestSkillNormalizer(unittest.TestCase):
    """Tests for SkillNormalizer"""

    def setUp(self):
        """Initialize normalizer for each test"""
        self.normalizer = SkillNormalizer()

    def test_normalize_aws_alias(self):
        """Test AWS alias normalization"""
        result = self.normalizer.normalize_skill("aws")
        self.assertEqual(result["canonical_name"], "Amazon Web Services")
        self.assertEqual(result["category"], "Cloud")
        self.assertEqual(result["confidence"], 1.0)

    def test_normalize_kubernetes_alias(self):
        """Test Kubernetes alias variations"""
        for variant in ["k8s", "kube", "kubernetes"]:
            result = self.normalizer.normalize_skill(variant)
            self.assertEqual(result["canonical_name"], "Kubernetes")
            self.assertEqual(result["category"], "DevOps")

    def test_normalize_unknown_skill(self):
        """Test normalizing unknown skill"""
        result = self.normalizer.normalize_skill("SuperRareSkill")
        self.assertEqual(result["canonical_name"], "Superrareskill")
        self.assertLess(result["confidence"], 1.0)

    def test_normalize_skills_deduplication(self):
        """Test that duplicate canonical skills are deduplicated"""
        raw_skills = ["aws", "AWS", "Amazon Web Services", "k8s", "kubernetes"]
        normalized = self.normalizer.normalize_skills(raw_skills)

        canonical_names = [s["canonical_name"] for s in normalized]
        self.assertEqual(len(canonical_names), 2)  # AWS and Kubernetes only
        self.assertIn("Amazon Web Services", canonical_names)
        self.assertIn("Kubernetes", canonical_names)

    def test_fuzzy_match_skill(self):
        """Test fuzzy skill matching"""
        candidates = ["Python", "JavaScript", "TypeScript"]

        # Close match
        match = self.normalizer.fuzzy_match_skill("pyton", candidates, threshold=0.7)
        self.assertEqual(match, "Python")

        # No match below threshold
        match = self.normalizer.fuzzy_match_skill("ruby", candidates, threshold=0.8)
        self.assertIsNone(match)

    def test_extract_tech_stack(self):
        """Test grouping skills by category"""
        raw_skills = ["Python", "AWS", "Docker", "PostgreSQL", "Terraform"]
        normalized = self.normalizer.normalize_skills(raw_skills)
        tech_stack = self.normalizer.extract_tech_stack(normalized)

        self.assertIn("Cloud", tech_stack)
        self.assertIn("DevOps", tech_stack)
        self.assertIn("Programming", tech_stack)
        self.assertIn("Amazon Web Services", tech_stack["Cloud"])

    def test_add_skill_alias(self):
        """Test adding custom skill alias"""
        self.normalizer.add_skill_alias("vue", "Vue.js", "Frontend")

        result = self.normalizer.normalize_skill("vue")
        self.assertEqual(result["canonical_name"], "Vue.js")
        self.assertEqual(result["category"], "Frontend")

    def test_get_skill_suggestions(self):
        """Test getting skill suggestions"""
        suggestions = self.normalizer.get_skill_suggestions("kub", limit=5)
        self.assertIn("Kubernetes", suggestions)


if __name__ == "__main__":
    unittest.main()
