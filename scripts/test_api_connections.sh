#!/bin/bash
# Test API connections for all job board providers

set -e

echo "=========================================="
echo "Testing API Connections"
echo "=========================================="

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# Test Indeed API
echo -e "\n🔍 Testing Indeed API..."
curl -s -w "\nHTTP Status: %{http_code}\n" \
    "https://api.indeed.com/ads/apisearch?publisher=${INDEED_API_KEY}&q=test&l=test&format=json&limit=1" \
    | head -n 5

# Test USAJobs API
echo -e "\n🏛️  Testing USAJobs API..."
curl -s -w "\nHTTP Status: %{http_code}\n" \
    -H "Host: data.usajobs.gov" \
    -H "User-Agent: ${USAJOBS_EMAIL}" \
    "https://data.usajobs.gov/api/search?Keyword=engineer&ResultsPerPage=1" \
    | head -n 5

# Test Monster API
echo -e "\n👾 Testing Monster API..."
curl -s -w "\nHTTP Status: %{http_code}\n" \
    -H "Authorization: Bearer ${MONSTER_API_KEY}" \
    "https://api.monster.com/v2/jobs/search?q=test&location=test&page=1" \
    | head -n 5

echo -e "\n=========================================="
echo "✅ API connection tests complete"
echo "=========================================="
