"""
File: src/matching/matching_engine.py
Description: Dynamic Location-Driven Matching Engine for For Your Service
Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from typing import Dict, List, Optional
import pandas as pd


class DynamicLocationMatchingEngine:
    """
    Dynamic Search Driver: Ingests any candidate location payload at runtime
    to drive region-agnostic job database queries.
    """

    @staticmethod
    def filter_jobs_by_location(job_database: pd.DataFrame, candidate_input: Dict) -> pd.DataFrame:
        """
        Dynamically drive the search based entirely on the candidate's input.

        Args:
            job_database: DataFrame containing job postings
            candidate_input: Dictionary containing target_city, target_state, commute_radius_miles, remote_ok

        Returns:
            Filtered DataFrame of candidate jobs
        """
        target_city = candidate_input.get("target_city")
        target_state = candidate_input.get("target_state")
        commute_radius = candidate_input.get("commute_radius_miles", candidate_input.get("target_radius", 50))
        remote_ok = candidate_input.get("remote_ok", True)

        if job_database is None or len(job_database) == 0:
            return pd.DataFrame()

        if target_city and target_state:
            # Dynamically drive the search based entirely on the candidate's input
            city_mask = job_database["city"].astype(str).str.strip().str.lower() == str(target_city).strip().lower()
            state_mask = job_database["state"].astype(str).str.strip().str.upper() == str(target_state).strip().upper()
            loc_match = city_mask & state_mask

            if remote_ok and "remote_allowed" in job_database.columns:
                return job_database[loc_match | (job_database["remote_allowed"] == True)]
            elif remote_ok and "remote_option" in job_database.columns:
                return job_database[loc_match | (job_database["remote_option"] == True)]
            return job_database[loc_match]
        else:
            # Fallback to remote or nationwide if no specific location is provided
            if "remote_allowed" in job_database.columns:
                return job_database[job_database["remote_allowed"] == True]
            elif "remote_option" in job_database.columns:
                return job_database[job_database["remote_option"] == True]
            return job_database
