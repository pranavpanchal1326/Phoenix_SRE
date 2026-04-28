# Phoenix SRE: Architecture Overview

## System Architecture

Phoenix SRE implements a modern 4-tier enterprise architecture optimized for GPU orchestration, real-time monitoring, and AI-powered incident response.

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    TIER 1: Presentation Layer                    │
│                      (Next.js 15 + Vercel)                       │
├─────────────────────────────────────────────────────────────────┤
│  • Material Design 3 UI with glassmorphism                       │
│  • Real-time WebSocket client (Socket.IO)                        │
│  • 3D topology visualization (React Three Fiber)                 │
│  • State management (Zustand + React Query)                      │
│  • Responsive PWA (mobile-first)                                 │
│  • Edge deployment (global CDN)                                  │
└────────────────────┬────────────────────────────────────────────┘
                     │ WebSocket (200ms) + REST API
┌────────────────────┴────────────────────────────────────────────┐
│              TIER 2: AI Agent Orchestration Layer                │
│                  (FastAPI + ADK + Cloud Run)                     │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐    │
│  │         PhoenixOrchestratorAgent (Master)               │    │
│  │  • Coordinates all agents                               │    │
│  │  • Manages incident workflow                            │    │
│  │  • Human-in-the-loop approval                           │    │
│  └─────────────────────────────────────────────────────────┘    │
│                                                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐           │
│  │  Monitoring  │ │   Analysis   │ │ Remediation  │           │
│  │    Agent     │ │    Agent     │ │    Agent     │           │
│  │              │ │              │ │              │           │
│  │ • Anomaly    │ │ • Root cause │ │ • Auto-heal  │           │
│  │   detection  │ │   (Gemini)   │ │ • Scale up   │           │
│  │ • Thresholds │ │ • Confidence │ │ • Optimize   │           │
│  └──────────────┘ └──────────────┘ └──────────────┘           │
│                                                                  │
│  ┌──────────────┐                                               │
│  │     Cost     │                                               │
│  │ Optimization │                                               │
│  │    Agent     │                                               │
│  │              │                                               │
│  │ • Budget     │                                               │
│  │   tracking   │                                               │
│  │ • Predictions│                                               │
│  └──────────────┘                                               │
│                                                                  │
│  • WebSocket server (Socket.IO)                                 │
│  • Chaos engineering endpoints                                  │
│  • Incidents tracking API                                       │
│  • Metrics broadcasting (200ms)                                 │
└────────────────────┬────────────────────────────────────────────┘
                     │ HTTP API (Ollama)
┌────────────────────┴────────────────────────────────────────────┐
│               TIER 3: GPU Inference Layer                        │
│              (Ollama + Gemma 3 + Cloud Run GPU)                  │
├─────────────────────────────────────────────────────────────────┤
│  • NVIDIA L4 GPU (24GB VRAM)                                     │
│  • Gemma 3 270M model                                            │
│  • vLLM + Flash Attention optimization                           │
│  • 200-500ms latency (P95)                                       │
│  • 20-50 tokens/sec throughput                                   │
│  • Scale-to-zero (cost optimization)                             │
└────────────────────┬────────────────────────────────────────────┘
                     │ Data Persistence
┌────────────────────┴────────────────────────────────────────────┐
│               TIER 4: Data Persistence Layer                     │
│            (Firestore + Redis + BigQuery)                        │
├─────────────────────────────────────────────────────────────────┤
│  • Firestore: Incident logs, metrics history                     │
│  • Redis Cloud: WebSocket sessions, cache (FREE 30MB)            │
│  • BigQuery: Analytics, long-term storage (optional)             │
│  • Cloud Storage: Reports, backups                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

### Real-Time Metrics Streaming

```
MetricsEngine → Orchestrator → Monitoring Agent → WebSocket → Frontend
     ↓              ↓                ↓                ↓           ↓
  Generate      Analyze         Detect          Broadcast    Display
  Metrics       Anomalies       Alerts          Events       Live Data
```

### Incident Workflow

```
1. Anomaly Detected (Monitoring Agent)
   ↓
2. Root Cause Analysis (Analysis Agent + Gemini)
   ↓
3. Remediation Plan Created (Remediation Agent)
   ↓
4. Cost Impact Calculated (Cost Agent)
   ↓
5. Human Approval Requested (WebSocket → Frontend)
   ↓
6. Plan Executed (Remediation Agent)
   ↓
7. Incident Resolved (Orchestrator)
```

### Chaos Engineering Flow

```
Frontend → Chaos API → WebSocket → All Clients
    ↓          ↓           ↓            ↓
  Click    Trigger     Broadcast    Receive
  Button   Scenario    Event        Alert
```

---

## Component Details

### Frontend (Next.js 15)

**Key Components**:
- `app/page.tsx` - Main dashboard with live metrics
- `components/dashboard/MetricCard.tsx` - Hero metric cards
- `components/dashboard/ChaosCard.tsx` - Chaos scenario cards
- `hooks/useWebSocket.ts` - WebSocket client hook

