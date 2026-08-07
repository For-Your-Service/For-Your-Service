"""
Adzuna API Data Models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class Company(BaseModel):
    """Company information"""
    display_name: str


class Location(BaseModel):
    """Job location"""
    display_name: str
    area: List[str]


class AdzunaJob(BaseModel):
    """Adzuna job posting"""
    id: str
    title: str
    company: Company
    location: Location
    description: str
    created: str
    redirect_url: str
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    contract_time: Optional[str] = None
    contract_type: Optional[str] = None
    category: Optional[dict] = None
