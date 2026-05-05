"""
Threads API 클라이언트 (graph.threads.net).
공식 Threads API만 사용. 기존 threads_client.py 리팩토링 + 안전 규칙 적용.

안전 규칙:
  1. 링크 포함은 직접 요청이 있을 때만, 5회 중 1회 이하
  2. API 호출 간 불규칙 지연 (30~180초)
  3. 한 세션 최대 응답 개수 제한 (기본 5개)
  4. 로컬 replied.json으로 중복 응답 방지 (API 중복 체크 제거)

Reference:
  - https://developers.facebook.com/docs/threads
  - graph.threads.net/v1.0
"""

import time
import random
from typing import Optional

import requests

BASE_URL = "https://graph.threads.net/v1.0"

# ── 안전 상수 ──────────────────────────────────────────
MIN_DELAY = 30        # API 호출 간 최소 대기 (초)
MAX_DELAY = 180       # API 호출 간 최대 대기 (초)
MAX_REPLIES_PER_SESSION = 5  # 한 번 응답 세션에서 최대 응답 수
LINK_INCLUDE_RATE = 0.2      # 링크 포함할 확률 (5회 중 1회)


class ThreadsClient:
    """Threads 공식 Graph API 클라이언트. 안전 규칙 내장."""

    def __init__(self, user_id: str, access_token: str):
        self.user_id = user_id
        self.token = access_token

    def _post(self, path: str, data: dict) -> dict:
        resp = requests.post(f"{BASE_URL}/{path}", data={
            **data,
            "access_token": self.token,
        })
        if not resp.ok:
            raise ThreadsAPIError(resp.status_code, resp.text)
        return resp.json()

    def _get(self, path: str, params: dict = None) -> dict:
        p = {"access_token": self.token, **(params or {})}
        resp = requests.get(f"{BASE_URL}/{path}", params=p)
        if not resp.ok:
            raise ThreadsAPIError(resp.status_code, resp.text)
        return resp.json()

    # ── 게시물 ──────────────────────────────────────────

    def create_post(self, text: str) -> str:
        """Threads에 텍스트 게시물 발행."""
        container = self._post(f"{self.user_id}/threads", {
            "media_type": "TEXT",
            "text": text,
        })
        result = self._post(f"{self.user_id}/threads_publish", {
            "creation_id": container["id"],
        })
        return result["id"]

    def get_my_threads(self, limit: int = 50) -> list[dict]:
        data = self._get(f"{self.user_id}/threads", {
            "fields": "id,permalink,text,timestamp",
            "limit": limit,
        })
        return data.get("data", [])

    # ── 댓글 / 답글 ─────────────────────────────────────

    def get_replies(self, post_id: str, limit: int = 100) -> list[dict]:
        """게시물 댓글 전체 조회 (페이지네이션)."""
        results = []
        params = {
            "fields": "id,text,username,timestamp",
            "limit": min(limit, 100),
        }
        while True:
            data = self._get(f"{post_id}/replies", params)
            results.extend(data.get("data", []))
            next_cursor = (
                data.get("paging", {}).get("cursors", {}).get("after")
            )
            if not next_cursor or len(results) >= limit:
                break
            params["after"] = next_cursor
        return results[:limit]

    def reply_to_comment(self, comment_id: str, text: str) -> str:
        """
        댓글에 답글 작성.
        컨테이너 생성 후 3초 뒤 발행 (Threads API 요구사항).
        """
        container = self._post(f"{self.user_id}/threads", {
            "media_type": "TEXT",
            "text": text,
            "reply_to_id": comment_id,
        })
        time.sleep(3)
        result = self._post(f"{self.user_id}/threads_publish", {
            "creation_id": container["id"],
        })
        return result["id"]

    # ── 인사이트 ───────────────────────────────────────

    def get_post_insights(self, post_id: str) -> dict:
        """게시물 인사이트 (조회수, 좋아요, 답글 수)."""
        return self._get(f"{post_id}/insights", {
            "metric": "views,likes,replies,quotes,reposts",
        })

    # ── 안전 유틸리티 ───────────────────────────────────

    @staticmethod
    def safe_delay(min_sec: float = MIN_DELAY, max_sec: float = MAX_DELAY):
        """불규칙 지연으로 사람처럼 보이게."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)


class ThreadsAPIError(Exception):
    """Threads API 오류."""
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"Threads API {status_code}: {body}")