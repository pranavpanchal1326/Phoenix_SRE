"""
Phoenix SRE: FastAPI Main Application
Production-grade API server with WebSocket support
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
import os
from dotenv import load_dotenv
import logging

# Import ADK agents
from agents.orchestrator import PhoenixOrchestratorAgent
from agents.monitoring import MonitoringAgent
from agents.analysis import AnalysisAgent
from agents.remediation import RemediationAgent
from agents.cost import CostOptimizationAgent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="Phoenix SRE API",
    description="ADK Multi-Agent Orchestrator for GPU Observability",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create Socket.IO server
sio = socketio.AsyncServer(
    async_mode='asgi',
    cors_allowed_origins='*',
    ping_timeout=60,
    ping_interval=25,
    logger=True,
    engineio_logger=False
)

# Wrap with ASGI app
socket_app = socketio.ASGIApp(
    sio,
    other_asgi_app=app,
    socketio_path='/socket.io'
)

# Initialize ADK agents
orchestrator = PhoenixOrchestratorAgent()
monitoring_agent = MonitoringAgent()
analysis_agent = AnalysisAgent()
remediation_agent = RemediationAgent()
cost_agent = CostOptimizationAgent(budget_limit=10.0)

@app.on_event("startup")
async def startup_event():
    """Initialize agents on startup"""
    await orchestrator.initialize(
        monitoring_agent,
        analysis_agent,
        remediation_agent,
        cost_agent
    )
    logger.info("[START] Phoenix SRE API started successfully")
    logger.info("[INIT] ADK Multi-Agent System initialized")
    
    # Initialize WebSocket server
    from api.websocket import startup_event as ws_startup
    await ws_startup()
    logger.info("[INIT] WebSocket server initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    from api.websocket import shutdown_event as ws_shutdown
    await ws_shutdown()
    logger.info("[STOP] WebSocket server stopped")

# Register routers
from api.chaos import router as chaos_router
from api.incidents import router as incidents_router
app.include_router(chaos_router)
app.include_router(incidents_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Phoenix SRE API",
        "version": "1.0.0",
        "status": "healthy",
        "agents": {
            "orchestrator": "active",
            "monitoring": "active",
            "analysis": "active" if analysis_agent.enabled else "fallback",
            "remediation": "active",
            "cost": "active"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {
        "status": "healthy",
        "service": "phoenix-sre-api"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:socket_app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        reload=True,
        log_level="info"
    )
