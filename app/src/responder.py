import json
from pathlib import Path
from typing import Set
import anthropic

KEYWORD_TRIGGERS = ["자료", "어떻게", "저도", "링크", "공유", "주세요", "보내"]
LINK_KEYWORDS = ["자료", "링크", "공유", "주세요", "보내", "어디", "받고"]
LINK_REPLY_TEMPLATE = "여기 있어요! 😊 {url}"
REPLIED_PATH = Path("state/replied.json")
MODEL = "claude-sonnet-4-6"

REPLY_SYSTEM = """당신은 @nodev.build(비개발dev) Threads 계정 운영자입니다.
비개발자 직장인 팔로워의 댓글에 따뜻하고 실용적으로 답합니다.
1~2문장, 이모지 1개, 구어체."""

_client = anthropic.Anthropic()

def load_replied() -> Set[str]:
    if not REPLIED_PATH.exists():
        return set()
    return set(json.loads(REPLIED_PATH.read_text()))

def save_replied(replied: Set[str]) -> None:
    REPLIED_PATH.parent.mkdir(exist_ok=True)
    REPLIED_PATH.write_text(json.dumps(list(replied), ensure_ascii=False, indent=2))

def _has_keyword(text: str) -> bool:
    return any(kw in text for kw in KEYWORD_TRIGGERS)

def select_comments_to_reply(comments: list, already_replied: Set[str]) -> list:
    sorted_comments = sorted(comments, key=lambda c: c["timestamp"])
    top10 = sorted_comments[:10]
    keyword_rest = [c for c in sorted_comments[10:] if _has_keyword(c["text"])]
    candidates = top10 + keyword_rest
    return [c for c in candidates if c["id"] not in already_replied]

def generate_reply(post_content: str, comment_text: str) -> str:
    resp = _client.messages.create(
        model=MODEL,
        max_tokens=200,
        system=REPLY_SYSTEM,
        messages=[{"role": "user", "content": f"포스트 내용:\n{post_content}\n\n댓글:\n{comment_text}\n\n답변을 작성해주세요."}],
    )
    return resp.content[0].text.strip()

def _is_link_request(text: str) -> bool:
    return any(kw in text for kw in LINK_KEYWORDS)


def respond_to_post(threads_client, post_id: str, post_content: str, resource_url: str = None) -> list:
    replied = load_replied()
    comments = threads_client.get_replies(post_id)
    to_reply = select_comments_to_reply(comments, replied)
    reply_ids = []
    for comment in to_reply:
        if resource_url and _is_link_request(comment["text"]):
            text = LINK_REPLY_TEMPLATE.format(url=resource_url)
        else:
            text = generate_reply(post_content, comment["text"])
        reply_id = threads_client.reply_to_comment(comment["id"], text)
        replied.add(comment["id"])
        reply_ids.append(reply_id)
    save_replied(replied)
    return reply_ids
