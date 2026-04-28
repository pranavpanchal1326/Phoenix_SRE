"use client";

import * as React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Clock, DollarSign } from "lucide-react";

interface ChaosCardProps {
    id: string;
    title: string;
    description: string;
    icon?: React.ReactNode;
    severity: "low" | "medium" | "high" | "critical";
    duration: string;
    costImpact: string;
    onTrigger: (id: string) => void;
    className?: string;
}

export function ChaosCard({
    id,
    title,
    description,
    icon,
    severity,
    duration,
    costImpact,
    onTrigger,
    className
}: ChaosCardProps) {
    const [isTriggering, setIsTriggering] = React.useState(false);

    const severityConfig = {
        low: {
            badge: "bg-blue-500/20 text-blue-400 border-blue-500/30",
            gradient: "from-blue-500/10 to-cyan-500/10",
            glow: "shadow-blue-500/20"
        },
        medium: {
            badge: "bg-yellow-500/20 text-yellow-400 border-yellow-500/30",
            gradient: "from-yellow-500/10 to-orange-500/10",
            glow: "shadow-yellow-500/20"
        },
        high: {
            badge: "bg-orange-500/20 text-orange-400 border-orange-500/30",
            gradient: "from-orange-500/10 to-red-500/10",
            glow: "shadow-orange-500/20"
        },
        critical: {
            badge: "bg-red-500/20 text-red-400 border-red-500/30",
            gradient: "from-red-500/10 to-pink-500/10",
            glow: "shadow-red-500/20"
        }
    };

    const config = severityConfig[severity];

    const handleTrigger = async () => {
        setIsTriggering(true);

        try {
            // Call backend API to trigger chaos scenario
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/chaos/trigger`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    scenario_id: id,
                    duration: parseInt(duration) * 60, // Convert minutes to seconds
                    intensity: severity
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to trigger chaos scenario');
            }

            const data = await response.json();
            console.log('Chaos scenario triggered:', data);

            // Call the onTrigger callback
            onTrigger(id);
        } catch (error) {
            console.error('Error triggering chaos scenario:', error);
        } finally {
            setTimeout(() => setIsTriggering(false), 2000);
        }
    };

    return (
        <Card className={cn(
            "glass-card glass-card-hover relative overflow-hidden",
            config.glow,
            className
        )}>
            {/* Gradient background */}
            <div className={cn(
                "absolute inset-0 bg-gradient-to-br opacity-50",
                config.gradient
            )} />

            <CardHeader className="relative">
                <div className="flex items-start justify-between">
                    <div className="flex items-center gap-3">
                        {icon && <div className="text-text-secondary">{icon}</div>}
                        <div>
                            <CardTitle className="text-lg font-semibold text-text-primary">
                                {title}
                            </CardTitle>
                            <span className={cn(
                                "inline-block mt-2 px-2 py-1 text-xs font-medium rounded-full border",
                                config.badge
                            )}>
                                {severity.toUpperCase()}
                            </span>
                        </div>
                    </div>
                </div>
            </CardHeader>

            <CardContent className="relative space-y-4">
                <p className="text-sm text-text-secondary">
                    {description}
                </p>

                <div className="flex items-center gap-4 text-xs text-text-tertiary">
                    <div className="flex items-center gap-1">
                        <Clock className="h-3 w-3" />
                        <span>{duration}</span>
                    </div>
                    <div className="flex items-center gap-1">
                        <DollarSign className="h-3 w-3" />
                        <span>{costImpact}</span>
                    </div>
                </div>

                <Button
                    onClick={handleTrigger}
                    disabled={isTriggering}
                    className={cn(
                        "w-full font-semibold transition-all",
                        isTriggering && "opacity-50 cursor-not-allowed"
                    )}
                    variant="destructive"
                >
                    {isTriggering ? "Triggering..." : "Trigger Scenario"}
                </Button>
            </CardContent>
        </Card>
    );
}
