"""
Selenium Indeed Scraper

Bypasses 403 blocks using headless Chrome automation.
Targets Greenville, SC + Remote jobs for veterans.

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import logging
from typing import List, Dict, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)


class SeleniumIndeedScraper:
    """Scrape Indeed.com using Selenium (bypasses 403 errors)"""

    BASE_URL = "https://www.indeed.com"

    def __init__(self, headless: bool = True, delay_seconds: float = 2.0):
        """
        Initialize Selenium scraper

        Args:
            headless: Run Chrome in headless mode
            delay_seconds: Delay between requests
        """
        self.headless = headless
        self.delay = delay_seconds
        self.driver = None

    def _init_driver(self):
        """Initialize Chrome WebDriver"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")

        # Anti-detection measures
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Auto-download ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Remove webdriver property (anti-detection)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )

        logger.info("Chrome WebDriver initialized")

    def search_jobs(
        self,
        keywords: str = "DevOps Engineer",
        location: str = "Greenville, SC",
        max_results: int = 25,
        max_pages: int = 3,
    ) -> List[Dict]:
        """
        Search Indeed for jobs

        Args:
            keywords: Job search keywords
            location: Target location
            max_results: Maximum jobs to return
            max_pages: Maximum pages to scrape

        Returns:
            List of normalized job dictionaries
        """
        if not self.driver:
            self._init_driver()

        jobs = []

        try:
            # Build search URL
            search_url = f"{self.BASE_URL}/jobs"
            params = f"?q={keywords.replace(' ', '+')}&l={location.replace(' ', '+')}&sort=date"
            full_url = search_url + params

            logger.info(f"Scraping: {full_url}")

            for page in range(max_pages):
                if page > 0:
                    # Add pagination
                    page_url = full_url + f"&start={page * 10}"
                else:
                    page_url = full_url

                self.driver.get(page_url)

                # Wait for job cards to load
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "job_seen_beacon"))
                    )
                except Exception:
                    logger.warning(f"Timeout waiting for jobs on page {page+1}")
                    break

                # Parse page
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                job_cards = soup.find_all("div", class_=re.compile(r"job_seen_beacon"))

                logger.info(f"Page {page+1}: Found {len(job_cards)} job cards")

                for card in job_cards:
                    if len(jobs) >= max_results:
                        break

                    job = self._parse_job_card(card)
                    if job:
                        jobs.append(job)

                if len(jobs) >= max_results:
                    break

                # Rate limiting
                time.sleep(self.delay)

        except Exception as e:
            logger.error(f"Error scraping Indeed: {e}")

        finally:
            if self.driver:
                self.driver.quit()
                self.driver = None

        return jobs

    def search_multiple_locations(
        self, keywords_list: List[str], locations: List[str], max_per_search: int = 10
    ) -> List[Dict]:
        """
        Search multiple keywords and locations

        Args:
            keywords_list: List of job titles to search
            locations: List of target locations
            max_per_search: Max jobs per search

        Returns:
            Deduplicated list of jobs
        """
        all_jobs = []

        for keywords in keywords_list:
            for location in locations:
                logger.info(f"Searching: {keywords} in {location}")

                jobs = self.search_jobs(
                    keywords=keywords, location=location, max_results=max_per_search, max_pages=2
                )

                all_jobs.extend(jobs)

                # Delay between searches
                time.sleep(self.delay)

        # Deduplicate by job_id
        seen_ids = set()
        unique_jobs = []
        for job in all_jobs:
            job_id = job.get("job_id")
            if job_id not in seen_ids:
                seen_ids.add(job_id)
                unique_jobs.append(job)

        return unique_jobs

    def _parse_job_card(self, card) -> Optional[Dict]:
        """Parse a single job card"""
        try:
            # Title
            title_elem = card.find("h2", class_="jobTitle")
            if title_elem:
                title_span = title_elem.find("span")
                title = (
                    title_span.get_text(strip=True)
                    if title_span
                    else title_elem.get_text(strip=True)
                )
            else:
                title = "Unknown"

            # Company
            company_elem = card.find("span", class_="companyName")
            company = company_elem.get_text(strip=True) if company_elem else "Unknown"

            # Location
            location_elem = card.find("div", class_="companyLocation")
            location = location_elem.get_text(strip=True) if location_elem else "Unknown"

            # Salary
            salary_elem = card.find("div", class_="salary-snippet")
            salary_text = salary_elem.get_text(strip=True) if salary_elem else ""
            salary_min, salary_max = self._parse_salary(salary_text)

            # Snippet/Description
            snippet_elem = card.find("div", class_="job-snippet")
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

            # Job URL
            link_elem = card.find("a", class_="jcs-JobTitle")
            job_url = ""
            job_id = ""
            if link_elem and link_elem.get("href"):
                job_url = self.BASE_URL + link_elem["href"]
                if "jk=" in job_url:
                    job_id = job_url.split("jk=")[1].split("&")[0]

            if not job_id:
                job_id = f"indeed_{hash(title + company)}"

            return {
                "job_id": job_id,
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
                "data_source": "indeed_selenium",
                "url": job_url,
            }

        except Exception as e:
            logger.error(f"Error parsing job card: {e}")
            return None

    def _parse_salary(self, salary_text: str) -> tuple:
        """Extract salary range"""
        if not salary_text:
            return (0, 0)

        numbers = re.findall(r"\$?([\d,]+)", salary_text)

        if len(numbers) >= 2:
            try:
                min_sal = int(numbers[0].replace(",", ""))
                max_sal = int(numbers[1].replace(",", ""))

                # Handle hourly conversion (rough estimate)
                if "hour" in salary_text.lower():
                    min_sal = min_sal * 2080  # 40 hrs/week * 52 weeks
                    max_sal = max_sal * 2080

                return (min_sal, max_sal)
            except ValueError:
                pass
        elif len(numbers) == 1:
            try:
                sal = int(numbers[0].replace(",", ""))
                if "hour" in salary_text.lower():
                    sal = sal * 2080
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
            "aws",
            "azure",
            "gcp",
            "kubernetes",
            "k8s",
            "docker",
            "terraform",
            "ansible",
            "jenkins",
            "python",
            "java",
            "linux",
            "windows",
            "networking",
            "security",
            "ci/cd",
            "devops",
            "cloud",
            "scripting",
            "automation",
            "monitoring",
            "databricks",
            "spark",
            "pyspark",
            "sql",
            "git",
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
        """Detect work arrangement"""
        text = (description + " " + location).lower()

        if "remote" in text:
            if "hybrid" in text:
                return "Hybrid"
            return "Remote"
        return "Onsite"

    def _check_clearance(self, text: str) -> Optional[str]:
        """Check for security clearance"""
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
        """Check for veteran-friendly indicators"""
        if not text:
            return False

        text_lower = text.lower()
        keywords = ["veteran", "military", "vets welcome", "gi bill"]

        return any(kw in text_lower for kw in keywords)

    def __del__(self):
        """Cleanup driver on deletion"""
        if self.driver:
            try:
                self.driver.quit()
            except Exception:
                pass
