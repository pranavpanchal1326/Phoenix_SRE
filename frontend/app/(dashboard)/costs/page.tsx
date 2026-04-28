"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { DollarSign, TrendingDown, TrendingUp, AlertCircle } from 'lucide-react';
import { useRealtimeMetrics } from '@/hooks/useRealtimeMetrics';

export default function CostsPage() {
    const { metrics } = useRealtimeMetrics();

    const budgetLimit = 10.00;
    const currentSpend = 3.60;
    const budgetUsed = (currentSpend / budgetLimit) * 100;
    const remaining = budgetLimit - currentSpend;

    const costBreakdown = [
        { service: 'Gemma GPU (Cloud Run)', cost: 4.20, percentage: 42 },
        { service: 'ADK Agent (Cloud Run)', cost: 0.16, percentage: 1.6 },
        { service: 'Gemini API', cost: 0.01, percentage: 0.1 },
        { service: 'BigQuery', cost: 0.50, percentage: 5 },
        { service: 'Networking', cost: 0.50, percentage: 5 },
        { service: 'Cloud Storage', cost: 0.05, percentage: 0.5 },
    ];

    return (
        <div className="container mx-auto p-6 space-y-6">
            {/* Header */}
            <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Cost Tracking</h1>
                <p className="text-muted-foreground">
                    Monitor budget usage and optimize costs
                </p>
            </div>

            {/* Budget Overview */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="glass-card col-span-2">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <DollarSign className="h-5 w-5" />
                            Budget Overview
                        </CardTitle>
                        <CardDescription>
                            $10.00 GCP credit limit for BNB Marathon 2025
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        {/* Budget Bar */}
                        <div className="space-y-2">
                            <div className="flex items-center justify-between text-sm">
                                <span className="text-muted-foreground">Budget Used</span>
                                <span className="font-medium">{budgetUsed.toFixed(1)}%</span>
                            </div>
                            <div className="h-4 bg-muted rounded-full overflow-hidden">
                                <div
                                    className="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all duration-500"
                                    style={{ width: `${budgetUsed}%` }}
                                />
                            </div>
                        </div>

                        {/* Stats Grid */}
                        <div className="grid grid-cols-3 gap-4 pt-4">
                            <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">Total Budget</p>
                                <p className="text-2xl font-bold">${budgetLimit.toFixed(2)}</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">Current Spend</p>
                                <p className="text-2xl font-bold text-blue-500">${currentSpend.toFixed(2)}</p>
                            </div>
                            <div className="space-y-1">
                                <p className="text-sm text-muted-foreground">Remaining</p>
                                <p className="text-2xl font-bold text-green-500">${remaining.toFixed(2)}</p>
                            </div>
                        </div>
                    </CardContent>
                </Card>

                <Card className="glass-card">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <TrendingDown className="h-5 w-5 text-green-500" />
                            Cost Savings
                        </CardTitle>
                        <CardDescription>
                            Hybrid LLM strategy
                        </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-muted-foreground">Gemma (Local)</span>
                                <Badge variant="outline" className="bg-green-500/20 text-green-400">
                                    FREE
                                </Badge>
                            </div>
                            <div className="flex items-center justify-between">
                                <span className="text-sm text-muted-foreground">Gemini (Cloud)</span>
                                <Badge variant="outline" className="bg-blue-500/20 text-blue-400">
                                    $0.25/1M
                                </Badge>
                            </div>
                        </div>
                        <div className="pt-4 border-t">
                            <p className="text-3xl font-bold text-green-500">80%</p>
                            <p className="text-sm text-muted-foreground">Cost Reduction</p>
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Cost Breakdown */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle>Cost Breakdown</CardTitle>
                    <CardDescription>
                        Estimated costs for 6-hour demo
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        {costBreakdown.map((item, index) => (
                            <div key={index} className="space-y-2">
                                <div className="flex items-center justify-between text-sm">
                                    <span className="font-medium">{item.service}</span>
                                    <span className="text-muted-foreground">${item.cost.toFixed(2)}</span>
                                </div>
                                <div className="h-2 bg-muted rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-gradient-to-r from-blue-500 to-cyan-500"
                                        style={{ width: `${item.percentage}%` }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </CardContent>
            </Card>

            {/* Real-Time Cost */}
            {metrics && (
                <Card className="glass-card border-blue-500/50">
                    <CardHeader>
                        <CardTitle className="flex items-center gap-2">
                            <Badge variant="outline" className="bg-blue-500/20 text-blue-400">
                                LIVE
                            </Badge>
                            Real-Time Cost
                        </CardTitle>
                        <CardDescription>
                            Current cost per hour based on active services
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-baseline gap-2">
                            <p className="text-4xl font-bold">${metrics.cost_per_hour.toFixed(2)}</p>
                            <span className="text-muted-foreground">/hour</span>
                        </div>
                        <p className="text-sm text-muted-foreground mt-2">
                            Projected 6-hour cost: ${(metrics.cost_per_hour * 6).toFixed(2)}
                        </p>
                    </CardContent>
                </Card>
            )}

            {/* Optimization Recommendations */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <TrendingUp className="h-5 w-5" />
                        Optimization Recommendations
                    </CardTitle>
                    <CardDescription>
                        AI-powered cost optimization suggestions
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <div className="space-y-4">
                        <div className="flex items-start gap-3">
                            <AlertCircle className="h-5 w-5 text-blue-500 mt-0.5" />
                            <div className="space-y-1">
                                <p className="text-sm font-medium">Scale-to-Zero Enabled</p>
                                <p className="text-sm text-muted-foreground">
                                    All Cloud Run services scale to 0 when idle, saving ~60% on costs
                                </p>
                            </div>
                        </div>
                        <div className="flex items-start gap-3">
                            <AlertCircle className="h-5 w-5 text-green-500 mt-0.5" />
                            <div className="space-y-1">
                                <p className="text-sm font-medium">Hybrid LLM Strategy Active</p>
                                <p className="text-sm text-muted-foreground">
                                    Using Gemma for simple tasks saves $250/1M tokens vs Gemini
                                </p>
                            </div>
                        </div>
                        <div className="flex items-start gap-3">
                            <AlertCircle className="h-5 w-5 text-yellow-500 mt-0.5" />
                            <div className="space-y-1">
                                <p className="text-sm font-medium">Request Batching Enabled</p>
                                <p className="text-sm text-muted-foreground">
                                    Batching API calls reduces overhead by 40%
                                </p>
                            </div>
                        </div>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
