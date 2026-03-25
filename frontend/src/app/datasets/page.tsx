import { fetchDatasets } from "@/lib/api";

export default async function DatasetsPage() {
  const data = await fetchDatasets();

  return (
    <main style={{ padding: "32px", fontFamily: "sans-serif" }}>
      <h1>データセット一覧</h1>
      <p>登録済みデータセットを表示します。</p>

      <div style={{ marginTop: "24px", overflowX: "auto" }}>
        <table
          style={{
            width: "100%",
            borderCollapse: "collapse",
            border: "1px solid #ccc",
          }}
        >
          <thead>
            <tr>
              <th style={thStyle}>タイトル</th>
              <th style={thStyle}>ソース種別</th>
              <th style={thStyle}>最終更新日</th>
              <th style={thStyle}>監視有効</th>
              <th style={thStyle}>スコア除外</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 ? (
              <tr>
                <td style={tdStyle} colSpan={5}>
                  データがありません
                </td>
              </tr>
            ) : (
              data.items.map((dataset) => (
                <tr key={dataset.datasetId}>
                  <td style={tdStyle}>{dataset.title ?? "-"}</td>
                  <td style={tdStyle}>{dataset.sourceType}</td>
                  <td style={tdStyle}>
                    {dataset.lastUpdated
                      ? new Date(dataset.lastUpdated).toLocaleString("ja-JP")
                      : "-"}
                  </td>
                  <td style={tdStyle}>
                    {dataset.monitoringEnabled ? "有効" : "無効"}
                  </td>
                  <td style={tdStyle}>
                    {dataset.excludedFromScoring ? "除外" : "対象"}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </main>
  );
}

const thStyle: React.CSSProperties = {
  borderBottom: "1px solid #ccc",
  textAlign: "left",
  padding: "12px",
  backgroundColor: "#f5f5f5",
};

const tdStyle: React.CSSProperties = {
  borderBottom: "1px solid #eee",
  padding: "12px",
};