"""
AI Diagnosis Engine - Gemini 2.0 Flash integration for root cause analysis
Implements multi-tier fallback strategy for reliability
"""

import os
from typing import Dict, Optional, List
import google.generativeai as genai
from datetime import datetime
import requests


class AIDiagnosisEngine:
    """
    AI-powered root cause analysis using Gemini 2.0 Flash
    Falls back gracefully through multiple model tiers
    """
    
    def __init__(self, api_key: Optional[str] = None, use_local: bool = True):
        """
        Initialize AI diagnosis engine
        
        Args:
            api_key: Gemini API key (defaults to env variable)
            use_local: Try local Ollama first before cloud
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        self.use_local = use_local
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.ollama_model = os.getenv("OLLAMA_DEFAULT_MODEL", "gemma:2b")
        
        # Check if local Ollama is available
        self.local_available = self._check_ollama()
        
        # Configure Gemini if API key available
        if self.api_key:
            genai.configure(api_key=self.api_key)
        
        # Model tier strategy
        self.models = {
            "local_fast": self.ollama_model,
            "local_quality": "gemma:7b",
            "primary": os.getenv("GEMINI_PRIMARY_MODEL", "gemini-2.0-flash-exp"),
            "fallback": os.getenv("GEMINI_FALLBACK_MODEL", "gemini-1.5-flash-latest"),
            "premium": os.getenv("GEMINI_PREMIUM_MODEL", "gemini-1.5-pro-latest"),
        }
        
        self.current_model = self.models["local_fast"] if self.local_available else self.models["primary"]
    
    def _check_ollama(self) -> bool:
        """Check if Ollama server is running"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False
        
    def analyze_incident(
        self,
        metrics: Dict,
        scenario: Optional[str] = None,
        use_premium: bool = False,
        force_local: bool = False
    ) -> Dict[str, str]:
        """
        Analyze incident and provide root cause analysis
        
        Args:
            metrics: Current metrics snapshot
            scenario: Optional scenario name for context
            use_premium: Use premium model for deep analysis
            force_local: Force use of local Ollama
            
        Returns:
            Dict with root_cause, recommendation, and confidence
        """
        # Try local Ollama first if available and preferred
        if (self.use_local or force_local) and self.local_available:
            try:
                return self._analyze_with_ollama(metrics, scenario, use_premium)
            except Exception as e:
                print(f"Local Ollama failed: {e}, falling back to cloud")
        
        # Try cloud Gemini
        if self.api_key:
            try:
                # Select model
                model_name = self.models["premium"] if use_premium else self.models["primary"]
                model = genai.GenerativeModel(model_name)
                
                # Build prompt
                prompt = self._build_analysis_prompt(metrics, scenario)
                
                # Generate analysis
                response = model.generate_content(prompt)
                
                # Parse response
                analysis = self._parse_response(response.text)
                analysis["model_used"] = model_name
                analysis["source"] = "cloud_gemini"
                analysis["timestamp"] = datetime.now().isoformat()
                
                return analysis
                
            except Exception as e:
                print(f"Cloud Gemini failed: {e}")
        
        # Final fallback to rules-based analysis
        return self._fallback_analysis(metrics, scenario, error="All AI models unavailable")
    
    def _analyze_with_ollama(
        self,
        metrics: Dict,
        scenario: Optional[str],
        use_quality: bool = False
    ) -> Dict[str, str]:
        """Analyze using local Ollama"""
        model = self.models["local_quality"] if use_quality else self.models["local_fast"]
        
        # Build prompt
        prompt = self._build_analysis_prompt(metrics, scenario)
        
        # Call Ollama API
        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 500
                }
            },
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            response_text = data.get('response', '')
            
            # Parse response
            analysis = self._parse_response(response_text)
            analysis["model_used"] = model
            analysis["source"] = "local_ollama"
            analysis["timestamp"] = datetime.now().isoformat()
            analysis["latency_ms"] = data.get('total_duration', 0) // 1_000_000  # Convert to ms
            
            return analysis
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    
    def _build_analysis_prompt(self, metrics: Dict, scenario: Optional[str]) -> str:
        """Build detailed prompt for Gemini"""
        prompt = f"""You are an expert Site Reliability Engineer analyzing a GPU workload incident.

**Current Metrics:**
- GPU Utilization: {metrics.get('gpu_utilization', 'N/A')}%
- GPU Memory: {metrics.get('gpu_memory', 'N/A')} MB
- GPU Temperature: {metrics.get('gpu_temperature', 'N/A')}°C
- Request Latency: {metrics.get('request_latency', 'N/A')} ms
- Requests/Second: {metrics.get('requests_per_second', 'N/A')}
- Error Rate: {metrics.get('error_rate', 'N/A')}%
- Active Instances: {metrics.get('active_instances', 'N/A')}

**Service Context:**
- Service: ollama-gemma3-270m-gpu (Cloud Run with NVIDIA L4)
- Region: europe-west1
- Model: Gemma 3 (270M parameters)
- Runtime: vLLM acceleration

"""
        
        if scenario:
            prompt += f"**Known Scenario:** {scenario}\n\n"
        
        prompt += """**Task:**
Provide a concise root cause analysis and actionable recommendation.

**Response Format:**
ROOT CAUSE: [2-3 sentences explaining what went wrong and why]

RECOMMENDATION: [Specific action to take, including technical details]

CONFIDENCE: [high/medium/low based on metric clarity]

Keep your response professional, technical, and actionable for an SRE team."""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> Dict[str, str]:
        """Parse Gemini response into structured format"""
        lines = response_text.strip().split('\n')
        
        root_cause = ""
        recommendation = ""
        confidence = "medium"
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("ROOT CAUSE:"):
                current_section = "root_cause"
                root_cause = line.replace("ROOT CAUSE:", "").strip()
            elif line.startswith("RECOMMENDATION:"):
                current_section = "recommendation"
                recommendation = line.replace("RECOMMENDATION:", "").strip()
            elif line.startswith("CONFIDENCE:"):
                current_section = "confidence"
                confidence = line.replace("CONFIDENCE:", "").strip().lower()
            elif current_section and line:
                if current_section == "root_cause":
                    root_cause += " " + line
                elif current_section == "recommendation":
                    recommendation += " " + line
        
        return {
            "root_cause": root_cause.strip() or "Unable to determine root cause from current metrics.",
            "recommendation": recommendation.strip() or "Monitor metrics and collect more data.",
            "confidence": confidence if confidence in ["high", "medium", "low"] else "medium",
        }
    
    def _fallback_analysis(
        self,
        metrics: Dict,
        scenario: Optional[str],
        error: str = ""
    ) -> Dict[str, str]:
        """
        Rules-based fallback analysis when AI fails
        Ensures the system never completely fails
        """
        root_cause = "AI analysis unavailable. "
        recommendation = ""
        confidence = "low"
        
        # Simple rules-based analysis
        gpu_util = metrics.get("gpu_utilization", 0)
        gpu_memory = metrics.get("gpu_memory", 0)
        latency = metrics.get("request_latency", 0)
        error_rate = metrics.get("error_rate", 0)
        
        if gpu_util > 90:
            root_cause += "GPU utilization critically high (>90%). Likely cause: insufficient GPU capacity for current workload."
            recommendation = "Scale GPU instances from current count to handle increased load. Consider implementing request queuing."
            confidence = "high"
            
        elif gpu_memory > 20000:
            root_cause += "GPU memory critically high (>20GB). Likely cause: memory leak or large batch processing."
            recommendation = "Restart affected instances to clear memory. Investigate memory usage patterns and implement cleanup routines."
            confidence = "high"
            
        elif latency > 1000:
            root_cause += "Request latency critically high (>1000ms). Likely cause: network congestion or GPU bottleneck."
            recommendation = "Check network connectivity and GPU queue depth. Consider enabling multi-region failover."
            confidence = "medium"
            
        elif error_rate > 5:
            root_cause += "Error rate critically high (>5%). Likely cause: service instability or resource exhaustion."
            recommendation = "Review error logs for patterns. Consider scaling instances or implementing circuit breaker."
            confidence = "medium"
        else:
            root_cause += "Metrics within normal ranges. No immediate action required."
            recommendation = "Continue monitoring. Set up proactive alerts for early detection."
            confidence = "low"
        
        return {
            "root_cause": root_cause,
            "recommendation": recommendation,
            "confidence": confidence,
            "model_used": "rules-based-fallback",
            "timestamp": datetime.now().isoformat(),
            "error": error,
        }
    
    def generate_blog_post(self, incident_data: Dict) -> str:
        """
        Generate a blog post about an incident using Gemini
        
        Args:
            incident_data: Complete incident object
            
        Returns:
            Markdown-formatted blog post
        """
        try:
            model = genai.GenerativeModel(self.models["premium"])
            
            prompt = f"""Write a technical blog post about this GPU incident for a Site Reliability Engineering audience.

**Incident Details:**
- Trace ID: {incident_data['trace_id']}
- Scenario: {incident_data['scenario_name']}
- Duration: {incident_data['duration_minutes']} minutes
- Severity: {incident_data['severity']}
- Root Cause: {incident_data['root_cause']}
- Resolution: {incident_data['ai_recommendation']}

**Requirements:**
- 800-1200 words
- Technical but accessible
- Include lessons learned
- Markdown format with headers
- Professional tone

**Structure:**
1. Executive Summary
2. Incident Timeline
3. Technical Analysis
4. Resolution Steps
5. Lessons Learned
6. Preventive Measures
"""
            
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"# Incident Report: {incident_data['trace_id']}\n\nBlog post generation failed: {str(e)}"
    
    def predict_scaling_need(self, metrics_history: List[Dict]) -> Dict:
        """
        Predict if scaling is needed based on metric trends
        
        Args:
            metrics_history: List of recent metric snapshots
            
        Returns:
            Prediction with confidence and recommended action
        """
        if len(metrics_history) < 5:
            return {
                "should_scale": False,
                "confidence": "low",
                "reason": "Insufficient data for prediction"
            }
        
        # Calculate trends
        recent_gpu = [m.get("gpu_utilization", 0) for m in metrics_history[-5:]]
        avg_gpu = sum(recent_gpu) / len(recent_gpu)
        trend = recent_gpu[-1] - recent_gpu[0]  # Positive = increasing
        
        should_scale = False
        reason = ""
        
        if avg_gpu > 80 and trend > 10:
            should_scale = True
            reason = f"GPU utilization trending upward ({trend:.1f}% increase) with average {avg_gpu:.1f}%"
        elif avg_gpu > 90:
            should_scale = True
            reason = f"GPU utilization critically high at {avg_gpu:.1f}%"
        else:
            reason = f"GPU utilization stable at {avg_gpu:.1f}%"
        
        return {
            "should_scale": should_scale,
            "confidence": "high" if abs(trend) > 15 else "medium",
            "reason": reason,
            "current_avg": round(avg_gpu, 1),
            "trend": round(trend, 1),
        }
