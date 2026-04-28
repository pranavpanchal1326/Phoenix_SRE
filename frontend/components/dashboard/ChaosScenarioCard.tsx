"use client"

import { motion } from 'framer-motion';
import { LucideIcon, Clock, DollarSign, Zap } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

interface ChaosScenarioCardProps {
    id: string;
    title: string;
    description: string;
    icon: LucideIcon;
    riskLevel: 'low' | 'medium' | 'high' | 'critical';
    duration: string;
    costImpact: string;
    onTrigger: () => void;
    isTriggering?: boolean;
}

export function ChaosScenarioCard({
    id,
    title,
    description,
    icon: Icon,
    riskLevel,
    duration,
    costImpact,
    onTrigger,
    isTriggering = false
}: ChaosScenarioCardProps) {
    const riskColors = {
        low: 'bg-success/20 text-success border-success/30',
        medium: 'bg-warning/20 text-warning border-warning/30',
        high: 'bg-danger/20 text-danger border-danger/30',
        critical: 'bg-danger/30 text-danger border-danger/50'
    };

    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.02, y: -4 }}
            whileTap={{ scale: 0.98 }}
            transition={{ duration: 0.2 }}
            className="group relative overflow-hidden rounded-2xl border border-border bg-surface/50 backdrop-blur-xl p-6 hover:border-primary/50 transition-all shadow-lg hover:shadow-primary/20"
        >
            {/* Glow effect on hover */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary/0 via-primary/0 to-primary/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

            <div className="relative space-y-4">
                {/* Header */}
                <div className="flex items-start justify-between">
                    <div className="flex items-center gap-4">
                        <motion.div
                            whileHover={{ rotate: 360 }}
                            transition={{ duration: 0.5 }}
                            className="h-14 w-14 rounded-xl bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors"
                        >
                            <Icon className="h-7 w-7 text-primary" />
                        </motion.div>

                        <div>
                            <h3 className="text-xl font-semibold text-foreground group-hover:text-primary transition-colors">
                                {title}
                            </h3>
                            <Badge className={cn('mt-1 uppercase text-xs border', riskColors[riskLevel])}>
                                {riskLevel}
                            </Badge>
                        </div>
                    </div>
                </div>

                {/* Description */}
                <p className="text-sm text-muted leading-relaxed">
                    {description}
                </p>

                {/* Metrics */}
                <div className="grid grid-cols-2 gap-4 pt-2">
                    <div className="flex items-center gap-2">
                        <Clock className="h-4 w-4 text-muted" />
                        <div>
                            <p className="text-xs text-muted">Duration</p>
                            <p className="text-sm font-semibold text-foreground">{duration}</p>
                        </div>
                    </div>

                    <div className="flex items-center gap-2">
                        <DollarSign className="h-4 w-4 text-muted" />
                        <div>
                            <p className="text-xs text-muted">Cost Impact</p>
                            <p className="text-sm font-semibold text-foreground">{costImpact}</p>
                        </div>
                    </div>
                </div>

                {/* Trigger Button */}
                <Button
                    onClick={onTrigger}
                    disabled={isTriggering}
                    className="w-full bg-primary hover:bg-primary/90 text-primary-foreground shadow-lg shadow-primary/20 group-hover:shadow-primary/40 transition-all disabled:opacity-50"
                    size="lg"
                >
                    {isTriggering ? (
                        <>
                            <motion.div
                                animate={{ rotate: 360 }}
                                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            >
                                <Zap className="mr-2 h-4 w-4" />
                            </motion.div>
                            Triggering...
                        </>
                    ) : (
                        <>
                            <Zap className="mr-2 h-4 w-4" />
                            Trigger Scenario
                        </>
                    )}
                </Button>
            </div>
        </motion.div>
    );
}
