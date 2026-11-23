from functools import cache

import anthropic
from anthropic.types import TextBlock


@cache
def _client() -> anthropic.Anthropic:
    return anthropic.Anthropic()


def create_text_message(*, model: str, max_tokens: int, system: str, prompt: str) -> str:
    response = _client().messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    for block in response.content:
        if isinstance(block, TextBlock):
            return block.text.strip()
    raise ValueError("Claude 응답에 텍스트 블록이 없습니다.")
