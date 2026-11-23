from src.responder import ENGAGEMENT_KEYWORDS, select_comments

SAMPLE_COMMENTS = [
    {"id": "c1", "text": "자료 주시면 감사합니다", "username": "user1", "timestamp": "2026-04-18T08:00:00Z"},
    {"id": "c2", "text": "좋은 내용이네요", "username": "user2", "timestamp": "2026-04-18T08:01:00Z"},
    {"id": "c3", "text": "저도 해보고 싶어요", "username": "user3", "timestamp": "2026-04-18T08:02:00Z"},
    {"id": "c4", "text": "어떻게 시작하나요", "username": "user4", "timestamp": "2026-04-18T08:03:00Z"},
    {"id": "c5", "text": "그냥 구경 중", "username": "user5", "timestamp": "2026-04-18T08:04:00Z"},
]

def test_keyword_comments_are_included():
    comments = [
        {"id": str(i), "text": "안녕하세요", "timestamp": f"2026-04-18T07:{i:02d}:00Z"}
        for i in range(10)
    ]
    selected = select_comments(comments + SAMPLE_COMMENTS, already_replied=set(), max_count=15)
    ids = {c["id"] for c in selected}
    assert {"c1", "c3", "c4"} <= ids
    assert "c5" not in ids

def test_max_count_limits_results():
    many = [{"id": str(i), "text": f"댓글 {i}", "username": f"u{i}", "timestamp": f"2026-04-18T08:{i:02d}:00Z"} for i in range(15)]
    selected = select_comments(many, already_replied=set(), max_count=3)
    assert len(selected) == 3

def test_already_replied_are_excluded():
    selected = select_comments(SAMPLE_COMMENTS, already_replied={"c1", "c3"})
    ids = [c["id"] for c in selected]
    assert "c1" not in ids
    assert "c3" not in ids

def test_keyword_triggers_cover_expected_words():
    for word in ["자료", "어떻게", "저도", "링크", "공유", "주세요", "보내"]:
        assert word in ENGAGEMENT_KEYWORDS
