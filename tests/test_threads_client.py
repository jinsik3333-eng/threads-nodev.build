import pytest
from unittest.mock import patch, MagicMock
from src.threads_client import ThreadsClient

BASE = "https://graph.threads.net/v1.0"

@pytest.fixture
def client():
    return ThreadsClient(user_id="123", access_token="tok")

def test_create_post_calls_correct_endpoints(client):
    with patch("src.threads_client.requests.post") as mock_post:
        mock_post.side_effect = [
            MagicMock(ok=True, json=lambda: {"id": "container_1"}),
            MagicMock(ok=True, json=lambda: {"id": "post_1"}),
        ]
        post_id = client.create_post("안녕하세요")
        assert post_id == "post_1"
        assert mock_post.call_count == 2
        first_call = mock_post.call_args_list[0]
        assert first_call[0][0] == f"{BASE}/123/threads"
        assert first_call[1]["data"]["text"] == "안녕하세요"

def test_get_replies_returns_list(client):
    with patch("src.threads_client.requests.get") as mock_get:
        mock_get.return_value = MagicMock(ok=True, json=lambda: {
            "data": [{"id": "r1", "text": "감사합니다", "username": "user1", "timestamp": "2026-04-18T07:30:00Z"}]
        })
        replies = client.get_replies("post_1")
        assert len(replies) == 1
        assert replies[0]["id"] == "r1"

def test_reply_to_comment_publishes(client):
    with patch("src.threads_client.requests.post") as mock_post:
        mock_post.side_effect = [
            MagicMock(ok=True, json=lambda: {"id": "container_r"}),
            MagicMock(ok=True, json=lambda: {"id": "reply_1"}),
        ]
        reply_id = client.reply_to_comment("comment_1", "도움이 되셨나요?")
        assert reply_id == "reply_1"
        first_call = mock_post.call_args_list[0]
        assert first_call[1]["data"]["reply_to_id"] == "comment_1"

def test_create_post_raises_on_api_error(client):
    with patch("src.threads_client.requests.post") as mock_post:
        mock_post.return_value = MagicMock(ok=False, status_code=400, text="Bad Request")
        with pytest.raises(RuntimeError, match="Threads API 오류"):
            client.create_post("테스트")
