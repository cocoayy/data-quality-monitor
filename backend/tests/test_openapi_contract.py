from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_openapi_available() -> None:
    response = client.get("/openapi.json")
    assert response.status_code == 200

    data = response.json()
    assert "openapi" in data
    assert "paths" in data
    assert "/api/v1/datasets" in data["paths"]
    assert "/api/v1/alerts" in data["paths"]
    assert "/api/v1/dashboard/summary" in data["paths"]
