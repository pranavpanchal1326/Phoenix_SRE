"""
Phoenix SRE: ADK Orchestrator Agent
Master coordinator for multi-agent system
"""

import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class PhoenixOrchestratorAgent:
    """
    Master orchestrator agent that coordinates all other agents
    
    Workflow:
    1. Receive telemetry from monitoring agent
    2. Detect anomalies
    3. Trigger analysis agent for root cause
    4. Create remediation plan
    5. Request human approval
    6. Execute remediation
    7. Generate report
    """
    
    def __init__(self):
        self.monitoring_agent = None  # Will be set by main
        self.analysis_agent = None
        self.remediation_agent = None
        self.cost_agent = None
        self.active_incidents: Dict[str, Dict] = {}
        
    async def initialize(self, monitoring, analysis, remediation, cost):
        """Initialize with agent instances"""
        self.monitoring_agent = monitoring
        self.analysis_agent = analysis
        self.remediation_agent = remediation
        self.cost_agent = cost
        logger.info("✅ Orchestrator initialized with all agents")
    
    async def process_telemetry_stream(self, metrics: Dict) -> Dict:
        """
        Main orchestration loop for processing telemetry
        
        Args:
            metrics: Real-time metrics from Cloud Run
            
        Returns:
            Status and any incidents detected
        """
        try:
            # Step 1: Detect anomalies
            anomalies = await self.monitoring_agent.detect_anomalies(metrics)
            
            if not anomalies:
                return {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "metrics": metrics
                }
            
            # Step 2: Create incident
            incident_id = f"INC-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
            incident = {
                "id": incident_id,
                "timestamp": datetime.now().isoformat(),
                "anomalies": anomalies,
                "metrics": metrics,
                "status": "detected"
            }
            
            self.active_incidents[incident_id] = incident
            logger.warning(f"⚠️ Incident detected: {incident_id}")
            
            # Step 3: Analyze root cause (using Gemini)
            root_cause = await self.analysis_agent.diagnose(anomalies, metrics)
            incident["root_cause"] = root_cause
            incident["status"] = "analyzed"
            
            # Step 4: Create remediation plan
            plan = await self.remediation_agent.create_plan(root_cause, metrics)
            incident["remediation_plan"] = plan
            incident["status"] = "plan_created"
            
            # Step 5: Calculate cost impact
            cost_impact = await self.cost_agent.calculate_impact(metrics, plan)
            incident["cost_impact"] = cost_impact
            
            # Step 6: Request human approval (via WebSocket)
            incident["status"] = "awaiting_approval"
            
            return {
                "status": "incident_detected",
                "incident": incident,
                "requires_approval": True
            }
            
        except Exception as e:
            logger.error(f"❌ Error in orchestration: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def execute_remediation(self, incident_id: str, approved: bool) -> Dict:
        """
        Execute approved remediation plan
        
        Args:
            incident_id: Incident ID
            approved: Whether human approved the plan
            
        Returns:
            Execution result
        """
        if incident_id not in self.active_incidents:
            return {"status": "error", "message": "Incident not found"}
        
        incident = self.active_incidents[incident_id]
        
        if not approved:
            incident["status"] = "rejected"
            logger.info(f"❌ Remediation rejected for {incident_id}")
            return {
                "status": "rejected",
                "incident_id": incident_id
            }
        
        try:
            # Execute remediation
            incident["status"] = "executing"
            result = await self.remediation_agent.execute(
                incident["remediation_plan"]
            )
            
            incident["execution_result"] = result
            incident["status"] = "resolved"
            incident["resolved_at"] = datetime.now().isoformat()
            
            logger.info(f"✅ Incident resolved: {incident_id}")
            
            return {
                "status": "resolved",
                "incident_id": incident_id,
                "result": result
            }
            
        except Exception as e:
            incident["status"] = "failed"
            incident["error"] = str(e)
            logger.error(f"❌ Remediation failed for {incident_id}: {e}")
            
            return {
                "status": "failed",
                "incident_id": incident_id,
                "error": str(e)
            }
    
    def get_incident(self, incident_id: str) -> Optional[Dict]:
        """Get incident by ID"""
        return self.active_incidents.get(incident_id)
    
    def get_all_incidents(self) -> List[Dict]:
        """Get all incidents"""
        return list(self.active_incidents.values())
