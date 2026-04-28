"use client"

import { useState, useEffect } from 'react';
import { useWebSocket } from './useWebSocket';

export interface Metrics {
    gpu_util: number;
    latency_p95: number;
    error_rate: number;
    memory_usage: number;
    queue_depth: number;
    instance_count: number;
    cost_per_hour: number;
    timestamp: string;
}

export function useRealtimeMetrics() {
    const { socket, connected } = useWebSocket();
    const [metrics, setMetrics] = useState<Metrics | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!socket || !connected) {
            setLoading(false);
            return;
        }

        // Listen for metrics updates
        socket.on('metrics:update', (data: { data: Metrics; timestamp: string }) => {
            setMetrics(data.data);
            setLoading(false);
            setError(null);
        });

        // Subscribe to metrics stream
        socket.emit('subscribe_metrics', {
            metrics: ['all'],
            interval: 200
        });

        // Handle errors
        socket.on('error', (err: Error) => {
            setError(err.message);
            setLoading(false);
        });

        return () => {
            socket.off('metrics:update');
            socket.off('error');
        };
    }, [socket, connected]);

    return {
        metrics,
        loading,
        error,
        connected
    };
}
