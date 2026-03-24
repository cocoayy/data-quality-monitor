export default function Home() {
  return (
    <main style={{ padding: "32px", fontFamily: "sans-serif" }}>
      <h1>Data Quality Monitor</h1>
      <p>オープンデータ向けのデータ品質監視ツール</p>

      <section style={{ marginTop: "24px" }}>
        <h2>今後の実装予定</h2>
        <ul>
          <li>ダッシュボード</li>
          <li>データセット一覧</li>
          <li>データセット詳細</li>
          <li>スコア履歴</li>
          <li>アラート一覧</li>
        </ul>
      </section>
    </main>
  );
}