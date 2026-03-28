"use client";

import { ErrorState } from "@/components/ui/ErrorState";

export default function Error({
    reset,
}: {
    error: Error;
    reset: () => void;
}) {
    return (
        <main style={{ padding: 32, fontFamily: "sans-serif" }}>
            <h1>ダッシュボード</h1>
            <ErrorState message="ダッシュボードの取得に失敗しました。" reset={reset} />
        </main>
    );
}
