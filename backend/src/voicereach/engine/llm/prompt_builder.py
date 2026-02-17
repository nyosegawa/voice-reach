"""Prompt builder for candidate generation.

Assembles system prompts with PVP, context, and instructions
following the 3-layer cache design:
  Layer 1 (static): PVP + task instructions (~2300 tokens)
  Layer 2 (session): environment + conversation partner (~300 tokens)
  Layer 3 (dynamic): conversation history + feedback (~900 tokens)
"""

from __future__ import annotations

from voicereach.models.context import ContextFrame


SYSTEM_PROMPT_TEMPLATE = """あなたはALS患者の代わりに発話候補を生成するアシスタントです。

## 指示
- 患者が会話の中で言いそうな発話候補を{num_candidates}個生成してください
- 各候補は異なる意図軸（感情表現、質問、自己言及、他者言及、行動依頼、ユーモア、話題転換）から選んでください
- 患者の口調・語彙・表現パターンを忠実に再現してください
- 短く自然な日本語で、1-2文以内にしてください

## 出力形式
以下のJSON配列で出力してください:
```json
[
  {{"text": "発話テキスト", "intent": "意図軸名", "confidence": 0.0-1.0}},
  ...
]
```

意図軸: emotional_response, question, self_reference, other_reference, action_request, humor, topic_change

{pvp_section}
{environment_section}"""


def build_system_prompt(
    context: ContextFrame,
    num_candidates: int = 4,
) -> str:
    """Build the system prompt for candidate generation."""
    pvp_section = ""
    if context.pvp_text:
        pvp_section = f"\n## パーソナルボイスプロファイル (PVP)\n{context.pvp_text}"

    env = context.environment
    env_parts = []
    if env.location:
        env_parts.append(f"場所: {env.location}")
    if env.people_present:
        env_parts.append(f"会話相手: {', '.join(env.people_present)}")
    if env.time_of_day:
        env_parts.append(f"時間帯: {env.time_of_day}")
    if env.activity:
        env_parts.append(f"状況: {env.activity}")

    environment_section = ""
    if env_parts:
        environment_section = "\n## 環境情報\n" + "\n".join(f"- {p}" for p in env_parts)

    return SYSTEM_PROMPT_TEMPLATE.format(
        num_candidates=num_candidates,
        pvp_section=pvp_section,
        environment_section=environment_section,
    )


def build_messages(
    context: ContextFrame,
    num_candidates: int = 4,
) -> list[dict[str, str]]:
    """Build the full message list for LLM generation."""
    system = build_system_prompt(context, num_candidates)
    messages: list[dict[str, str]] = [{"role": "system", "content": system}]

    # Add conversation history
    for entry in context.conversation_history[-10:]:
        role = "assistant" if entry.role == "patient" else "user"
        messages.append({"role": role, "content": entry.text})

    # If no recent conversation, add a generic prompt
    if not context.conversation_history:
        messages.append({
            "role": "user",
            "content": "（会話が始まったところです。最初の発話候補を生成してください）",
        })

    return messages
