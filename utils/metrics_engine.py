"""
Metrics Engine - Time-series simulation for GPU metrics
Supports both live Cloud Run integration and chaos simulation mode
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random


class MetricsEngine:
    """
    Hybrid metrics engine that works with or without real GPU services
    Falls back gracefully to simulation mode if Cloud Run services unavailable
    """
    
    def __init__(self, mode: str = "chaos"):
        """
        Initialize metrics engine
        
        Args:
            mode: "live" for real Cloud Run, "chaos" for simulation
        """
        self.mode = mode
        self.current_time = datetime.now()
        self.baseline_metrics = {
            "gpu_utilization": 45.0,
            "gpu_memory": 8192,  # MB
            "gpu_temperature": 65.0,  # Celsius
            "request_latency": 120.0,  # ms
            "requests_per_second": 50.0,
            "error_rate": 0.1,  # percentage
            "active_instances": 2,
        }
        
    def generate_time_series(
        self, 
        duration_minutes: int = 60,
        interval_seconds: int = 10,
        scenario: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Generate realistic time-series metrics
        
        Args:
            duration_minutes: How many minutes of data to generate
            interval_seconds: Data point interval
            scenario: Optional chaos scenario to apply
            
        Returns:
            DataFrame with timestamp and all metrics
        """
        num_points = (duration_minutes * 60) // interval_seconds
        timestamps = [
            self.current_time - timedelta(seconds=i * interval_seconds)
            for i in range(num_points, 0, -1)
        ]
        
        data = {
            "timestamp": timestamps,
            "gpu_utilization": self._generate_metric_series(
                num_points, self.baseline_metrics["gpu_utilization"], 
                variance=10, scenario=scenario
            ),
            "gpu_memory": self._generate_metric_series(
                num_points, self.baseline_metrics["gpu_memory"],
                variance=512, scenario=scenario
            ),
            "gpu_temperature": self._generate_metric_series(
                num_points, self.baseline_metrics["gpu_temperature"],
                variance=5, scenario=scenario
            ),
            "request_latency": self._generate_metric_series(
                num_points, self.baseline_metrics["request_latency"],
                variance=30, scenario=scenario
            ),
            "requests_per_second": self._generate_metric_series(
                num_points, self.baseline_metrics["requests_per_second"],
                variance=15, scenario=scenario
            ),
            "error_rate": self._generate_metric_series(
                num_points, self.baseline_metrics["error_rate"],
                variance=0.05, scenario=scenario, min_val=0, max_val=5
            ),
            "active_instances": self._generate_instance_series(
                num_points, scenario=scenario
            ),
        }
        
        df = pd.DataFrame(data)
        
        # Apply chaos scenario if specified
        if scenario:
            df = self._apply_chaos_scenario(df, scenario)
            
        return df
    
    def _generate_metric_series(
        self,
        num_points: int,
        baseline: float,
        variance: float,
        scenario: Optional[str] = None,
        min_val: Optional[float] = None,
        max_val: Optional[float] = None
    ) -> List[float]:
        """Generate realistic metric series with noise and trends"""
        series = []
        current_value = baseline
        
        for i in range(num_points):
            # Add random walk
            current_value += np.random.normal(0, variance * 0.1)
            
            # Add some cyclical pattern (simulates daily traffic)
            cycle = np.sin(2 * np.pi * i / (num_points / 3)) * variance * 0.3
            
            # Add noise
            noise = np.random.normal(0, variance * 0.2)
            
            value = current_value + cycle + noise
            
            # Clamp values
            if min_val is not None:
                value = max(value, min_val)
            if max_val is not None:
                value = min(value, max_val)
                
            series.append(value)
            
        return series
    
    def _generate_instance_series(
        self,
        num_points: int,
        scenario: Optional[str] = None
    ) -> List[int]:
        """Generate instance count series (stays constant unless scaling)"""
        base_instances = self.baseline_metrics["active_instances"]
        series = [base_instances] * num_points
        
        # Add occasional scaling events
        if random.random() > 0.7:
            scale_point = random.randint(num_points // 3, 2 * num_points // 3)
            for i in range(scale_point, num_points):
                series[i] = base_instances + random.choice([1, 2])
                
        return series
    
    def _apply_chaos_scenario(self, df: pd.DataFrame, scenario: str) -> pd.DataFrame:
        """Apply chaos engineering scenario to metrics"""
        num_points = len(df)
        incident_start = num_points // 2  # Start incident halfway through
        incident_duration = num_points // 4  # Last 25% of timeline
        
        if scenario == "gpu_spike":
            # Gradual GPU utilization spike
            for i in range(incident_start, min(incident_start + incident_duration, num_points)):
                progress = (i - incident_start) / incident_duration
                df.loc[i, "gpu_utilization"] = 45 + (progress * 50)  # Ramp to 95%
                df.loc[i, "gpu_temperature"] = 65 + (progress * 20)  # Heat up
                df.loc[i, "request_latency"] = 120 + (progress * 300)  # Slow down
                
        elif scenario == "memory_leak":
            # Memory gradually fills up
            for i in range(incident_start, min(incident_start + incident_duration, num_points)):
                progress = (i - incident_start) / incident_duration
                df.loc[i, "gpu_memory"] = 8192 + (progress * 15000)  # Fill to 23GB
                df.loc[i, "gpu_utilization"] = 45 + (progress * 30)
                
        elif scenario == "latency_spike":
            # Sudden latency increase
            for i in range(incident_start, min(incident_start + incident_duration, num_points)):
                df.loc[i, "request_latency"] = 120 + random.uniform(500, 1500)
                df.loc[i, "error_rate"] = 0.1 + random.uniform(2, 8)
                
        elif scenario == "instance_crash":
            # Instance crashes, then recovers
            crash_point = incident_start + incident_duration // 2
            for i in range(incident_start, crash_point):
                df.loc[i, "active_instances"] = max(1, df.loc[i, "active_instances"] - 1)
                df.loc[i, "error_rate"] = 0.1 + random.uniform(5, 15)
                df.loc[i, "request_latency"] = 120 + random.uniform(800, 2000)
                
        return df
    
    def get_current_metrics(self) -> Dict[str, float]:
        """Get current snapshot of metrics"""
        if self.mode == "live":
            # TODO: Fetch from real Cloud Run service
            return self._get_simulated_metrics()
        else:
            return self._get_simulated_metrics()
    
    def _get_simulated_metrics(self) -> Dict[str, float]:
        """Generate current metrics snapshot"""
        return {
            "gpu_utilization": self.baseline_metrics["gpu_utilization"] + np.random.normal(0, 5),
            "gpu_memory": self.baseline_metrics["gpu_memory"] + np.random.normal(0, 256),
            "gpu_temperature": self.baseline_metrics["gpu_temperature"] + np.random.normal(0, 2),
            "request_latency": self.baseline_metrics["request_latency"] + np.random.normal(0, 20),
            "requests_per_second": self.baseline_metrics["requests_per_second"] + np.random.normal(0, 10),
            "error_rate": max(0, self.baseline_metrics["error_rate"] + np.random.normal(0, 0.1)),
            "active_instances": self.baseline_metrics["active_instances"],
            "timestamp": datetime.now().isoformat(),
        }
    
    def detect_anomaly(self, metrics: Dict[str, float]) -> Optional[Dict]:
        """
        Simple anomaly detection based on thresholds
        
        Returns:
            Anomaly details if detected, None otherwise
        """
        anomalies = []
        
        if metrics["gpu_utilization"] > 85:
            anomalies.append({
                "metric": "gpu_utilization",
                "value": metrics["gpu_utilization"],
                "threshold": 85,
                "severity": "high" if metrics["gpu_utilization"] > 95 else "medium"
            })
            
        if metrics["gpu_memory"] > 20000:  # 20GB
            anomalies.append({
                "metric": "gpu_memory",
                "value": metrics["gpu_memory"],
                "threshold": 20000,
                "severity": "high"
            })
            
        if metrics["request_latency"] > 500:
            anomalies.append({
                "metric": "request_latency",
                "value": metrics["request_latency"],
                "threshold": 500,
                "severity": "medium"
            })
            
        if metrics["error_rate"] > 5:
            anomalies.append({
                "metric": "error_rate",
                "value": metrics["error_rate"],
                "threshold": 5,
                "severity": "critical"
            })
            
        return anomalies if anomalies else None
