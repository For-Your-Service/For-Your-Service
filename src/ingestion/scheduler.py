"""
Scheduling logic for data ingestion
"""
from typing import List
import schedule
import time
import logging

logger = logging.getLogger(__name__)


class IngestionScheduler:
    """Schedules periodic data ingestion jobs"""
    
    def __init__(self, orchestrator, bronze_writer):
        """
        Initialize scheduler
        
        Args:
            orchestrator: DataOrchestrator instance
            bronze_writer: BronzeWriter instance
        """
        self.orchestrator = orchestrator
        self.bronze_writer = bronze_writer
        
    def daily_job_collection(self):
        """Daily collection of job postings"""
        logger.info("Running daily job collection")
        
        keywords = [
            "cybersecurity",
            "network engineer",
            "logistics",
            "healthcare"
        ]
        
        locations = [
            "California",
            "Texas",
            "Florida",
            "Virginia"
        ]
        
        jobs = self.orchestrator.collect_job_postings(keywords, locations)
        self.bronze_writer.write_job_postings(jobs)
        
        logger.info("Daily job collection complete")
    
    def schedule_jobs(self):
        """Set up scheduled jobs"""
        # Daily at 6 AM UTC
        schedule.every().day.at("06:00").do(self.daily_job_collection)
        
        logger.info("Scheduled jobs configured")
        
    def run(self):
        """Run the scheduler loop"""
        self.schedule_jobs()
        
        logger.info("Scheduler started")
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
