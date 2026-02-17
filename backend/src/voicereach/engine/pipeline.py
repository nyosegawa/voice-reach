"""Main pipeline coordinator.

Ties together all engine components:
  Camera -> Gaze Engine -> Zone -> IAL -> LLM Orchestrator -> TTS

This is the central orchestration point that the WebSocket handler
interacts with.
"""

from __future__ import annotations

import asyncio
import logging
import time

import numpy as np

from voicereach.config import settings
from voicereach.engine.gaze.calibration import GazeCalibrator
from voicereach.engine.gaze.gaze_estimator import GazeEstimator
from voicereach.engine.gaze.mediapipe_tracker import FaceData
from voicereach.engine.gaze.smoother import DualAxisSmoother
from voicereach.engine.gaze.zone_mapper import ZoneMapper, ZoneResult
from voicereach.engine.input.ial import IAL
from voicereach.engine.input.keyboard_adapter import KeyboardAdapter
from voicereach.engine.llm.orchestrator import HybridLLMOrchestrator
from voicereach.engine.tts.cosyvoice import CosyVoiceEngine
from voicereach.engine.tts.router import TTSRouter
from voicereach.models.context import ContextFrame, ConversationEntry, PatientState
from voicereach.models.events import (
    CandidateSet,
    CandidateUpdate,
    EventType,
    IALEvent,
    ServerMessage,
    TTSReady,
)

logger = logging.getLogger(__name__)


class Pipeline:
    """Main VoiceReach processing pipeline."""

    def __init__(self) -> None:
        # Gaze components
        self._calibrator = GazeCalibrator()
        self._smoother = DualAxisSmoother()
        self._zone_mapper = ZoneMapper(num_zones=settings.num_zones)
        self._gaze_estimator = GazeEstimator()

        # Input
        self._ial = IAL()
        self._keyboard = KeyboardAdapter()

        # LLM
        self._llm = HybridLLMOrchestrator()

        # TTS
        self._tts_engine = CosyVoiceEngine()
        self._tts_router = TTSRouter()

        # State
        self._context = ContextFrame()
        self._current_request_id: str | None = None
        self._current_candidates: CandidateSet | None = None
        self._message_callback = None

    async def initialize(self) -> None:
        """Initialize all pipeline components."""
        # Register keyboard adapter for dev mode
        self._ial.register_adapter(self._keyboard)
        self._ial.subscribe(self._on_ial_event)
        await self._ial.start()

        # Initialize gaze estimator (ONNX model, falls back to heuristic)
        self._gaze_estimator.initialize()

        # Initialize TTS
        await self._tts_engine.initialize()
        self._tts_router.set_engine(self._tts_engine)

        logger.info("Pipeline initialized")

    async def shutdown(self) -> None:
        """Shutdown all components."""
        await self._ial.stop()
        self._gaze_estimator.close()
        logger.info("Pipeline shut down")

    def set_message_callback(self, callback) -> None:
        """Set callback for sending messages to the client."""
        self._message_callback = callback

    def handle_gaze_update(self, zone_id: int, confidence: float) -> ZoneResult:
        """Process a gaze zone update from the client."""
        self._context.current_zone_id = zone_id
        return self._zone_mapper.map(zone_id / max(settings.num_zones - 1, 1), 0.5)

    def process_face_data(self, face_data: FaceData) -> ZoneResult | None:
        """Process extracted face data through gaze estimation + zone mapping.

        This runs the full server-side gaze pipeline:
          1. GazeEstimator  -- pitch/yaw from eye patches or heuristic
          2. DualAxisSmoother -- Kalman filtering for stability
          3. ZoneMapper -- continuous angles to discrete UI zone
        """
        gaze = self._gaze_estimator.estimate(face_data)
        smoothed_pitch, smoothed_yaw = self._smoother.update(
            gaze.pitch, gaze.yaw
        )
        # Normalise to 0-1 range for the zone mapper
        norm_x = (smoothed_yaw + 30) / 60  # yaw:  -30 .. +30 degrees
        norm_y = (smoothed_pitch + 20) / 40  # pitch: -20 .. +20 degrees
        norm_x = max(0.0, min(1.0, norm_x))
        norm_y = max(0.0, min(1.0, norm_y))
        return self._zone_mapper.map(norm_x, norm_y)

    def handle_key(self, key: str) -> None:
        """Forward a keyboard event to the keyboard adapter."""
        self._keyboard.handle_key(key)

    async def handle_candidate_selected(self, request_id: str, index: int) -> None:
        """Handle candidate selection by the user."""
        if self._current_candidates and self._current_candidates.request_id == request_id:
            if 0 <= index < len(self._current_candidates.candidates):
                candidate = self._current_candidates.candidates[index]
                text = candidate.text

                # Add to conversation history
                self._context.conversation_history.append(
                    ConversationEntry(role="patient", text=text)
                )

                # Cancel pending LLM stages
                await self._llm.cancel_pending(request_id)

                # Synthesize speech
                audio_path = await self._tts_router.synthesize(text)
                if audio_path and self._message_callback:
                    await self._message_callback(TTSReady(
                        audio_url=f"/audio/{audio_path.name}",
                        text=text,
                    ))

    async def trigger_generation(self) -> None:
        """Trigger new candidate generation based on current context."""
        async for candidate_set in self._llm.generate_candidates(
            context=self._context,
            num_candidates=settings.num_candidates,
        ):
            self._current_candidates = candidate_set
            self._current_request_id = candidate_set.request_id

            if self._message_callback:
                await self._message_callback(CandidateUpdate(
                    request_id=candidate_set.request_id,
                    candidate_set=candidate_set,
                    is_final=candidate_set.is_final,
                ))

    def _on_ial_event(self, event: IALEvent) -> None:
        """Handle IAL events."""
        if event.event_type == EventType.CONFIRM:
            # Confirm = select the currently gazed candidate
            if self._current_candidates and self._context.current_zone_id >= 0:
                asyncio.create_task(
                    self.handle_candidate_selected(
                        self._current_candidates.request_id,
                        self._context.current_zone_id,
                    )
                )
        elif event.event_type == EventType.SELECT:
            if event.target_id is not None and self._current_candidates:
                asyncio.create_task(
                    self.handle_candidate_selected(
                        self._current_candidates.request_id,
                        event.target_id,
                    )
                )
        elif event.event_type == EventType.EMERGENCY:
            logger.warning("EMERGENCY event received!")
            # TODO: Trigger emergency notification to caregivers

    def add_partner_utterance(self, text: str) -> None:
        """Add a conversation partner's utterance and trigger generation."""
        self._context.conversation_history.append(
            ConversationEntry(role="partner", text=text)
        )
        asyncio.create_task(self.trigger_generation())
