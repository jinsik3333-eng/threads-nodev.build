import json

import httpx2
import pytest
from anthropic import Anthropic, DefaultHttpxClient
from src import claude_client, generator, responder


@pytest.fixture
def response_blocks():
    return [
        {"type": "thinking", "thinking": "응답 준비", "signature": "test-signature"},
        {"type": "text", "text": "  모의 응답  "},
    ]


@pytest.fixture
def claude_requests(mocker, response_blocks):
    requests = []

    def handle(request: httpx2.Request) -> httpx2.Response:
        requests.append(request)
        return httpx2.Response(
            200,
            json={
                "id": "msg_test",
                "model": "claude-sonnet-4-6",
                "role": "assistant",
                "type": "message",
                "content": response_blocks,
                "stop_reason": "end_turn",
                "stop_sequence": None,
                "usage": {"input_tokens": 7, "output_tokens": 3},
            },
        )

    transport = httpx2.MockTransport(handle)
    with Anthropic(
        api_key="test-key",
        base_url="https://api.anthropic.com",
        http_client=DefaultHttpxClient(transport=transport),
    ) as client:
        mocker.patch.object(claude_client, "_client", return_value=client)
        yield requests


@pytest.mark.parametrize(
    ("generate", "args", "system", "max_tokens", "prompt_parts"),
    [
        (
            generator.generate_instagram_caption,
            ("업무 자동화", "도구 화면"),
            generator.INSTAGRAM_SYSTEM,
            500,
            ("업무 자동화", "도구 화면"),
        ),
        (
            generator.generate_threads_post,
            ("보고서 자동화",),
            generator.THREADS_SYSTEM,
            500,
            ("보고서 자동화",),
        ),
        (
            generator.generate_free_content_post,
            ("설치 가이드", "https://example.com/guide.html"),
            generator.FREE_CONTENT_SYSTEM,
            400,
            ("설치 가이드", "https://example.com/guide.html"),
        ),
        (
            responder._generate_reply,
            ("업무 자동화 소개", "어떻게 시작하나요?"),
            responder.REPLY_SYSTEM,
            200,
            ("업무 자동화 소개", "어떻게 시작하나요?"),
        ),
    ],
)
def test_messages_api(generate, args, system, max_tokens, prompt_parts, claude_requests):
    assert generate(*args) == "모의 응답"

    (request,) = claude_requests
    assert request.method == "POST"
    assert str(request.url) == "https://api.anthropic.com/v1/messages"
    assert request.headers["anthropic-version"] == "2026-10-21"
    assert request.headers["authorization"] == "Bearer test-key"
    assert "x-api-key" not in request.headers

    body = json.loads(request.content)
    (message,) = body["messages"]
    assert message["role"] == "user"
    assert all(part in message["content"] for part in prompt_parts)
    assert body == {
        "model": "claude-sonnet-4-6",
        "system": system,
        "max_tokens": max_tokens,
        "messages": [message],
    }


def test_generate_cross_platform_uses_both_system_prompts(claude_requests):
    assert generator.generate_cross_platform("업무 자동화") == {
        "instagram": "모의 응답",
        "threads": "모의 응답",
    }
    assert [json.loads(request.content)["system"] for request in claude_requests] == [
        generator.INSTAGRAM_SYSTEM,
        generator.THREADS_SYSTEM,
    ]


def test_messages_api_requires_a_text_block(claude_requests, response_blocks):
    response_blocks.pop()

    with pytest.raises(ValueError, match="텍스트 블록이 없습니다"):
        generator.generate_threads_post("보고서 자동화")
    assert len(claude_requests) == 1
