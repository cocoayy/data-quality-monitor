"use client";

export function ErrorState({
    message,
    reset,
}: {
    message?: string;
    reset?: () => void;
}) {
    return (
        <div
            style={{
                border: "1px solid #f0b4b4",
                backgroundColor: "#fff5f5",
                borderRadius: 8,
                padding: 16,
                marginTop: 16,
            }}
        >
            <p>{message ?? "データ取得に失敗しました。"}</p>
            {reset && (
                <button onClick={reset} style={{ marginTop: 8 }}>
                    再試行
                </button>
            )}
        </div>
    );
}
