#!/bin/bash
# Phoenix SRE: Master Deployment Script
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  Phoenix SRE: Complete Deployment     ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo ""

# Navigate to scripts directory
cd "$(dirname "$0")/deployment"

# Step 1: Deploy Ollama GPU Backend
echo -e "${YELLOW}[1/3] Deploying Ollama GPU Backend...${NC}"
bash deploy-ollama.sh
echo ""

# Step 2: Deploy ADK Agent Orchestrator
echo -e "${YELLOW}[2/3] Deploying ADK Agent Orchestrator...${NC}"
bash deploy-backend.sh
echo ""

# Step 3: Deploy Next.js Frontend
echo -e "${YELLOW}[3/3] Deploying Next.js Frontend...${NC}"
bash deploy-frontend.sh
echo ""

# Verify all services
echo -e "${YELLOW}🔍 Verifying deployments...${NC}"
bash verify-deployment.sh

echo ""
echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🎉 Deployment Complete!              ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
