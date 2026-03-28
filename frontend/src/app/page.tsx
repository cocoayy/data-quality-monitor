import Link from "next/link";

export default function Home() {
  return (
    <main style={{ padding: "32px", fontFamily: "sans-serif" }}>
      <h1>Data Quality Monitor</h1>
      <p>オープンデータ向けのデータ品質監視ツール</p>

      <div style={{ marginTop: "24px", display: "grid", gap: 12 }}>
        <Link href="/dashboard">ダッシュボードを見る</Link>
        <Link href="/datasets">データセット一覧を見る</Link>
        <Link href="/alerts">アラート一覧を見る</Link>
      </div>
    </main>
  );
}
