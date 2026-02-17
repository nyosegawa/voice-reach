"""WebSocket endpoint for patient UI <-> backend communication."""

from __future__ import annotations

import json
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError

from voicereach.models.events import (
    CandidateSelected,
    GazeUpdate,
    InputEvent,
)

logger = logging.getLogger(__name__)
router = APIRouter()


class ConnectionManager:
    """Manages active WebSocket connections."""

    def __init__(self) -> None:
        self.patient_connections: list[WebSocket] = []
        self.caregiver_connections: list[WebSocket] = []

    async def connect_patient(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.patient_connections.append(websocket)

    async def connect_caregiver(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.caregiver_connections.append(websocket)

    def disconnect_patient(self, websocket: WebSocket) -> None:
        self.patient_connections.remove(websocket)

    def disconnect_caregiver(self, websocket: WebSocket) -> None:
        self.caregiver_connections.remove(websocket)

    async def broadcast_to_caregivers(self, message: dict) -> None:
        for connection in self.caregiver_connections:
            await connection.send_json(message)


manager = ConnectionManager()


def parse_client_message(data: dict) -> GazeUpdate | InputEvent | CandidateSelected | None:
    """Parse an incoming WebSocket message by its type field."""
    msg_type = data.get("type")
    try:
        if msg_type == "gaze_update":
            return GazeUpdate(**data)
        if msg_type == "input_event":
            return InputEvent(**data)
        if msg_type == "candidate_selected":
            return CandidateSelected(**data)
    except ValidationError as e:
        logger.warning("Invalid message: %s", e)
    return None


@router.websocket("/ws/patient")
async def patient_websocket(websocket: WebSocket) -> None:
    """WebSocket endpoint for the patient UI."""
    await manager.connect_patient(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = parse_client_message(data)
            if message is None:
                await websocket.send_json({"type": "error", "detail": "unknown message type"})
                continue
            # TODO: Route to pipeline coordinator
            logger.debug("Received: %s", message)
    except WebSocketDisconnect:
        manager.disconnect_patient(websocket)


@router.websocket("/ws/caregiver")
async def caregiver_websocket(websocket: WebSocket) -> None:
    """WebSocket endpoint for the caregiver PWA."""
    await manager.connect_caregiver(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.debug("Caregiver message: %s", data)
    except WebSocketDisconnect:
        manager.disconnect_caregiver(websocket)
