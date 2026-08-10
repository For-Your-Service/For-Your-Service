#!/bin/bash
# Example API requests for For Your Service
# Organization: 7 Eagle Group

# Base URL (update after deployment)
API_BASE="https://huggingface.co/spaces/7eaglegroup/for-your-service"

echo "==================================="
echo "For Your Service - API Examples"
echo "==================================="

# 1. Register Veteran Profile
echo ""
echo "1. Register Veteran Profile"
curl -X POST "$API_BASE/veteran/register" \
  -H "Content-Type: application/json" \
  -d @examples/veteran_profile_example.json

# 2. Get Job Matches
echo ""
echo "2. Get Job Matches for Veteran"
curl -X POST "$API_BASE/match" \
  -H "Content-Type: application/json" \
  -d '{
    "veteran_id": "vet_12345",
    "top_k": 10,
    "min_score": 0.7
  }'

# 3. Search Jobs
echo ""
echo "3. Search Jobs by Keywords"
curl -X GET "$API_BASE/jobs/search?keywords=devops+engineer&location=Greenville,SC&radius=50"

# 4. Get Veteran Profile
echo ""
echo "4. Retrieve Veteran Profile"
curl -X GET "$API_BASE/veteran/vet_12345"

# 5. Update Veteran Preferences
echo ""
echo "5. Update Veteran Preferences"
curl -X PATCH "$API_BASE/veteran/vet_12345/preferences" \
  -H "Content-Type: application/json" \
  -d '{
    "desired_salary": {"min": 125000, "max": 185000},
    "remote_preference": "remote"
  }'

echo ""
echo "==================================="
