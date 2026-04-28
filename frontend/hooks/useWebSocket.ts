"use client";

import { useEffect, useState, useRef, useCallback } from 'react';
import { io, Socket } from 'socket.io-client';

interface RealtimeMetrics {
    gpu_util: number;
    latency_p95: number;
    error_rate: number;
    instance_count: number;
    cost_per_hour: number;
    memory_usage: number;
    queue_depth: number;
    requests_per_sec: number;
}

interface SystemStatus {
    status: 'healthy' | 'warning' | 'critical';
    active_incidents: number;
    budget_remaining: number;
    uptime_percentage: number;
}

interface UseWebSocketReturn {
    metrics: RealtimeMetrics | null;
    status: SystemStatus | null;
    connected: boolean;
    socket: Socket | null;
    triggerChaos: (scenario: string, params?: any) => void;
    approveRemediation: (incidentId: string, approved: boolean) => void;
}

export function useWebSocket(): UseWebSocketReturn {
    const [metrics, setMetrics] = useState<RealtimeMetrics | null>(null);
    const [status, setStatus] = useState<SystemStatus | null>(null);
    const [connected, setConnected] = useState(false);
    const [socket, setSocket] = useState<Socket | null>(null);

    const reconnectAttempts = useRef(0);
    const maxReconnectAttempts = 10;

    useEffect(() => {
        const WEBSOCKET_URL = process.env.NEXT_PUBLIC_WEBSOCKET_URL || 'http://localhost:8081';

        const socketInstance = io(WEBSOCKET_URL, {
            transports: ['websocket', 'polling'],
            reconnection: true,
            reconnectionDelay: 1000,
            reconnectionDelayMax: 5000,
            reconnectionAttempts: maxReconnectAttempts,
            timeout: 20000,
            autoConnect: true
        });

        // Connection established
        socketInstance.on('connect', () => {
            console.log('✅ Connected to Phoenix SRE WebSocket');
            setConnected(true);
            reconnectAttempts.current = 0;

            // Subscribe to all metrics with 200ms interval
            socketInstance.emit('subscribe_metrics', {
                metrics: ['all'],
                interval: 200
            });
        });

        // Connection lost
        socketInstance.on('disconnect', (reason) => {
            console.log('🔴 Disconnected from WebSocket:', reason);
            setConnected(false);
        });

        // Reconnection attempt
        socketInstance.on('reconnect_attempt', (attempt) => {
            reconnectAttempts.current = attempt;
            console.log(`🔄 Reconnection attempt ${attempt}/${maxReconnectAttempts}`);
        });

        // Welcome message
        socketInstance.on('welcome', (data) => {
            console.log('👋 Welcome:', data.message);
        });

        // Initial status
        socketInstance.on('initial_status', (data: SystemStatus) => {
            setStatus(data);
        });

        // Real-time metrics update (every 200ms)
        socketInstance.on('metrics:update', (data: { data: RealtimeMetrics, timestamp: string }) => {
            setMetrics(data.data);
        });

        // New incident detected
        socketInstance.on('incident:new', (incident) => {
            console.log('⚠️ New incident:', incident);
        });

        // Incident resolved
        socketInstance.on('incident:resolved', (data) => {
            console.log('✅ Incident resolved:', data);
        });

        // Chaos scenario triggered
        socketInstance.on('chaos_triggered', (data) => {
            console.log('🔥 Chaos triggered:', data);
        });

        // Remediation approved
        socketInstance.on('remediation_approved', (data) => {
            console.log(data.approved ? '✅ Remediation approved' : '❌ Remediation denied');
        });

        setSocket(socketInstance);

        // Cleanup on unmount
        return () => {
            socketInstance.disconnect();
        };
    }, []);

    // Trigger chaos scenario
    const triggerChaos = useCallback((scenario: string, params?: any) => {
        if (socket) {
            socket.emit('trigger_chaos', { scenario, params });
        }
    }, [socket]);

    // Approve/deny remediation
    const approveRemediation = useCallback((incidentId: string, approved: boolean) => {
        if (socket) {
            socket.emit('approve_remediation', { incident_id: incidentId, approved });
        }
    }, [socket]);

    return {
        metrics,
        status,
        connected,
        socket,
        triggerChaos,
        approveRemediation
    };
}
