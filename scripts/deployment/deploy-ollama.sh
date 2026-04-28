#!/bin/bash
# Phoenix SRE: Deploy Ollama + Gemma GPU Service to Cloud Run
set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'  # No Color

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"your-project-id"}
REGION="europe-west1"
SERVICE_NAME="ollama-gemma3-270m-gpu"

echo -e "${GREEN}🚀 Deploying Gemma 3 270M with NVIDIA L4 GPU...${NC}"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"
echo ""

# Navigate to backend directory
cd "$(dirname "$0")/.."

# Deploy to Cloud Run
echo -e "${YELLOW}📦 Building and deploying...${NC}"

gcloud run deploy $SERVICE_NAME \
  --source ./ollama-backend \
  --region $REGION \
  --project $PROJECT_ID \
  --platform managed \
  --allow-unauthenticated \
  \
  `# Instance Configuration` \
  --min-instances 0 \
  --max-instances 3 \
  --concurrency 7 \
  \
  `# Compute Resources` \
  --cpu 8 \
  --memory 16Gi \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --no-cpu-throttling \
  \
  `# Environment Variables` \
  --set-env-vars OLLAMA_NUM_PARALLEL=4 \
  --set-env-vars OLLAMA_KEEP_ALIVE=-1 \
  --set-env-vars OLLAMA_FLASH_ATTENTION=1 \
  --set-env-vars OLLAMA_MAX_QUEUE=100 \
  \
  `# Timeouts & Networking` \
  --timeout 600 \
  --port 8080 \
  --use-http2 \
  \
  `# Labels for Tracking` \
  --labels project=phoenix-sre,env=production,marathon=bnb2025,gpu=nvidia-l4

# Check deployment status
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
else
    echo -e "${RED}❌ Deployment failed!${NC}"
    exit 1
fi

# Export URL
export OLLAMA_URL=$(gcloud run services describe $SERVICE_NAME \
    --region=$REGION \
    --format='value(status.url)')

echo ""
echo -e "${GREEN}📊 Service Details:${NC}"
echo "URL: $OLLAMA_URL"
echo ""

# Test endpoint
echo -e "${YELLOW}🧪 Testing endpoint...${NC}"

curl -X POST $OLLAMA_URL/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemma3:270m",
    "prompt": "Diagnose this system: GPU utilization at 98%, latency 2500ms, error rate 5%. What is the root cause?",
    "stream": false
  }' | jq '.'

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Service is responding correctly!${NC}"
else
    echo -e "${RED}⚠️ Service may not be fully ready yet. Wait 30s and try again.${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Deployment complete!${NC}"
echo "Add this to your .env file:"
echo "OLLAMA_URL=$OLLAMA_URL"
