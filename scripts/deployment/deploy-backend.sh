#!/bin/bash
# Phoenix SRE: Deploy ADK Backend to Cloud Run
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"your-project-id"}
REGION="europe-west1"
SERVICE_NAME="phoenix-adk-agent"

echo -e "${GREEN}🚀 Deploying ADK Agent Orchestrator...${NC}"

cd "$(dirname "$0")/.."

gcloud run deploy $SERVICE_NAME \
  --source ./backend \
  --region $REGION \
  --project $PROJECT_ID \
  --platform managed \
  --allow-unauthenticated \
  \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 20 \
  \
  --cpu 4 \
  --memory 8Gi \
  --timeout 300 \
  --port 8080 \
  \
  --labels project=phoenix-sre,env=production,component=adk-agent

echo -e "${GREEN}✅ ADK Agent deployed!${NC}"
