"""
Tests for Resume Schema

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import unittest
from datetime import date
from src.resume_parser.schema import (
    SkillEntry,
    ExperienceEntry,
    EducationEntry,
    ResumeSchema
)


class TestSkillEntry(unittest.TestCase):
    """Tests for SkillEntry dataclass"""
    
    def test_skill_creation(self):
        """Test creating a skill entry"""
        skill = SkillEntry(
            name="Python",
            category="Technical",
            proficiency="Expert",
            years_experience=5.0
        )
        self.assertEqual(skill.name, "Python")
        self.assertEqual(skill.category, "Technical")
        
    def test_skill_to_dict(self):
        """Test skill serialization to dict"""
        skill = SkillEntry(name="AWS", category="Cloud")
        skill_dict = skill.to_dict()
        self.assertIn("name", skill_dict)
        self.assertEqual(skill_dict["name"], "AWS")


class TestExperienceEntry(unittest.TestCase):
    """Tests for ExperienceEntry dataclass"""
    
    def test_experience_duration(self):
        """Test calculating experience duration"""
        exp = ExperienceEntry(
            title="DevOps Engineer",
            company="7 Eagle Group",
            start_date=date(2020, 1, 1),
            end_date=date(2022, 1, 1)
        )
        self.assertEqual(exp.duration_years, 2.0)
    
    def test_current_position(self):
        """Test current position (no end date)"""
        exp = ExperienceEntry(
            title="Cloud Architect",
            company="Tech Corp",
            start_date=date(2023, 1, 1),
            end_date=None  # Current position
        )
        # Duration should be calculated to today
        self.assertIsNotNone(exp.duration_years)
        self.assertGreater(exp.duration_years, 0)
    
    def test_experience_to_dict(self):
        """Test experience serialization"""
        exp = ExperienceEntry(
            title="Engineer",
            company="ACME",
            start_date=date(2020, 1, 1)
        )
        exp_dict = exp.to_dict()
        self.assertEqual(exp_dict["title"], "Engineer")
        self.assertIn("duration_years", exp_dict)


class TestEducationEntry(unittest.TestCase):
    """Tests for EducationEntry dataclass"""
    
    def test_education_creation(self):
        """Test creating education entry"""
        edu = EducationEntry(
            degree="Bachelor of Science",
            institution="State University",
            field_of_study="Computer Science",
            gpa=3.8
        )
        self.assertEqual(edu.degree, "Bachelor of Science")
        self.assertEqual(edu.gpa, 3.8)


class TestResumeSchema(unittest.TestCase):
    """Tests for ResumeSchema dataclass"""
    
    def test_resume_creation(self):
        """Test creating resume schema"""
        resume = ResumeSchema(
            full_name="Free Hall",
            email="whall4.wh@gmail.com",
            location="Greenville, SC"
        )
        self.assertEqual(resume.full_name, "Free Hall")
        self.assertEqual(resume.email, "whall4.wh@gmail.com")
    
    def test_veteran_fields(self):
        """Test veteran-specific fields"""
        resume = ResumeSchema(
            full_name="John Doe",
            military_branch="Army",
            military_mos="18B",
            security_clearance="TS/SCI",
            years_of_service=10.0
        )
        self.assertEqual(resume.military_branch, "Army")
        self.assertEqual(resume.military_mos, "18B")
    
    def test_total_experience_calculation(self):
        """Test calculating total years of experience"""
        exp1 = ExperienceEntry(
            title="Engineer",
            company="Corp",
            start_date=date(2020, 1, 1),
            end_date=date(2022, 1, 1)
        )
        exp2 = ExperienceEntry(
            title="Senior Engineer",
            company="Corp",
            start_date=date(2022, 1, 1),
            end_date=date(2024, 1, 1)
        )
        
        resume = ResumeSchema(
            full_name="Test User",
            experience=[exp1, exp2],
            years_of_service=5.0
        )
        
        # 2 + 2 + 5 = 9 years total
        self.assertEqual(resume.total_years_experience, 9.0)
    
    def test_resume_to_dict(self):
        """Test complete resume serialization"""
        skill = SkillEntry(name="Python", category="Technical")
        resume = ResumeSchema(
            full_name="Free Hall",
            email="whall4.wh@gmail.com",
            skills=[skill]
        )
        
        resume_dict = resume.to_dict()
        self.assertIn("full_name", resume_dict)
        self.assertIn("skills", resume_dict)
        self.assertEqual(len(resume_dict["skills"]), 1)


if __name__ == '__main__':
    unittest.main()
