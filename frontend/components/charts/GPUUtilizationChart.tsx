"use client"

import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, Area, AreaChart, ReferenceLine } from 'recharts';
import { Activity, TrendingUp, TrendingDown } from 'lucide-react';
import { MetricCard } from '../dashboard/EnterpriseMetricCard';

interface GPUDataPoint {
    timestamp: number;
    value: number;
}

interface GPUUtilizationChartProps {
    data: GPUDataPoint[];
    currentValue: number;
}

export function GPUUtilizationChart({ data, currentValue }: GPUUtilizationChartProps) {
    const average = data.length > 0
        ? data.reduce((sum, d) => sum + d.value, 0) / data.length
        : 0;
    const peak = data.length > 0
        ? Math.max(...data.map(d => d.value))
        : 0;

    return (
        <MetricCard title="GPU Utilization" icon={Activity}>
            {/* Chart */}
            <div className="h-64 -mx-2">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data}>
                        <defs>
                            <linearGradient id="gpuGradient" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="rgb(138, 180, 248)" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="rgb(138, 180, 248)" stopOpacity={0} />
                            </linearGradient>
                        </defs>

                        <XAxis
                            dataKey="timestamp"
                            stroke="rgb(139, 148, 158)"
                            fontSize={12}
                            tickFormatter={(value) => {
                                const date = new Date(value);
                                return `${date.getHours()}:${date.getMinutes().toString().padStart(2, '0')}`;
                            }}
                            tick={{ fill: 'rgb(139, 148, 158)' }}
                        />

                        <YAxis
                            stroke="rgb(139, 148, 158)"
                            fontSize={12}
                            domain={[0, 100]}
                            tickFormatter={(value) => `${value}%`}
                            tick={{ fill: 'rgb(139, 148, 158)' }}
                        />

                        <Tooltip
                            contentStyle={{
                                backgroundColor: 'rgb(22, 27, 34)',
                                border: '1px solid rgb(48, 54, 61)',
                                borderRadius: '8px',
                                fontSize: '14px',
                                boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)'
                            }}
                            labelStyle={{ color: 'rgb(230, 237, 243)', marginBottom: '4px' }}
                            itemStyle={{ color: 'rgb(138, 180, 248)' }}
                            formatter={(value: number) => [`${value.toFixed(1)}%`, 'GPU']}
                            labelFormatter={(value) => new Date(value).toLocaleTimeString()}
                        />

                        {/* Threshold lines */}
                        <ReferenceLine
                            y={80}
                            stroke="rgb(187, 128, 9)"
                            strokeDasharray="5 5"
                            strokeWidth={1}
                            label={{ value: 'Warning', position: 'right', fill: 'rgb(187, 128, 9)', fontSize: 10 }}
                        />
                        <ReferenceLine
                            y={90}
                            stroke="rgb(248, 81, 73)"
                            strokeDasharray="5 5"
                            strokeWidth={1}
                            label={{ value: 'Critical', position: 'right', fill: 'rgb(248, 81, 73)', fontSize: 10 }}
                        />

                        {/* Main data area */}
                        <Area
                            type="monotone"
                            dataKey="value"
                            stroke="rgb(138, 180, 248)"
                            strokeWidth={2}
                            fill="url(#gpuGradient)"
                            animationDuration={300}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            {/* Current Value Display */}
            <div className="grid grid-cols-3 gap-4 pt-4 border-t border-border">
                <div>
                    <p className="text-sm text-muted mb-1">Current</p>
                    <div className="flex items-baseline gap-2">
                        <p className="text-2xl font-bold font-mono text-foreground">
                            {currentValue.toFixed(1)}%
                        </p>
                        {currentValue > average ? (
                            <TrendingUp className="h-4 w-4 text-success" />
                        ) : (
                            <TrendingDown className="h-4 w-4 text-danger" />
                        )}
                    </div>
                </div>
                <div>
                    <p className="text-sm text-muted mb-1">Average (5m)</p>
                    <p className="text-2xl font-bold font-mono text-foreground">
                        {average.toFixed(1)}%
                    </p>
                </div>
                <div>
                    <p className="text-sm text-muted mb-1">Peak</p>
                    <p className="text-2xl font-bold font-mono text-foreground">
                        {peak.toFixed(1)}%
                    </p>
                </div>
            </div>
        </MetricCard>
    );
}
