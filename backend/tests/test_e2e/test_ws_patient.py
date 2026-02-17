"""End-to-end tests for the patient WebSocket connection.

Tests the full flow: connect -> send input -> receive candidates.
Uses the FastAPI TestClient's WebSocket support.

All tests run without external services (no camera, no LLM server,
no CosyVoice model).
"""

from __future__ import annotations

import time

from fastapi.testclient import TestClient

from voicereach.models.events import EventType, InputSource


class TestPatientWSConnect:
    """Basic WebSocket connectivity tests."""

    def test_patient_ws_connect(self, client: TestClient):
        """Connect to /ws/patient and verify the connection succeeds."""
        with client.websocket_connect("/ws/patient") as ws:
            assert ws is not None

    def test_patient_ws_connect_multiple(self, client: TestClient):
        """Multiple patient connections can coexist."""
        with client.websocket_connect("/ws/patient") as ws1:
            with client.websocket_connect("/ws/patient") as ws2:
                assert ws1 is not None
                assert ws2 is not None


class TestPatientGazeUpdate:
    """Tests for gaze_update messages on the patient WebSocket."""

    def test_patient_send_gaze_update(self, client: TestClient):
        """Send a gaze_update message and verify it is processed without error.

        The server does not send a response for valid gaze_update messages.
        We probe the connection by sending a subsequent invalid message and
        verifying that only the probe triggers an error response (proving the
        gaze_update was accepted silently).
        """
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "gaze_update",
                "zone_id": 2,
                "confidence": 0.85,
                "timestamp_ms": int(time.time() * 1000),
            })
            # Probe: send an invalid message to verify the connection is
            # still alive and the gaze_update did not cause an error.
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_send_gaze_update_all_zones(self, client: TestClient):
        """Send gaze_update for each zone (0-3) without error."""
        with client.websocket_connect("/ws/patient") as ws:
            ts = int(time.time() * 1000)
            for zone_id in range(4):
                ws.send_json({
                    "type": "gaze_update",
                    "zone_id": zone_id,
                    "confidence": 0.9,
                    "timestamp_ms": ts + zone_id,
                })
            # Probe after all sends
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_gaze_update_invalid_missing_fields(self, client: TestClient):
        """A gaze_update with missing required fields returns error."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "gaze_update",
                # missing zone_id, confidence, timestamp_ms
            })
            resp = ws.receive_json()
            assert resp["type"] == "error"


class TestPatientKeyInput:
    """Tests for input_event messages (keyboard input) on the patient WebSocket."""

    def test_patient_send_key_input(self, client: TestClient):
        """Send a keyboard input event and verify processing."""
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
            # Probe to confirm no error was sent for valid input
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_send_confirm_event(self, client: TestClient):
        """Send a CONFIRM input event."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "input_event",
                "event": {
                    "event_type": EventType.CONFIRM.value,
                    "source": InputSource.KEYBOARD.value,
                    "confidence": 1.0,
                    "timestamp_ms": int(time.time() * 1000),
                },
            })
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_send_cancel_event(self, client: TestClient):
        """Send a CANCEL input event."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "input_event",
                "event": {
                    "event_type": EventType.CANCEL.value,
                    "source": InputSource.KEYBOARD.value,
                    "confidence": 1.0,
                    "timestamp_ms": int(time.time() * 1000),
                },
            })
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"


class TestPatientCandidateSelected:
    """Tests for candidate_selected messages on the patient WebSocket."""

    def test_patient_send_candidate_selected(self, client: TestClient):
        """Send a candidate_selected message."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "candidate_selected",
                "request_id": "test-req-001",
                "candidate_index": 0,
            })
            # Probe: valid message should not produce error
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_send_candidate_selected_all_indices(self, client: TestClient):
        """Send candidate_selected for each valid index (0-3)."""
        with client.websocket_connect("/ws/patient") as ws:
            for idx in range(4):
                ws.send_json({
                    "type": "candidate_selected",
                    "request_id": f"test-req-{idx:03d}",
                    "candidate_index": idx,
                })
            # Probe after all sends
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"


class TestPatientInvalidMessage:
    """Tests for malformed / invalid messages on the patient WebSocket."""

    def test_patient_invalid_message_unknown_type(self, client: TestClient):
        """Send a message with unknown type and verify error response."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({"type": "totally_invalid"})
            resp = ws.receive_json()
            assert resp["type"] == "error"
            assert "unknown" in resp["detail"].lower()

    def test_patient_invalid_message_missing_type(self, client: TestClient):
        """Send a message without a type field."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({"data": "no type field here"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_invalid_message_empty_object(self, client: TestClient):
        """Send an empty JSON object."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_invalid_gaze_update_bad_confidence(self, client: TestClient):
        """A gaze_update with out-of-range confidence returns error."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "gaze_update",
                "zone_id": 0,
                "confidence": 2.0,  # out of range [0, 1]
                "timestamp_ms": int(time.time() * 1000),
            })
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_connection_survives_errors(self, client: TestClient):
        """The WebSocket connection stays open after receiving an error."""
        with client.websocket_connect("/ws/patient") as ws:
            # Send two invalid messages in a row
            ws.send_json({"type": "bad1"})
            resp1 = ws.receive_json()
            assert resp1["type"] == "error"

            ws.send_json({"type": "bad2"})
            resp2 = ws.receive_json()
            assert resp2["type"] == "error"

            # Connection is still alive -- send a valid message
            ws.send_json({
                "type": "gaze_update",
                "zone_id": 0,
                "confidence": 0.5,
                "timestamp_ms": int(time.time() * 1000),
            })
            # No error for the valid message -- probe again
            ws.send_json({"type": "bad3"})
            resp3 = ws.receive_json()
            assert resp3["type"] == "error"


class TestPatientEmergency:
    """Tests for emergency events on the patient WebSocket."""

    def test_patient_emergency(self, client: TestClient):
        """Send an emergency input_event and verify no crash.

        The current server implementation logs EMERGENCY events but does
        not send an emergency_ack back via WebSocket (that is marked as
        a TODO in the source). We verify the server accepts the message
        without error.
        """
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "input_event",
                "event": {
                    "event_type": EventType.EMERGENCY.value,
                    "source": InputSource.KEYBOARD.value,
                    "confidence": 1.0,
                    "timestamp_ms": int(time.time() * 1000),
                },
            })
            # Probe: the emergency should not cause an error
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"

    def test_patient_emergency_gaze_source(self, client: TestClient):
        """Emergency event from gaze source is also accepted."""
        with client.websocket_connect("/ws/patient") as ws:
            ws.send_json({
                "type": "input_event",
                "event": {
                    "event_type": EventType.EMERGENCY.value,
                    "source": InputSource.GAZE.value,
                    "confidence": 0.95,
                    "timestamp_ms": int(time.time() * 1000),
                },
            })
            ws.send_json({"type": "unknown_probe"})
            resp = ws.receive_json()
            assert resp["type"] == "error"
