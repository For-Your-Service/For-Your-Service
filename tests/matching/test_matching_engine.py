"""
Unit tests for DynamicLocationMatchingEngine
"""

import unittest
import pandas as pd
from src.matching.matching_engine import DynamicLocationMatchingEngine


class TestDynamicLocationMatchingEngine(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame([
            {"job_id": "1", "title": "DevOps Engineer", "city": "Dallas", "state": "TX", "remote_allowed": False},
            {"job_id": "2", "title": "Cloud Architect", "city": "Greenville", "state": "SC", "remote_allowed": False},
            {"job_id": "3", "title": "Full Stack Dev", "city": "Remote", "state": "US", "remote_allowed": True},
        ])

    def test_dynamic_location_filter_dallas(self):
        candidate = {"target_city": "Dallas", "target_state": "TX", "remote_ok": True}
        res = DynamicLocationMatchingEngine.filter_jobs_by_location(self.df, candidate)
        self.assertEqual(len(res), 2)
        cities = set(res["city"])
        self.assertIn("Dallas", cities)
        self.assertIn("Remote", cities)

    def test_dynamic_location_filter_no_remote(self):
        candidate = {"target_city": "Dallas", "target_state": "TX", "remote_ok": False}
        res = DynamicLocationMatchingEngine.filter_jobs_by_location(self.df, candidate)
        self.assertEqual(len(res), 1)
        self.assertEqual(res.iloc[0]["city"], "Dallas")

    def test_dynamic_location_fallback_remote(self):
        candidate = {"target_city": "", "target_state": "", "remote_ok": True}
        res = DynamicLocationMatchingEngine.filter_jobs_by_location(self.df, candidate)
        self.assertEqual(len(res), 1)
        self.assertEqual(res.iloc[0]["city"], "Remote")


if __name__ == "__main__":
    unittest.main()
