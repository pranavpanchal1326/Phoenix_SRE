"use client"

import { motion } from 'framer-motion';
import { Activity, Zap, DollarSign, TrendingUp } from 'lucide-react';
import { cn } from '@/lib/utils';

interface StatusBannerProps {
    status: 'healthy' | 'warning' | 'critical';
    metrics: {
        gpuUtil: number;
        instanceCount: number;
        costPerHour: number;
    };
    budget: {
        total: number;
        remaining: number;
    };
}

export function StatusBanner({ status, metrics, budget }: StatusBannerProps) {
    const statusColors = {
        healthy: {
            bg: 'bg-success/20',
            text: 'text-success',
            border: 'border-success',
            glow: 'shadow-success/20'
        },
        warning: {
            bg: 'bg-warning/20',
            text: 'text-warning',
            border: 'border-warning',
            glow: 'shadow-warning/20'
        },
        critical: {
            bg: 'bg-danger/20',
            text: 'text-danger',
            border: 'border-danger',
            glow: 'shadow-danger/20'
        }
    };

    const statusConfig = statusColors[status];
    const budgetPercent = (budget.remaining / budget.total) * 100;

    return (
        <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="relative overflow-hidden rounded-2xl border border-border bg-surface/50 backdrop-blur-xl p-6 shadow-lg"
        >
            {/* Animated background gradient */}
            <div className="absolute inset-0 bg-gradient-to-r from-primary/5 via-transparent to-primary/5 animate-shimmer" />

            <div className="relative grid grid-cols-4 gap-6">
                {/* System Status */}
                <div className="flex items-center gap-4">
                    <div className="relative">
                        <div className={cn(
                            "h-12 w-12 rounded-full flex items-center justify-center",
                            statusConfig.bg
                        )}>
                            <Activity className={cn(
                                "h-6 w-6 animate-pulse",
                                statusConfig.text
                            )} />
                        </div>
                        {/* Pulsing ring */}
                        <motion.div
                            className={cn(
                                "absolute inset-0 rounded-full border-2",
                                statusConfig.border
                            )}
                            animate={{
                                scale: [1, 1.2, 1],
                                opacity: [1, 0, 1]
                            }}
                            transition={{ duration: 2, repeat: Infinity }}
                        />
                    </div>

                    <div>
                        <p className="text-sm text-muted">System Status</p>
                        <p className="text-xl font-semibold text-foreground capitalize">
                            {status}
                        </p>
                    </div>
                </div>

                {/* GPU Utilization */}
                <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-full bg-primary/20 flex items-center justify-center">
                        <Zap className="h-6 w-6 text-primary" />
                    </div>
                    <div>
                        <p className="text-sm text-muted">GPU Utilization</p>
                        <p className="text-xl font-semibold font-mono text-foreground">
                            {metrics.gpuUtil.toFixed(1)}%
                            <span className="text-sm text-muted ml-2">
                                ({metrics.instanceCount} instances)
                            </span>
                        </p>
                    </div>
                </div>

                {/* Cost per Hour */}
                <div className="flex items-center gap-4">
                    <div className="h-12 w-12 rounded-full bg-warning/20 flex items-center justify-center">
                        <DollarSign className="h-6 w-6 text-warning" />
                    </div>
                    <div>
                        <p className="text-sm text-muted">Cost / Hour</p>
                        <p className="text-xl font-semibold font-mono text-foreground">
                            ${metrics.costPerHour.toFixed(2)}
                        </p>
                    </div>
                </div>

                {/* Budget Remaining */}
                <div className="flex items-center gap-4">
                    <div className="relative h-12 w-12">
                        {/* Circular progress */}
                        <svg className="transform -rotate-90 h-12 w-12">
                            <circle
                                cx="24"
                                cy="24"
                                r="20"
                                stroke="currentColor"
                                strokeWidth="4"
                                fill="none"
                                className="text-surface-elevated"
                            />
                            <circle
                                cx="24"
                                cy="24"
                                r="20"
                                stroke="currentColor"
                                strokeWidth="4"
                                fill="none"
                                strokeDasharray={`${(budgetPercent / 100) * 125.6} 125.6`}
                                className="text-success transition-all duration-300"
                            />
                        </svg>
                        <div className="absolute inset-0 flex items-center justify-center">
                            <span className="text-xs font-bold text-foreground">
                                {Math.round(budgetPercent)}%
                            </span>
                        </div>
                    </div>
                    <div>
                        <p className="text-sm text-muted">Budget Remaining</p>
                        <p className="text-xl font-semibold font-mono text-foreground">
                            ${budget.remaining.toFixed(2)}
                        </p>
                    </div>
                </div>
            </div>
        </motion.div>
    );
}
