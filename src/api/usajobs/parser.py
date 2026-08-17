"""
USAJobs API Response Parser
Transforms raw API responses into structured data for Bronze layer
"""

from typing import Dict, List, Optional
import re


class USAJobsParser:
    """Parser for USAJobs API responses"""

    @staticmethod
    def parse_salary(remuneration_list: List[Dict]) -> Dict[str, Optional[float]]:
        """Extract salary range from remuneration data"""
        if not remuneration_list:
            return {"min_salary": None, "max_salary": None, "pay_period": None}

        renum = remuneration_list[0]
        min_str = renum.get("MinimumRange", "0")
        max_str = renum.get("MaximumRange", "0")

        # Remove $ and , from salary strings
        min_salary = float(re.sub(r"[$,]", "", min_str))
        max_salary = float(re.sub(r"[$,]", "", max_str))
        pay_period = renum.get("RateIntervalCode", "PA")

        return {
            "min_salary": min_salary if min_salary > 0 else None,
            "max_salary": max_salary if max_salary > 0 else None,
            "pay_period": pay_period,
        }
