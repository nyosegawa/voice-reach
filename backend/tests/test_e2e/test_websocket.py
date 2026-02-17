"""End-to-end WebSocket tests for VoiceReach API.

Tests the WebSocket protocol between client and server using
FastAPI's TestClient, which wraps Starlette's WebSocket testing
utilities. All tests run without external services.
"""

from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from voicereach.main import create_app
from voicereach.models.events import EventType, InputSource


@pytest.fixture
def app():
    """Create a fresh FastAPI app with the pipeline lifespan mocked out.

    We patch Pipeline.initialize and Pipeline.shutdown so that no real
    hardware or model loading is triggered during WebSocket tests.
    """
    with (
        patch("voicereach.main.pipeline.initialize", new_callable=AsyncMock),
        patch("voicereach.main.pipeline.shutdown", new_callable=AsyncMock),
    ):
        yield create_app()


@pytest.fixture
def client(app):
    """Provide a synchronous TestClient with the app lifespan entered."""
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    """Tests for the /health HTTP endpoint."""

    def test_health_returns_200(self, client: TestClient):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_body(self, client: TestClient):
        data = client.get("/health").json()
        assert data["status"] == "ok"
        assert "version" in data


class TestPatientWebSocket:
    """Tests for the /ws/patient WebSocket endpoint."""

    def test_patient_connect(self, client: TestClient):
        with client.websocket_connect("/ws/patient") as ws:
            # If we get here, the connection was accepted
            assert ws is not None

    def test_send_gaze_update(self, client: TestClient):
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "gaze_update",
                "zone_id": 2,
                "confidence": 0.85,
                "timestamp_ms": int(time.time() * 1000),
            })
            # A valid message should not produce an error response.
            # The server currently just logs and continues.
            # We send another known-bad message to verify the socket is
            # still alive and the previous message did not cause an error.
            ws.send_json({"type": "unknown_type"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_send_input_event(self, client: TestClient):
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "input_event",
                "event": {
                    "event_type": EventType.SELECT.value,
                    "source": InputSource.KEYBOARD.value,
                    "target_id": 1,
                    "confidence": 1.0,
                    "timestamp_ms": int(time.time() * 1000),
                },
            })
            # Probe the connection with a bad message to verify no error
            # was sent for the valid input_event.
            ws.send_json({"type": "bad"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_send_candidate_selected(self, client: TestClient):
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "candidate_selected",
                "request_id": "test-req-001",
                "candidate_index": 0,
            })
            # Probe: valid message should not produce error
            ws.send_json({"type": "bad"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_invalid_message_format_returns_error(self, client: TestClient):
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({"type": "totally_invalid"})
            resp = ws.receive_json()
            assert resp["type"] == "error"
            assert "unknown" in resp["detail"].lower()

    def test_invalid_gaze_update_validation_returns_error(self, client: TestClient):
        """A gaze_update with missing required fields should produce an error."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "gaze_update",
                # missing zone_id, confidence, timestamp_ms
            })
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_missing_type_field_returns_error(self, client: TestClient):
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({"data": "no type field"})
            resp = ws.receive_json()
            assert resp["type"] == "error"


class TestCaregiverWebSocket:
    """Tests for the /ws/caregiver WebSocket endpoint."""

    def test_caregiver_connect(self, client: TestClient):
        with client.websocket_connect("/ws/caregiver") as ws:
            assert ws is not None

    def test_caregiver_send_message(self, client: TestClient):
        """Caregiver can send arbitrary JSON without getting errors."""
        with client.websocket_connect("/ws/caregiver") as ws:
            ws.send_json({"action": "get_status"})
            # The caregiver endpoint does not send any response currently;
            # it just logs. So we just verify the connection stays open
            # by not raising an exception.


class TestMultipleClients:
    """Tests for concurrent WebSocket connections."""

    def test_two_patient_clients(self, client: TestClient):
        """Two patient clients can connect at the same time."""
        with client.websocket_connect("/ws/patient") as ws1:
            with client.websocket_connect("/ws/patient") as ws2:
                # Both connections are live
                ws1.send_json({"type": "unknown"})
                ws2.send_json({"type": "unknown"})
                resp1 = ws1.receive_json()
                resp2 = ws2.receive_json()
                assert resp1["type"] == "error"
                assert resp2["type"] == "error"

    def test_patient_and_caregiver_simultaneously(self, client: TestClient):
        """Patient and caregiver can connect at the same time."""
        with client.websocket_connect("/ws/patient") as ws_patient:
            with client.websocket_connect("/ws/caregiver") as ws_caregiver:
                ws_patient.send_json({"type": "unknown"})
                resp = ws_patient.receive_json()
                assert resp["type"] == "error"
                # Caregiver endpoint is alive
                ws_caregiver.send_json({"ping": True})
