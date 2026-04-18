import pytest
from unittest.mock import patch, MagicMock
from src.generator import generate_experience_post, generate_free_content_post

def make_mock_response(text: str):
    mock = MagicMock()
    mock.content = [MagicMock(text=text)]
    return mock

def test_generate_experience_post_returns_string(mocker):
    mocker.patch("src.generator.anthropic.Anthropic").return_value.messages.create.return_value = \
        make_mock_response("개발팀한테 요청했더니 백로그에 넣었습니다.\n코딩 몰라도 하루만에 만들었습니다.")
    result = generate_experience_post("엑셀 자동화 도구가 필요했던 상황")
    assert isinstance(result, str)
    assert len(result) > 10

def test_generate_experience_post_includes_idea_in_prompt(mocker):
    mock_create = mocker.patch("src.generator.anthropic.Anthropic").return_value.messages.create
    mock_create.return_value = make_mock_response("포스트 내용")
    generate_experience_post("보고서 자동화")
    call_args = mock_create.call_args
    prompt_text = call_args[1]["messages"][0]["content"]
    assert "보고서 자동화" in prompt_text

def test_generate_free_content_post_returns_string(mocker):
    mocker.patch("src.generator.anthropic.Anthropic").return_value.messages.create.return_value = \
        make_mock_response("무료 가이드 드립니다. 팔로우+댓글 남겨주세요.")
    result = generate_free_content_post("Claude Code 설치 가이드", "https://example.com/guide.html")
    assert isinstance(result, str)
    assert len(result) > 10
