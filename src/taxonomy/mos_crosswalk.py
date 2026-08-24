"""
Military Occupational Specialty (MOS) to civilian skill crosswalk.

Maps Army/Marine/Air Force MOS codes to equivalent civilian technical skills.
"""

from typing import List, Dict


class MOSCrosswalk:
    """Translate military MOS codes to civilian skills."""
    
    # MOS → Civilian skill mappings
    MOS_SKILLS = {
        # IT/Communications
        '25B': ['network administration', 'cisco', 'routing', 'switching', 'it support'],
        '25U': ['radio communications', 'satellite communications', 'signal operations'],
        '25S': ['satellite communications', 'network security', 'encryption'],
        
        # Cyber/Intelligence
        '35T': ['military intelligence', 'signals intelligence', 'cyber operations'],
        '17C': ['cyber security', 'penetration testing', 'network defense', 'siem'],
        '35N': ['signals intelligence', 'data analysis', 'intelligence analysis'],
        
        # Aviation/Maintenance
        '15T': ['aviation maintenance', 'aircraft systems', 'troubleshooting'],
        '15Y': ['helicopter maintenance', 'rotor systems', 'flight operations'],
        
        # Logistics/Supply
        '92A': ['supply chain management', 'inventory management', 'logistics'],
        '88M': ['transportation', 'fleet management', 'route planning'],
        
        # Special Forces (18 Series)
        '18A': ['leadership', 'strategic planning', 'operations management'],
        '18B': ['weapons systems', 'tactical operations', 'team leadership'],
        '18C': ['communications', 'radio systems', 'field operations'],
        '18D': ['medical operations', 'field medicine', 'emergency response'],
        '18E': ['intelligence operations', 'threat assessment', 'cultural awareness'],
        '18F': ['intelligence analysis', 'information operations', 'analysis'],
        
        # Marine Corps
        '0671': ['data systems', 'network administration', 'computer systems'],
        '0689': ['cyber security', 'network defense', 'information assurance'],
        
        # Air Force
        '1D7X1': ['cyber operations', 'network security', 'system administration'],
        '3D1X1': ['network infrastructure', 'cisco', 'routing', 'switching'],
    }
    
    @classmethod
    def get_civilian_skills(cls, mos_code: str) -> List[str]:
        """
        Get civilian skill equivalents for MOS code.
        
        Args:
            mos_code: Military MOS code (e.g., '25B', '18A')
            
        Returns:
            List of equivalent civilian skills
        """
        return cls.MOS_SKILLS.get(mos_code.upper(), [])
    
    @classmethod
    def enrich_veteran_profile(cls, mos_codes: List[str]) -> List[str]:
        """
        Enrich veteran profile with all civilian skills from MOS history.
        
        Args:
            mos_codes: List of MOS codes from military service
            
        Returns:
            Deduplicated list of civilian skills
        """
        all_skills = []
        for mos in mos_codes:
            all_skills.extend(cls.get_civilian_skills(mos))
        
        return list(set(all_skills))
