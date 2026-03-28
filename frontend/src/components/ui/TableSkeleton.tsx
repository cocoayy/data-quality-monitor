export function TableSkeleton({ rows = 5 }: { rows?: number }) {
    return (
        <div style={{ marginTop: 16 }}>
            {Array.from({ length: rows }).map((_, idx) => (
                <div
                    key={idx}
                    style={{
                        height: 44,
                        borderRadius: 6,
                        backgroundColor: "#f3f3f3",
                        marginBottom: 10,
                    }}
                />
            ))}
        </div>
    );
}
