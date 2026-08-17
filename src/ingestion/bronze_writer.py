"""
Writes raw data to Bronze layer (Unity Catalog or Cloud Storage)
"""

from typing import List, Dict
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class BronzeWriter:
    """Writes raw data to Bronze layer"""

    def __init__(self, storage_path: str):
        """
        Initialize bronze writer

        Args:
            storage_path: GCS path or Unity Catalog table name
        """
        self.storage_path = storage_path

    def write_job_postings(self, jobs: List[Dict]) -> None:
        """
        Write job postings to bronze layer

        Args:
            jobs: List of job posting dictionaries
        """
        timestamp = datetime.utcnow().isoformat()

        for job in jobs:
            job["ingestion_timestamp"] = timestamp

        logger.info(f"Writing {len(jobs)} jobs to {self.storage_path}")

        # TODO: Implement actual write to Unity Catalog or GCS
        # For now, just log
        logger.info(f"  Would write to: {self.storage_path}")
