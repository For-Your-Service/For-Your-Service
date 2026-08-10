#!/bin/bash
# System health check script

echo "🏥 For Your Service - Health Check"
echo "===================================="
echo ""

# Check Databricks connectivity
echo "📊 Checking Databricks..."
if databricks workspace list &> /dev/null; then
    echo "✅ Databricks: Connected"
else
    echo "❌ Databricks: Connection failed"
fi

# Check tables exist
echo ""
echo "📋 Checking tables..."
tables=("workspace.fys_bronze.job_postings")
for table in "${tables[@]}"; do
    if databricks sql execute --statement "SELECT COUNT(*) FROM $table LIMIT 1" &> /dev/null; then
        echo "✅ $table: Exists"
    else
        echo "❌ $table: Missing or inaccessible"
    fi
done

# Check recent data
echo ""
echo "📅 Checking data freshness..."
# Add data freshness checks here

echo ""
echo "Health check complete!"
