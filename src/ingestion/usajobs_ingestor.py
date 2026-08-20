"""
File: src/ingestion/usajobs_ingestor.py
Description: Production USAJOBS API Ingestor for Bronze Layer (workspace.fys_bronze.job_postings)
Lead Architect: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any


class USAJobsIngestor:
    """Ingest live federal job postings from USAJOBS API into Medallion Bronze Layer"""

    BASE_URL = "https://data.usajobs.gov/api/search"

    def __init__(
        self,
        api_key: Optional[str] = None,
        email: Optional[str] = None
    ):
        self.api_key = api_key or os.getenv("USAJOBS_API_KEY")
        self.email = email or os.getenv("USAJOBS_EMAIL", "whall4.wh@gmail.com")
        
        if not self.api_key:
            print("[!] WARNING: USAJOBS_API_KEY is not set. API calls will require an active key.")

    def _get_headers(self) -> Dict[str, str]:
        """Construct mandated USAJOBS API headers"""
        return {
            "Host": "data.usajobs.gov",
            "User-Agent": self.email,
            "Authorization-Key": self.api_key or ""
        }

    def fetch_jobs(
        self,
        keyword: str = "Information Technology",
        location: Optional[str] = None,
        radius: int = 50,
        results_per_page: int = 25,
        page: int = 1,
        hiring_path: str = "vet"  # Defaults to Veterans' Preference
    ) -> Optional[Dict[str, Any]]:
        """
        Fetch live job postings from USAJOBS API
        
        Args:
            keyword: Job title or skill keywords
            location: City, State or Zip (e.g. 'Greenville, SC')
            radius: Search radius in miles
            results_per_page: Batch size (1-500)
            page: Pagination index
            hiring_path: Filter by hiring path ('vet', 'fed', 'public', etc.)
            
        Returns:
            JSON response payload or None on error
        """
        params = {
            "Keyword": keyword,
            "ResultsPerPage": str(results_per_page),
            "Page": str(page)
        }
        
        if location:
            params["LocationName"] = location
            params["Radius"] = str(radius)
            
        if hiring_path:
            params["HiringPath"] = hiring_path

        try:
            print(f"[*] Querying USAJOBS API: Keyword='{keyword}', Location='{location or 'Nationwide'}' (Page {page})...")
            response = requests.get(
                self.BASE_URL,
                headers=self._get_headers(),
                params=params,
                timeout=15
            )
            
            print(f"[{response.status_code}] USAJOBS Search API Response")
            
            if response.status_code == 200:
                data = response.json()
                items = data.get("SearchResult", {}).get("SearchResultItems", [])
                total_count = data.get("SearchResult", {}).get("SearchResultCountAll", len(items))
                print(f" [OK] Successfully fetched {len(items)} jobs (Total Available: {total_count})")
                return data
            elif response.status_code == 401:
                print(" [ERROR 401] Unauthorized: Invalid or missing USAJOBS_API_KEY / User-Agent.")
            elif response.status_code == 429:
                print(" [ERROR 429] Rate Limit Exceeded (USAJOBS allows up to 250 requests/day).")
            else:
                print(f" [ERROR {response.status_code}] {response.text}")
                
            return None
            
        except requests.exceptions.RequestException as e:
            print(f"[!] Network / Request Error: {e}")
            return None

    def transform_to_bronze(self, raw_items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Transform raw USAJOBS search items into workspace.fys_bronze.job_postings schema
        """
        bronze_records = []
        now_ts = datetime.now()
        
        for item in raw_items:
            descriptor = item.get("MatchedObjectDescriptor", {})
            position_id = item.get("MatchedObjectId") or descriptor.get("PositionID", "unknown")
            
            # Extract compensation
            remuneration = descriptor.get("PositionRemuneration", [{}])
            sal_min = 0.0
            sal_max = 0.0
            if remuneration:
                try:
                    sal_min = float(remuneration[0].get("MinimumRange", 0.0) or 0.0)
                    sal_max = float(remuneration[0].get("MaximumRange", 0.0) or 0.0)
                except (ValueError, TypeError):
                    sal_min, sal_max = 0.0, 0.0
                    
            # Extract location
            locations = descriptor.get("PositionLocation", [{}])
            loc_display = descriptor.get("PositionLocationDisplay")
            if not loc_display and locations:
                loc_display = locations[0].get("LocationName", "United States")
                
            # Extract clearance
            clearance_code = descriptor.get("UserArea", {}).get("Details", {}).get("SecurityClearance", "None")

            record = {
                "job_id": f"usajobs_{position_id}",
                "source": "usajobs",
                "raw_json": json.dumps(item),
                "title": descriptor.get("PositionTitle", "Untitled Role"),
                "company": descriptor.get("OrganizationName", descriptor.get("DepartmentName", "Federal Agency")),
                "description": descriptor.get("UserArea", {}).get("Details", {}).get("JobSummary", ""),
                "location": loc_display or "United States",
                "salary_min": sal_min,
                "salary_max": sal_max,
                "clearance_required": clearance_code,
                "application_url": descriptor.get("PositionURI", ""),
                "posted_date": descriptor.get("PublicationStartDate"),
                "fetched_at": now_ts.isoformat(),
                "ingestion_date": now_ts.strftime("%Y-%m-%d")
            }
            bronze_records.append(record)
            
        return bronze_records
