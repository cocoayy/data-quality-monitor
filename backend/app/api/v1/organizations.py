from fastapi import APIRouter

from app.db.connection import get_connection

router = APIRouter(prefix="/api/v1/organizations", tags=["organizations"])


@router.get("")
def list_organizations() -> dict:
    query = """
        SELECT
            id,
            name,
            display_name,
            source_type,
            is_active,
            created_at,
            updated_at
        FROM organizations
        ORDER BY created_at DESC
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

    items = []
    for row in rows:
        items.append(
            {
                "organizationId": str(row["id"]),
                "name": row["name"],
                "displayName": row["display_name"],
                "sourceType": row["source_type"],
                "isActive": row["is_active"],
                "createdAt": row["created_at"].isoformat() if row["created_at"] else None,
                "updatedAt": row["updated_at"].isoformat() if row["updated_at"] else None,
            }
        )

    return {"items": items}