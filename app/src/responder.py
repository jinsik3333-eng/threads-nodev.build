"""
Threads 댓글 자동 응답 모듈 (안전 규칙 완전 적용).

안전 규칙 (2회 계정 정지 경험 기반):
  1. 한 세션 최대 5개까지만 응답
  2. 응답 간 30~180초 불규칙 지연
  3. 매번 Claude로 다른 표현 생성 (템플릿 금지)
  4. 링크 포함은 직접 요청 시에만, 5회 중 1회 이하
  5. 로컬 replied.json으로 중복 방지 (API 중복 체크 X)
  6. 하루 2~3회만 실행

포스트 타겟팅: 팔로워 상위 댓글 우선 + 키워드 필터
"""

import json
import random
from pathlib import Path
from typing import Set, Optional

import anthropic

from .threads import ThreadsClient, MAX_REPLIES_PER_SESSION, LINK_INCLUDE_RATE

# ── 설정 ────────────────────────────────────────────────

REPLIED_PATH = Path("state/replied.json")
MODEL = "claude-sonnet-4-6"
LINK_REQUEST_KEYWORDS = [
    "자료", "링크", "공유", "주세요", "보내", "받고", "어디",
    "다운", "파일", "드롭", "구글", "노션",
]
ENGAGEMENT_KEYWORDS = [
    "자료", "어떻게", "저도", "링크", "공유", "주세요", "보내",
    "좋아요", "궁금", "알려", "가르쳐", "도움", "팁", "추천",
    "방법", "만들", "코딩", "코드", "제작",
]

# ── Claude 시스템 프롬프트 (템플릿 없는 완전 자유 생성) ──

REPLY_SYSTEM = """당신은 Threads에서 비개발자 직장인을 위한 계정을 운영하고 있습니다.
댓글에 답변할 때 다음 원칙을 지켜주세요:
- 1~2문장, 친근한 구어체, 이모지 1개
- 매번 완전히 다른 표현으로 (패턴 반복 절대 금지)
- 상대방이 한 말에 공감하면서 짧게 답변
- 링크 절대 포함하지 말 것 (링크는 별도 처리)
- 과도한 친절 자제, 또래 직장인 말투"""


# ── 상태 관리 ───────────────────────────────────────────

def _load_replied() -> Set[str]:
    if not REPLIED_PATH.exists():
        return set()
    try:
        return set(json.loads(REPLIED_PATH.read_text()))
    except (json.JSONDecodeError, OSError):
        return set()


def _save_replied(replied: Set[str]) -> None:
    REPLIED_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPLIED_PATH.write_text(
        json.dumps(sorted(replied), ensure_ascii=False, indent=2)
    )


# ── 댓글 선별 ──────────────────────────────────────────

def _has_keyword(text: str, keywords: list[str]) -> bool:
    return any(kw in text for kw in keywords)


def select_comments(
    comments: list[dict],
    already_replied: Set[str],
    max_count: int = MAX_REPLIES_PER_SESSION,
) -> list[dict]:
    """
    응답할 댓글을 안전하게 선별.
    1. 아직 응답 안 한 댓글만
    2. 시간순 상위 우선
    3. 키워드(참여 의사) 있는 댓글 추가 선별
    4. 무작위성을 더해 패턴 감지 회피
    """
    # 미응답 댓글만
    fresh = [c for c in comments if c["id"] not in already_replied]
    if not fresh:
        return []

    # 시간순 정렬 (오래된 댓글이 먼저)
    fresh.sort(key=lambda c: c.get("timestamp", ""))

    # 상위 10개는 무조건 후보
    top_candidates = fresh[:10]
    # 나머지 중 키워드 있는 댓글 추가
    rest = fresh[10:]
    keyword_candidates = [
        c for c in rest if _has_keyword(c.get("text", ""), ENGAGEMENT_KEYWORDS)
    ]

    # 후보 합치고 섞음 (패턴 감지 회피)
    candidates = top_candidates + keyword_candidates
    random.shuffle(candidates)

    # 최대 개수만큼만 선택
    return candidates[:max_count]


# ── 답글 생성 ──────────────────────────────────────────

_client = anthropic.Anthropic()


def _generate_reply(post_content: str, comment_text: str) -> str:
    """Claude API로 매번 다른 답글 생성 (템플릿 절대 사용 안 함)."""
    resp = _client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=REPLY_SYSTEM,
        messages=[{
            "role": "user",
            "content": (
                f"포스트 내용:\n{post_content[:300]}\n\n"
                f"댓글:\n{comment_text[:200]}\n\n"
                "위 댓글에 대한 짧은 답변을 작성해주세요."
            ),
        }],
    )
    return resp.content[0].text.strip()


def _is_link_request(text: str) -> bool:
    """직접적인 링크/자료 요청인지 확인."""
    return _has_keyword(text, LINK_REQUEST_KEYWORDS)


def _should_include_link(link_request_count: int, total_reply_count: int) -> bool:
    """
    링크 포함 여부 결정.
    - 직접 링크 요청이 있고
    - 현재까지 링크 포함률이 20% 미만인 경우에만
    """
    if link_request_count == 0:
        return False
    current_rate = link_request_count / max(total_reply_count, 1)
    return current_rate < LINK_INCLUDE_RATE


# ── 메인 응답 로직 ─────────────────────────────────────

def respond_to_post(
    threads_client: ThreadsClient,
    post_id: str,
    post_content: str,
    resource_url: Optional[str] = None,
    max_replies: int = MAX_REPLIES_PER_SESSION,
) -> dict:
    """
    게시물 하나에 대해 안전하게 댓글 응답 처리.

    Returns:
        {"replied": N, "link_replied": N, "comment_ids": [...]}
    """
    replied_set = _load_replied()
    comments = threads_client.get_replies(post_id)
    to_reply = select_comments(comments, replied_set, max_replies)

    stats = {"replied": 0, "link_included": 0, "comment_ids": []}

    for i, comment in enumerate(to_reply):
        comment_text = comment.get("text", "")

        # 답글 생성
        if resource_url and _is_link_request(comment_text):
            if _should_include_link(stats["link_included"], stats["replied"] + 1):
                text = f"여기 있어요! 😊 {resource_url}"
                stats["link_included"] += 1
            else:
                # 링크 요청이지만 포함률 초과 → 그냥 일반 답변
                text = _generate_reply(post_content, comment_text)
        else:
            text = _generate_reply(post_content, comment_text)

        # 발행
        reply_id = threads_client.reply_to_comment(comment["id"], text)
        replied_set.add(comment["id"])
        stats["replied"] += 1
        stats["comment_ids"].append(reply_id)

        # 마지막 응답이 아니면 불규칙 지연
        if i < len(to_reply) - 1:
            ThreadsClient.safe_delay()

    _save_replied(replied_set)
    return stats