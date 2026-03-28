import { QualityReason } from "@/types/dataset";

type Props = {
  items: QualityReason[];
};

export function ScoreReasonsList({ items }: Props) {
  if (items.length === 0) {
    return <p>スコア理由データがありません</p>;
  }

  const grouped = items.reduce<Record<string, QualityReason[]>>((acc, item) => {
    if (!acc[item.metricType]) {
      acc[item.metricType] = [];
    }
    acc[item.metricType].push(item);
    return acc;
  }, {});

  const metricOrder = [
    "completeness",
    "freshness",
    "accessibility",
    "format_quality",
    "total",
  ];

  const sortedGroups = Object.entries(grouped).sort((a, b) => {
    return metricOrder.indexOf(a[0]) - metricOrder.indexOf(b[0]);
  });

  return (
    <div style={{ marginTop: 16, display: "grid", gap: 20 }}>
      {sortedGroups.map(([metricType, reasons]) => (
        <section key={metricType}>
          <h3 style={{ marginBottom: 12 }}>{metricType}</h3>

          <div style={{ display: "grid", gap: 12 }}>
            {reasons.map((item, index) => (
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
                  <strong>{item.reasonCode}</strong>
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
        </section>
      ))}
    </div>
  );
}
