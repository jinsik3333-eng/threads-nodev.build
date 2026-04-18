import json
import pytest
from unittest.mock import MagicMock
from src.publisher import enqueue, pop_next, mark_published, publish_next, QUEUE_PATH


@pytest.fixture(autouse=True)
def clean_queue(tmp_path, monkeypatch):
    monkeypatch.setattr("src.publisher.QUEUE_PATH", tmp_path / "queue.json")
    (tmp_path / "queue.json").write_text("[]")


def test_enqueue_adds_item():
    from src.publisher import load_queue
    enqueue("테스트 포스트", "experience")
    queue = load_queue()
    assert len(queue) == 1
    assert queue[0]["content"] == "테스트 포스트"
    assert queue[0]["published_at"] is None


def test_pop_next_returns_pending():
    enqueue("첫 번째", "experience")
    enqueue("두 번째", "experience")
    item = pop_next()
    assert item["content"] == "첫 번째"


def test_mark_published_sets_timestamp():
    item = enqueue("포스트", "experience")
    mark_published(item["id"], "post_abc")
    from src.publisher import load_queue
    queue = load_queue()
    assert queue[0]["published_at"] is not None
    assert queue[0]["post_id"] == "post_abc"


def test_publish_next_calls_client_and_marks_published():
    enqueue("발행할 포스트", "experience")
    mock_client = MagicMock()
    mock_client.create_post.return_value = "post_123"
    post_id = publish_next(mock_client)
    assert post_id == "post_123"
    from src.publisher import load_queue
    queue = load_queue()
    assert queue[0]["published_at"] is not None


def test_publish_next_returns_none_when_empty():
    mock_client = MagicMock()
    result = publish_next(mock_client)
    assert result is None


def test_mark_published_raises_for_unknown_id():
    with pytest.raises(ValueError, match="Queue에서 item_id를 찾을 수 없음"):
        mark_published("nonexistent-id", "post_x")
