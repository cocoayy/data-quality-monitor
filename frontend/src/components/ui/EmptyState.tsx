export function EmptyState({ message }: { message: string }) {
    return (
        <div
            style={{
                border: "1px dashed #ccc",
                borderRadius: 8,
                padding: 24,
                textAlign: "center",
                color: "#666",
                marginTop: 16,
            }}
        >
            {message}
        </div>
    );
}
