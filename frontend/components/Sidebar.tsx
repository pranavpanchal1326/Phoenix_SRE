"use client"

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';
import {
    LayoutDashboard,
    Zap,
    Brain,
    AlertTriangle,
    DollarSign,
    BarChart3,
    Settings,
    Activity
} from 'lucide-react';

const navigation = [
    { name: 'Dashboard', href: '/', icon: LayoutDashboard },
    { name: 'Chaos Engineering', href: '/chaos', icon: Zap },
    { name: 'AI Diagnosis', href: '/ai', icon: Brain },
    { name: 'Incidents', href: '/incidents', icon: AlertTriangle },
    { name: 'Cost Tracking', href: '/costs', icon: DollarSign },
    { name: 'Analysis', href: '/analysis', icon: BarChart3 },
    { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex h-screen w-64 flex-col fixed left-0 top-0 z-40 border-r border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            {/* Logo */}
            <div className="flex h-16 items-center border-b border-border px-6">
                <Activity className="h-6 w-6 text-primary" />
                <span className="ml-2 text-xl font-bold bg-gradient-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">
                    Phoenix SRE
                </span>
            </div>

            {/* Navigation */}
            <nav className="flex-1 space-y-1 px-3 py-4">
                {navigation.map((item) => {
                    const isActive = pathname === item.href ||
                        (item.href !== '/' && pathname.startsWith(item.href));

                    return (
                        <Link
                            key={item.name}
                            href={item.href}
                            className={cn(
                                "flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-all hover:bg-accent hover:text-accent-foreground",
                                isActive
                                    ? "bg-accent text-accent-foreground"
                                    : "text-muted-foreground"
                            )}
                        >
                            <item.icon className="h-5 w-5" />
                            {item.name}
                        </Link>
                    );
                })}
            </nav>

            {/* Footer */}
            <div className="border-t border-border p-4">
                <div className="flex items-center gap-3 rounded-lg bg-muted px-3 py-2">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-primary/10">
                        <Activity className="h-4 w-4 text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                        <p className="text-sm font-medium truncate">BNB Marathon 2025</p>
                        <p className="text-xs text-muted-foreground truncate">Production Ready</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
