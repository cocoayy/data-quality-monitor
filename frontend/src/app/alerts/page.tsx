"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchAlerts } from "@/lib/api";
import { AlertSummary } from "@/types/alert";
import { AlertDetailModal } from "@/components/AlertDetailModal";
import { EmptyState } from "@/components/ui/EmptyState";

export default function AlertsPage() {
    const [items, setItems] = useState<AlertSummary[]>([]);
    const [selectedAlertId, setSelectedAlertId] = useState<string | null>(null);

    const [severity, setSeverity] = useState("");
    const [alertType, setAlertType] = useState("");
    const [keyword, setKeyword] = useState("");

    const load = async () => {
        const data = await fetchAlerts({
            severity: severity || undefined,
            alertType: alertType || undefined,
            keyword: keyword || undefined,
        });
        setItems(data.items);
    };

    useEffect(() => {
        load();
    }, []);

    return (
        <main style={{ padding: "32px", fontFamily: "sans-serif" }}>
            <h1>アラート一覧</h1>
            <p>発生中・過去のアラートを確認します。</p>

            <div style={{ display: "flex", gap: 12, marginTop: 16, flexWrap: "wrap" }}>
                <select value={severity} onChange={(e) => setSeverity(e.target.value)}>
                    <option value="">全重要度</option>
                    <option value="critical">critical</option>
                    <option value="warning">warning</option>
                    <option value="info">info</option>
                </select>

                <select value={alertType} onChange={(e) => setAlertType(e.target.value)}>
                    <option value="">全種別</option>
                    <option value="low_total_score">low_total_score</option>
                    <option value="stale_dataset">stale_dataset</option>
                    <option value="inaccessible_dataset">inaccessible_dataset</option>
                    <option value="sudden_score_drop">sudden_score_drop</option>
                </select>

                <input
                    type="text"
                    placeholder="キーワード検索"
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                />

                <button onClick={load}>検索</button>
            </div>

            {items.length === 0 ? (
                <EmptyState message="アラートはありません。" />
            ) : (
                <table style={tableStyle}>
                    <thead>
                        <tr>
                            <th style={headerCellStyle}>日時</th>
                            <th style={headerCellStyle}>重要度</th>
                            <th style={headerCellStyle}>種別</th>
                            <th style={headerCellStyle}>データセット</th>
                            <th style={headerCellStyle}>メッセージ</th>
                            <th style={headerCellStyle}>詳細</th>
                        </tr>
                    </thead>
                    <tbody>
                        {items.map((alert) => (
                            <tr key={alert.alertId}>
                                <td style={valueStyle}>
                                    {alert.measuredAt
                                        ? new Date(alert.measuredAt).toLocaleString("ja-JP")
                                        : "-"}
                                </td>
                                <td style={valueStyle}>{alert.severity}</td>
                                <td style={valueStyle}>{alert.alertType}</td>
                                <td style={valueStyle}>
                                    <Link href={`/datasets/${alert.datasetId}`}>
                                        {alert.datasetTitle}
                                    </Link>
                                </td>
                                <td style={valueStyle}>{alert.message}</td>
                                <td style={valueStyle}>
                                    <button onClick={() => setSelectedAlertId(alert.alertId)}>
                                        詳細
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}

            <AlertDetailModal
                alertId={selectedAlertId}
                onClose={() => setSelectedAlertId(null)}
            />
        </main>
    );
}

const tableStyle: React.CSSProperties = {
    width: "100%",
    borderCollapse: "collapse",
    marginTop: 12,
};

const headerCellStyle: React.CSSProperties = {
    padding: 12,
    borderBottom: "1px solid #ccc",
    textAlign: "left",
    backgroundColor: "#f5f5f5",
};

const valueStyle: React.CSSProperties = {
    padding: 12,
    borderBottom: "1px solid #ddd",
};
