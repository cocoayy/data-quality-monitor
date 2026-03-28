"use client";

import { useEffect, useState } from "react";
import { fetchAlertById } from "@/lib/api";
import { AlertDetail } from "@/types/alert";

type Props = {
    alertId: string | null;
    onClose: () => void;
};

export function AlertDetailModal({ alertId, onClose }: Props) {
    const [alert, setAlert] = useState<AlertDetail | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        if (!alertId) return;

        const load = async () => {
            setLoading(true);
            setError(null);

            try {
                const data = await fetchAlertById(alertId);
                setAlert(data);
            } catch {
                setError("アラート詳細の取得に失敗しました。");
            } finally {
                setLoading(false);
            }
        };

        load();
    }, [alertId]);

    if (!alertId) return null;

    return (
        <div style={overlayStyle} onClick={onClose}>
            <div style={modalStyle} onClick={(e) => e.stopPropagation()}>
                <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <h3 style={{ marginTop: 0 }}>アラート詳細</h3>
                    <button onClick={onClose}>閉じる</button>
                </div>

                {loading && <p>読み込み中...</p>}
                {error && <p>{error}</p>}

                {!loading && !error && alert && (
                    <div style={{ display: "grid", gap: 12 }}>
                        <div><strong>alertId:</strong> {alert.alertId}</div>
                        <div><strong>datasetId:</strong> {alert.datasetId}</div>
                        <div><strong>alertType:</strong> {alert.alertType}</div>
                        <div><strong>severity:</strong> {alert.severity}</div>
                        <div><strong>message:</strong> {alert.message}</div>
                        <div>
                            <strong>measuredAt:</strong>{" "}
                            {alert.measuredAt
                                ? new Date(alert.measuredAt).toLocaleString("ja-JP")
                                : "-"}
                        </div>

                        <div>
                            <strong>payload:</strong>
                            <pre
                                style={{
                                    marginTop: 8,
                                    padding: 12,
                                    backgroundColor: "#f7f7f7",
                                    borderRadius: 6,
                                    overflowX: "auto",
                                }}
                            >
                                {JSON.stringify(alert.payload, null, 2)}
                            </pre>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

const overlayStyle: React.CSSProperties = {
    position: "fixed",
    inset: 0,
    backgroundColor: "rgba(0,0,0,0.4)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    padding: 24,
};

const modalStyle: React.CSSProperties = {
    width: "100%",
    maxWidth: 720,
    backgroundColor: "#fff",
    borderRadius: 12,
    padding: 24,
};
