"""
Military Occupational Specialty (MOS) to civilian occupation mapping
"""
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class MOSMapper:
    """Maps MOS codes to O*NET civilian occupations"""
    
    # Sample MOS to O*NET mapping (Army example)
    MOS_TO_ONET = {
        # Cyber/IT
        "25B": ["15-1231.00", "15-1232.00"],  # IT Specialist
        "25D": ["15-1212.00"],  # Cyber Network Defender
        "17C": ["15-1212.00", "15-1299.08"],  # Cyber Operations Specialist
        
        # Intelligence
        "35F": ["33-3021.00", "19-3094.00"],  # Intelligence Analyst
        "35M": ["33-3021.06"],  # Human Intelligence Collector
        
        # Logistics
        "92A": ["13-1081.00"],  # Automated Logistical Specialist
        "92Y": ["43-5061.00"],  # Unit Supply Specialist
        
        # Medical
        "68W": ["29-2041.00", "31-9092.00"],  # Combat Medic
        "68P": ["29-2034.00"],  # Radiology Specialist
        
        # Engineering
        "12B": ["47-2061.00"],  # Combat Engineer
        "12N": ["17-3026.00"],  # Horizontal Construction Engineer
    }
    
    def get_civilian_occupations(self, mos_code: str) -> List[str]:
        """
        Get civilian O*NET codes for a military MOS
        
        Args:
            mos_code: Military MOS code (e.g., "25B")
            
        Returns:
            List of O*NET occupation codes
        """
        return self.MOS_TO_ONET.get(mos_code, [])
    
    def get_skills_from_mos(self, mos_code: str) -> List[str]:
        """
        Extract transferable skills from MOS
        
        Args:
            mos_code: Military MOS code
            
        Returns:
            List of skill keywords
        """
        # Simplified skill extraction
        skills_by_category = {
            "25B": ["networking", "cisco", "windows", "linux", "troubleshooting"],
            "25D": ["cybersecurity", "network defense", "incident response"],
            "17C": ["penetration testing", "malware analysis", "cryptography"],
            "35F": ["intelligence analysis", "geospatial intelligence", "data analysis"],
            "92A": ["supply chain", "logistics", "inventory management"],
            "68W": ["emergency medical", "patient care", "triage"]
        }
        
        return skills_by_category.get(mos_code, [])
