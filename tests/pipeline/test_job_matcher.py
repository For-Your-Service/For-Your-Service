"""
Unit tests for Job Matcher

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import unittest
import numpy as np
from src.pipeline.job_matcher import JobMatcher, JobMatch


class TestJobMatcher(unittest.TestCase):
    """Test job matching functionality"""

    def setUp(self):
        """Initialize test fixtures"""
        self.matcher = JobMatcher(similarity_threshold=0.6)

    def test_cosine_similarity_identical(self):
        """Test cosine similarity for identical vectors"""
        vec1 = np.array([1.0, 2.0, 3.0])
        vec2 = np.array([1.0, 2.0, 3.0])

        similarity = self.matcher.cosine_similarity(vec1, vec2)

        self.assertAlmostEqual(similarity, 1.0, places=5)

    def test_cosine_similarity_orthogonal(self):
        """Test cosine similarity for orthogonal vectors"""
        vec1 = np.array([1.0, 0.0])
        vec2 = np.array([0.0, 1.0])

        similarity = self.matcher.cosine_similarity(vec1, vec2)

        self.assertAlmostEqual(similarity, 0.5, places=5)  # Normalized to 0-1

    def test_cosine_similarity_opposite(self):
        """Test cosine similarity for opposite vectors"""
        vec1 = np.array([1.0, 0.0])
        vec2 = np.array([-1.0, 0.0])

        similarity = self.matcher.cosine_similarity(vec1, vec2)

        self.assertAlmostEqual(similarity, 0.0, places=5)

    def test_zero_vector_handling(self):
        """Test handling of zero vectors"""
        vec1 = np.array([1.0, 2.0, 3.0])
        vec2 = np.array([0.0, 0.0, 0.0])

        similarity = self.matcher.cosine_similarity(vec1, vec2)

        self.assertEqual(similarity, 0.0)

    def test_find_matches_basic(self):
        """Test basic job matching"""
        candidate_emb = np.array([1.0, 0.5, 0.8])

        job_embeddings = [
            (
                "job1",
                np.array([1.0, 0.5, 0.8]),
                {
                    "title": "DevOps Engineer",
                    "company": "Tech Corp",
                    "location": "Remote",
                    "skills": ["AWS", "Kubernetes"],
                },
            ),
            (
                "job2",
                np.array([0.2, 0.1, 0.3]),
                {
                    "title": "Data Scientist",
                    "company": "Data Inc",
                    "location": "NYC",
                    "skills": ["Python", "R"],
                },
            ),
        ]

        result = self.matcher.find_matches(candidate_emb, job_embeddings, top_k=5)

        self.assertGreater(len(result.matches), 0)
        self.assertEqual(result.total_jobs_searched, 2)
        self.assertEqual(result.matches[0].job_id, "job1")  # Best match

    def test_similarity_threshold_filtering(self):
        """Test that matches below threshold are filtered"""
        matcher = JobMatcher(similarity_threshold=0.9)
        candidate_emb = np.array([1.0, 0.0])

        job_embeddings = [
            (
                "job1",
                np.array([0.5, 0.5]),
                {  # Lower similarity
                    "title": "Job 1",
                    "company": "Company 1",
                    "location": "Remote",
                    "skills": [],
                },
            )
        ]

        result = matcher.find_matches(candidate_emb, job_embeddings, top_k=10)

        self.assertEqual(len(result.matches), 0)  # No matches above threshold

    def test_location_filtering(self):
        """Test location-based filtering"""
        candidate_emb = np.array([1.0, 1.0])

        job_embeddings = [
            (
                "job1",
                np.array([1.0, 1.0]),
                {
                    "title": "Job 1",
                    "company": "Company 1",
                    "location": "Greenville, SC",
                    "remote_option": False,
                    "skills": [],
                },
            ),
            (
                "job2",
                np.array([1.0, 1.0]),
                {
                    "title": "Job 2",
                    "company": "Company 2",
                    "location": "NYC",
                    "remote_option": False,
                    "skills": [],
                },
            ),
            (
                "job3",
                np.array([1.0, 1.0]),
                {
                    "title": "Job 3",
                    "company": "Company 3",
                    "location": "Remote",
                    "remote_option": True,
                    "skills": [],
                },
            ),
        ]

        result = self.matcher.find_matches(
            candidate_emb, job_embeddings, top_k=10, location_filter="Greenville, SC"
        )

        # Should match Greenville job and remote jobs
        self.assertGreaterEqual(len(result.matches), 2)
        locations = {m.location for m in result.matches}
        self.assertIn("Greenville, SC", locations)

    def test_salary_filtering(self):
        """Test salary-based filtering"""
        candidate_emb = np.array([1.0, 1.0])

        job_embeddings = [
            (
                "job1",
                np.array([1.0, 1.0]),
                {
                    "title": "Junior Role",
                    "company": "Company 1",
                    "location": "Remote",
                    "salary_range": "$80K-$100K",
                    "skills": [],
                },
            ),
            (
                "job2",
                np.array([1.0, 1.0]),
                {
                    "title": "Senior Role",
                    "company": "Company 2",
                    "location": "Remote",
                    "salary_range": "$150K-$180K",
                    "skills": [],
                },
            ),
        ]

        result = self.matcher.find_matches(
            candidate_emb, job_embeddings, top_k=10, salary_min=120000
        )

        self.assertEqual(len(result.matches), 1)
        self.assertEqual(result.matches[0].job_title, "Senior Role")

    def test_top_k_limiting(self):
        """Test top K match limiting"""
        candidate_emb = np.array([1.0, 1.0])

        # Create 10 jobs with same similarity
        job_embeddings = [
            (
                f"job{i}",
                np.array([1.0, 1.0]),
                {
                    "title": f"Job {i}",
                    "company": f"Company {i}",
                    "location": "Remote",
                    "skills": [],
                },
            )
            for i in range(10)
        ]

        result = self.matcher.find_matches(candidate_emb, job_embeddings, top_k=5)

        self.assertEqual(len(result.matches), 5)

    def test_veteran_friendly_boosting(self):
        """Test veteran-friendly employer score boosting"""
        matches = [
            JobMatch(
                job_id="job1",
                job_title="Job 1",
                company="Company 1",
                location="Remote",
                similarity_score=0.7,
                matching_skills=[],
                veteran_friendly=False,
            ),
            JobMatch(
                job_id="job2",
                job_title="Job 2",
                company="Company 2",
                location="Remote",
                similarity_score=0.7,
                matching_skills=[],
                veteran_friendly=True,
            ),
        ]

        boosted = self.matcher.rank_by_veteran_preference(matches)

        # Veteran-friendly should now be ranked higher
        self.assertTrue(boosted[0].veteran_friendly)
        self.assertGreater(boosted[0].similarity_score, 0.7)

    def test_batch_matching(self):
        """Test batch candidate matching"""
        candidate_embeddings = [
            ("candidate1", np.array([1.0, 0.0])),
            ("candidate2", np.array([0.0, 1.0])),
        ]

        job_embeddings = [
            (
                "job1",
                np.array([1.0, 0.0]),
                {"title": "Job 1", "company": "Company 1", "location": "Remote", "skills": []},
            )
        ]

        results = self.matcher.batch_match(candidate_embeddings, job_embeddings, top_k=5)

        self.assertEqual(len(results), 2)
        self.assertIn("candidate1", results)
        self.assertIn("candidate2", results)
        # Candidate1 should have higher similarity to job1
        self.assertGreater(
            results["candidate1"].avg_similarity, results["candidate2"].avg_similarity
        )

    def test_salary_extraction(self):
        """Test salary range extraction logic"""
        test_cases = [
            ("$120K-$180K", 120000),
            ("$150,000-$200,000", 150000),
            ("$100K", 100000),
            ("Invalid", None),
        ]

        for salary_str, expected_min in test_cases:
            result = self.matcher._extract_min_salary(salary_str)
            self.assertEqual(result, expected_min)


if __name__ == "__main__":
    unittest.main()
