"""Shared E2E fixtures for VoiceReach backend tests."""

from __future__ import annotations

from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from voicereach.main import create_app


@pytest.fixture
def app():
    """Create a fresh FastAPI app for testing.

    The Pipeline.initialize and Pipeline.shutdown methods are mocked so
    that no real hardware, ONNX models, or TTS models are required.
    """
    with (
        patch("voicereach.main.pipeline.initialize", new_callable=AsyncMock),
        patch("voicereach.main.pipeline.shutdown", new_callable=AsyncMock),
    ):
        yield create_app()


@pytest.fixture
def client(app):
    """Synchronous HTTP / WebSocket test client with app lifespan entered."""
    with TestClient(app) as c:
        yield c
