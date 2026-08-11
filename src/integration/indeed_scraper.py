"""
Indeed Job Scraper

Scrapes real job postings from Indeed.com (no API key required).
Ethical scraping with rate limiting and user-agent.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Optional
from datetime import datetime
import logging
import re


logger = logging.getLogger(__name__)


class IndeedScraper:
    """Scrape job listings from Indeed.com"""
    
    BASE_URL = "https://www.indeed.com"
    
    def __init__(self, delay_seconds: float = 2.0):
        """
        Initialize Indeed scraper
        
        Args:
            delay_seconds: Delay between requests (be respectful)
        """
        self.delay = delay_seconds
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        })
    
    def search_jobs(
        self,
        keywords: str = "DevOps Engineer",
        location: str = "Greenville, SC",
        max_results: int = 25
    ) -> List[Dict]:
        """
        Search for jobs on Indeed
        
        Args:
            keywords: Job search keywords
            location: Location filter
            max_results: Maximum number of jobs to return
            
        Returns:
            List of normalized job dictionaries
        """
        jobs = []
        
        # Build search URL
        params = {
            "q": keywords,
            "l": location,
            "sort": "date",  # Most recent first
            "vjk": "",  # View job key
        }
        
        try:
            # Construct URL
            search_url = f"{self.BASE_URL}/jobs"
            response = self.session.get(search_url, params=params, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find job cards
            job_cards = soup.find_all('div', class_=re.compile(r'job_seen_beacon'))
            
            logger.info(f"Found {len(job_cards)} job cards for '{keywords}'")
            
            for card in job_cards[:max_results]:
                job = self._parse_job_card(card)
                if job:
                    jobs.append(job)
                
                # Rate limiting
                time.sleep(self.delay)
            
        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")
        
        return jobs
    
    def _parse_job_card(self, card) -> Optional[Dict]:
        """
        Parse a single job card
        
        Args:
            card: BeautifulSoup job card element
            
        Returns:
            Normalized job dictionary or None
        """
        try:
            # Extract title
            title_elem = card.find('h2', class_='jobTitle')
            title = title_elem.get_text(strip=True) if title_elem else "Unknown"
            
            # Extract company
            company_elem = card.find('span', class_='companyName')
            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
            
            # Extract location
            location_elem = card.find('div', class_='companyLocation')
            location = location_elem.get_text(strip=True) if location_elem else "Unknown"
            
            # Extract salary (if available)
            salary_elem = card.find('div', class_='salary-snippet')
            salary_text = salary_elem.get_text(strip=True) if salary_elem else ""
            salary_min, salary_max = self._parse_salary(salary_text)
            
            # Extract snippet
            snippet_elem = card.find('div', class_='job-snippet')
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""
            
            # Extract job URL
            link_elem = card.find('a', class_='jcs-JobTitle')
            job_url = ""
            if link_elem and link_elem.get('href'):
                job_url = self.BASE_URL + link_elem['href']
            
            # Extract job ID from URL
            job_id = ""
            if 'jk=' in job_url:
                job_id = job_url.split('jk=')[1].split('&')[0]
            
            return {
                "job_id": job_id or f"indeed_{hash(title + company)}",
                "title": title,
                "company": company,
                "location": location,
                "description": snippet,
                "required_skills": self._extract_skills(snippet),
                "salary_min": salary_min,
                "salary_max": salary_max,
                "salary_range": salary_text if salary_text else "Not specified",
                "remote": self._detect_remote(snippet, location),
                "clearance_required": self._check_clearance(snippet),
                "veteran_friendly": self._check_veteran_friendly(snippet),
                "posted_date": datetime.now().isoformat(),
                "data_source": "indeed",
                "url": job_url
            }
            
        except Exception as e:
            logger.error(f"Error parsing job card: {e}")
            return None
    
    def _parse_salary(self, salary_text: str) -> tuple:
        """Extract min and max salary from text"""
        if not salary_text:
            return (0, 0)
        
        # Remove non-numeric characters except commas, periods, and hyphens
        numbers = re.findall(r'\$?([\d,]+)', salary_text)
        
        if len(numbers) >= 2:
            try:
                min_sal = int(numbers[0].replace(',', ''))
                max_sal = int(numbers[1].replace(',', ''))
                return (min_sal, max_sal)
            except ValueError:
                pass
        elif len(numbers) == 1:
            try:
                sal = int(numbers[0].replace(',', ''))
                return (sal, sal)
            except ValueError:
                pass
        
        return (0, 0)
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        
        skill_keywords = {
            "aws", "azure", "gcp", "kubernetes", "k8s", "docker",
            "terraform", "ansible", "jenkins", "python", "java",
            "linux", "windows", "networking", "security", "ci/cd",
            "devops", "cloud", "scripting", "automation", "monitoring",
            "databricks", "spark", "sql", "git"
        }
        
        found_skills = []
        for skill in skill_keywords:
            if skill in text_lower:
                if skill == "aws":
                    found_skills.append("AWS")
                elif skill == "k8s":
                    found_skills.append("Kubernetes")
                elif skill == "ci/cd":
                    found_skills.append("CI/CD")
                else:
                    found_skills.append(skill.title())
        
        return found_skills
    
    def _detect_remote(self, description: str, location: str) -> str:
        """Detect if job is remote/hybrid/onsite"""
        text = (description + " " + location).lower()
        
        if "remote" in text:
            if "hybrid" in text:
                return "Hybrid"
            return "Remote"
        return "Onsite"
    
    def _check_clearance(self, text: str) -> Optional[str]:
        """Check for security clearance requirements"""
        if not text:
            return None
        
        text_lower = text.lower()
        
        if "ts/sci" in text_lower or "top secret" in text_lower:
            return "TS/SCI"
        elif "secret clearance" in text_lower:
            return "Secret"
        elif "clearance" in text_lower:
            return "Required"
        
        return None
    
    def _check_veteran_friendly(self, text: str) -> bool:
        """Check if employer mentions veteran-friendly"""
        if not text:
            return False
        
        text_lower = text.lower()
        keywords = ["veteran", "military", "vets welcome", "gi bill"]
        
        return any(kw in text_lower for kw in keywords)
