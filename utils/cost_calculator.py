"""
Cost Calculator - Real-time GCP cost tracking
Estimates costs for Cloud Run, Firestore, and Gemini API
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional


class CostCalculator:
    """
    Calculate and track GCP costs for Phoenix SRE
    Provides real-time cost estimates and budget tracking
    """
    
    # GCP Pricing (as of 2024, europe-west1)
    PRICING = {
        "cloud_run_cpu": {
            "cpu_per_second": 0.00002400,  # per vCPU-second
            "memory_per_gb_second": 0.00000250,  # per GB-second
            "requests": 0.40 / 1_000_000,  # per million requests
        },
        "cloud_run_gpu": {
            "l4_per_hour": 1.20,  # NVIDIA L4 GPU
            "cpu_per_second": 0.00002400,
            "memory_per_gb_second": 0.00000250,
        },
        "firestore": {
            "read": 0.06 / 100_000,  # per 100k reads
            "write": 0.18 / 100_000,  # per 100k writes
            "delete": 0.02 / 100_000,  # per 100k deletes
            "storage_per_gb": 0.18 / 30,  # per GB-month (daily rate)
        },
        "gemini_api": {
            "flash_input": 0.00,  # FREE for 2.0 Flash Experimental
            "flash_output": 0.00,
            "pro_input": 1.25 / 1_000_000,  # per million tokens
            "pro_output": 5.00 / 1_000_000,
        },
    }
    
    def __init__(self, budget_limit: float = 10.00):
        """
        Initialize cost calculator
        
        Args:
            budget_limit: Total budget in USD
        """
        self.budget_limit = budget_limit
        self.start_time = datetime.now()
        self.cost_history = []
        
    def calculate_cloud_run_cost(
        self,
        cpu_cores: int,
        memory_gb: int,
        active_hours: float,
        requests: int = 0,
        has_gpu: bool = False
    ) -> Dict[str, float]:
        """
        Calculate Cloud Run service cost
        
        Args:
            cpu_cores: Number of vCPUs
            memory_gb: Memory in GB
            active_hours: Hours service was active
            requests: Number of requests
            has_gpu: Whether service uses GPU
            
        Returns:
            Cost breakdown
        """
        active_seconds = active_hours * 3600
        
        # CPU cost
        cpu_cost = cpu_cores * active_seconds * self.PRICING["cloud_run_cpu"]["cpu_per_second"]
        
        # Memory cost
        memory_cost = memory_gb * active_seconds * self.PRICING["cloud_run_cpu"]["memory_per_gb_second"]
        
        # Request cost
        request_cost = requests * self.PRICING["cloud_run_cpu"]["requests"]
        
        # GPU cost (if applicable)
        gpu_cost = 0
        if has_gpu:
            gpu_cost = active_hours * self.PRICING["cloud_run_gpu"]["l4_per_hour"]
        
        total = cpu_cost + memory_cost + request_cost + gpu_cost
        
        return {
            "cpu_cost": round(cpu_cost, 4),
            "memory_cost": round(memory_cost, 4),
            "request_cost": round(request_cost, 4),
            "gpu_cost": round(gpu_cost, 4),
            "total": round(total, 4),
        }
    
    def calculate_firestore_cost(
        self,
        reads: int = 0,
        writes: int = 0,
        deletes: int = 0,
        storage_gb: float = 0.1
    ) -> Dict[str, float]:
        """
        Calculate Firestore cost
        
        Args:
            reads: Number of document reads
            writes: Number of document writes
            deletes: Number of document deletes
            storage_gb: Storage used in GB
            
        Returns:
            Cost breakdown
        """
        read_cost = reads * self.PRICING["firestore"]["read"]
        write_cost = writes * self.PRICING["firestore"]["write"]
        delete_cost = deletes * self.PRICING["firestore"]["delete"]
        storage_cost = storage_gb * self.PRICING["firestore"]["storage_per_gb"]
        
        total = read_cost + write_cost + delete_cost + storage_cost
        
        return {
            "read_cost": round(read_cost, 4),
            "write_cost": round(write_cost, 4),
            "delete_cost": round(delete_cost, 4),
            "storage_cost": round(storage_cost, 4),
            "total": round(total, 4),
        }
    
    def calculate_gemini_cost(
        self,
        model: str = "flash",
        input_tokens: int = 0,
        output_tokens: int = 0
    ) -> Dict[str, float]:
        """
        Calculate Gemini API cost
        
        Args:
            model: "flash" or "pro"
            input_tokens: Number of input tokens
            output_tokens: Number of output tokens
            
        Returns:
            Cost breakdown
        """
        if model == "flash":
            input_cost = input_tokens * self.PRICING["gemini_api"]["flash_input"]
            output_cost = output_tokens * self.PRICING["gemini_api"]["flash_output"]
        else:  # pro
            input_cost = input_tokens * self.PRICING["gemini_api"]["pro_input"]
            output_cost = output_tokens * self.PRICING["gemini_api"]["pro_output"]
        
        total = input_cost + output_cost
        
        return {
            "input_cost": round(input_cost, 4),
            "output_cost": round(output_cost, 4),
            "total": round(total, 4),
        }
    
    def estimate_demo_cost(self, demo_duration_hours: float = 2.0) -> Dict[str, float]:
        """
        Estimate total cost for demo period
        
        Args:
            demo_duration_hours: Expected demo duration
            
        Returns:
            Complete cost estimate
        """
        # Phoenix Dashboard (CPU-only, 2 cores, 4GB)
        dashboard_cost = self.calculate_cloud_run_cost(
            cpu_cores=2,
            memory_gb=4,
            active_hours=demo_duration_hours,
            requests=500,  # Estimated requests during demo
            has_gpu=False
        )
        
        # Firestore (minimal usage)
        firestore_cost = self.calculate_firestore_cost(
            reads=100,
            writes=20,
            deletes=0,
            storage_gb=0.01
        )
        
        # Gemini API (Flash is FREE!)
        gemini_cost = self.calculate_gemini_cost(
            model="flash",
            input_tokens=50000,
            output_tokens=10000
        )
        
        total = dashboard_cost["total"] + firestore_cost["total"] + gemini_cost["total"]
        
        return {
            "dashboard": dashboard_cost["total"],
            "firestore": firestore_cost["total"],
            "gemini": gemini_cost["total"],
            "total": round(total, 2),
            "budget_remaining": round(self.budget_limit - total, 2),
            "budget_used_percent": round((total / self.budget_limit) * 100, 1),
        }
    
    def get_budget_status(self, current_spend: float = 0) -> Dict:
        """
        Get current budget status
        
        Args:
            current_spend: Current spend amount
            
        Returns:
            Budget status with alerts
        """
        remaining = self.budget_limit - current_spend
        percent_used = (current_spend / self.budget_limit) * 100
        
        # Determine alert level
        if percent_used >= 90:
            alert_level = "critical"
            alert_message = "⚠️ Budget 90% exhausted!"
        elif percent_used >= 75:
            alert_level = "warning"
            alert_message = "⚠️ Budget 75% used"
        elif percent_used >= 50:
            alert_level = "info"
            alert_message = "ℹ️ Budget 50% used"
        else:
            alert_level = "ok"
            alert_message = "✅ Budget healthy"
        
        # Predict exhaustion time
        elapsed_hours = (datetime.now() - self.start_time).total_seconds() / 3600
        if elapsed_hours > 0 and current_spend > 0:
            burn_rate = current_spend / elapsed_hours
            hours_remaining = remaining / burn_rate if burn_rate > 0 else float('inf')
            exhaustion_time = datetime.now() + timedelta(hours=hours_remaining)
        else:
            hours_remaining = float('inf')
            exhaustion_time = None
        
        return {
            "budget_limit": self.budget_limit,
            "current_spend": round(current_spend, 2),
            "remaining": round(remaining, 2),
            "percent_used": round(percent_used, 1),
            "alert_level": alert_level,
            "alert_message": alert_message,
            "burn_rate_per_hour": round(current_spend / elapsed_hours, 4) if elapsed_hours > 0 else 0,
            "hours_remaining": round(hours_remaining, 1) if hours_remaining != float('inf') else "∞",
            "exhaustion_time": exhaustion_time.isoformat() if exhaustion_time else None,
        }
