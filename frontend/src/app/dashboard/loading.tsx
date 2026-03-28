import { TableSkeleton } from "@/components/ui/TableSkeleton";

export default function Loading() {
    return (
        <main style={{ padding: 32, fontFamily: "sans-serif" }}>
            <h1>ダッシュボード</h1>
            <TableSkeleton rows={6} />
        </main>
    );
}
