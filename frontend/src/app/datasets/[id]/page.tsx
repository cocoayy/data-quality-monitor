import Link from "next/link";
import {
  fetchDatasetById,
  fetchDatasetScoreHistory,
  fetchDatasetScoreReasons,
} from "@/lib/api";
import { ScoreHistoryChart } from "@/components/ScoreHistoryChart";
import { ScoreReasonsList } from "@/components/ScoreReasonsList";
import { MonitoringSettingsForm } from "@/components/MonitoringSettingsForm";


type PageProps = {
  params: Promise<{
    id: string;
  }>;
};

export default async function DatasetDetailPage({ params }: PageProps) {
  const { id } = await params;

  const [dataset, history, reasons] = await Promise.all([
    fetchDatasetById(id),
    fetchDatasetScoreHistory(id),
    fetchDatasetScoreReasons(id),
  ]);

  return (
    <main style={{ padding: "32px", fontFamily: "sans-serif" }}>
      <div style={{ marginBottom: "16px" }}>
        <Link href="/datasets">← データセット一覧へ戻る</Link>
      </div>

      <h1>{dataset.title ?? "無題のデータセット"}</h1>
      <p style={{ color: "#666" }}>{dataset.organization.name}</p>

      <section style={sectionStyle}>
        <h2>基本情報</h2>
        <table style={tableStyle}>
          <tbody>
            <tr>
              <td style={labelStyle}>データセットID</td>
              <td style={valueStyle}>{dataset.datasetId}</td>
            </tr>
            <tr>
              <td style={labelStyle}>ソース種別</td>
              <td style={valueStyle}>{dataset.sourceType}</td>
            </tr>
            <tr>
              <td style={labelStyle}>説明</td>
              <td style={valueStyle}>{dataset.description ?? "-"}</td>
            </tr>
            <tr>
              <td style={labelStyle}>ライセンス</td>
              <td style={valueStyle}>{dataset.license ?? "-"}</td>
            </tr>
            <tr>
              <td style={labelStyle}>カテゴリ</td>
              <td style={valueStyle}>{dataset.category ?? "-"}</td>
            </tr>
            <tr>
              <td style={labelStyle}>タグ</td>
              <td style={valueStyle}>
                {dataset.tags && dataset.tags.length > 0
                  ? dataset.tags.join(", ")
                  : "-"}
              </td>
            </tr>
            <tr>
              <td style={labelStyle}>最終更新日</td>
              <td style={valueStyle}>
                {dataset.lastUpdated
                  ? new Date(dataset.lastUpdated).toLocaleString("ja-JP")
                  : "-"}
              </td>
            </tr>
            <tr>
              <td style={labelStyle}>更新周期</td>
              <td style={valueStyle}>{dataset.expectedUpdateCycle ?? "-"}</td>
            </tr>
            <tr>
              <td style={labelStyle}>監視有効</td>
              <td style={valueStyle}>
                {dataset.monitoringEnabled ? "有効" : "無効"}
              </td>
            </tr>
            <tr>
              <td style={labelStyle}>スコア除外</td>
              <td style={valueStyle}>
                {dataset.excludedFromScoring ? "除外" : "対象"}
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      
      <section style={sectionStyle}>
        <h2>監視設定</h2>
        <MonitoringSettingsForm
          datasetId={dataset.datasetId}
          monitoringEnabled={dataset.monitoringEnabled}
          excludedFromScoring={dataset.excludedFromScoring}
          expectedUpdateCycle={dataset.expectedUpdateCycle}
        />
      </section>


      <section style={sectionStyle}>
        <h2>最新スコア</h2>
        <div style={scoreGridStyle}>
          <ScoreCard label="Completeness" value={dataset.latestQualityScore.completeness} />
          <ScoreCard label="Freshness" value={dataset.latestQualityScore.freshness} />
          <ScoreCard label="Accessibility" value={dataset.latestQualityScore.accessibility} />
          <ScoreCard label="Format Quality" value={dataset.latestQualityScore.formatQuality} />
          <ScoreCard label="Total Score" value={dataset.latestQualityScore.total} />
          <div style={scoreCardStyle}>
            <div style={{ fontSize: "14px", color: "#666" }}>Rank / Status</div>
            <div style={{ fontSize: "24px", fontWeight: "bold", marginTop: "8px" }}>
              {dataset.latestQualityScore.rank ?? "-"}
            </div>
            <div style={{ marginTop: "8px", color: "#444" }}>
              {dataset.latestQualityScore.evaluationStatus ?? "-"}
            </div>
          </div>
        </div>
      </section>

      <section style={sectionStyle}>
        <h2>スコア履歴</h2>
        <ScoreHistoryChart history={history.history} />
      </section>

      <section style={sectionStyle}>
        <h2>スコア理由</h2>
        <ScoreReasonsList items={reasons.items} />
      </section>

      <section style={sectionStyle}>
        <h2>リソース一覧</h2>
        <div style={{ overflowX: "auto" }}>
          <table style={tableStyle}>
            <thead>
              <tr>
                <th style={headerCellStyle}>種別</th>
                <th style={headerCellStyle}>形式</th>
                <th style={headerCellStyle}>URL</th>
                <th style={headerCellStyle}>HTTP Status</th>
                <th style={headerCellStyle}>Response Time</th>
                <th style={headerCellStyle}>Checked At</th>
              </tr>
            </thead>
            <tbody>
              {dataset.resources.length === 0 ? (
                <tr>
                  <td style={valueStyle} colSpan={6}>
                    リソースがありません
                  </td>
                </tr>
              ) : (
                dataset.resources.map((resource) => (
                  <tr key={resource.resourceId}>
                    <td style={valueStyle}>{resource.resourceType}</td>
                    <td style={valueStyle}>{resource.format ?? "-"}</td>
                    <td style={valueStyle}>
                      {resource.resourceUrl ? (
                        <a href={resource.resourceUrl} target="_blank" rel="noreferrer">
                          {resource.resourceUrl}
                        </a>
                      ) : (
                        "-"
                      )}
                    </td>
                    <td style={valueStyle}>{resource.latestHttpStatus ?? "-"}</td>
                    <td style={valueStyle}>
                      {resource.latestResponseTimeMs != null
                        ? `${resource.latestResponseTimeMs} ms`
                        : "-"}
                    </td>
                    <td style={valueStyle}>
                      {resource.latestCheckedAt
                        ? new Date(resource.latestCheckedAt).toLocaleString("ja-JP")
                        : "-"}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>
    </main>
  );
}

function ScoreCard({
  label,
  value,
}: {
  label: string;
  value: number | null;
}) {
  return (
    <div style={scoreCardStyle}>
      <div style={{ fontSize: "14px", color: "#666" }}>{label}</div>
      <div style={{ fontSize: "28px", fontWeight: "bold", marginTop: "8px" }}>
        {value ?? "-"}
      </div>
    </div>
  );
}

const sectionStyle: React.CSSProperties = {
  marginTop: "32px",
};

const tableStyle: React.CSSProperties = {
  width: "100%",
  borderCollapse: "collapse",
  marginTop: "12px",
};

const labelStyle: React.CSSProperties = {
  width: "220px",
  padding: "12px",
  borderBottom: "1px solid #ddd",
  backgroundColor: "#f8f8f8",
  fontWeight: 600,
  verticalAlign: "top",
};

const valueStyle: React.CSSProperties = {
  padding: "12px",
  borderBottom: "1px solid #ddd",
};

const headerCellStyle: React.CSSProperties = {
  padding: "12px",
  borderBottom: "1px solid #ccc",
  textAlign: "left",
  backgroundColor: "#f5f5f5",
};

const scoreGridStyle: React.CSSProperties = {
  display: "grid",
  gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))",
  gap: "16px",
  marginTop: "16px",
};

const scoreCardStyle: React.CSSProperties = {
  border: "1px solid #ddd",
  borderRadius: "8px",
  padding: "16px",
  backgroundColor: "#fff",
};