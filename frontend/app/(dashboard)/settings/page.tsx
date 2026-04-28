"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Settings as SettingsIcon, Bell, Palette, Zap } from 'lucide-react';

export default function SettingsPage() {
    return (
        <div className="container mx-auto p-6 space-y-6">
            {/* Header */}
            <div className="space-y-2">
                <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
                <p className="text-muted-foreground">
                    Configure Phoenix SRE platform settings
                </p>
            </div>

            {/* General Settings */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <SettingsIcon className="h-5 w-5" />
                        General Settings
                    </CardTitle>
                    <CardDescription>
                        Basic platform configuration
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Project Name</label>
                        <Input defaultValue="Phoenix SRE" />
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Environment</label>
                        <Select defaultValue="development">
                            <SelectTrigger>
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="development">Development</SelectItem>
                                <SelectItem value="staging">Staging</SelectItem>
                                <SelectItem value="production">Production</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium">GCP Project ID</label>
                        <Input defaultValue="phoenix-sre-prod" />
                    </div>
                </CardContent>
            </Card>

            {/* Notifications */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Bell className="h-5 w-5" />
                        Notifications
                    </CardTitle>
                    <CardDescription>
                        Configure alert and notification preferences
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <p className="text-sm font-medium">Incident Alerts</p>
                            <p className="text-xs text-muted-foreground">
                                Receive notifications for new incidents
                            </p>
                        </div>
                        <Badge variant="outline" className="bg-green-500/20 text-green-400">
                            ENABLED
                        </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <p className="text-sm font-medium">Budget Alerts</p>
                            <p className="text-xs text-muted-foreground">
                                Alert when budget reaches threshold
                            </p>
                        </div>
                        <Badge variant="outline" className="bg-green-500/20 text-green-400">
                            ENABLED
                        </Badge>
                    </div>
                    <div className="flex items-center justify-between">
                        <div className="space-y-0.5">
                            <p className="text-sm font-medium">Chaos Events</p>
                            <p className="text-xs text-muted-foreground">
                                Notify when chaos scenarios are triggered
                            </p>
                        </div>
                        <Badge variant="outline" className="bg-green-500/20 text-green-400">
                            ENABLED
                        </Badge>
                    </div>
                </CardContent>
            </Card>

            {/* Appearance */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Palette className="h-5 w-5" />
                        Appearance
                    </CardTitle>
                    <CardDescription>
                        Customize the look and feel
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Theme</label>
                        <Select defaultValue="dark">
                            <SelectTrigger>
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="light">Light</SelectItem>
                                <SelectItem value="dark">Dark</SelectItem>
                                <SelectItem value="system">System</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Accent Color</label>
                        <Select defaultValue="blue">
                            <SelectTrigger>
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="blue">Blue</SelectItem>
                                <SelectItem value="green">Green</SelectItem>
                                <SelectItem value="purple">Purple</SelectItem>
                                <SelectItem value="orange">Orange</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                </CardContent>
            </Card>

            {/* Performance */}
            <Card className="glass-card">
                <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                        <Zap className="h-5 w-5" />
                        Performance
                    </CardTitle>
                    <CardDescription>
                        Optimize platform performance
                    </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div className="space-y-2">
                        <label className="text-sm font-medium">Metrics Update Interval</label>
                        <Select defaultValue="200">
                            <SelectTrigger>
                                <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value="100">100ms (10/sec)</SelectItem>
                                <SelectItem value="200">200ms (5/sec)</SelectItem>
                                <SelectItem value="500">500ms (2/sec)</SelectItem>
                                <SelectItem value="1000">1000ms (1/sec)</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="space-y-2">
                        <label className="text-sm font-medium">WebSocket Reconnect Timeout</label>
                        <Input type="number" defaultValue="5000" />
                        <p className="text-xs text-muted-foreground">
                            Time in milliseconds before attempting reconnection
                        </p>
                    </div>
                </CardContent>
            </Card>

            {/* Save Button */}
            <div className="flex justify-end gap-2">
                <Button variant="outline">Reset to Defaults</Button>
                <Button>Save Changes</Button>
            </div>
        </div>
    );
}
