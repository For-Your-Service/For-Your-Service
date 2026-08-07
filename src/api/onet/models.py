"""
O*NET API Data Models
"""
from pydantic import BaseModel
from typing import List, Optional


class ONetOccupation(BaseModel):
    """O*NET occupation profile"""
    code: str
    title: str
    description: str
    tags: Optional[dict] = None


class Skill(BaseModel):
    """Skill requirement"""
    name: str
    level: dict
    

class ONetSkillsResponse(BaseModel):
    """O*NET skills response"""
    occupation: str
    skill: List[Skill]
