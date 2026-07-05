"""
One smoke test: does the app boot and does /health return 200? This isn't
about coverage — it's a tripwire. If a future change breaks app startup
(bad import, broken config), this fails immediately instead of surfacing as
a confusing CI lint pass but runtime crash.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check_returns_ok():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
