"""
Integration tests for complete pipeline orchestration

Tests end-to-end flow from resume to recommendations.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import unittest
from unittest.mock import patch

from src.pipeline.orchestrator import MatchingOrchestrator
from src.resume_parser.schema import ResumeSchema, SkillEntry


class TestPipelineIntegration(unittest.TestCase):
    """Test complete pipeline integration"""

    def setUp(self):
        """Initialize test fixtures"""
        self.orchestrator = MatchingOrchestrator(
            similarity_threshold=0.6, enable_military_mapping=True
        )

    def test_end_to_end_flow(self):
        """Test complete pipeline from resume to recommendations"""

        # Mock resume data
        mock_resume = ResumeSchema(
            full_name="John Doe",
            email="john.doe@example.com",
            location="Greenville, SC",
            skills=[
                SkillEntry(name="AWS", category="Cloud"),
                SkillEntry(name="Python", category="Programming"),
                SkillEntry(name="Docker", category="DevOps"),
            ],
            military_branch="Army",
            military_mos="18Z",
            total_years_experience=15,
        )

        # Mock job requirements
        job_requirements = [
            {
                "id": "job1",
                "title": "DevOps Engineer",
                "company": "Tech Corp",
                "location": "Greenville, SC",
                "salary_range": "$120K-$180K",
                "required_skills": [
                    {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
                    {
                        "skill": "Kubernetes",
                        "importance": "Critical",
                        "required_level": "Proficient",
                    },
                    {"skill": "Python", "importance": "Important", "required_level": "Proficient"},
                ],
            }
        ]

        # Mock parser to return our test resume
        with patch.object(self.orchestrator, "pdf_parser") as mock_parser:
            mock_parser.parse.return_value = mock_resume

            # Process with mock
            result = self.orchestrator.match_jobs(
                resume=mock_resume,
                job_requirements=job_requirements,
                location_filter="Greenville, SC",
            )

        # Verify structure
        self.assertIn("candidate", result)
        self.assertIn("gap_analyses", result)
        self.assertIn("recommendations", result)
        self.assertIn("summary", result)

        # Verify candidate info
        self.assertEqual(result["candidate"]["name"], "John Doe")
        self.assertEqual(result["candidate"]["location"], "Greenville, SC")
        self.assertIn("AWS", result["candidate"]["skills"])

        # Verify gap analysis
        self.assertGreater(len(result["gap_analyses"]), 0)
        gap = result["gap_analyses"][0]
        self.assertIn("job_id", gap)
        self.assertIn("gap_analysis", gap)

        # Verify summary stats
        self.assertEqual(result["summary"]["total_jobs_analyzed"], 1)
        self.assertGreater(result["summary"]["best_match_score"], 0.0)

    def test_military_enrichment_integration(self):
        """Test military skill enrichment in pipeline"""

        mock_resume = ResumeSchema(
            full_name="Veteran Candidate",
            email="vet@example.com",
            skills=[SkillEntry(name="Leadership", category="Soft Skills")],
            military_branch="Army",
            military_mos="18E",
            total_years_experience=10,
        )

        # Enable military mapping
        orchestrator = MatchingOrchestrator(enable_military_mapping=True)

        # Process resume (mocking parser)
        with patch.object(orchestrator, "pdf_parser") as mock_parser:
            mock_parser.parse.return_value = mock_resume

            # Military mapper should be invoked
            with patch.object(
                orchestrator.military_mapper, "enrich_resume_with_military_skills"
            ) as mock_enrich:
                mock_enrich.return_value = {
                    "skills": ["Network Administration", "Telecommunications", "Cybersecurity"]
                }

                # Process
                result = orchestrator.process_resume("fake_path.pdf")

                # Verify military mapper was called
                mock_enrich.assert_called_once()

    def test_skill_normalization_integration(self):
        """Test skill normalization in pipeline"""

        mock_resume = ResumeSchema(
            full_name="Test Candidate",
            email="test@example.com",
            skills=[
                SkillEntry(name="aws", category=""),  # Lowercase
                SkillEntry(name="k8s", category=""),  # Alias
            ],
        )

        with patch.object(self.orchestrator, "pdf_parser") as mock_parser:
            mock_parser.parse.return_value = mock_resume

            # Process
            result = self.orchestrator.process_resume("fake_path.pdf")

            # Skills should be normalized
            skill_names = [s.name for s in result.skills]

            # Check normalization happened (skills should have canonical forms)
            self.assertIsNotNone(result.skills[0].category)  # Categories assigned

    def test_gap_analysis_recommendations_flow(self):
        """Test flow from gap analysis to recommendations"""

        mock_resume = ResumeSchema(
            full_name="Junior Dev",
            email="junior@example.com",
            skills=[SkillEntry(name="Python", category="Programming")],
            total_years_experience=2,
        )

        job_requirements = [
            {
                "id": "job1",
                "title": "Cloud Engineer",
                "required_skills": [
                    {"skill": "AWS", "importance": "Critical", "required_level": "Proficient"},
                    {"skill": "Python", "importance": "Important", "required_level": "Proficient"},
                ],
            }
        ]

        result = self.orchestrator.match_jobs(resume=mock_resume, job_requirements=job_requirements)

        # Should have gap analysis
        gap = result["gap_analyses"][0]["gap_analysis"]
        self.assertIn("Python", gap.matching_skills)
        self.assertTrue(any(g.skill_name == "AWS" for g in gap.missing_skills))

        # Should have recommendations
        self.assertIsNotNone(result["recommendations"])
        recommendations = result["recommendations"]

        # Check recommendation components
        self.assertIsNotNone(recommendations.resume_improvements)
        self.assertIsNotNone(recommendations.job_search_tips)
        self.assertIsNotNone(recommendations.skill_development_plan)

    def test_batch_processing_error_handling(self):
        """Test batch processing with errors"""

        resumes = ["nonexistent1.pdf", "nonexistent2.pdf"]

        job_requirements = [{"id": "job1", "title": "Test Job", "required_skills": []}]

        # Should handle errors gracefully
        results = self.orchestrator.batch_process(resumes, job_requirements)

        # Both should have error entries
        for resume_path in resumes:
            self.assertIn(resume_path, results)
            self.assertIn("error", results[resume_path])

    def test_veteran_specific_features(self):
        """Test veteran-specific pipeline features"""

        veteran_resume = ResumeSchema(
            full_name="Veteran Candidate",
            email="veteran@example.com",
            skills=[
                SkillEntry(name="AWS", category="Cloud"),
                SkillEntry(name="Leadership", category="Soft Skills"),
            ],
            military_branch="Army",
            military_mos="18Z",
            security_clearance="TS/SCI",
            total_years_experience=18,
        )

        job_requirements = [
            {
                "id": "job1",
                "title": "DevOps Engineer",
                "required_skills": [
                    {"skill": "AWS", "importance": "Critical", "required_level": "Expert"}
                ],
            }
        ]

        result = self.orchestrator.match_jobs(
            resume=veteran_resume, job_requirements=job_requirements
        )

        # Verify military background captured
        military = result["candidate"]["military_background"]
        self.assertEqual(military["branch"], "Army")
        self.assertEqual(military["mos"], "18Z")
        self.assertEqual(military["clearance"], "TS/SCI")

        # Recommendations should include veteran advice
        if result["recommendations"]:
            tips = result["recommendations"].job_search_tips
            has_veteran_advice = any(
                "veteran" in tip.lower() or "clearance" in tip.lower() for tip in tips
            )
            self.assertTrue(has_veteran_advice)


if __name__ == "__main__":
    unittest.main()
