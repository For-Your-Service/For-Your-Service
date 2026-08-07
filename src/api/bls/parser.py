"""
BLS Response Parser
"""
from typing import Dict, List
from datetime import datetime


class BLSParser:
    """Parser for BLS API responses"""
    
    @staticmethod
    def parse_wage_data(raw_response: Dict, soc_code: str) -> Dict:
        """Parse BLS wage data"""
        results = raw_response.get("Results", {})
        series_list = results.get("series", [])
        
        if not series_list:
            return {"soc_code": soc_code, "data_points": []}
        
        series = series_list[0]
        data_points = []
        
        for point in series.get("data", []):
            data_points.append({
                "year": point.get("year"),
                "period": point.get("period"),
                "period_name": point.get("periodName"),
                "value": float(point.get("value", 0)),
                "footnotes": point.get("footnotes", [])
            })
        
        return {
            "soc_code": soc_code,
            "series_id": series.get("seriesID"),
            "data_points": data_points,
            "fetched_at": datetime.utcnow().isoformat()
        }
