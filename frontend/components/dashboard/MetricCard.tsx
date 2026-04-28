"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import { TrendingUp, TrendingDown } from "lucide-react";

interface MetricCardProps {
    title: string;
    value: string | number;
    delta?: number;
    deltaLabel?: string;
    icon?: React.ReactNode;
    className?: string;
}

export function MetricCard({
    title,
    value,
    delta,
    deltaLabel,
    icon,
    className
}: MetricCardProps) {
    const isPositive = delta !== undefined && delta > 0;
    const isNegative = delta !== undefined && delta < 0;

    return (
        <Card className={cn("glass-card glass-card-hover", className)}>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-text-secondary">
                    {title}
                </CardTitle>
                {icon && <div className="text-text-tertiary">{icon}</div>}
            </CardHeader>
            <CardContent>
                <div className="text-4xl font-bold text-text-primary tabular-nums">
                    {value}
                </div>
                {delta !== undefined && (
                    <div className="flex items-center gap-1 mt-2">
                        {isPositive && <TrendingUp className="h-4 w-4 text-success" />}
                        {isNegative && <TrendingDown className="h-4 w-4 text-danger" />}
                        <span
                            className={cn(
                                "text-sm font-medium",
                                isPositive && "text-success",
                                isNegative && "text-danger",
                                !isPositive && !isNegative && "text-text-tertiary"
                            )}
                        >
                            {delta > 0 ? "+" : ""}{delta}
                            {deltaLabel && ` ${deltaLabel}`}
                        </span>
                    </div>
                )}
            </CardContent>
        </Card>
    );
}
