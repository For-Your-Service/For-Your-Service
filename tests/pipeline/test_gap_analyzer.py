"""
Unit tests for Gap Analyzer

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import unittest
from src.pipeline.gap_analyzer import GapAnalyzer, SkillGap, GapAnalysis


class TestGapAnalyzer(unittest.TestCase):
    """Test gap analysis functionality"""
    
    def setUp(self):
        """Initialize test fixtures"""
        self.analyzer = GapAnalyzer()
    
    def test_perfect_match(self):
        """Test 100% skill match scenario"""
        candidate_skills = ["AWS", "Kubernetes", "Python", "Docker"]
        job_requirements = [
            {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Kubernetes", "importance": "Important", "required_level": "Proficient"},
            {"skill": "Python", "importance": "Important", "required_level": "Proficient"},
            {"skill": "Docker", "importance": "Nice-to-have", "required_level": "Proficient"}
        ]
        
        result = self.analyzer.analyze(candidate_skills, job_requirements)
        
        self.assertEqual(len(result.matching_skills), 4)
        self.assertEqual(len(result.missing_skills), 0)
        self.assertEqual(result.match_score, 1.0)
        self.assertIn("Ready Now", result.estimated_readiness)
    
    def test_partial_match(self):
        """Test partial skill match with gaps"""
        candidate_skills = ["AWS", "Python"]
        job_requirements = [
            {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Kubernetes", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Python", "importance": "Important", "required_level": "Proficient"},
            {"skill": "Terraform", "importance": "Nice-to-have", "required_level": "Proficient"}
        ]
        
        result = self.analyzer.analyze(candidate_skills, job_requirements)
        
        self.assertEqual(len(result.matching_skills), 2)
        self.assertEqual(len(result.missing_skills), 2)
        self.assertGreater(result.match_score, 0.0)
        self.assertLess(result.match_score, 1.0)
    
    def test_critical_gap_identification(self):
        """Test identification of critical missing skills"""
        candidate_skills = ["Python", "Docker"]
        job_requirements = [
            {"skill": "AWS", "importance": "Critical", "required_level": "Expert"},
            {"skill": "Python", "importance": "Important", "required_level": "Proficient"}
        ]
        
        result = self.analyzer.analyze(candidate_skills, job_requirements)
        
        critical_gaps = [g for g in result.missing_skills if g.importance == "Critical"]
        self.assertEqual(len(critical_gaps), 1)
        self.assertEqual(critical_gaps[0].skill_name, "AWS")
        self.assertEqual(critical_gaps[0].target_level, "Expert")
    
    def test_learning_resources(self):
        """Test learning resource recommendations"""
        candidate_skills = []
        job_requirements = [
            {"skill": "Kubernetes", "importance": "Critical", "required_level": "Proficient"}
        ]
        
        result = self.analyzer.analyze(candidate_skills, job_requirements)
        
        k8s_gap = result.missing_skills[0]
        self.assertGreater(len(k8s_gap.learning_resources), 0)
        self.assertIsNotNone(k8s_gap.estimated_time)
        self.assertIn("Kubernetes", k8s_gap.learning_resources[0])
    
    def test_recommendation_generation(self):
        """Test recommendation generation logic"""
        candidate_skills = ["AWS", "Python"]
        job_requirements = [
            {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Kubernetes", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Python", "importance": "Important", "required_level": "Proficient"}
        ]
        
        result = self.analyzer.analyze(candidate_skills, job_requirements, candidate_experience_years=5)
        
        self.assertGreater(len(result.recommendations), 0)
        # Should highlight matching skills
        self.assertTrue(any("Strong foundation" in r for r in result.recommendations))
    
    def test_certification_suggestions(self):
        """Test certification recommendation logic"""
        candidate_skills = ["Python"]
        job_requirements = [
            {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "Kubernetes", "importance": "Important", "required_level": "Proficient"}
        ]
        
        result = self.analyzer.analyze(candidate_skills, job_requirements)
        
        self.assertGreater(len(result.certification_suggestions), 0)
        self.assertTrue(any("AWS" in cert for cert in result.certification_suggestions))
    
    def test_experience_level_recommendations(self):
        """Test experience-based recommendations"""
        candidate_skills = ["AWS"]
        job_requirements = [
            {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"}
        ]
        
        # Junior candidate
        junior_result = self.analyzer.analyze(candidate_skills, job_requirements, candidate_experience_years=1)
        self.assertTrue(any("portfolio" in r.lower() for r in junior_result.recommendations))
        
        # Senior candidate
        senior_result = self.analyzer.analyze(candidate_skills, job_requirements, candidate_experience_years=15)
        self.assertTrue(any("leadership" in r.lower() for r in senior_result.recommendations))
    
    def test_skill_priority_ordering(self):
        """Test skill gap priority sorting"""
        gaps = [
            SkillGap(skill_name="Docker", importance="Nice-to-have"),
            SkillGap(skill_name="AWS", importance="Critical"),
            SkillGap(skill_name="Python", importance="Important")
        ]
        
        sorted_gaps = self.analyzer.get_skill_priority_order(gaps)
        
        self.assertEqual(sorted_gaps[0].importance, "Critical")
        self.assertEqual(sorted_gaps[1].importance, "Important")
        self.assertEqual(sorted_gaps[2].importance, "Nice-to-have")
    
    def test_case_insensitive_matching(self):
        """Test case-insensitive skill matching"""
        candidate_skills = ["aws", "KUBERNETES", "Python"]
        job_requirements = [
            {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
            {"skill": "kubernetes", "importance": "Important", "required_level": "Proficient"}
        ]
        
        result = self.analyzer.analyze(candidate_skills, job_requirements)
        
        self.assertEqual(len(result.matching_skills), 2)
    
    def test_empty_requirements(self):
        """Test handling of empty job requirements"""
        candidate_skills = ["AWS", "Python"]
        job_requirements = []
        
        result = self.analyzer.analyze(candidate_skills, job_requirements)
        
        self.assertEqual(result.match_score, 1.0)
        self.assertEqual(len(result.missing_skills), 0)


if __name__ == "__main__":
    unittest.main()
