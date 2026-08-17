#!/bin/bash
# File: deploy.sh
# Description: Deployment script for For Your Service AWS infrastructure
# Organization: 7 Eagle Group
# Author: Free Hall <whall4.wh@gmail.com>

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}For Your Service - AWS Infrastructure${NC}"
echo -e "${GREEN}7 Eagle Group${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if terraform is installed
if ! command -v terraform &> /dev/null; then
    echo -e "${RED}❌ Terraform is not installed${NC}"
    echo "Install from: https://www.terraform.io/downloads"
    exit 1
fi

echo -e "${GREEN}✅ Terraform found: $(terraform version | head -1)${NC}"
echo ""

# Check if terraform.tfvars exists
if [ ! -f "terraform.tfvars" ]; then
    echo -e "${YELLOW}⚠️  terraform.tfvars not found${NC}"
    echo "Creating from template..."
    cp terraform.tfvars.example terraform.tfvars
    echo ""
    echo -e "${RED}⚠️  IMPORTANT: Edit terraform.tfvars and set your databricks_external_id${NC}"
    echo "Get it from: Databricks → Catalog → Storage Credentials → Create"
    echo ""
    echo "Press any key to open terraform.tfvars for editing..."
    read -n 1
    ${EDITOR:-nano} terraform.tfvars
fi

# Initialize Terraform
echo -e "${GREEN}🔧 Initializing Terraform...${NC}"
terraform init
echo ""

# Validate configuration
echo -e "${GREEN}🔍 Validating Terraform configuration...${NC}"
terraform validate
echo ""

# Show plan
echo -e "${GREEN}📋 Generating deployment plan...${NC}"
terraform plan
echo ""

# Confirm deployment
echo -e "${YELLOW}Ready to deploy infrastructure. Continue? (yes/no)${NC}"
read -r response

if [[ "$response" != "yes" ]]; then
    echo -e "${YELLOW}Deployment cancelled${NC}"
    exit 0
fi

# Apply configuration
echo -e "${GREEN}🚀 Deploying infrastructure...${NC}"
terraform apply -auto-approve
echo ""

# Show outputs
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✅ Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
terraform output
echo ""

# Save outputs to file
terraform output -json > outputs.json
echo -e "${GREEN}✅ Outputs saved to outputs.json${NC}"
echo ""

echo -e "${YELLOW}Next Steps:${NC}"
echo "1. Copy the IAM Role ARN above"
echo "2. Go to Databricks → Catalog → Storage Credentials → Create"
echo "3. Enter the Role ARN and External ID"
echo "4. Create External Location pointing to the S3 bucket"
echo ""
echo -e "${GREEN}See README.md for detailed Databricks integration steps${NC}"
