"""
콘텐츠 생성기 — Claude API 기반.
Instagram + Threads 겸용. 플랫폼별 최적화된 톤과 길이 적용.

Instagram 포맷:
  - 캡션 길이: 150~300자 (인스타는 시각 중심이므로 텍스트는 간결하게)
  - 해시태그 자동 생성 (인스타 노출에 중요)
  - 이모지 2~3개

Threads 포맷 (기존 유지):
  - 길이: 200~350자
  - 구조: 공감 → 비개발자인데 → 해결 → 당신도 됩니다
  - 이모지 1~2개
"""

import anthropic

MODEL = "claude-sonnet-4-6"
_client = anthropic.Anthropic()

# ── 플랫폼별 시스템 프롬프트 ───────────────────────────

INSTAGRAM_SYSTEM = """당신은 비개발자 직장인을 위한 Instagram 계정의 콘텐츠 작성자입니다.
타깃: 코딩 경험 없는 비개발자 직장인.
작성 원칙:
- 친근하고 실용적인 말투
- 150~300자 (인스타 캡션은 간결하게)
- 이모지 2~3개 적절히 사용
- 줄바꿈으로 가독성 확보
- 마지막에 관련 해시태그 5~7개 자동 생성 (#으로 시작)
- 구조: [흥미 유발 첫 줄] → [내용] → [행동 유도] → [해시태그]"""

THREADS_SYSTEM = """당신은 Threads 계정의 콘텐츠 작성자입니다.
타깃: 코딩 경험 없는 비개발자 직장인.
톤: 솔직하고 공감가는 직장인 말투. 이모지 1~2개 사용.
길이: 200~350자.
구조: [공감 상황] → [나는 비개발자인데] → [이렇게 해결했다] → [당신도 됩니다]"""

FREE_CONTENT_SYSTEM = """당신은 비개발자 직장인을 위한 콘텐츠 작성자입니다.
타깃: 코딩 경험 없는 비개발자 직장인.
톤: 친근하고 실용적. 이모지 1~2개.
길이: 150~250자.
구조: [무료 자료 소개] → [이걸 보면 뭘 할 수 있나] → [팔로우+댓글 남기시면 드립니다]"""


# ── 생성 함수 ──────────────────────────────────────────

def generate_instagram_caption(topic: str, image_description: str = "") -> str:
    """Instagram 게시물용 캡션 생성. 해시태그 자동 포함."""
    context = f"주제: {topic}"
    if image_description:
        context += f"\n이미지 설명: {image_description}"

    resp = _client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=INSTAGRAM_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"다음 내용으로 Instagram 게시물을 작성해주세요:\n{context}",
        }],
    )
    return resp.content[0].text.strip()


def generate_threads_post(idea: str) -> str:
    """Threads 포스트 생성."""
    resp = _client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=THREADS_SYSTEM,
        messages=[{
            "role": "user",
            "content": f"다음 상황을 바탕으로 Threads 포스트를 작성해주세요:\n{idea}",
        }],
    )
    return resp.content[0].text.strip()


def generate_free_content_post(resource_name: str, resource_url: str) -> str:
    """무료 자료 배포용 포스트 생성 (Threads + Instagram 겸용)."""
    resp = _client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=FREE_CONTENT_SYSTEM,
        messages=[{
            "role": "user",
            "content": (
                f"자료명: {resource_name}\n"
                f"링크: {resource_url}\n\n"
                "위 무료 자료를 배포하는 포스트를 작성해주세요."
            ),
        }],
    )
    return resp.content[0].text.strip()


def generate_cross_platform(topic: str) -> dict:
    """
    Instagram + Threads 동시 게시용 콘텐츠 생성.
    동일 주제에 대해 각 플랫폼에 최적화된 버전을 만듦.
    """
    return {
        "instagram": generate_instagram_caption(topic),
        "threads": generate_threads_post(topic),
    }