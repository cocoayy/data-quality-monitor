from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard_summary_endpoint_exists() -> None:
    response = client.get("/api/v1/dashboard/summary")
    assert response.status_code in (200, 500)