**Features**:
- Material Design 3 color system
- Glassmorphism effects
- Real-time updates (200ms)
- Responsive design
- Dark/light theme

### Backend (FastAPI + ADK)

**Key Modules**:
- `agents/orchestrator.py` - Master coordinator
- `agents/monitoring.py` - Anomaly detection
- `agents/analysis.py` - Gemini 2.0 Flash integration
- `agents/remediation.py` - Auto-healing
- `agents/cost.py` - Budget tracking
- `api/main.py` - FastAPI application
- `api/websocket.py` - Socket.IO server
- `api/chaos.py` - Chaos engineering endpoints
- `api/incidents.py` - Incidents tracking

**Features**:
- Multi-agent coordination
- Real-time WebSocket broadcasting
- Chaos engineering
- Incident management
- Cost optimization

### GPU Backend (Ollama)

**Configuration**:
- Model: Gemma 3 270M
- GPU: NVIDIA L4 (24GB VRAM)
- Optimization: vLLM + Flash Attention
- Deployment: Cloud Run with GPU

**Features**:
- Fast inference (200-500ms)
- Scale-to-zero
- Cost-effective ($1.40/hour when active)

---

## Technology Decisions

### Why Next.js 15?
- App Router for better performance
- React 19 RC for latest features
- Vercel Edge deployment (FREE)
- Excellent TypeScript support

### Why FastAPI?
- High performance (async/await)
- Automatic API documentation
- WebSocket support (Socket.IO)
- Python ecosystem for AI/ML

### Why Gemini 2.0 Flash?
- Fast inference (2-3s)
- Cost-effective ($0.25/1M tokens)
- Excellent reasoning capabilities
- Google Cloud integration

### Why Gemma 3 270M?
- Small model (270M parameters)
- Fast inference (200-500ms)
- Self-hosted ($0 cost)
- Good for simple tasks

### Why Hybrid LLM Strategy?
- 80% cost savings
- Gemma for fast tasks (anomaly detection, log parsing)
- Gemini for complex tasks (root cause analysis, reports)
- Intelligent routing based on task complexity

---

## Deployment Architecture

### Production Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                    Vercel Edge Network                       │
│                  (Global CDN, FREE tier)                     │
│  • Next.js frontend                                          │
│  • Automatic HTTPS                                           │
│  • Edge functions                                            │
│  • Analytics                                                 │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────┴────────────────────────────────────────┐
│                  Google Cloud Platform                       │
│                    (europe-west1)                            │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Cloud Run (CPU) - ADK Agent Orchestrator           │    │
│  │  • Min instances: 0 (scale-to-zero)                 │    │
│  │  • Max instances: 10                                │    │
│  │  • CPU: 4, RAM: 8GB                                 │    │
│  │  • Cost: $0.08/hour when active                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Cloud Run (GPU) - Ollama + Gemma                   │    │
│  │  • Min instances: 0 (scale-to-zero)                 │    │
│  │  • Max instances: 3                                 │    │
│  │  • GPU: NVIDIA L4, CPU: 8, RAM: 16GB                │    │
│  │  • Cost: $1.40/hour when active                     │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  Firestore (NoSQL Database)                         │    │
│  │  • FREE tier (1GB storage)                          │    │
│  │  • Incident logs, metrics history                   │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Redis Cloud (FREE)                        │
│  • 30MB storage                                              │
│  • WebSocket sessions                                        │
│  • Cache layer                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Security

### Authentication & Authorization
- API keys for backend services
- CORS configuration
- Rate limiting
- Request validation

### Data Protection
- HTTPS everywhere
- Environment variables for secrets
- No sensitive data in logs
- Firestore security rules

### Network Security
- VPC for internal communication
- Cloud Run IAM policies
- Service-to-service authentication

---

## Monitoring & Observability

### Metrics
- Real-time metrics streaming (200ms)
- GPU utilization, latency, error rate
- Cost tracking
- Budget alerts

### Logging
- Structured logging (JSON)
- Cloud Logging integration
- Error tracking
- Audit logs

### Tracing
- OpenTelemetry integration (optional)
- Distributed tracing
- Performance monitoring

---

## Scalability

### Horizontal Scaling
- Cloud Run auto-scaling (0-10 instances)
- Load balancing
- WebSocket session management

### Vertical Scaling
- CPU/RAM configuration
- GPU allocation
- Concurrency limits

### Cost Optimization
- Scale-to-zero when idle
- Intelligent LLM routing
- Request batching
- Edge caching

---

## Disaster Recovery

### Backup Strategy
- Firestore automatic backups
- Redis persistence
- Code versioning (Git)

### High Availability
- Multi-region deployment (optional)
- Health checks
- Auto-restart on failure

### Incident Response
- Automated remediation
- Human approval workflow
- Rollback capability

---

**Last Updated**: 2025-11-25  
**Version**: 1.0.0
