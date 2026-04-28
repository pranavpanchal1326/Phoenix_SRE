"""
Phoenix SRE: Analysis Agent
Root cause analysis using Gemini AI
"""

import logging
from typing import Dict, List
import os
import google.generativeai as genai

logger = logging.getLogger(__name__)

class AnalysisAgent:
    """
    Analysis agent for root cause analysis
    
    Uses Gemini 2.5 Pro for deep reasoning and analysis
    """
    
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-2.0-flash-exp')
            self.enabled = True
            logger.info("✅ Analysis agent initialized with Gemini 2.0 Flash")
        else:
            self.model = None
            self.enabled = False
            logger.warning("⚠️ Gemini API key not found, using rules-based analysis")
    
    async def diagnose(self, anomalies: List[Dict], metrics: Dict) -> Dict:
        """
        Diagnose root cause of anomalies
        
        Args:
            anomalies: List of detected anomalies
            metrics: Current metrics
            
        Returns:
            Root cause analysis
        """
        try:
            if self.enabled and self.model:
                return await self._gemini_analysis(anomalies, metrics)
            else:
                return self._rules_based_analysis(anomalies, metrics)
                
        except Exception as e:
            logger.error(f"❌ Error in diagnosis: {e}")
            return self._rules_based_analysis(anomalies, metrics)
    
    async def _gemini_analysis(self, anomalies: List[Dict], metrics: Dict) -> Dict:
        """Use Gemini for deep analysis"""
        prompt = f"""You are an expert SRE analyzing a production incident.

**Anomalies Detected:**
{self._format_anomalies(anomalies)}

**Current Metrics:**
- GPU Utilization: {metrics.get('gpu_util', 0):.1f}%
- P95 Latency: {metrics.get('latency_p95', 0):.0f}ms
- Error Rate: {metrics.get('error_rate', 0):.2f}%
- Memory Usage: {metrics.get('memory_usage', 0):.1f}%
- Queue Depth: {metrics.get('queue_depth', 0)}
- Requests/sec: {metrics.get('requests_per_sec', 0)}
- Instance Count: {metrics.get('instance_count', 0)}

**Task:**
1. Identify the root cause
2. Assess the impact
3. Provide confidence score (0-100)
4. Suggest immediate remediation steps

Be concise and actionable."""

        try:
            response = self.model.generate_content(prompt)
            
            return {
                "analysis": response.text,
                "confidence": 85,  # Gemini analysis
                "source": "gemini-2.0-flash",
                "timestamp": metrics.get("timestamp")
            }
        except Exception as e:
            logger.error(f"❌ Gemini analysis failed: {e}")
            return self._rules_based_analysis(anomalies, metrics)
    
    def _rules_based_analysis(self, anomalies: List[Dict], metrics: Dict) -> Dict:
        """Fallback rules-based analysis"""
        root_causes = []
        
        for anomaly in anomalies:
            if anomaly["type"] == "gpu_saturation":
                root_causes.append({
                    "cause": "GPU Overload",
                    "description": "GPU utilization exceeded 95%, indicating compute saturation",
                    "impact": "High latency, request queueing, potential timeouts",
                    "recommendation": "Scale up GPU instances or reduce request rate"
                })
            elif anomaly["type"] == "latency_spike":
                root_causes.append({
                    "cause": "Latency Degradation",
                    "description": f"P95 latency at {anomaly['value']:.0f}ms, exceeding threshold",
                    "impact": "Poor user experience, potential SLA violations",
                    "recommendation": "Investigate slow queries, optimize model inference"
                })
            elif anomaly["type"] == "error_burst":
                root_causes.append({
                    "cause": "Error Rate Spike",
                    "description": f"Error rate at {anomaly['value']:.2f}%, indicating failures",
                    "impact": "Service degradation, failed requests",
                    "recommendation": "Check logs, investigate error patterns"
                })
        
        return {
            "analysis": self._format_root_causes(root_causes),
            "confidence": 70,  # Rules-based
            "source": "rules-engine",
            "root_causes": root_causes,
            "timestamp": metrics.get("timestamp")
        }
    
    def _format_anomalies(self, anomalies: List[Dict]) -> str:
        """Format anomalies for prompt"""
        lines = []
        for i, anomaly in enumerate(anomalies, 1):
            lines.append(f"{i}. [{anomaly['severity'].upper()}] {anomaly['message']}")
        return "\n".join(lines)
    
    def _format_root_causes(self, root_causes: List[Dict]) -> str:
        """Format root causes as text"""
        lines = ["**Root Cause Analysis:**\n"]
        for i, cause in enumerate(root_causes, 1):
            lines.append(f"{i}. **{cause['cause']}**")
            lines.append(f"   - Description: {cause['description']}")
            lines.append(f"   - Impact: {cause['impact']}")
            lines.append(f"   - Recommendation: {cause['recommendation']}\n")
        return "\n".join(lines)
