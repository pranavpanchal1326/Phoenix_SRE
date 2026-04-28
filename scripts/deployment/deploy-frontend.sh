#!/bin/bash
# Phoenix SRE: Deploy Frontend to Vercel
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🚀 Deploying Frontend to Vercel...${NC}"

cd "$(dirname "$0")/../frontend"

# Install Vercel CLI if not present
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}📦 Installing Vercel CLI...${NC}"
    npm install -g vercel
fi

# Deploy to production
echo -e "${YELLOW}🌐 Deploying to production...${NC}"
vercel --prod

echo -e "${GREEN}✅ Frontend deployed!${NC}"
