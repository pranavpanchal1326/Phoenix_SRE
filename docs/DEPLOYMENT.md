# Phoenix SRE: Deployment Guide

This guide covers deploying the Phoenix SRE platform to production using Google Cloud Platform and Vercel.

---

## Prerequisites

### Required Accounts
- Google Cloud Platform account with $10 credits
- Vercel account (free tier)
- GitHub account
- Redis Cloud account (free 30MB tier)

### Required Tools
- `gcloud` CLI (Google Cloud SDK)
- `vercel` CLI
- `docker` (for local testing)
- `git`
- Node.js 18+
- Python 3.11+

---

## Local Development Setup

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/phoenix-sre.git
cd phoenix-sre
```

### 2. Frontend Setup
```bash
cd frontend
npm install
cp .env.example .env.local
```

Edit `.env.local`:
```bash
NEXT_PUBLIC_WEBSOCKET_URL=http://localhost:8080
NEXT_PUBLIC_API_URL=http://localhost:8080/api
```

Start frontend:
```bash
npm run dev
# Frontend: http://localhost:3000
```

### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env`:
```bash
GEMINI_API_KEY=your-gemini-api-key
PORT=8080
DEBUG=true
```

Start backend:
```bash
python -m uvicorn api.main:socket_app --host 0.0.0.0 --port 8080 --reload
# Backend: http://localhost:8080
```

### 4. Verify Local Setup
- Navigate to http://localhost:3000
- Check connection status (should show "Connected" with green indicator)
- Verify live metrics are streaming
- Test chaos scenario trigger

---

## Production Deployment

### Phase 1: GCP Setup

**1. Initialize GCP Project**
```bash
# Set project ID
export PROJECT_ID="phoenix-sre-prod"
export REGION="europe-west1"

# Create project
gcloud projects create $PROJECT_ID

# Set as active project
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

**2. Set up Firestore**
```bash
# Create Firestore database
gcloud firestore databases create --region=$REGION
```

**3. Set up Artifact Registry**
```bash
# Create Docker repository
gcloud artifacts repositories create phoenix-sre \
  --repository-format=docker \
  --location=$REGION \
  --description="Phoenix SRE container images"
```

---

### Phase 2: Deploy Backend (ADK Agent)

**1. Build and Push Docker Image**
```bash
cd backend

# Build image
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/phoenix-sre/backend:latest .

# Configure Docker auth
gcloud auth configure-docker $REGION-docker.pkg.dev

# Push image
docker push $REGION-docker.pkg.dev/$PROJECT_ID/phoenix-sre/backend:latest
```

**2. Deploy to Cloud Run**
```bash
gcloud run deploy phoenix-sre-backend \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/phoenix-sre/backend:latest \
  --region $REGION \
  --platform managed \
  --min-instances 0 \
  --max-instances 10 \
  --cpu 4 \
  --memory 8Gi \
  --concurrency 80 \
  --timeout 300 \
  --allow-unauthenticated \
  --set-env-vars="GEMINI_API_KEY=your-api-key,BUDGET_LIMIT_USD=10.00"
```

**3. Get Backend URL**
```bash
export BACKEND_URL=$(gcloud run services describe phoenix-sre-backend \
  --region $REGION \
  --format 'value(status.url)')

echo "Backend URL: $BACKEND_URL"
```

---

### Phase 3: Deploy Ollama GPU Backend (Optional)

**1. Create Dockerfile**
```dockerfile
# ollama-backend/Dockerfile
FROM ollama/ollama:latest

ENV OLLAMA_HOST=0.0.0.0:8080
ENV OLLAMA_KEEP_ALIVE=-1
ENV OLLAMA_NUM_PARALLEL=4
ENV OLLAMA_FLASH_ATTENTION=1

# Pre-pull model
RUN ollama serve & sleep 5 && ollama pull gemma3:270m && pkill ollama

HEALTHCHECK CMD curl -f http://localhost:8080/api/tags || exit 1

EXPOSE 8080
ENTRYPOINT ["ollama", "serve"]
```

**2. Build and Deploy**
```bash
cd ollama-backend

# Build image
docker build -t $REGION-docker.pkg.dev/$PROJECT_ID/phoenix-sre/ollama:latest .

# Push image
docker push $REGION-docker.pkg.dev/$PROJECT_ID/phoenix-sre/ollama:latest

# Deploy to Cloud Run with GPU
gcloud run deploy phoenix-sre-ollama \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/phoenix-sre/ollama:latest \
  --region $REGION \
  --platform managed \
  --min-instances 0 \
  --max-instances 3 \
  --cpu 8 \
  --memory 16Gi \
  --gpu 1 \
  --gpu-type nvidia-l4 \
  --concurrency 7 \
  --timeout 600 \
  --allow-unauthenticated
