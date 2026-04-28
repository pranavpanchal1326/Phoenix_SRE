#!/bin/bash

# Phoenix SRE - One-Command Deployment Script
# BNB Marathon 2025

set -e  # Exit on error

echo "🔥 Phoenix SRE: Adaptive GPU Orchestrator"
echo "=========================================="
echo ""

# Configuration
export PROJECT_ID="${GCP_PROJECT:-phoenix-sre-marathon}"
export REGION="${GCP_REGION:-europe-west1}"
export GEMINI_API_KEY="${GEMINI_API_KEY:-your-gemini-api-key-here}"
export SERVICE_NAME="phoenix-sre-dashboard"

echo "📋 Configuration:"
echo "  Project ID: $PROJECT_ID"
echo "  Region: $REGION"
echo "  Service Name: $SERVICE_NAME"
echo ""

# Step 1: Set GCP project
echo "1️⃣ Setting GCP project..."
gcloud config set project $PROJECT_ID

# Step 2: Enable required APIs
echo ""
echo "2️⃣ Enabling required GCP APIs..."
gcloud services enable \
    run.googleapis.com \
    cloudbuild.googleapis.com \
    containerregistry.googleapis.com \
    firestore.googleapis.com

# Step 3: Build Docker image
echo ""
echo "3️⃣ Building Docker image..."
docker build -t gcr.io/$PROJECT_ID/phoenix-sre:latest .

# Step 4: Push to Google Container Registry
echo ""
echo "4️⃣ Pushing to Google Container Registry..."
docker push gcr.io/$PROJECT_ID/phoenix-sre:latest

# Step 5: Deploy to Cloud Run
echo ""
echo "5️⃣ Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/phoenix-sre:latest \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --min-instances 0 \
    --max-instances 5 \
    --cpu 2 \
    --memory 4Gi \
    --timeout 300 \
    --set-env-vars GEMINI_API_KEY=$GEMINI_API_KEY,GCP_PROJECT=$PROJECT_ID,APP_MODE=chaos

# Step 6: Get service URL
echo ""
echo "6️⃣ Deployment complete!"
echo ""
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

echo "✅ Phoenix SRE Dashboard deployed successfully!"
echo ""
echo "🌐 Service URL: $SERVICE_URL"
echo ""
echo "📊 Next steps:"
echo "  1. Open the dashboard: $SERVICE_URL"
echo "  2. Run a chaos scenario"
echo "  3. Generate incident reports"
echo "  4. Monitor costs in real-time"
echo ""
echo "🎉 Ready for BNB Marathon 2025 demo!"
