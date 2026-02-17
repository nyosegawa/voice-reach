"""Local LLM client via vllm-mlx OpenAI-compatible API.

Connects to a locally running vllm-mlx server that serves
Qwen3-0.6B and Qwen3-1.7B models with prefix caching.
"""

from __future__ import annotations

import logging

from openai import AsyncOpenAI

from voicereach.config import settings

logger = logging.getLogger(__name__)


class LocalLLMClient:
    """Client for local LLM inference via vllm-mlx."""

    def __init__(self, base_url: str | None = None) -> None:
        self._base_url = base_url or settings.local_llm_base_url
        self._client = AsyncOpenAI(
            base_url=self._base_url,
            api_key="not-needed",  # Local server
        )

    async def generate(
        self,
        model: str,
        messages: list[dict[str, str]],
        temperature: float = 0.5,
        max_tokens: int = 100,
        timeout_s: float = 5.0,
    ) -> str | None:
        """Generate a completion from a local model.

        Args:
            model: Model name (e.g., "Qwen/Qwen3-0.6B")
            messages: Chat messages in OpenAI format
            temperature: Sampling temperature
            max_tokens: Maximum output tokens
            timeout_s: Timeout in seconds

        Returns:
            Generated text or None if failed.
        """
        try:
            response = await self._client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=timeout_s,
            )
            content = response.choices[0].message.content
            return content.strip() if content else None
        except Exception:
            logger.exception("Local LLM generation failed for %s", model)
            return None

    async def health_check(self) -> bool:
        """Check if the local LLM server is accessible."""
        try:
            await self._client.models.list()
            return True
        except Exception:
            return False
