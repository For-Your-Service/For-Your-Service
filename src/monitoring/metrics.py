"""Prometheus metrics."""
from prometheus_client import Counter, Histogram

resume_parse_count = Counter('resume_parse_total', 'Total resumes parsed')
resume_parse_duration = Histogram('resume_parse_duration_seconds', 'Resume parse time')

match_request_count = Counter('match_request_total', 'Total match requests')
match_duration = Histogram('match_duration_seconds', 'Match request time')
