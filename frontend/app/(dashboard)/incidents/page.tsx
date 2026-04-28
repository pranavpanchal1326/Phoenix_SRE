"use client"

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AlertTriangle, CheckCircle, Clock, XCircle } from 'lucide-react';

interface Incident {
    id: string;
    title: string;
    status: 'active' | 'resolved' | 'investigating';
    severity: 'low' | 'medium' | 'high' | 'critical';
    timestamp: string;
    description: string;
    remediation?: string;
}

export default function IncidentsPage() {
    const [incidents, setIncidents] = useState<Incident[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // Fetch incidents from API
        const fetchIncidents = async () => {
            try {
                const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/incidents/`);
                if (response.ok) {
                    const data = await response.json();
                    setIncidents(data);
                }
            } catch (error) {
                console.error('Failed to fetch incidents:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchIncidents();
    }, []);

    const getStatusIcon = (status: string) => {
        switch (status) {
            case 'active':
                return <AlertTriangle className="h-4 w-4 text-red-500" />;
            case 'investigating':
                return <Clock className="h-4 w-4 text-yellow-500" />;
            case 'resolved':
                return <CheckCircle className="h-4 w-4 text-green-500" />;
            default:
                return <XCircle className="h-4 w-4 text-gray-500" />;
        }
    };

    const getSeverityColor = (severity: string) => {
        switch (severity) {
            case 'critical':
                return 'bg-red-500/20 text-red-400 border-red-500/30';
            case 'high':
                return 'bg-orange-500/20 text-orange-400 border-orange-500/30';
            case 'medium':
                return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
            case 'low':
                return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
            default:
                return 'bg-gray-500/20 text-gray-400 border-gray-500/30';
        }
    };

    return (
        <div className="container mx-auto p-6 space-y-6">
            {/* Header */}
            <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Incidents</h1>
                <p className="text-muted-foreground">
                    Track and manage system incidents and remediation
                </p>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <Card className="glass-card">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Active Incidents
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">
                            {incidents.filter(i => i.status === 'active').length}
                        </p>
                    </CardContent>
                </Card>
                <Card className="glass-card">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Investigating
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">
                            {incidents.filter(i => i.status === 'investigating').length}
                        </p>
                    </CardContent>
                </Card>
                <Card className="glass-card">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            Resolved Today
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">
                            {incidents.filter(i => i.status === 'resolved').length}
                        </p>
                    </CardContent>
                </Card>
                <Card className="glass-card">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium text-muted-foreground">
                            MTTR
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p className="text-3xl font-bold">4.2m</p>
                    </CardContent>
                </Card>
            </div>

            {/* Incidents List */}
            <Tabs defaultValue="all">
                <TabsList>
                    <TabsTrigger value="all">All Incidents</TabsTrigger>
                    <TabsTrigger value="active">Active</TabsTrigger>
                    <TabsTrigger value="resolved">Resolved</TabsTrigger>
                </TabsList>

                <TabsContent value="all" className="space-y-4">
                    {loading ? (
                        <Card className="glass-card">
                            <CardContent className="py-8">
                                <p className="text-center text-muted-foreground">Loading incidents...</p>
                            </CardContent>
                        </Card>
                    ) : incidents.length === 0 ? (
                        <Card className="glass-card">
                            <CardContent className="py-8">
                                <p className="text-center text-muted-foreground">
                                    No incidents found. Your system is healthy! 🎉
                                </p>
                            </CardContent>
                        </Card>
                    ) : (
                        incidents.map((incident) => (
                            <Card key={incident.id} className="glass-card">
                                <CardHeader>
                                    <div className="flex items-start justify-between">
                                        <div className="space-y-1">
                                            <CardTitle className="flex items-center gap-2">
                                                {getStatusIcon(incident.status)}
                                                {incident.title}
                                            </CardTitle>
                                            <CardDescription>
                                                {new Date(incident.timestamp).toLocaleString()}
                                            </CardDescription>
                                        </div>
                                        <div className="flex items-center gap-2">
                                            <Badge variant="outline" className={getSeverityColor(incident.severity)}>
                                                {incident.severity.toUpperCase()}
                                            </Badge>
                                            <Badge variant="outline" className="capitalize">
                                                {incident.status}
                                            </Badge>
                                        </div>
                                    </div>
                                </CardHeader>
                                <CardContent className="space-y-4">
                                    <p className="text-sm text-muted-foreground">
                                        {incident.description}
                                    </p>
                                    {incident.remediation && (
                                        <div className="space-y-2">
                                            <p className="text-sm font-medium">Remediation:</p>
                                            <p className="text-sm text-muted-foreground">
                                                {incident.remediation}
                                            </p>
                                        </div>
                                    )}
                                    <div className="flex gap-2">
                                        <Button size="sm" variant="outline">
                                            View Details
                                        </Button>
                                        {incident.status === 'active' && (
                                            <Button size="sm" variant="destructive">
                                                Approve Remediation
                                            </Button>
                                        )}
                                    </div>
                                </CardContent>
                            </Card>
                        ))
                    )}
                </TabsContent>

                <TabsContent value="active">
                    <Card className="glass-card">
                        <CardContent className="py-8">
                            <p className="text-center text-muted-foreground">
                                {incidents.filter(i => i.status === 'active').length} active incidents
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>

                <TabsContent value="resolved">
                    <Card className="glass-card">
                        <CardContent className="py-8">
                            <p className="text-center text-muted-foreground">
                                {incidents.filter(i => i.status === 'resolved').length} resolved incidents
                            </p>
                        </CardContent>
                    </Card>
                </TabsContent>
            </Tabs>
        </div>
    );
}
