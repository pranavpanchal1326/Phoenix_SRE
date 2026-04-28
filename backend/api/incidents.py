"""
Phoenix SRE: Incidents Endpoints
Track and manage incidents
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/incidents", tags=["incidents"])

class Incident(BaseModel):
    id: str
    timestamp: str
    status: str
    anomalies: List[dict]
    root_cause: Optional[dict] = None
    remediation_plan: Optional[dict] = None
    cost_impact: Optional[dict] = None

@router.get("/", response_model=List[Incident])
async def list_incidents():
    """List all incidents"""
    from api.main import orchestrator
    
    incidents = orchestrator.get_all_incidents()
    return incidents

@router.get("/{incident_id}", response_model=Incident)
async def get_incident(incident_id: str):
    """Get incident by ID"""
    from api.main import orchestrator
    
    incident = orchestrator.get_incident(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    return incident

@router.post("/{incident_id}/approve")
async def approve_remediation(incident_id: str, approved: bool):
    """Approve or reject remediation plan"""
    from api.main import orchestrator
    
    result = await orchestrator.execute_remediation(incident_id, approved)
    
    # Broadcast to WebSocket clients
    from api.websocket import manager
    await manager.broadcast_to_room('default', 'remediation:approved', {
        'incident_id': incident_id,
        'approved': approved,
        'result': result,
        'timestamp': datetime.now().isoformat()
    })
    
    return result
