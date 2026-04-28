"""
Phoenix SRE: Monitoring Agent
Real-time anomaly detection and alerting
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class MonitoringAgent:
    """
    Monitoring agent for anomaly detection
    
    Uses statistical analysis and ML-based pattern recognition
    to detect anomalies in real-time metrics
    """
    
    def __init__(self):
        self.thresholds = {
            "gpu_util": {"warning": 80.0, "critical": 95.0},
            "latency_p95": {"warning": 1000, "critical": 2000},
            "error_rate": {"warning": 1.0, "critical": 5.0},
            "memory_usage": {"warning": 80.0, "critical": 90.0},
            "queue_depth": {"warning": 50, "critical": 100}
        }
        self.baseline = {}
        
    async def detect_anomalies(self, metrics: Dict) -> List[Dict]:
        """
        Detect anomalies in metrics
        
        Args:
            metrics: Current metrics
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        try:
            # Check GPU utilization
            if metrics.get("gpu_util", 0) > self.thresholds["gpu_util"]["critical"]:
                anomalies.append({
                    "type": "gpu_saturation",
                    "severity": "critical",
                    "metric": "gpu_util",
                    "value": metrics["gpu_util"],
                    "threshold": self.thresholds["gpu_util"]["critical"],
                    "message": f"GPU utilization at {metrics['gpu_util']:.1f}% (critical threshold: {self.thresholds['gpu_util']['critical']}%)"
                })
            elif metrics.get("gpu_util", 0) > self.thresholds["gpu_util"]["warning"]:
                anomalies.append({
                    "type": "gpu_high",
                    "severity": "warning",
                    "metric": "gpu_util",
                    "value": metrics["gpu_util"],
                    "threshold": self.thresholds["gpu_util"]["warning"],
                    "message": f"GPU utilization at {metrics['gpu_util']:.1f}% (warning threshold: {self.thresholds['gpu_util']['warning']}%)"
                })
            
            # Check latency
            if metrics.get("latency_p95", 0) > self.thresholds["latency_p95"]["critical"]:
                anomalies.append({
                    "type": "latency_spike",
                    "severity": "critical",
                    "metric": "latency_p95",
                    "value": metrics["latency_p95"],
                    "threshold": self.thresholds["latency_p95"]["critical"],
                    "message": f"P95 latency at {metrics['latency_p95']:.0f}ms (critical threshold: {self.thresholds['latency_p95']['critical']}ms)"
                })
            elif metrics.get("latency_p95", 0) > self.thresholds["latency_p95"]["warning"]:
                anomalies.append({
                    "type": "latency_high",
                    "severity": "warning",
                    "metric": "latency_p95",
                    "value": metrics["latency_p95"],
                    "threshold": self.thresholds["latency_p95"]["warning"],
                    "message": f"P95 latency at {metrics['latency_p95']:.0f}ms (warning threshold: {self.thresholds['latency_p95']['warning']}ms)"
                })
            
            # Check error rate
            if metrics.get("error_rate", 0) > self.thresholds["error_rate"]["critical"]:
                anomalies.append({
                    "type": "error_burst",
                    "severity": "critical",
                    "metric": "error_rate",
                    "value": metrics["error_rate"],
                    "threshold": self.thresholds["error_rate"]["critical"],
                    "message": f"Error rate at {metrics['error_rate']:.2f}% (critical threshold: {self.thresholds['error_rate']['critical']}%)"
                })
            elif metrics.get("error_rate", 0) > self.thresholds["error_rate"]["warning"]:
                anomalies.append({
                    "type": "error_elevated",
                    "severity": "warning",
                    "metric": "error_rate",
                    "value": metrics["error_rate"],
                    "threshold": self.thresholds["error_rate"]["warning"],
                    "message": f"Error rate at {metrics['error_rate']:.2f}% (warning threshold: {self.thresholds['error_rate']['warning']}%)"
                })
            
            # Check memory usage
            if metrics.get("memory_usage", 0) > self.thresholds["memory_usage"]["critical"]:
                anomalies.append({
                    "type": "memory_pressure",
                    "severity": "critical",
                    "metric": "memory_usage",
                    "value": metrics["memory_usage"],
                    "threshold": self.thresholds["memory_usage"]["critical"],
                    "message": f"Memory usage at {metrics['memory_usage']:.1f}% (critical threshold: {self.thresholds['memory_usage']['critical']}%)"
                })
            
            # Check queue depth
            if metrics.get("queue_depth", 0) > self.thresholds["queue_depth"]["critical"]:
                anomalies.append({
                    "type": "queue_overflow",
                    "severity": "critical",
                    "metric": "queue_depth",
                    "value": metrics["queue_depth"],
                    "threshold": self.thresholds["queue_depth"]["critical"],
                    "message": f"Queue depth at {metrics['queue_depth']} (critical threshold: {self.thresholds['queue_depth']['critical']})"
                })
            
            if anomalies:
                logger.warning(f"⚠️ Detected {len(anomalies)} anomalies")
                for anomaly in anomalies:
                    logger.warning(f"  - {anomaly['severity'].upper()}: {anomaly['message']}")
            
            return anomalies
            
        except Exception as e:
            logger.error(f"❌ Error detecting anomalies: {e}")
            return []
    
    def update_baseline(self, metrics: Dict):
        """Update baseline metrics for adaptive thresholds"""
        for key, value in metrics.items():
            if key not in self.baseline:
                self.baseline[key] = []
            
            self.baseline[key].append(value)
            
            # Keep only last 100 values
            if len(self.baseline[key]) > 100:
                self.baseline[key] = self.baseline[key][-100:]
