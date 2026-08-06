"""
Orchestrates data collection from multiple APIs
"""
from typing import List, Dict
import logging
from datetime import datetime

from src.api.usajobs.client import USAJobsClient
from src.api.adzuna.client import AdzunaClient
from src.api.bls.client import BLSClient
from src.api.onet.client import ONetClient
from src.api.careeronestop.client import CareerOneStopClient
from src.api.config import APIConfig
from src.api.rate_limiter import APIRateLimiters

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataOrchestrator:
    """Orchestrates data collection from multiple sources"""
    
    def __init__(self):
        """Initialize API clients with configuration"""
        self.config = APIConfig()
        self.clients = self._initialize_clients()
        
    def _initialize_clients(self) -> Dict:
        """Initialize all API clients"""
        clients = {}
        
        if self.config.USAJOBS_API_KEY:
            clients['usajobs'] = USAJobsClient(
                api_key=self.config.USAJOBS_API_KEY,
                user_agent=self.config.USAJOBS_USER_AGENT
            )
            
        if self.config.ADZUNA_APP_ID and self.config.ADZUNA_API_KEY:
            clients['adzuna'] = AdzunaClient(
                app_id=self.config.ADZUNA_APP_ID,
                api_key=self.config.ADZUNA_API_KEY
            )
            
        if self.config.BLS_API_KEY:
            clients['bls'] = BLSClient(api_key=self.config.BLS_API_KEY)
            
        if self.config.ONET_API_KEY:
            clients['onet'] = ONetClient(username=self.config.ONET_USERNAME)
            
        if self.config.CAREERONESTOP_USER_ID:
            clients['careeronestop'] = CareerOneStopClient(
                user_id=self.config.CAREERONESTOP_USER_ID,
                authorization_token=self.config.CAREERONESTOP_TOKEN
            )
            
        logger.info(f"Initialized {len(clients)} API clients")
        return clients
    
    def collect_job_postings(
        self,
        keywords: List[str],
        locations: List[str]
    ) -> List[Dict]:
        """
        Collect job postings from all configured sources
        
        Args:
            keywords: List of search keywords
            locations: List of locations to search
            
        Returns:
            List of normalized job postings
        """
        all_jobs = []
        
        for keyword in keywords:
            for location in locations:
                logger.info(f"Collecting: {keyword} in {location}")
                
                # USAJobs
                if 'usajobs' in self.clients:
                    APIRateLimiters.usajobs.wait_if_needed()
                    try:
                        jobs = self.clients['usajobs'].search_jobs(
                            keyword=keyword,
                            location=location
                        )
                        all_jobs.extend(jobs)
                        logger.info(f"  USAJobs: {len(jobs)} jobs")
                    except Exception as e:
                        logger.error(f"USAJobs error: {e}")
                
                # Adzuna
                if 'adzuna' in self.clients:
                    APIRateLimiters.adzuna.wait_if_needed()
                    try:
                        jobs = self.clients['adzuna'].search_jobs(
                            what=keyword,
                            where=location
                        )
                        all_jobs.extend(jobs)
                        logger.info(f"  Adzuna: {len(jobs)} jobs")
                    except Exception as e:
                        logger.error(f"Adzuna error: {e}")
        
        logger.info(f"Total jobs collected: {len(all_jobs)}")
        return all_jobs
