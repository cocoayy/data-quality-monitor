"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { QualityScoreHistoryItem } from "@/types/dataset";

type Props = {
  history: QualityScoreHistoryItem[];
};

export function ScoreHistoryChart({ history }: Props) {
  const chartData = history.map((item) => ({
    measuredDate: item.measuredDate,
    total: item.scores.total,
  }));

  if (chartData.length === 0) {
    return <p>履歴データがありません</p>;
  }

  return (
    <div style={{ width: "100%", height: 320, marginTop: 16 }}>
      <ResponsiveContainer>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="measuredDate" />
          <YAxis domain={[0, 100]} />
          <Tooltip />
          <Line type="monotone" dataKey="total" strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}