```

**Cost**: $1.40/hour when active, $0 when idle (scale-to-zero)

---

### Phase 4: Deploy Frontend (Vercel)

**1. Install Vercel CLI**
```bash
npm install -g vercel
```

**2. Login to Vercel**
```bash
vercel login
```

**3. Configure Environment Variables**
Create `.env.production` in frontend directory:
```bash
NEXT_PUBLIC_WEBSOCKET_URL=https://phoenix-sre-backend-xxx.run.app
NEXT_PUBLIC_API_URL=https://phoenix-sre-backend-xxx.run.app/api
```

**4. Deploy**
```bash
cd frontend

# Deploy to production
vercel --prod

# Set environment variables
vercel env add NEXT_PUBLIC_WEBSOCKET_URL production
vercel env add NEXT_PUBLIC_API_URL production
```

**5. Get Frontend URL**
```bash
# Vercel will provide URL like: https://phoenix-sre.vercel.app
```

---

## Environment Variables

### Backend (.env)
```bash
# GCP Configuration
GCP_PROJECT_ID=phoenix-sre-prod
GCP_REGION=europe-west1

# Service URLs
OLLAMA_URL=https://phoenix-sre-ollama-xxx.run.app
REDIS_URL=redis://redis-cloud-url:6379
FIRESTORE_PROJECT=phoenix-sre-prod

# AI Configuration
GEMINI_API_KEY=your-gemini-api-key-here
GEMINI_MODEL=gemini-2.0-flash
GEMMA_MODEL=gemma3:270m

# Budget Configuration
BUDGET_LIMIT_USD=10.00
COST_ALERT_THRESHOLD=0.8

# Server Configuration
PORT=8080
DEBUG=false
LOG_LEVEL=INFO
```

### Frontend (.env.local / .env.production)
```bash
NEXT_PUBLIC_WEBSOCKET_URL=https://phoenix-sre-backend-xxx.run.app
NEXT_PUBLIC_API_URL=https://phoenix-sre-backend-xxx.run.app/api
```

---

## Verification

### 1. Health Checks
```bash
# Backend health
curl https://phoenix-sre-backend-xxx.run.app/

# Ollama health (if deployed)
curl https://phoenix-sre-ollama-xxx.run.app/api/tags
```

### 2. WebSocket Connection
```bash
# Test WebSocket connection
wscat -c wss://phoenix-sre-backend-xxx.run.app/socket.io/?transport=websocket
```

### 3. Frontend Access
- Navigate to https://phoenix-sre.vercel.app
- Check connection status (should show "Connected")
- Verify live metrics are streaming
- Test chaos scenario trigger

---

## Monitoring

### Cloud Run Metrics
```bash
# View backend metrics
gcloud run services describe phoenix-sre-backend \
  --region $REGION \
  --format yaml

# View logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=phoenix-sre-backend" \
  --limit 50 \
  --format json
```

### Cost Tracking
```bash
# View current spend
gcloud billing accounts list

# View budget alerts
gcloud billing budgets list
```

---

## Troubleshooting

### Backend Not Starting
```bash
# Check logs
gcloud logging read "resource.type=cloud_run_revision" --limit 50

# Check environment variables
gcloud run services describe phoenix-sre-backend --region $REGION
```

### WebSocket Connection Failed
- Verify backend URL in frontend .env
- Check CORS configuration in backend
- Verify Cloud Run allows unauthenticated access

### High Costs
- Check Cloud Run instance count
- Verify scale-to-zero is working
- Review Gemini API usage
- Check GPU instance status

---

## Rollback

### Rollback Backend
```bash
# List revisions
gcloud run revisions list --service phoenix-sre-backend --region $REGION

# Rollback to previous revision
gcloud run services update-traffic phoenix-sre-backend \
  --to-revisions REVISION_NAME=100 \
  --region $REGION
```

### Rollback Frontend
```bash
cd frontend
vercel rollback
```

---

## Budget Optimization

### Scale-to-Zero Configuration
```bash
# Ensure min-instances=0
gcloud run services update phoenix-sre-backend \
  --min-instances 0 \
  --region $REGION
```

### Request Batching
- Configure WebSocket to batch metrics updates
- Reduce Gemini API calls by using Gemma for simple tasks

### Monitoring Costs
```bash
# Set up budget alerts
gcloud billing budgets create \
  --billing-account=BILLING_ACCOUNT_ID \
  --display-name="Phoenix SRE Budget" \
  --budget-amount=10USD \
  --threshold-rule=percent=50 \
  --threshold-rule=percent=80 \
  --threshold-rule=percent=100
```

---

## CI/CD Pipeline (Optional)

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy Phoenix SRE

on:
  push:
    branches: [main]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: google-github-actions/setup-gcloud@v1
      - name: Build and Deploy
        run: |
          cd backend
          gcloud run deploy phoenix-sre-backend \
            --source . \
            --region europe-west1

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - name: Deploy to Vercel
        run: |
          cd frontend
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}
```

---

## Security Best Practices

### API Keys
- Never commit API keys to Git
- Use environment variables
- Rotate keys regularly

### CORS Configuration
- Restrict origins to your frontend domain
- Use HTTPS only

### IAM Permissions
- Use least privilege principle
- Create service accounts for Cloud Run
- Enable Cloud Run IAM authentication

---

**Last Updated**: 2025-11-25  
**Version**: 1.0.0
