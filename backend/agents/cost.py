"""
Phoenix SRE: Cost Optimization Agent
Budget tracking and cost optimization
"""

import logging
from typing import Dict

logger = logging.getLogger(__name__)

class CostOptimizationAgent:
    """
    Cost optimization agent for budget management
    
    Tracks costs and provides optimization recommendations
    """
    
    def __init__(self, budget_limit: float = 10.0):
        self.budget_limit = budget_limit
        self.total_spent = 0.0
        self.cost_history = []
        
    async def calculate_impact(self, metrics: Dict, plan: Dict) -> Dict:
        """
        Calculate cost impact of remediation plan
        
        Args:
            metrics: Current metrics
            plan: Remediation plan
            
        Returns:
            Cost impact analysis
        """
        current_cost = metrics.get("cost_per_hour", 1.40)
        
        # Calculate impact based on actions
        projected_cost = current_cost
        
        for action in plan.get("actions", []):
            if action["type"] == "scale_up":
                # Each additional instance costs ~$1.40/hour
                instances_added = action["to"] - action["from"]
                projected_cost += instances_added * 1.40
            elif action["type"] == "restart_instances":
                # No cost change
                pass
            elif action["type"] == "clear_cache":
                # No cost change
                pass
        
        impact = {
            "current_cost_per_hour": current_cost,
            "projected_cost_per_hour": projected_cost,
            "delta": projected_cost - current_cost,
            "budget_remaining": self.budget_limit - self.total_spent,
            "hours_until_budget_exhausted": (self.budget_limit - self.total_spent) / projected_cost if projected_cost > 0 else float('inf')
        }
        
        return impact
    
    async def get_optimization_recommendations(self, metrics: Dict) -> Dict:
        """
        Get cost optimization recommendations
        
        Args:
            metrics: Current metrics
            
        Returns:
            Optimization recommendations
        """
        recommendations = []
        
        # Check if GPU utilization is low
        if metrics.get("gpu_util", 0) < 30:
            recommendations.append({
                "type": "scale_down",
                "priority": "high",
                "description": "GPU utilization is low, consider scaling down instances",
                "potential_savings": "$1.40/hour per instance"
            })
        
        # Check if using expensive models unnecessarily
        if metrics.get("requests_per_sec", 0) < 10:
            recommendations.append({
                "type": "use_smaller_model",
                "priority": "medium",
                "description": "Low request rate, consider using smaller Gemma model",
                "potential_savings": "$0.50/hour"
            })
        
        # Check if caching can be improved
        if metrics.get("error_rate", 0) < 1:
            recommendations.append({
                "type": "increase_caching",
                "priority": "low",
                "description": "System is stable, increase cache TTL to reduce API calls",
                "potential_savings": "$0.10/hour"
            })
        
        return {
            "recommendations": recommendations,
            "total_potential_savings": sum(
                float(r.get("potential_savings", "$0/hour").replace("$", "").replace("/hour", ""))
                for r in recommendations
            )
        }
    
    def update_spend(self, amount: float):
        """Update total spend"""
        self.total_spent += amount
        self.cost_history.append({
            "amount": amount,
            "total": self.total_spent,
            "remaining": self.budget_limit - self.total_spent
        })
        
        if self.total_spent > self.budget_limit * 0.8:
            logger.warning(f"⚠️ Budget alert: ${self.total_spent:.2f} / ${self.budget_limit:.2f} (80% used)")
