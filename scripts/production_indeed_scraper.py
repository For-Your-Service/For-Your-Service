"""
Production Indeed Job Scraper

Fetches REAL job postings from Indeed.com using Playwright
NO MOCK DATA - Only real scraped job listings

Author: Free Hall <whall4.wh@gmail.com>
Organization: 7 Eagle Group
"""

import asyncio
import json
import re
from datetime import datetime
from typing import List, Dict
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


class ProductionIndeedScraper:
    """Scrape real jobs from Indeed.com"""
    
    def __init__(self, headless: bool = True):
        self.headless = headless
        self.base_url = "https://www.indeed.com"
    
    async def scrape_jobs(
        self,
        keywords: str = "DevOps Engineer",
        location: str = "Greenville, SC",
        max_jobs: int = 10
    ) -> List[Dict]:
        """
        Scrape REAL jobs from Indeed
        
        Args:
            keywords: Job search terms
            location: Target location
            max_jobs: Maximum jobs to scrape
            
        Returns:
            List of real job dictionaries
        """
        print(f"🌐 Launching browser for Indeed scraping...")
        print(f"   Keywords: {keywords}")
        print(f"   Location: {location}")
        print(f"   Target: {max_jobs} jobs")
        
        async with async_playwright() as p:
            # Launch Chromium
            browser = await p.chromium.launch(
                headless=self.headless,
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled'
                ]
            )
            
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = await context.new_page()
            await stealth_async(page)
            
            # Build search URL
            search_url = (
                f"{self.base_url}/jobs?"
                f"q={keywords.replace(' ', '+')}"
                f"&l={location.replace(' ', '+')}"
                f"&sort=date"
            )
            
            print(f"\n📡 Connecting to: {search_url}")
            
            try:
                await page.goto(search_url, wait_until='domcontentloaded', timeout=30000)
                await page.wait_for_timeout(3000)
                
                print(f"✓ Page loaded")
                
                # Extract job cards
                job_cards = await page.query_selector_all('div.job_seen_beacon')
                
                print(f"✓ Found {len(job_cards)} job listings")
                
                jobs = []
                
                for i, card in enumerate(job_cards[:max_jobs]):
                    try:
                        # Extract job details
                        title_elem = await card.query_selector('h2.jobTitle span[title]')
                        title = await title_elem.get_attribute('title') if title_elem else None
                        
                        company_elem = await card.query_selector('[data-testid="company-name"]')
                        company = await company_elem.inner_text() if company_elem else None
                        
                        location_elem = await card.query_selector('[data-testid="text-location"]')
                        job_location = await location_elem.inner_text() if location_elem else None
                        
                        # Get job link
                        link_elem = await card.query_selector('h2.jobTitle a')
                        job_url = None
                        if link_elem:
                            href = await link_elem.get_attribute('href')
                            if href:
                                job_url = f"{self.base_url}{href}" if href.startswith('/') else href
                        
                        # Salary (if available)
                        salary_elem = await card.query_selector('[data-testid="attribute_snippet_testid"]')
                        salary_text = await salary_elem.inner_text() if salary_elem else None
                        
                        # Job snippet/description
                        snippet_elem = await card.query_selector('[data-testid="job-snippet"]')
                        description = await snippet_elem.inner_text() if snippet_elem else ""
                        
                        if title and company:
                            job = {
                                "id": f"indeed_{i}_{datetime.now().strftime('%Y%m%d')}",
                                "title": title,
                                "company": {"display_name": company},
                                "location": {"display_name": job_location or location},
                                "description": description,
                                "salary_text": salary_text,
                                "redirect_url": job_url,
                                "created": datetime.now().isoformat(),
                                "source": "indeed_scraped",
                                "contract_type": "full_time",
                                "category": {"label": "IT Jobs"}
                            }
                            
                            jobs.append(job)
                            
                            print(f"\n   [{i+1}] {title}")
                            print(f"       Company: {company}")
                            print(f"       Location: {job_location or location}")
                            if salary_text:
                                print(f"       Salary: {salary_text}")
                        
                    except Exception as e:
                        print(f"   ⚠️  Error parsing job {i+1}: {e}")
                        continue
                
                await browser.close()
                
                print(f"\n✅ Scraped {len(jobs)} REAL jobs from Indeed")
                
                return jobs
                
            except Exception as e:
                print(f"❌ Scraping failed: {e}")
                await browser.close()
                return []


async def scrape_indeed_greenville():
    """Scrape DevOps jobs in Greenville, SC"""
    scraper = ProductionIndeedScraper(headless=True)
    
    jobs = await scraper.scrape_jobs(
        keywords="DevOps Engineer",
        location="Greenville, SC",
        max_jobs=5
    )
    
    return jobs


# Run the scraper
if __name__ == "__main__":
    jobs = asyncio.run(scrape_indeed_greenville())
    print(f"\nTotal jobs scraped: {len(jobs)}")
