"""
Indeed Job Scraper and Ingestion Utilities
"""

import requests


def normalize_location(location_str: str) -> str:
    """Normalize location string to 'City, ST' format"""
    if not location_str:
        return ""
    parts = [p.strip() for p in location_str.split(",")]
    if len(parts) == 2:
        city = parts[0].title()
        state = parts[1].upper() if len(parts[1]) == 2 else parts[1].title()
        return f"{city}, {state}"
    return location_str.strip().title()


def parse_job_response(response_data: dict, source: str = "indeed") -> list:
    """Parse API response into structured job dicts"""
    results = response_data.get("results", [])
    jobs = []
    for item in results:
        job_id = item.get("jobkey", item.get("id", ""))
        jobs.append(
            {
                "job_id": f"{source}_{job_id}" if job_id else f"{source}_unknown",
                "title": item.get("jobtitle", item.get("title", "")),
                "company": item.get("company", ""),
                "location": normalize_location(
                    item.get("formattedLocation", item.get("location", ""))
                ),
                "snippet": item.get("snippet", ""),
                "date": item.get("date", ""),
                "data_source": source,
            }
        )
    return jobs


def fetch_indeed_jobs(query: str, location: str = "") -> list:
    """Fetch jobs from Indeed API"""
    url = "https://api.indeed.com/ads/apisearch"
    params = {"q": query, "l": location, "format": "json", "v": "2"}
    response = requests.get(url, params=params)
    if response.status_code == 429:
        raise Exception(
            f"Rate limited: Retry-After {response.headers.get('Retry-After', 'unknown')}"
        )
    if response.status_code != 200:
        raise Exception(f"Indeed API error {response.status_code}")
    data = response.json()
    return parse_job_response(data, source="indeed")
