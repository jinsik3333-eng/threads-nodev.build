import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

QUEUE_PATH = Path("posts/queue.json")


def load_queue() -> list:
    if not QUEUE_PATH.exists():
        return []
    return json.loads(QUEUE_PATH.read_text())


def save_queue(queue: list) -> None:
    QUEUE_PATH.write_text(json.dumps(queue, ensure_ascii=False, indent=2))


def enqueue(content: str, post_type: str) -> dict:
    queue = load_queue()
    item = {
        "id": str(uuid.uuid4()),
        "type": post_type,
        "content": content,
        "queued_at": datetime.now().isoformat(),
        "published_at": None,
    }
    queue.append(item)
    save_queue(queue)
    return item


def pop_next() -> Optional[dict]:
    queue = load_queue()
    pending = [item for item in queue if item["published_at"] is None]
    if not pending:
        return None
    return pending[0]


def mark_published(item_id: str, post_id: str) -> None:
    queue = load_queue()
    for item in queue:
        if item["id"] == item_id:
            item["published_at"] = datetime.now().isoformat()
            item["post_id"] = post_id
            break
    save_queue(queue)


def publish_next(client) -> Optional[str]:
    item = pop_next()
    if not item:
        return None
    post_id = client.create_post(item["content"])
    mark_published(item["id"], post_id)
    return post_id
