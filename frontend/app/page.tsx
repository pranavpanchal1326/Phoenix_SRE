"use client"

import { useState, useEffect } from 'react';
import { StatusBanner } from '@/components/dashboard/StatusBanner';
// import { GPUUtilizationChart } from '@/components/charts/GPUUtilizationChart'; // Temporarily disabled due to recharts dependency issue
import { ChaosScenarioCard } from '@/components/dashboard/ChaosScenarioCard';
import { useWebSocket } from '@/hooks/useWebSocket';
import { Activity, Zap, AlertTriangle, XCircle, TrendingUp, DollarSign } from 'lucide-react';
import { motion } from 'framer-motion';

interface Metrics {
  gpu_util: number;
  latency_p95: number;
  error_rate: number;
  memory_usage: number;
  queue_depth: number;
  instance_count: number;
  cost_per_hour: number;
  timestamp: string;
}

export default function DashboardPage() {
  const { socket, connected } = useWebSocket();
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [gpuHistory, setGpuHistory] = useState<Array<{ timestamp: number; value: number }>>([]);
  const [status, setStatus] = useState<'healthy' | 'warning' | 'critical'>('healthy');

  useEffect(() => {
    if (!socket || !connected) return;

    socket.on('metrics:update', (data: { data: Metrics }) => {
      const newMetrics = data.data;
      setMetrics(newMetrics);

      // Update GPU history (keep last 50 points)
      setGpuHistory(prev => {
        const newHistory = [...prev, {
          timestamp: Date.now(),
          value: newMetrics.gpu_util
        }];
        return newHistory.slice(-50);
      });

      // Determine status
      if (newMetrics.gpu_util > 90 || newMetrics.error_rate > 5) {
        setStatus('critical');
      } else if (newMetrics.gpu_util > 80 || newMetrics.error_rate > 1) {
        setStatus('warning');
      } else {
        setStatus('healthy');
      }
    });

    return () => {
      socket.off('metrics:update');
    };
  }, [socket, connected]);

  const chaosScenarios = [
    {
      id: 'gpu-saturation',
      title: 'GPU Saturation Attack',
      description: 'Saturate GPU to 95%+ utilization to test auto-scaling and performance degradation handling.',
      icon: Zap,
      riskLevel: 'high' as const,
      duration: '5 min',
      costImpact: '$0.12'
    },
    {
      id: 'latency-spike',
      title: 'Latency Spike Injection',
      description: 'Inject 2000ms+ latency into requests to test timeout handling and user experience.',
      icon: Activity,
      riskLevel: 'medium' as const,
      duration: '3 min',
      costImpact: '$0.07'
    },
    {
      id: 'error-burst',
      title: 'Error Burst Simulation',
      description: 'Generate 5%+ error rate to test error handling, retry logic, and alerting systems.',
      icon: AlertTriangle,
      riskLevel: 'medium' as const,
      duration: '2 min',
      costImpact: '$0.05'
    },
    {
      id: 'instance-crash',
      title: 'Instance Crash Test',
      description: 'Simulate instance failure to test auto-recovery, failover, and service continuity.',
      icon: XCircle,
      riskLevel: 'critical' as const,
      duration: '1 min',
      costImpact: '$0.02'
    }
  ];

  const handleTriggerChaos = async (scenarioId: string) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8081'}/api/chaos/trigger`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          scenario_id: scenarioId,
          duration: 300,
          intensity: 'medium'
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to trigger chaos scenario');
      }

      const data = await response.json();
      console.log('Chaos scenario triggered:', data);
    } catch (error) {
      console.error('Error triggering chaos scenario:', error);
    }
  };

  // Removed blocking connection check - dashboard renders immediately, WebSocket connects in background
  /*
  if (!connected) {
    // Show loading for max 5 seconds, then show dashboard anyway
    setTimeout(() => {
      if (!connected) {
        console.log('WebSocket connection timeout - showing dashboard anyway');
      }
    }, 5000);
    
    return (
      <div className="min-h-screen flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-center space-y-4"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="h-16 w-16 mx-auto rounded-full border-4 border-primary border-t-transparent"
          />
          <p className="text-xl font-semibold text-foreground">Connecting to Phoenix SRE...</p>
          <p className="text-sm text-muted">Establishing WebSocket connection</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-4 px-4 py-2 bg-primary text-primary-foreground rounded-lg hover:bg-primary/90"
          >
            Skip & Continue
          </button>
        </motion.div>
      </div>
    );
  }
  */

  return (
    <div className="min-h-screen bg-background p-6 space-y-6">
      {/* Status Banner - Full Width */}
      {metrics && (
        <StatusBanner
          status={status}
          metrics={{
            gpuUtil: metrics.gpu_util,
            instanceCount: metrics.instance_count,
            costPerHour: metrics.cost_per_hour
          }}
          budget={{
            total: 10.00,
            remaining: 6.40
          }}
        />
      )}

      {/* Metrics Grid */}
      <div className="grid grid-cols-12 gap-6">
        {/* Left Column - Charts */}
        <div className="col-span-8 space-y-6">
          {/* GPU Utilization Chart - Temporarily disabled */}
          {/* {metrics && (
            <GPUUtilizationChart
              data={gpuHistory}
              currentValue={metrics.gpu_util}
            />
          )} */}

          {/* Placeholder for GPU Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card p-6 h-96 flex items-center justify-center"
          >
            <div className="text-center">
              <Activity className="h-16 w-16 text-primary mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-foreground mb-2">GPU Utilization Chart</h3>
              <p className="text-sm text-muted">Real-time chart coming soon</p>
              {metrics && (
                <p className="text-4xl font-bold font-mono text-primary mt-4">
                  {metrics.gpu_util.toFixed(1)}%
                </p>
              )}
            </div>
          </motion.div>

          {/* Additional Metrics Row */}
          <div className="grid grid-cols-3 gap-6">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="glass-card p-6"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="h-10 w-10 rounded-lg bg-info/10 flex items-center justify-center">
                  <TrendingUp className="h-5 w-5 text-info" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">P95 Latency</h3>
              </div>
              <p className="metric-value text-foreground">
                {metrics?.latency_p95 || 0}ms
              </p>
              <p className="text-sm text-muted mt-1">95th percentile</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="glass-card p-6"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="h-10 w-10 rounded-lg bg-danger/10 flex items-center justify-center">
                  <AlertTriangle className="h-5 w-5 text-danger" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">Error Rate</h3>
              </div>
              <p className="metric-value text-foreground">
                {metrics?.error_rate.toFixed(2) || 0}%
              </p>
              <p className="text-sm text-muted mt-1">Last 5 minutes</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="glass-card p-6"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="h-10 w-10 rounded-lg bg-warning/10 flex items-center justify-center">
                  <DollarSign className="h-5 w-5 text-warning" />
                </div>
                <h3 className="text-lg font-semibold text-foreground">Queue Depth</h3>
              </div>
              <p className="metric-value text-foreground">
                {metrics?.queue_depth || 0}
              </p>
              <p className="text-sm text-muted mt-1">Pending requests</p>
            </motion.div>
          </div>
        </div>

        {/* Right Column - AI Insights Placeholder */}
        <div className="col-span-4">
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="glass-card p-6 h-full"
          >
            <h3 className="text-lg font-semibold text-foreground mb-4">AI Insights</h3>
            <div className="space-y-4">
              <div className="p-4 rounded-lg bg-primary/5 border border-primary/20">
                <p className="text-sm text-foreground font-medium mb-2">System Health: Optimal</p>
                <p className="text-xs text-muted">All metrics within normal ranges. No anomalies detected.</p>
              </div>
              <div className="p-4 rounded-lg bg-success/5 border border-success/20">
                <p className="text-sm text-foreground font-medium mb-2">Cost Optimization</p>
                <p className="text-xs text-muted">Current configuration is cost-efficient. No recommendations.</p>
              </div>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Chaos Engineering Section */}
      <div className="space-y-4">
        <h2 className="text-2xl font-bold text-foreground">Chaos Engineering</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {chaosScenarios.map((scenario, index) => (
            <motion.div
              key={scenario.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <ChaosScenarioCard
                {...scenario}
                onTrigger={() => handleTriggerChaos(scenario.id)}
              />
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
