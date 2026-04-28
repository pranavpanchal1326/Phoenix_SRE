"use client"

import { motion } from 'framer-motion';
import { LucideIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface MetricCardProps {
    title: string;
    icon: LucideIcon;
    children: React.ReactNode;
    className?: string;
}

export function MetricCard({ title, icon: Icon, children, className }: MetricCardProps) {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            whileHover={{ scale: 1.02, y: -4 }}
            transition={{ duration: 0.2 }}
            className={cn(
                "relative overflow-hidden rounded-2xl border border-border",
                "bg-surface/50 backdrop-blur-xl p-6",
                "hover:border-primary/50 transition-all duration-300",
                "shadow-lg hover:shadow-primary/20",
                "group",
                className
            )}
        >
            {/* Card Header */}
            <div className="flex items-center gap-3 mb-4">
                <motion.div
                    whileHover={{ rotate: 360 }}
                    transition={{ duration: 0.5 }}
                    className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center group-hover:bg-primary/20 transition-colors"
                >
                    <Icon className="h-5 w-5 text-primary" />
                </motion.div>
                <h3 className="text-lg font-semibold text-foreground group-hover:text-primary transition-colors">
                    {title}
                </h3>
            </div>

            {/* Card Content */}
            <div className="space-y-4">
                {children}
            </div>

            {/* Subtle gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-transparent pointer-events-none opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

            {/* Glow effect on hover */}
            <div className="absolute inset-0 bg-gradient-to-br from-primary/0 via-primary/0 to-primary/10 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
        </motion.div>
    );
}
