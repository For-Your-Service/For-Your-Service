#!/bin/bash
# File: destroy.sh
# Description: Teardown script for For Your Service AWS infrastructure
# Organization: 7 Eagle Group
# Author: Free Hall <whall4.wh@gmail.com>

set -e

RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${RED}========================================${NC}"
echo -e "${RED}⚠️  AWS INFRASTRUCTURE TEARDOWN${NC}"
echo -e "${RED}========================================${NC}"
echo ""
echo -e "${RED}This will PERMANENTLY DELETE:${NC}"
echo "  - S3 bucket and all data"
echo "  - IAM role and policies"
echo "  - All Terraform state"
echo ""
echo -e "${YELLOW}Type 'destroy' to confirm:${NC}"
read -r response

if [[ "$response" != "destroy" ]]; then
    echo -e "${GREEN}Teardown cancelled${NC}"
    exit 0
fi

echo ""
echo -e "${RED}🔥 Destroying infrastructure...${NC}"
terraform destroy
echo ""
echo -e "${GREEN}✅ Infrastructure destroyed${NC}"
