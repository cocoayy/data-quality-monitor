import Link from "next/link";
import { fetchAlerts, fetchDashboardSummary, fetchOrganizations } from "@/lib/api";

export default async function DashboardPage() {
  const [summary, organizations, alerts] = await Promise.all([
    fetchDashboardSummary(),
    fetchOrganizations(),
    fetchAlerts(),
  ]);

  return (
    <main style={{ padding: "32px", fontFamily: "sans-serif" }}>
      <h1>ダッシュボード</h1>
      <p>データ品質監視ツールの全体状況を表示します。</p>

      <section style={sectionStyle}>
        <h2>サマリー</h2>
        <div style={cardGridStyle}>
          <SummaryCard label="総データセット数" value={summary.summary.totalDatasets} />
          <SummaryCard label="評価済み件数" value={summary.summary.evaluatedDatasets} />
          <SummaryCard label="評価不能件数" value={summary.summary.unevaluableDatasets} />
          <SummaryCard
            label="平均総合スコア"
            value={summary.summary.averageTotalScore.toFixed(1)}
          />
          <SummaryCard label="Critical Alerts" value={summary.summary.criticalAlerts} />
          <SummaryCard label="Warning Alerts" value={summary.summary.warningAlerts} />
        </div>
      </section>

      <section style={sectionStyle}>
        <h2>ランク分布</h2>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={headerCellStyle}>A</th>
              <th style={headerCellStyle}>B</th>
              <th style={headerCellStyle}>C</th>
              <th style={headerCellStyle}>D</th>
              <th style={headerCellStyle}>E</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style={valueStyle}>{summary.summary.rankDistribution.A}</td>
              <td style={valueStyle}>{summary.summary.rankDistribution.B}</td>
              <td style={valueStyle}>{summary.summary.rankDistribution.C}</td>
              <td style={valueStyle}>{summary.summary.rankDistribution.D}</td>
              <td style={valueStyle}>{summary.summary.rankDistribution.E}</td>
            </tr>
          </tbody>
        </table>
      </section>

      <section style={sectionStyle}>
        <h2>組織一覧</h2>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={headerCellStyle}>組織名</th>
              <th style={headerCellStyle}>表示名</th>
              <th style={headerCellStyle}>ソース種別</th>
              <th style={headerCellStyle}>有効</th>
            </tr>
          </thead>
          <tbody>
            {organizations.items.length === 0 ? (
              <tr>
                <td style={valueStyle} colSpan={4}>
                  組織データがありません
                </td>
              </tr>
            ) : (
              organizations.items.map((org) => (
                <tr key={org.organizationId}>
                  <td style={valueStyle}>{org.name}</td>
                  <td style={valueStyle}>{org.displayName ?? "-"}</td>
                  <td style={valueStyle}>{org.sourceType}</td>
                  <td style={valueStyle}>{org.isActive ? "有効" : "無効"}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>

      <section style={sectionStyle}>
        <h2>最新アラート</h2>
        <table style={tableStyle}>
          <thead>
            <tr>
              <th style={headerCellStyle}>日時</th>
              <th style={headerCellStyle}>重要度</th>
              <th style={headerCellStyle}>種別</th>
              <th style={headerCellStyle}>データセット</th>
              <th style={headerCellStyle}>メッセージ</th>
            </tr>
          </thead>
          <tbody>
            {alerts.items.length === 0 ? (
              <tr>
                <td style={valueStyle} colSpan={5}>
                  アラートがありません
                </td>
              </tr>
            ) : (
              alerts.items.slice(0, 10).map((alert) => (
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
                </tr>
              ))
            )}
          </tbody>
        </table>
      </section>
    </main>
  );
}

function SummaryCard({
  label,
  value,
}: {
  label: string;
  value: string | number;
}) {
  return (
    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: 8,
        padding: 16,
        backgroundColor: "#fff",
      }}
    >
      <div style={{ fontSize: 14, color: "#666" }}>{label}</div>
      <div style={{ marginTop: 8, fontSize: 28, fontWeight: "bold" }}>{value}</div>
    </div>
  );
}

const sectionStyle: React.CSSProperties = {
  marginTop: 32,
};

const cardGridStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
  gap: 16,
  marginTop: 16,
};

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