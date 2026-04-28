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
    Activity,
    User
} from 'lucide-react';

const navigation = [
    { name: 'Overview', href: '/', icon: LayoutDashboard },
    { name: 'Monitoring', href: '/monitoring', icon: Activity },
    { name: 'Chaos', href: '/chaos', icon: Zap },
    { name: 'AI', href: '/ai', icon: Brain },
    { name: 'History', href: '/incidents', icon: AlertTriangle },
    { name: 'Cost', href: '/costs', icon: DollarSign },
];

export function TopNav() {
    const pathname = usePathname();

    return (
        <nav className="fixed top-0 left-0 right-0 z-50 h-16 glass-nav border-b border-white/8">
            <div className="container mx-auto h-full flex items-center justify-between px-6">
                {/* Logo */}
                <Link href="/" className="flex items-center gap-2 group">
                    <Activity className="h-6 w-6 text-primary transition-transform group-hover:scale-110" />
                    <span className="text-xl font-bold bg-gradient-to-r from-blue-500 to-cyan-500 bg-clip-text text-transparent">
                        Phoenix SRE
                    </span>
                </Link>

                {/* Navigation Links */}
                <div className="flex items-center gap-1">
                    {navigation.map((item) => {
                        const isActive = pathname === item.href ||
                            (item.href !== '/' && pathname.startsWith(item.href));

                        return (
                            <Link
                                key={item.name}
                                href={item.href}
                                className={cn(
                                    "flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all hover:-translate-y-0.5",
                                    isActive
                                        ? "text-white border-b-2 border-blue-500"
                                        : "text-gray-400 hover:text-white"
                                )}
                            >
                                <item.icon className="h-4 w-4" />
                                <span className="hidden md:inline">{item.name}</span>
                            </Link>
                        );
                    })}
                </div>

                {/* Right Section */}
                <div className="flex items-center gap-4">
                    <Link href="/settings" className="p-2 rounded-lg hover:bg-white/5 transition-colors">
                        <Settings className="h-5 w-5 text-gray-400 hover:text-white" />
                    </Link>
                    <button className="p-2 rounded-lg hover:bg-white/5 transition-colors">
                        <User className="h-5 w-5 text-gray-400 hover:text-white" />
                    </button>
                </div>
            </div>
        </nav>
    );
}
