"""End-to-end tests for the caregiver WebSocket connection.

Tests the /ws/caregiver endpoint: connection handling, message acceptance,
and coexistence with patient connections.
"""

from __future__ import annotations

import time

from fastapi.testclient import TestClient

from voicereach.models.events import EventType, InputSource


class TestCaregiverWSConnect:
    """Basic caregiver WebSocket connectivity."""

    def test_caregiver_ws_connect(self, client: TestClient):
        """Connect to /ws/caregiver and verify the connection succeeds."""
        with client.websocket_connect("/ws/caregiver") as ws:
            assert ws is not None

    def test_caregiver_ws_connect_multiple(self, client: TestClient):
        """Multiple caregiver connections can coexist."""
        with client.websocket_connect("/ws/caregiver") as ws1:
            with client.websocket_connect("/ws/caregiver") as ws2:
                assert ws1 is not None
                assert ws2 is not None


class TestCaregiverReceivesStatus:
    """Tests for caregiver receiving patient status updates.

    The current caregiver endpoint logs incoming messages but does not
    proactively push status updates. These tests verify the connection
    stays alive while messages are exchanged and that patient and
    caregiver connections work simultaneously.
    """

    def test_caregiver_accepts_json_messages(self, client: TestClient):
        """Caregiver can send arbitrary JSON without causing errors."""
        with client.websocket_connect("/ws/caregiver") as ws:
            ws.send_json({"action": "get_status"})
            ws.send_json({"action": "ping"})
            # The caregiver endpoint does not currently send responses;
            # it only logs. We verify the connection stays open by not
            # raising any exceptions.

    def test_caregiver_and_patient_simultaneous(self, client: TestClient):
        """Patient and caregiver connections work simultaneously."""
        with client.websocket_connect("/ws/patient") as ws_patient:
            with client.websocket_connect("/ws/caregiver") as ws_caregiver:
                # Patient sends a valid message
                ws_patient.send_json({
                    "type": "gaze_update",
                    "zone_id": 1,
                    "confidence": 0.9,
                    "timestamp_ms": int(time.time() * 1000),
                })

                # Caregiver sends a message
                ws_caregiver.send_json({"action": "status_request"})

                # Patient connection still works (probe with invalid message)
                ws_patient.send_json({"type": "unknown_probe"})
                resp = ws_patient.receive_json()
                assert resp["type"] == "error"

    def test_caregiver_survives_patient_invalid_messages(self, client: TestClient):
        """Caregiver connection stays alive when patient sends invalid data."""
        with client.websocket_connect("/ws/patient") as ws_patient:
            with client.websocket_connect("/ws/caregiver") as ws_caregiver:
                # Patient sends invalid message
                ws_patient.send_json({"type": "bad_type"})
                resp = ws_patient.receive_json()
                assert resp["type"] == "error"

                # Caregiver can still send messages
                ws_caregiver.send_json({"action": "still_alive"})
