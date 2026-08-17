#!/usr/bin/env python3
"""O*NET skill extraction utility"""

import requests


class OnetSkillExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://services.onetcenter.org/ws/online"

    def search_occupation(self, keyword):
        """Search for O*NET occupation by keyword"""
        url = f"{self.base_url}/search"
        params = {"keyword": keyword}
        headers = {"Authorization": f"Basic {self.api_key}"}

        response = requests.get(url, params=params, headers=headers)
        return response.json()

    def get_skills(self, onet_code):
        """Get skills for an O*NET occupation"""
        url = f"{self.base_url}/occupations/{onet_code}/skills"
        headers = {"Authorization": f"Basic {self.api_key}"}

        response = requests.get(url, headers=headers)
        return response.json()


if __name__ == "__main__":
    print("O*NET Skill Extractor")
    print("Load API key from environment or Databricks Secrets")
