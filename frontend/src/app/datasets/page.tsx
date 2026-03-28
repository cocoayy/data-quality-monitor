import Link from "next/link";
import { fetchDatasets } from "@/lib/api";

type SearchParams = Promise<{
  page?: string;
  keyword?: string;
  rank?: string;
  sort_by?: string;
  sort_order?: string;
}>;

export default async function DatasetsPage({
  searchParams,
}: {
  searchParams: SearchParams;
}) {
  const params = await searchParams;

  const page = Number(params.page ?? "1");
  const keyword = params.keyword ?? "";
  const rank = params.rank ?? "";
  const sortBy = params.sort_by ?? "created_at";
  const sortOrder = params.sort_order ?? "desc";

  const data = await fetchDatasets({
    page,
    pageSize: 10,
    keyword: keyword || undefined,
    rank: rank || undefined,
    sortBy,
    sortOrder,
  });

  return (
    <main style={{ padding: "32px", fontFamily: "sans-serif" }}>
      <h1>データセット一覧</h1>
      <p>登録済みデータセットを表示します。</p>

      <form method="GET" style={{ marginTop: 16, display: "flex", gap: 12, flexWrap: "wrap" }}>
        <input
          type="text"
          name="keyword"
          defaultValue={keyword}
          placeholder="キーワード検索"
        />

        <select name="rank" defaultValue={rank}>
          <option value="">すべてのランク</option>
          <option value="A">A</option>
          <option value="B">B</option>
          <option value="C">C</option>
          <option value="D">D</option>
          <option value="E">E</option>
        </select>

        <select name="sort_by" defaultValue={sortBy}>
          <option value="created_at">作成日</option>
          <option value="title">タイトル</option>
          <option value="last_updated">最終更新日</option>
          <option value="total_score">総合スコア</option>
        </select>

        <select name="sort_order" defaultValue={sortOrder}>
          <option value="desc">降順</option>
          <option value="asc">昇順</option>
        </select>

        <button type="submit">検索</button>
      </form>

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
              <th style={thStyle}>総合スコア</th>
              <th style={thStyle}>ランク</th>
              <th style={thStyle}>最終更新日</th>
              <th style={thStyle}>監視有効</th>
              <th style={thStyle}>詳細</th>
            </tr>
          </thead>
          <tbody>
            {data.items.length === 0 ? (
              <tr>
                <td style={tdStyle} colSpan={7}>
                  データがありません
                </td>
              </tr>
            ) : (
              data.items.map((dataset) => (
                <tr key={dataset.datasetId}>
                  <td style={tdStyle}>{dataset.title ?? "-"}</td>
                  <td style={tdStyle}>{dataset.sourceType}</td>
                  <td style={tdStyle}>{dataset.qualityScore?.total ?? "-"}</td>
                  <td style={tdStyle}>{dataset.qualityScore?.rank ?? "-"}</td>
                  <td style={tdStyle}>
                    {dataset.lastUpdated
                      ? new Date(dataset.lastUpdated).toLocaleString("ja-JP")
                      : "-"}
                  </td>
                  <td style={tdStyle}>
                    {dataset.monitoringEnabled ? "有効" : "無効"}
                  </td>
                  <td style={tdStyle}>
                    <Link href={`/datasets/${dataset.datasetId}`}>詳細</Link>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      <div style={{ marginTop: 16, display: "flex", gap: 12, alignItems: "center" }}>
        <span>
          Page {data.pagination.page} / {data.pagination.totalPages || 1}
        </span>

        {data.pagination.page > 1 && (
          <Link
            href={`/datasets?page=${data.pagination.page - 1}&keyword=${encodeURIComponent(
              keyword,
            )}&rank=${rank}&sort_by=${sortBy}&sort_order=${sortOrder}`}
          >
            前へ
          </Link>
        )}

        {data.pagination.page < data.pagination.totalPages && (
          <Link
            href={`/datasets?page=${data.pagination.page + 1}&keyword=${encodeURIComponent(
              keyword,
            )}&rank=${rank}&sort_by=${sortBy}&sort_order=${sortOrder}`}
          >
            次へ
          </Link>
        )}
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
