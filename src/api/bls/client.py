"""
BLS (Bureau of Labor Statistics) API Client
Official government wage and employment statistics
API Docs: https://www.bls.gov/developers/
"""

import requests
import json
from typing import Dict, List, Optional
from datetime import datetime


class BLSClient:
    """Client for Bureau of Labor Statistics API"""

    BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

    def __init__(self, api_key: str):
        """
        Initialize BLS API client

        Args:
            api_key: API key from data.bls.gov/registrationEngine/
        """
        self.api_key = api_key
        self.session = requests.Session()

    def get_series_data(
        self,
        series_ids: List[str],
        start_year: Optional[str] = None,
        end_year: Optional[str] = None,
        catalog: bool = False,
        calculations: bool = False,
        annual_averages: bool = False,
    ) -> Dict:
        """
        Get time series data for multiple series IDs

        Args:
            series_ids: List of BLS series IDs (max 50)
            start_year: Start year (YYYY format)
            end_year: End year (YYYY format)
            catalog: Include catalog metadata
            calculations: Include percent changes
            annual_averages: Include annual averages

        Returns:
            Dict containing time series data
        """
        if not start_year:
            start_year = str(datetime.now().year - 1)
        if not end_year:
            end_year = str(datetime.now().year)

        payload = {
            "seriesid": series_ids[:50],  # Max 50 series
            "startyear": start_year,
            "endyear": end_year,
            "registrationkey": self.api_key,
        }

        if catalog:
            payload["catalog"] = True
        if calculations:
            payload["calculations"] = True
        if annual_averages:
            payload["annualaverage"] = True

        headers = {"Content-type": "application/json"}

        response = self.session.post(
            self.BASE_URL, data=json.dumps(payload), headers=headers, timeout=30
        )
        response.raise_for_status()
        return response.json()

    def get_occupation_wages(
        self,
        soc_code: str,
        area_code: str = "0000000",  # National
        start_year: Optional[str] = None,
    ) -> Dict:
        """
        Get wage data for specific occupation

        Args:
            soc_code: SOC code (e.g., "15-1212" for Info Security Analysts)
            area_code: Area code (0000000=National, state FIPS, or MSA code)
            start_year: Start year for data

        Returns:
            Dict containing wage statistics
        """
        # Build OEWS series ID: OEUN + area + SOC code + data type
        # Example: OEUN000000015121203 = National, SOC 15-1212, Annual Mean Wage
        series_id = f"OEUN{area_code}{soc_code.replace('-', '')}03"

        return self.get_series_data([series_id], start_year=start_year)

    def get_employment_projections(self, soc_code: str, start_year: Optional[str] = None) -> Dict:
        """
        Get employment projections for occupation

        Args:
            soc_code: SOC code
            start_year: Start year

        Returns:
            Dict containing projection data
        """
        # Employment Projections series IDs
        series_id = f"EPU{soc_code.replace('-', '')}01"

        return self.get_series_data([series_id], start_year=start_year)

    def search_by_location(
        self, state_code: str, soc_codes: List[str], start_year: Optional[str] = None
    ) -> Dict:
        """
        Get wage data for multiple occupations in a state

        Args:
            state_code: 2-digit state FIPS code (e.g., "06" for CA)
            soc_codes: List of SOC codes
            start_year: Start year

        Returns:
            Dict with wage data for all occupations
        """
        # Build series IDs for state data
        series_ids = [f"OEUS{state_code}0000{soc.replace('-', '')}03" for soc in soc_codes]

        return self.get_series_data(series_ids, start_year=start_year)
