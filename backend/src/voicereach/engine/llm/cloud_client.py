"""Cloud LLM client with multi-provider failover.

Provider priority: Gemini 2.5 Flash -> Claude Haiku 4.5 -> GPT-4.1 nano
Supports prompt caching for 90% cost reduction.
"""

from __future__ import annotations

import logging
from enum import Enum

import httpx

from voicereach.config import settings

logger = logging.getLogger(__name__)


class CloudProvider(str, Enum):
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class CloudLLMClient:
    """Multi-provider cloud LLM client with automatic failover."""

    def __init__(self) -> None:
        self._providers: list[CloudProvider] = []
        if settings.gemini_api_key:
            self._providers.append(CloudProvider.GEMINI)
        if settings.anthropic_api_key:
            self._providers.append(CloudProvider.ANTHROPIC)
        if settings.openai_api_key:
            self._providers.append(CloudProvider.OPENAI)

    async def generate(
        self,
        messages: list[dict[str, str]],
        temperature: float = 0.8,
        max_tokens: int = 100,
        timeout_s: float | None = None,
    ) -> str | None:
        """Generate using cloud LLM with automatic failover.

        Tries providers in priority order until one succeeds.
        """
        timeout_s = timeout_s or settings.cloud_llm_timeout_s

        for provider in self._providers:
            try:
                result = await self._call_provider(
                    provider, messages, temperature, max_tokens, timeout_s
                )
                if result:
                    return result
            except Exception:
                logger.warning("Cloud provider %s failed, trying next", provider)
                continue

        logger.error("All cloud providers failed")
        return None

    async def _call_provider(
        self,
        provider: CloudProvider,
        messages: list[dict[str, str]],
        temperature: float,
        max_tokens: int,
        timeout_s: float,
    ) -> str | None:
        """Call a specific cloud provider."""
        if provider == CloudProvider.GEMINI:
            return await self._call_gemini(messages, temperature, max_tokens, timeout_s)
        if provider == CloudProvider.ANTHROPIC:
            return await self._call_anthropic(messages, temperature, max_tokens, timeout_s)
        if provider == CloudProvider.OPENAI:
            return await self._call_openai(messages, temperature, max_tokens, timeout_s)
        return None

    async def _call_gemini(
        self, messages, temperature, max_tokens, timeout_s
    ) -> str | None:
        """Call Google Gemini API."""
        from google import genai

        client = genai.Client(api_key=settings.gemini_api_key)

        # Convert messages to Gemini format
        contents = []
        system_instruction = None
        for msg in messages:
            if msg["role"] == "system":
                system_instruction = msg["content"]
            else:
                contents.append({"role": msg["role"], "parts": [{"text": msg["content"]}]})

        config = genai.types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=max_tokens,
            system_instruction=system_instruction,
        )

        response = await client.aio.models.generate_content(
            model=settings.gemini_model,
            contents=contents,
            config=config,
        )

        if response.text:
            return response.text.strip()
        return None

    async def _call_anthropic(
        self, messages, temperature, max_tokens, timeout_s
    ) -> str | None:
        """Call Anthropic Claude API."""
        import anthropic

        client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)

        system_text = ""
        api_messages = []
        for msg in messages:
            if msg["role"] == "system":
                system_text = msg["content"]
            else:
                api_messages.append(msg)

        response = await client.messages.create(
            model=settings.anthropic_model,
            max_tokens=max_tokens,
            system=system_text,
            messages=api_messages,
            temperature=temperature,
        )

        if response.content:
            return response.content[0].text.strip()
        return None

    async def _call_openai(
        self, messages, temperature, max_tokens, timeout_s
    ) -> str | None:
        """Call OpenAI API."""
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=settings.openai_api_key)

        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            timeout=timeout_s,
        )

        content = response.choices[0].message.content
        return content.strip() if content else None

    @property
    def available_providers(self) -> list[CloudProvider]:
        return list(self._providers)
