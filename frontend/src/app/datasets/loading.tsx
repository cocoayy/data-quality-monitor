import { TableSkeleton } from "@/components/ui/TableSkeleton";

export default function Loading() {
    return (
        <main style={{ padding: 32, fontFamily: "sans-serif" }}>
            <h1>データセット一覧</h1>
            <TableSkeleton rows={8} />
        </main>
    );
}
