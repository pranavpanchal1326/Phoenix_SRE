"use client"

import { useState } from 'react';
import { ChaosCard } from '@/components/dashboard/ChaosCard';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Zap, AlertTriangle, XCircle, Activity } from 'lucide-react';
import { useChaos } from '@/hooks/useChaos';

export default function ChaosPage() {
    const { triggerScenario, triggering, lastEvent } = useChaos();
    const [activeTab, setActiveTab] = useState('scenarios');

    const chaosScenarios = [
        {
            id: 'gpu-saturation',
            title: 'GPU Saturation Attack',
            description: 'Saturate GPU to 95%+ utilization to test auto-scaling',
            icon: <Zap className="h-6 w-6" />,
            severity: 'high' as const,
            duration: '5 min',
            costImpact: '$0.12'
        },
        {
            id: 'latency-spike',
            title: 'Latency Spike Injection',
            description: 'Inject 2000ms+ latency into requests',
            icon: <Activity className="h-6 w-6" />,
            severity: 'medium' as const,
            duration: '3 min',
            costImpact: '$0.07'
        },
        {
            id: 'error-burst',
            title: 'Error Burst Simulation',
            description: 'Generate 5%+ error rate to test error handling',
            icon: <AlertTriangle className="h-6 w-6" />,
            severity: 'medium' as const,
            duration: '2 min',
            costImpact: '$0.05'
        },
        {
            id: 'instance-crash',
            title: 'Instance Crash Test',
            description: 'Simulate instance failure and recovery',
            icon: <XCircle className="h-6 w-6" />,
            severity: 'critical' as const,
            duration: '1 min',
            costImpact: '$0.02'
        }
    ];

    const handleTrigger = async (id: string) => {
        try {
            await triggerScenario(id);
        } catch (error) {
            console.error('Failed to trigger scenario:', error);
        }
    };

    return (
        <div className="container mx-auto p-6 space-y-6">
            {/* Header */}
            <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Chaos Engineering</h1>
                <p className="text-muted-foreground">
                    Test system resilience with controlled chaos scenarios
                </p>
            </div>

            {/* Tabs */}
            <Tabs value={activeTab} onValueChange={setActiveTab}>
                <TabsList>
                    <TabsTrigger value="scenarios">Scenarios</TabsTrigger>
                    <TabsTrigger value="history">History</TabsTrigger>
                    <TabsTrigger value="analytics">Analytics</TabsTrigger>
                </TabsList>

                {/* Scenarios Tab */}
                <TabsContent value="scenarios" className="space-y-6">
                    {/* Last Event */}
                    {lastEvent && (
                        <Card className="glass-card border-yellow-500/50">
                            <CardHeader>
                                <CardTitle className="flex items-center gap-2">
                                    <Badge variant="outline" className="bg-yellow-500/20 text-yellow-400">
                                        ACTIVE
                                    </Badge>
                                    Last Triggered Scenario
                                </CardTitle>
                                <CardDescription>
                                    {lastEvent.scenario} - {new Date(lastEvent.timestamp).toLocaleString()}
                                </CardDescription>
                            </CardHeader>
                            <CardContent>
                                <div className="grid grid-cols-3 gap-4 text-sm">
                                    <div>
                                        <p className="text-muted-foreground">Incident ID</p>
                                        <p className="font-mono">{lastEvent.incident_id}</p>
                                    </div>
                                    <div>
                                        <p className="text-muted-foreground">Duration</p>
                                        <p>{lastEvent.duration}s</p>
                                    </div>
                                    <div>
                                        <p className="text-muted-foreground">Intensity</p>
                                        <p className="capitalize">{lastEvent.intensity}</p>
                                    </div>
                                </div>
                            </CardContent>
                        </Card>
                    )}

                    {/* Chaos Scenarios Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                        {chaosScenarios.map((scenario) => (
                            <ChaosCard
                                key={scenario.id}
                                {...scenario}
                                onTrigger={handleTrigger}
                            />
                        ))}
                    </div>
                </TabsContent>

                {/* History Tab */}
                <TabsContent value="history">
                    <Card className="glass-card">
                        <CardHeader>
                            <CardTitle>Chaos History</CardTitle>
                            <CardDescription>
                                View past chaos engineering experiments
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground text-center py-8">
                                No chaos scenarios triggered yet. Start your first experiment above.
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>

                {/* Analytics Tab */}
                <TabsContent value="analytics">
                    <Card className="glass-card">
                        <CardHeader>
                            <CardTitle>Chaos Analytics</CardTitle>
                            <CardDescription>
                                Analyze system resilience and recovery patterns
                            </CardDescription>
                        </CardHeader>
                        <CardContent>
                            <p className="text-muted-foreground text-center py-8">
                                Analytics will appear after running chaos scenarios
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
