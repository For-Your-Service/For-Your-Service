"""
O*NET Response Parser
"""
from typing import Dict, List
from datetime import datetime


class ONetParser:
    """Parser for O*NET API responses"""
    
    @staticmethod
    def parse_occupation(raw_occupation: Dict) -> Dict:
        """Parse O*NET occupation details"""
        return {
            "source": "onet",
            "onet_code": raw_occupation.get("code"),
            "title": raw_occupation.get("title"),
            "description": raw_occupation.get("description"),
            "tags": raw_occupation.get("tags", {}),
            "fetched_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def parse_skills(raw_skills: Dict) -> List[Dict]:
        """Parse O*NET skills response"""
        skills = []
        for skill in raw_skills.get("skill", []):
            skills.append({
                "name": skill.get("name"),
                "level": skill.get("level", {}).get("value"),
                "importance": skill.get("level", {}).get("importance")
            })
        return skills
