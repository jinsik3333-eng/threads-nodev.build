import pytest
from src.publisher import enqueue, get_pending, load_queue, mark_published, pop_next


@pytest.fixture(autouse=True)
def clean_queue(tmp_path, monkeypatch):
    monkeypatch.setattr("src.publisher.QUEUE_PATH", tmp_path / "queue.json")
    (tmp_path / "queue.json").write_text("[]")


def test_enqueue_adds_item():
    enqueue("테스트 포스트")
    queue = load_queue()
    assert len(queue) == 1
    assert queue[0]["content"] == "테스트 포스트"
    assert queue[0]["published"]["threads"]["at"] is None


def test_pop_next_returns_pending():
    enqueue("첫 번째")
    enqueue("두 번째")
    item = pop_next()
    assert item is not None
    assert item["content"] == "첫 번째"


def test_mark_published_sets_timestamp():
    item = enqueue("포스트")
    mark_published(item["id"], "threads", "post_abc")
    queue = load_queue()
    assert queue[0]["published"]["threads"]["at"] is not None
    assert queue[0]["published"]["threads"]["post_id"] == "post_abc"


def test_get_pending_tracks_publication_by_platform():
    item = enqueue("발행할 포스트", ["instagram", "threads"])
    mark_published(item["id"], "threads", "post_123")
    assert not get_pending("threads")
    assert [entry["id"] for entry in get_pending("instagram")] == [item["id"]]


def test_pop_next_returns_none_when_empty():
    assert pop_next() is None


def test_mark_published_raises_for_unknown_id():
    with pytest.raises(ValueError, match="큐에서 ID를 찾을 수 없음"):
        mark_published("nonexistent-id", "threads", "post_x")
