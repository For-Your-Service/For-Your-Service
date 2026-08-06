"""
CareerOneStop API Data Models
"""
from pydantic import BaseModel
from typing import List, Optional


class VeteranEmployer(BaseModel):
    """Veteran-friendly employer"""
    CompanyName: str
    City: str
    StateCode: str
    Distance: Optional[float] = None
    Description: Optional[str] = None
    

class TrainingProgram(BaseModel):
    """Training program"""
    SchoolName: str
    ProgramName: str
    Credential: Optional[str] = None
    Cost: Optional[str] = None
    Length: Optional[str] = None
