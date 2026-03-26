import { QualityReason } from "@/types/dataset";

type Props = {
  items: QualityReason[];
};

export function ScoreReasonsList({ items }: Props) {
  if (items.length === 0) {
    return <p>スコア理由データがありません</p>;
  }

  return (
    <div style={{ marginTop: 16, display: "grid", gap: 12 }}>
      {items.map((item, index) => (
        <div
          key={`${item.reasonCode}-${index}`}
          style={{
            border: "1px solid #ddd",
            borderRadius: 8,
            padding: 16,
            backgroundColor: "#fff",
          }}
        >
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <strong>{item.metricType}</strong>
            <span
              style={{
                border: "1px solid #ccc",
                borderRadius: 999,
                padding: "2px 8px",
                fontSize: 12,
              }}
            >
              {item.severity}
            </span>
          </div>

          <p style={{ marginTop: 8 }}>{item.message}</p>

          <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
            reasonCode: {item.reasonCode}
          </div>

          {item.detail && (
            <pre
              style={{
                marginTop: 12,
                padding: 12,
                backgroundColor: "#f7f7f7",
                borderRadius: 6,
                overflowX: "auto",
                fontSize: 12,
              }}
            >
              {JSON.stringify(item.detail, null, 2)}
            </pre>
          )}
        </div>
      ))}
    </div>
  );
}