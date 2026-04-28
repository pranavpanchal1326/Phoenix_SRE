"use client"

import { useState, useCallback } from 'react';
import { useWebSocket } from './useWebSocket';

export interface ChaosScenario {
    id: string;
    name: string;
    description: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    duration: string;
    costImpact: string;
}

export interface ChaosEvent {
    incident_id: string;
    scenario: string;
    scenario_id: string;
    duration: number;
    intensity: string;
    timestamp: string;
}

export function useChaos() {
    const { socket, connected } = useWebSocket();
    const [triggering, setTriggering] = useState(false);
    const [lastEvent, setLastEvent] = useState<ChaosEvent | null>(null);

    const triggerScenario = useCallback(async (
        scenarioId: string,
        duration: number = 300,
        intensity: string = 'medium'
    ) => {
        if (!connected) {
            throw new Error('WebSocket not connected');
        }

        setTriggering(true);

        try {
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'}/api/chaos/trigger`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    scenario_id: scenarioId,
                    duration,
                    intensity
                }),
            });

            if (!response.ok) {
                throw new Error('Failed to trigger chaos scenario');
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error('Error triggering chaos scenario:', error);
            throw error;
        } finally {
            setTimeout(() => setTriggering(false), 2000);
        }
    }, [connected]);

    // Listen for chaos events
    useState(() => {
        if (socket) {
            socket.on('chaos:triggered', (event: ChaosEvent) => {
                setLastEvent(event);
            });

            return () => {
                socket.off('chaos:triggered');
            };
        }
    });

    return {
        triggerScenario,
        triggering,
        lastEvent,
        connected
    };
}
