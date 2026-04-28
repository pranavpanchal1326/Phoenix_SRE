"""
Phoenix SRE: LLM Configuration
Intelligent routing between Gemma (local) and Gemini (cloud)
"""

import os
from enum import Enum
from dataclasses import dataclass
from typing import List, Optional

class ModelProvider(Enum):
    GEMMA = "gemma"
    GEMINI = "gemini"

@dataclass
class LLMConfig:
    provider: ModelProvider
    endpoint: Optional[str]
    model: str
    temperature: float
    max_tokens: int
    use_cases: List[str]
    cost_per_1m_tokens: float

class PhoenixLLMConfig:
    """
    Dual-LLM strategy for optimal cost vs. performance:
    
    - Gemma (self-hosted GPU): Fast, cheap, real-time monitoring
    - Gemini 2.5 Pro (API): Deep analysis, complex reasoning
    
    This hybrid approach saves ~80% on AI costs while maintaining
    high-quality insights.
    """
    
    # Fast inference for real-time decisions
    GEMMA_CONFIG = LLMConfig(
        provider=ModelProvider.GEMMA,
        endpoint=os.getenv('OLLAMA_URL'),
        model="gemma3:270m",
        temperature=0.3,
        max_tokens=512,
        use_cases=[
            "anomaly_classification",
            "quick_remediation_suggestions",
            "log_parsing",
            "metric_interpretation",
            "alert_triage",
            "simple_queries"
        ],
        cost_per_1m_tokens=0.0  # Self-hosted! 🎉
    )
    
    # Deep reasoning for complex analysis
    GEMINI_CONFIG = LLMConfig(
        provider=ModelProvider.GEMINI,
        endpoint=None,  # Uses Google AI SDK
        model="gemini-2.5-pro",
        temperature=0.2,
        max_tokens=2048,
        use_cases=[
            "root_cause_analysis",
            "incident_report_generation",
            "cost_optimization_strategy",
            "predictive_scaling_ml",
            "complex_troubleshooting",
            "strategic_recommendations"
        ],
        cost_per_1m_tokens=0.25  # API cost
    )
    
    @staticmethod
    def route_request(task_type: str, complexity: str = "simple") -> LLMConfig:
        """
        Intelligent routing based on task complexity
        
        Rules:
        1. If task is in Gemma use cases AND complexity is "simple" → Gemma
        2. If task requires deep reasoning OR complexity is "complex" → Gemini
        3. Default to Gemini for unknown tasks (safer)
        
        This saves ~80% on AI costs!
        """
        if task_type in PhoenixLLMConfig.GEMMA_CONFIG.use_cases and complexity == "simple":
            return PhoenixLLMConfig.GEMMA_CONFIG
        
        return PhoenixLLMConfig.GEMINI_CONFIG
    
    @staticmethod
    def estimate_cost(task_type: str, token_count: int) -> float:
        """Estimate cost for a specific task"""
        config = PhoenixLLMConfig.route_request(task_type)
        return (token_count / 1_000_000) * config.cost_per_1m_tokens
