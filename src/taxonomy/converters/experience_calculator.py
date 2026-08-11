"""Calculate experience duration."""
from datetime import datetime

def months_between(start_date: datetime, end_date: datetime) -> int:
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

def years_between(start_date: datetime, end_date: datetime) -> int:
    return months_between(start_date, end_date) // 12
