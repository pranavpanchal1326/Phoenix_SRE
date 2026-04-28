"""
Phoenix SRE: WebSocket Server
Real-time metrics streaming and event broadcasting
"""

from fastapi import WebSocket, WebSocketDisconnect
import socketio
import asyncio
import json
from datetime import datetime
from typing import Dict, Set, Optional
import os
import logging

# Optional Redis import
try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    redis = None
    REDIS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Import from main
from .main import sio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[str]] = {}  # room -> {sid, sid, ...}
        self.redis_client: Optional[redis.Redis] = None
        self.metrics_task: asyncio.Task = None
    
    async def initialize(self):
        """Initialize Redis connection (optional)"""
        if not REDIS_AVAILABLE:
            logger.warning("[WARN] Redis not available, using in-memory connection manager")
            return
        
        try:
            redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379')
            self.redis_client = redis.from_url(redis_url, decode_responses=True)
            logger.info("[OK] Redis connection established")
        except Exception as e:
            logger.warning(f"[WARN] Redis connection failed: {e}, using in-memory manager")
    
    async def connect(self, sid: str, room: str = "default"):
        """Register new client connection"""
        if room not in self.active_connections:
            self.active_connections[room] = set()
        
        self.active_connections[room].add(sid)
        if self.redis_client:
            await self.redis_client.sadd(f'room:{room}', sid)
        
        print(f"[OK] Client {sid} connected to room {room}")
        print(f"[INFO] Total connections in {room}: {len(self.active_connections[room])}")
    
    async def disconnect(self, sid: str):
        """Remove client connection"""
        for room, clients in self.active_connections.items():
            if sid in clients:
                clients.remove(sid)
                if self.redis_client:
                    await self.redis_client.srem(f'room:{room}', sid)
                print(f"[WARN] Client {sid} disconnected from room {room}")
                
                if len(clients) == 0:
                    del self.active_connections[room]
    
    async def broadcast_to_room(self, room: str, event: str, data: Dict):
        """Broadcast message to all clients in a room"""
        if room in self.active_connections:
            await sio.emit(event, data, room=room)

# Create connection manager instance
manager = ConnectionManager()

@sio.event
async def connect(sid, environ):
    """Handle client connection"""
    await manager.connect(sid, room="default")
    
    # Send welcome message
    await sio.emit('welcome', {
        'message': '[FIRE] Connected to Phoenix SRE',
        'server_time': datetime.now().isoformat(),
        'sid': sid
    }, room=sid)
    
    # Send initial system status
    status = {
        'status': 'healthy',
        'active_incidents': 0,
        'budget_remaining': 10.00,
        'uptime_percentage': 99.99
    }
    await sio.emit('initial_status', status, room=sid)

@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    await manager.disconnect(sid)

@sio.event
async def subscribe_metrics(sid, data):
    """
    Client subscribes to specific metric streams
    
    data = {
        "metrics": ["gpu_util", "latency", "error_rate"],
        "interval": 200  # ms
    }
    """
    metrics = data.get('metrics', ['all'])
    interval = data.get('interval', 200)
    
    # Store subscription preferences
    if manager.redis_client:
        await manager.redis_client.hset(
            f'subscriptions:{sid}',
            mapping={
                'metrics': json.dumps(metrics),
                'interval': interval
            }
        )
    
    await sio.emit('subscription_confirmed', {
        'metrics': metrics,
        'interval': interval
    }, room=sid)

@sio.event
async def trigger_chaos(sid, data):
    """
    Handle chaos scenario trigger from client
    
    data = {
        "scenario": "gpu-saturation",
        "params": {...}
    }
    """
    scenario = data.get('scenario')
    params = data.get('params', {})
    
    # TODO: Trigger chaos engineering scenario
    # result = await chaos_controller.trigger_scenario(scenario, params)
    
    # Broadcast to all clients
    await manager.broadcast_to_room('default', 'chaos_triggered', {
        'scenario': scenario,
        'incident_id': f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        'timestamp': datetime.now().isoformat()
    })

@sio.event
async def approve_remediation(sid, data):
    """
    Handle human approval for remediation plan
    
    data = {
        "incident_id": "...",
        "approved": true/false
    }
    """
    incident_id = data.get('incident_id')
    approved = data.get('approved', False)
    
    # TODO: Process approval
    # await remediation_controller.process_approval(incident_id, approved, sid)
    
    # Broadcast decision
    await manager.broadcast_to_room('default', 'remediation_approved', {
        'incident_id': incident_id,
        'approved': approved,
        'approved_by': sid,
        'timestamp': datetime.now().isoformat()
    })

async def metrics_broadcaster():
    """
    Background task: Emit metrics every 200ms to all connected clients
    """
    # Import here to avoid circular dependency
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    from utils.metrics_engine import MetricsEngine
    from api.main import orchestrator
    
    # Initialize metrics engine
    metrics_engine = MetricsEngine()
    
    logger.info("[INFO] Metrics broadcaster started")
    
    while True:
        try:
            # Fetch latest metrics from engine
            metrics = metrics_engine.get_current_metrics()
            
            # Add timestamp
            metrics['timestamp'] = datetime.now().isoformat()
            
            # Process through orchestrator for anomaly detection
            result = await orchestrator.process_telemetry_stream(metrics)
            
            # Broadcast to all clients in default room
            await manager.broadcast_to_room('default', 'metrics:update', {
                'data': metrics,
                'timestamp': metrics['timestamp']
            })
            
            # If incident detected, broadcast incident
            if result.get("status") == "incident_detected":
                incident = result.get("incident")
                await manager.broadcast_to_room('default', 'incident:new', {
                    'incident': incident,
                    'timestamp': datetime.now().isoformat()
                })
                logger.warning(f"[WARN] Incident broadcast: {incident['id']}")
            
            # Wait 200ms (5 updates per second)
            await asyncio.sleep(0.2)
            
        except Exception as e:
            logger.error(f"[ERROR] Error in metrics broadcaster: {e}")
            await asyncio.sleep(1)  # Back off on error

# Startup event
async def startup_event():
    """Initialize connections and start background tasks"""
    await manager.initialize()
    
    # Start metrics broadcaster
    manager.metrics_task = asyncio.create_task(metrics_broadcaster())
    
    print("[OK] WebSocket server started")

# Shutdown event
async def shutdown_event():
    """Cleanup on shutdown"""
    if manager.metrics_task:
        manager.metrics_task.cancel()
    
    if manager.redis_client:
        await manager.redis_client.close()
    
    print("[STOP] WebSocket server stopped")
