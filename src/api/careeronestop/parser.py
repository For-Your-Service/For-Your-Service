"""
CareerOneStop Response Parser
"""

from typing import Dict, List


class CareerOneStopParser:
    """Parser for CareerOneStop API responses"""

    @staticmethod
    def parse_veteran_employers(raw_response: Dict) -> List[Dict]:
        """Parse veteran-friendly employers"""
        employers = []
        for emp in raw_response.get("VeteranEmployerList", []):
            employers.append(
                {
                    "company_name": emp.get("CompanyName"),
                    "city": emp.get("City"),
                    "state": emp.get("StateCode"),
                    "distance": emp.get("Distance"),
                    "description": emp.get("Description"),
                    "is_veteran_friendly": True,
                }
            )
        return employers

    @staticmethod
    def parse_training_programs(raw_response: Dict) -> List[Dict]:
        """Parse training programs"""
        programs = []
        for prog in raw_response.get("Programs", []):
            programs.append(
                {
                    "school_name": prog.get("SchoolName"),
                    "program_name": prog.get("ProgramName"),
                    "credential": prog.get("Credential"),
                    "cost": prog.get("Cost"),
                    "length": prog.get("Length"),
                    "city": prog.get("City"),
                    "state": prog.get("StateCode"),
                }
            )
        return programs
