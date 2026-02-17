"""End-to-end tests for the /health HTTP endpoint.

Verifies that the health check endpoint returns the expected status
and version information.
"""

from __future__ import annotations

from fastapi.testclient import TestClient


class TestHealthEndpoint:

    def test_health_returns_200(self, client: TestClient):
        """GET /health returns HTTP 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_status_ok(self, client: TestClient):
        """GET /health body contains status 'ok'."""
        data = client.get("/health").json()
        assert data["status"] == "ok"

    def test_health_version_exists(self, client: TestClient):
        """GET /health body contains a version field."""
        data = client.get("/health").json()
        assert "version" in data
        assert isinstance(data["version"], str)
        assert len(data["version"]) > 0

    def test_health_response_shape(self, client: TestClient):
        """GET /health returns a dict with at least status and version."""
        data = client.get("/health").json()
        assert isinstance(data, dict)
        assert set(data.keys()) >= {"status", "version"}
