"use client";

import {
    CartesianGrid,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from "recharts";
import { DashboardHistoryItem } from "@/types/dashboard";

export function DashboardHistoryChart({
    items,
}: {
    items: DashboardHistoryItem[];
}) {
    if (items.length === 0) {
        return <p>履歴データがありません</p>;
    }

    return (
        <div style={{ width: "100%", height: 320, marginTop: 16 }}>
            <ResponsiveContainer>
                <LineChart data={items}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="measuredDate" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip />
                    <Line type="monotone" dataKey="averageTotalScore" strokeWidth={2} />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}
