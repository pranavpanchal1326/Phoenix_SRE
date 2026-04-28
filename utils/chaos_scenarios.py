"""
Chaos Scenarios - Predefined failure scenarios for testing
Implements 4 core chaos engineering patterns
"""

from typing import Dict, List
from datetime import datetime, timedelta
import random


class ChaosScenarios:
    """
    Chaos Engineering scenarios for GPU workloads
    Each scenario simulates a realistic production failure
    """
    
    SCENARIOS = {
        "gpu_spike": {
            "name": "GPU Utilization Spike",
            "description": "Gradual increase in GPU utilization due to model complexity increase",
            "icon": "📈",
            "severity": "high",
            "expected_duration": "5-10 minutes",
        },
        "memory_leak": {
            "name": "GPU Memory Leak",
            "description": "Memory gradually fills up due to tensor caching bug",
            "icon": "💾",
            "severity": "critical",
            "expected_duration": "10-15 minutes",
        },
        "latency_spike": {
            "name": "Request Latency Spike",
            "description": "Sudden increase in response times due to network congestion",
            "icon": "⏱️",
            "severity": "medium",
            "expected_duration": "3-7 minutes",
        },
        "instance_crash": {
            "name": "Instance Crash & Recovery",
            "description": "Container crashes due to OOM, auto-restarts",
            "icon": "💥",
            "severity": "critical",
            "expected_duration": "2-5 minutes",
        },
    }
    
    @staticmethod
    def get_all_scenarios() -> Dict:
        """Return all available chaos scenarios"""
        return ChaosScenarios.SCENARIOS
    
    @staticmethod
    def get_scenario_details(scenario_name: str) -> Dict:
        """Get details for a specific scenario"""
        return ChaosScenarios.SCENARIOS.get(scenario_name, {})
    
    @staticmethod
    def generate_incident_data(scenario_name: str) -> Dict:
        """
        Generate realistic incident data for a scenario
        
        Returns:
            Complete incident object with timeline, metrics, and metadata
        """
        scenario = ChaosScenarios.SCENARIOS.get(scenario_name)
        if not scenario:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        # Generate incident timeline
        start_time = datetime.now() - timedelta(minutes=random.randint(10, 60))
        detection_time = start_time + timedelta(seconds=random.randint(30, 120))
        analysis_time = detection_time + timedelta(seconds=random.randint(15, 45))
        approval_time = analysis_time + timedelta(seconds=random.randint(10, 30))
        resolution_time = approval_time + timedelta(minutes=random.randint(2, 5))
        
        # Generate trace ID
        trace_id = f"PHXSRE-{datetime.now().strftime('%Y%m%d')}-{random.randint(1000, 9999)}"
        
        # Scenario-specific metrics
        if scenario_name == "gpu_spike":
            metrics = {
                "peak_gpu_util": random.uniform(92, 99),
                "peak_temperature": random.uniform(82, 88),
                "peak_latency": random.uniform(800, 1500),
                "affected_requests": random.randint(5000, 15000),
            }
            root_cause = "Sudden traffic surge from new customer deployment increased model inference load beyond capacity. GPU utilization spiked from 45% to 96% within 3 minutes."
            ai_recommendation = "Scale GPU instances from 2 to 4 to handle increased load. Consider implementing request queuing and rate limiting."
            
        elif scenario_name == "memory_leak":
            metrics = {
                "peak_memory_mb": random.uniform(22000, 23500),
                "memory_growth_rate": random.uniform(150, 300),
                "oom_events": random.randint(2, 5),
                "affected_requests": random.randint(8000, 20000),
            }
            root_cause = "Memory leak in tensor caching layer causing gradual memory accumulation. GPU memory grew from 8GB to 23GB over 12 minutes, triggering OOM errors."
            ai_recommendation = "Restart affected instances to clear memory. Implement periodic cache cleanup and memory monitoring alerts."
            
        elif scenario_name == "latency_spike":
            metrics = {
                "peak_latency": random.uniform(1200, 2500),
                "p95_latency": random.uniform(800, 1500),
                "timeout_rate": random.uniform(3, 12),
                "affected_requests": random.randint(3000, 10000),
            }
            root_cause = "Network congestion in europe-west1 region caused packet loss and retransmissions. Request latency increased from 120ms to 1800ms."
            ai_recommendation = "Enable multi-region failover. Implement circuit breaker pattern to prevent cascade failures."
            
        elif scenario_name == "instance_crash":
            metrics = {
                "crashed_instances": random.randint(1, 2),
                "downtime_seconds": random.randint(45, 180),
                "error_rate": random.uniform(15, 35),
                "affected_requests": random.randint(2000, 8000),
            }
            root_cause = "Container exceeded memory limits due to large batch processing request. Instance crashed and auto-restarted after 90 seconds."
            ai_recommendation = "Increase memory limits from 16GB to 24GB. Implement request size validation and batch splitting."
        
        # Calculate cost impact
        base_cost_per_hour = 1.20  # L4 GPU cost
        incident_duration_hours = (resolution_time - start_time).total_seconds() / 3600
        scaling_cost = base_cost_per_hour * random.uniform(1.5, 2.5) * incident_duration_hours
        total_cost = scaling_cost + random.uniform(0.05, 0.15)
        cost_savings = random.uniform(50, 200)  # Savings from early detection
        
        return {
            "trace_id": trace_id,
            "scenario": scenario_name,
            "scenario_name": scenario["name"],
            "severity": scenario["severity"],
            "icon": scenario["icon"],
            "status": "resolved",
            
            # Timeline
            "start_time": start_time.isoformat(),
            "detection_time": detection_time.isoformat(),
            "analysis_time": analysis_time.isoformat(),
            "approval_time": approval_time.isoformat(),
            "resolution_time": resolution_time.isoformat(),
            "duration_minutes": round((resolution_time - start_time).total_seconds() / 60, 1),
            
            # Analysis
            "root_cause": root_cause,
            "ai_recommendation": ai_recommendation,
            "human_approved": True,
            
            # Metrics
            "metrics": metrics,
            
            # Impact
            "service": "ollama-gemma3-270m-gpu",
            "region": "europe-west1",
            "affected_users": random.randint(100, 500),
            
            # Cost
            "scaling_cost_per_hour": round(scaling_cost / incident_duration_hours, 2),
            "total_cost": round(total_cost, 2),
            "cost_savings": round(cost_savings, 2),
            
            # Actions taken
            "actions": [
                {
                    "time": detection_time.isoformat(),
                    "action": "Phoenix AI detected anomaly",
                    "actor": "AI System"
                },
                {
                    "time": analysis_time.isoformat(),
                    "action": "Gemini analyzed root cause",
                    "actor": "AI System"
                },
                {
                    "time": approval_time.isoformat(),
                    "action": "Human operator approved scaling",
                    "actor": "SRE Team"
                },
                {
                    "time": resolution_time.isoformat(),
                    "action": "Service scaled and recovered",
                    "actor": "Cloud Run"
                },
            ],
        }
    
    @staticmethod
    def get_random_scenario() -> str:
        """Return a random scenario name"""
        return random.choice(list(ChaosScenarios.SCENARIOS.keys()))
