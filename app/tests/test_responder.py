import pytest
from src.responder import select_comments_to_reply, KEYWORD_TRIGGERS

SAMPLE_COMMENTS = [
    {"id": "c1", "text": "자료 주시면 감사합니다", "username": "user1", "timestamp": "2026-04-18T08:00:00Z"},
    {"id": "c2", "text": "좋은 내용이네요", "username": "user2", "timestamp": "2026-04-18T08:01:00Z"},
    {"id": "c3", "text": "저도 해보고 싶어요", "username": "user3", "timestamp": "2026-04-18T08:02:00Z"},
    {"id": "c4", "text": "어떻게 시작하나요", "username": "user4", "timestamp": "2026-04-18T08:03:00Z"},
    {"id": "c5", "text": "그냥 구경 중", "username": "user5", "timestamp": "2026-04-18T08:04:00Z"},
]

def test_keyword_comments_are_included():
    selected = select_comments_to_reply(SAMPLE_COMMENTS, already_replied=set())
    ids = [c["id"] for c in selected]
    assert "c1" in ids  # "자료"
    assert "c3" in ids  # "저도"
    assert "c4" in ids  # "어떻게"

def test_top_10_limit():
    many = [{"id": str(i), "text": f"댓글 {i}", "username": f"u{i}", "timestamp": f"2026-04-18T08:{i:02d}:00Z"} for i in range(15)]
    selected = select_comments_to_reply(many, already_replied=set())
    assert len(selected) <= 10

def test_already_replied_are_excluded():
    selected = select_comments_to_reply(SAMPLE_COMMENTS, already_replied={"c1", "c3"})
    ids = [c["id"] for c in selected]
    assert "c1" not in ids
    assert "c3" not in ids

def test_keyword_triggers_cover_expected_words():
    for word in ["자료", "어떻게", "저도", "링크", "공유", "주세요", "보내"]:
        assert word in KEYWORD_TRIGGERS
