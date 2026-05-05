"""
멀티 플랫폼 발행 큐 관리.
Instagram + Threads 동시 발행 지원.

큐 항목 구조:
  {
    "id": "uuid",
    "platforms": ["instagram", "threads"],  // 게시할 플랫폼
    "content": "텍스트 내용",
    "instagram_caption": "인스타용 캡션 (선택)",
    "resource_url": "자료 링크 (선택)",
    "queued_at": "ISO timestamp",
    "published": {
      "instagram": {"at": null, "post_id": null},
      "threads": {"at": null, "post_id": null}
    }
  }
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

QUEUE_PATH = Path("state/queue.json")


def load_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    try:
        return json.loads(QUEUE_PATH.read_text())
    except (json.JSONDecodeError, OSError):
        return []


def save_queue(queue: list) -> None:
    QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    QUEUE_PATH.write_text(json.dumps(queue, ensure_ascii=False, indent=2))


def enqueue(
    content: str,
    platforms: list[str] = None,
    instagram_caption: str = None,
    resource_url: str = None,
) -> dict:
    """큐에 새 발행 항목 추가."""
    platforms = platforms or ["threads"]
    item = {
        "id": str(uuid.uuid4()),
        "platforms": platforms,
        "content": content,
        "instagram_caption": instagram_caption,
        "resource_url": resource_url,
        "queued_at": datetime.now().isoformat(),
        "published": {},
    }
    # 초기화
    for p in platforms:
        item["published"][p] = {"at": None, "post_id": None}

    queue = load_queue()
    queue.append(item)
    save_queue(queue)
    return item


def pop_next() -> Optional[dict]:
    """아직 발행 안 된 첫 항목 반환."""
    queue = load_queue()
    for item in queue:
        # 모든 플랫폼에 발행 안 됐으면
        if all(
            item["published"].get(p, {}).get("at") is None
            for p in item["platforms"]
        ):
            return item
    return None


def mark_published(item_id: str, platform: str, post_id: str) -> None:
    """특정 플랫폼에 발행 완료 표시."""
    queue = load_queue()
    for item in queue:
        if item["id"] == item_id:
            if platform not in item["published"]:
                item["published"][platform] = {}
            item["published"][platform] = {
                "at": datetime.now().isoformat(),
                "post_id": post_id,
            }
            save_queue(queue)
            return
    raise ValueError(f"큐에서 ID를 찾을 수 없음: {item_id}")


def get_pending(platform: str) -> list[dict]:
    """특정 플랫폼에 발행 대기 중인 항목 목록."""
    queue = load_queue()
    return [
        item for item in queue
        if platform in item["platforms"]
        and item["published"].get(platform, {}).get("at") is None
    ]


def get_recent_published(platform: str, count: int = 5) -> list[dict]:
    """최근 발행된 항목 조회."""
    queue = load_queue()
    published = [
        item for item in queue
        if item["published"].get(platform, {}).get("at") is not None
    ]
    published.sort(
        key=lambda i: i["published"][platform]["at"],
        reverse=True,
    )
    return published[:count]