"""Application configuration via environment variables."""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """VoiceReach application settings.

    All settings can be overridden via environment variables
    prefixed with VOICEREACH_ (e.g., VOICEREACH_HOST=0.0.0.0).
    """
    model_config = {"env_prefix": "VOICEREACH_"}

    # Server
    host: str = "127.0.0.1"
    port: int = 8765
    debug: bool = False

    # Local LLM (vllm-mlx)
    local_llm_base_url: str = "http://127.0.0.1:8000/v1"
    local_llm_model_fast: str = "Qwen/Qwen3-0.6B"
    local_llm_model_quality: str = "Qwen/Qwen3-1.7B"

    # Cloud LLM
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-haiku-4-5-20251001"
    openai_api_key: str = ""
    openai_model: str = "gpt-4.1-nano"

    # Cloud LLM timeout
    cloud_llm_timeout_s: float = 2.0

    # TTS
    tts_engine: str = "cosyvoice"
    tts_model_path: Path = Path("models/cosyvoice")
    tts_model_dir: str = "models/CosyVoice2-0.5B"
    tts_default_speaker: str = "default"

    # Eye tracking
    camera_id: int = 0
    gaze_model_path: str = "models/l2cs_net.onnx"
    num_zones: int = 4
    calibration_points: int = 5

    # Data paths
    data_dir: Path = Path("data")
    recordings_dir: Path = Path("data/recordings")
    cache_dir: Path = Path("data/cache")

    # Stage timeouts (ms)
    stage1_timeout_ms: int = 300
    stage2_timeout_ms: int = 600
    stage3_timeout_ms: int = 2000

    # Candidate generation
    num_candidates: int = 4
    stage1_temperature: float = 0.4
    stage2_temperature: float = 0.5
    stage3_temperature: float = 0.8


settings = Settings()
