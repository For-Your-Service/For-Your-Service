"""
BLS API Data Models
"""
from pydantic import BaseModel
from typing import List, Optional


class DataPoint(BaseModel):
    """BLS time series data point"""
    year: str
    period: str
    periodName: str
    value: str
    
    
class Series(BaseModel):
    """BLS time series"""
    seriesID: str
    data: List[DataPoint]
    

class BLSResponse(BaseModel):
    """BLS API response"""
    status: str
    responseTime: int
    message: List[str]
    Results: dict
