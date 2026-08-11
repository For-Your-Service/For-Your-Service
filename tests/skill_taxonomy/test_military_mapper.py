"""
Tests for Military Skill Mapper

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import unittest
from src.skill_taxonomy.military_mapper import MilitarySkillMapper


class TestMilitarySkillMapper(unittest.TestCase):
    """Tests for MilitarySkillMapper"""
    
    def setUp(self):
        """Initialize mapper for each test"""
        self.mapper = MilitarySkillMapper()
    
    def test_get_18z_role(self):
        """Test Army 18Z (Team Sergeant) mapping"""
        role = self.mapper.get_military_role("18Z", "Army")
        
        self.assertIsNotNone(role)
        self.assertEqual(role.code, "18Z")
        self.assertEqual(role.title, "Special Forces Senior Sergeant")
        self.assertIn("Leadership", role.skills)
    
    def test_get_18b_role(self):
        """Test Army 18B (Weapons Sergeant) mapping"""
        role = self.mapper.get_military_role("18B", "Army")
        
        self.assertIsNotNone(role)
        self.assertEqual(role.civilian_equivalent, "Technical Specialist / Systems Engineer")
        self.assertIn("Technical Training", role.skills)
    
    def test_get_18e_role(self):
        """Test Army 18E (Communications Sergeant) mapping"""
        role = self.mapper.get_military_role("18E", "Army")
        
        self.assertIsNotNone(role)
        self.assertIn("Network Administration", role.skills)
        self.assertIn("Security+", role.certifications)
    
    def test_case_insensitive_lookup(self):
        """Test that MOS lookup is case-insensitive"""
        role_upper = self.mapper.get_military_role("18Z", "Army")
        role_lower = self.mapper.get_military_role("18z", "Army")
        
        self.assertEqual(role_upper.code, role_lower.code)
    
    def test_extract_civilian_skills(self):
        """Test extracting civilian skills from MOS"""
        skills = self.mapper.extract_civilian_skills("18Z", "Army")
        
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)
        self.assertIn("Senior Leadership", skills)
    
    def test_get_recommended_certifications(self):
        """Test getting recommended certifications"""
        certs = self.mapper.get_recommended_certifications("25B", "Army")
        
        self.assertIn("CompTIA A+", certs)
        self.assertIn("Security+", certs)
    
    def test_get_civilian_equivalent(self):
        """Test getting civilian job equivalent"""
        equivalent = self.mapper.get_civilian_equivalent("18D", "Army")
        self.assertEqual(equivalent, "Paramedic / Emergency Medical Technician")
    
    def test_unknown_mos_returns_none(self):
        """Test that unknown MOS returns None"""
        role = self.mapper.get_military_role("99X", "Army")
        self.assertIsNone(role)
    
    def test_air_force_afsc(self):
        """Test Air Force AFSC mapping"""
        role = self.mapper.get_military_role("3D0X2", "Air Force")
        
        self.assertIsNotNone(role)
        self.assertEqual(role.branch, "Air Force")
        self.assertIn("Systems Administration", role.skills)
    
    def test_navy_rating(self):
        """Test Navy rating mapping"""
        role = self.mapper.get_military_role("CTN", "Navy")
        
        self.assertIsNotNone(role)
        self.assertEqual(role.branch, "Navy")
        self.assertIn("Cybersecurity", role.skills)
    
    def test_enrich_resume_with_military_skills(self):
        """Test enriching resume with military-derived skills"""
        resume = {
            "full_name": "John Doe",
            "military_branch": "Army",
            "military_mos": "18E",
            "skills": ["Leadership"]
        }
        
        enriched = self.mapper.enrich_resume_with_military_skills(resume)
        
        # Should add military skills
        self.assertIn("Network Administration", enriched["skills"])
        self.assertIn("Leadership", enriched["skills"])
        
        # Should add recommended certs
        self.assertIn("recommended_certifications", enriched)
        self.assertGreater(len(enriched["recommended_certifications"]), 0)
        
        # Should add civilian equivalent
        self.assertEqual(
            enriched["civilian_equivalent_title"],
            "Network Engineer / IT Specialist"
        )
    
    def test_enrich_resume_without_military_data(self):
        """Test enriching resume without military info"""
        resume = {
            "full_name": "Jane Doe",
            "skills": ["Python"]
        }
        
        enriched = self.mapper.enrich_resume_with_military_skills(resume)
        
        # Should return unchanged
        self.assertEqual(enriched["skills"], ["Python"])
        self.assertNotIn("recommended_certifications", enriched)


if __name__ == '__main__':
    unittest.main()
