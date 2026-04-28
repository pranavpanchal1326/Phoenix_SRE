"use client"

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Brain, Sparkles, DollarSign, Clock } from 'lucide-react';
import { useRealtimeMetrics } from '@/hooks/useRealtimeMetrics';

export default function AIPage() {
    const { metrics } = useRealtimeMetrics();
    const [aiSource, setAISource] = useState<'gemini' | 'gemma'>('gemini');
    const [analyzing, setAnalyzing] = useState(false);
    const [analysis, setAnalysis] = useState<string | null>(null);

    const handleAnalyze = async () => {
        setAnalyzing(true);

        // Simulate AI analysis
        setTimeout(() => {
            setAnalysis(`
**Root Cause Analysis**

Based on current metrics:
- GPU Utilization: ${metrics?.gpu_util.toFixed(1)}%
- P95 Latency: ${metrics?.latency_p95}ms
- Error Rate: ${metrics?.error_rate}%

**Findings:**
1. GPU utilization is ${metrics && metrics.gpu_util > 80 ? 'HIGH' : 'NORMAL'}
2. Latency is ${metrics && metrics.latency_p95 > 1000 ? 'ELEVATED' : 'ACCEPTABLE'}
3. Error rate is ${metrics && metrics.error_rate > 1 ? 'CONCERNING' : 'HEALTHY'}

**Recommendations:**
${metrics && metrics.gpu_util > 80 ? '- Consider scaling up GPU instances\n' : ''}
${metrics && metrics.latency_p95 > 1000 ? '- Optimize request processing\n' : ''}
${metrics && metrics.error_rate > 1 ? '- Investigate error patterns\n' : ''}
- Continue monitoring system health

**Confidence:** 85%
**Source:** ${aiSource === 'gemini' ? 'Gemini 2.0 Flash' : 'Gemma 3 270M'}
**Cost:** ${aiSource === 'gemini' ? '$0.0001' : '$0.00'}
      `.trim());
            setAnalyzing(false);
        }, 2000);
    };

    return (
        <div className="container mx-auto p-6 space-y-6">
            {/* Header */}
            <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">AI Diagnosis</h1>
                <p className="text-muted-foreground">
                    AI-powered root cause analysis and recommendations
                </p>
            </div>

            {/* AI Source Selector */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Brain className="h-5 w-5" />
                        AI Configuration
                    </CardTitle>
                    <CardDescription>
                        Choose between Gemini (cloud) or Gemma (local) for analysis
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">AI Source</label>
                            <Select value={aiSource} onValueChange={(value: 'gemini' | 'gemma') => setAISource(value)}>
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="gemini">
                                        <div className="flex items-center gap-2">
                                            <Sparkles className="h-4 w-4 text-blue-500" />
                                            Gemini 2.0 Flash (Cloud)
                                        </div>
                                    </SelectItem>
                                    <SelectItem value="gemma">
                                        <div className="flex items-center gap-2">
                                            <Sparkles className="h-4 w-4 text-green-500" />
                                            Gemma 3 270M (Local)
                                        </div>
                                    </SelectItem>
                                </SelectContent>
                            </Select>
                        </div>

                        <div className="space-y-2">
                            <label className="text-sm font-medium">Cost Estimate</label>
                            <div className="flex items-center gap-2 h-10 px-3 py-2 border rounded-md bg-muted">
                                <DollarSign className="h-4 w-4 text-muted-foreground" />
                                <span className="text-sm">
                                    {aiSource === 'gemini' ? '$0.25/1M tokens' : 'FREE (Self-hosted)'}
                                </span>
                            </div>
                        </div>
                    </div>

                    <Button
                        onClick={handleAnalyze}
                        disabled={analyzing || !metrics}
                        className="w-full"
                    >
                        {analyzing ? 'Analyzing...' : 'Run AI Analysis'}
                    </Button>
                </CardContent>
            </Card>

            {/* Current Metrics */}
            {metrics && (
                <Card className="glass-card">
                    <CardHeader>
                        <CardTitle>Current Metrics</CardTitle>
                        <CardDescription>Real-time system metrics for analysis</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                            <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">GPU Utilization</p>
                                <p className="text-2xl font-bold">{metrics.gpu_util.toFixed(1)}%</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">P95 Latency</p>
                                <p className="text-2xl font-bold">{metrics.latency_p95}ms</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">Error Rate</p>
                                <p className="text-2xl font-bold">{metrics.error_rate.toFixed(2)}%</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">Cost/Hour</p>
                                <p className="text-2xl font-bold">${metrics.cost_per_hour.toFixed(2)}</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* AI Analysis Results */}
            {analysis && (
                <Card className="glass-card border-blue-500/50">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Badge variant="outline" className="bg-blue-500/20 text-blue-400">
                                AI ANALYSIS
                            </Badge>
                            Analysis Results
                        </CardTitle>
                        <CardDescription>
                            Generated by {aiSource === 'gemini' ? 'Gemini 2.0 Flash' : 'Gemma 3 270M'}
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="prose prose-sm dark:prose-invert max-w-none">
                            <pre className="whitespace-pre-wrap font-sans text-sm">
                                {analysis}
                            </pre>
                        </div>
                    </CardContent>
                </Card>
            )}

            {/* Cost Comparison */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle>Hybrid LLM Strategy</CardTitle>
                    <CardDescription>
                        80% cost savings by using Gemma for simple tasks and Gemini for complex analysis
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <span className="text-sm">Gemma (Local)</span>
                                <Badge variant="outline" className="bg-green-500/20 text-green-400">
                                    FREE
                                </Badge>
                            </div>
                            <p className="text-xs text-muted-foreground">
                                Fast inference, simple tasks, 0 cost
                            </p>
                        </div>
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <span className="text-sm">Gemini (Cloud)</span>
                                <Badge variant="outline" className="bg-blue-500/20 text-blue-400">
                                    $0.25/1M
                                </Badge>
                            </div>
                            <p className="text-xs text-muted-foreground">
                                Deep reasoning, complex analysis, low cost
                            </p>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
