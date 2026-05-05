"""
Meta Graph API 통합 클라이언트.
Instagram Graph API + Threads API를 하나의 인증 체계로 관리.
공식 API만 사용 — 비공식 엔드포인트 일절 사용 금지.

Reference:
  - Instagram Graph API: https://developers.facebook.com/docs/instagram-api
  - Threads API: https://developers.facebook.com/docs/threads
"""

import time
import random
from typing import Optional

import requests


class MetaClient:
    """Meta Graph API 기본 클라이언트. 모든 API 호출의 기반."""

    BASE_URL = "https://graph.facebook.com/v20.0"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def _get(self, endpoint: str, params: dict = None) -> dict:
        """GET 요청. 공식 Graph API만 호출."""
        p = {"access_token": self.access_token, **(params or {})}
        resp = requests.get(f"{self.BASE_URL}/{endpoint}", params=p)
        if not resp.ok:
            raise MetaAPIError(resp.status_code, resp.text)
        return resp.json()

    def _post(self, endpoint: str, data: dict) -> dict:
        """POST 요청."""
        payload = {**data, "access_token": self.access_token}
        resp = requests.post(f"{self.BASE_URL}/{endpoint}", data=payload)
        if not resp.ok:
            raise MetaAPIError(resp.status_code, resp.text)
        return resp.json()

    def _delete(self, endpoint: str) -> dict:
        """DELETE 요청."""
        resp = requests.delete(
            f"{self.BASE_URL}/{endpoint}",
            params={"access_token": self.access_token},
        )
        if not resp.ok:
            raise MetaAPIError(resp.status_code, resp.text)
        return resp.json()

    @staticmethod
    def safe_delay(min_sec: float = 5.0, max_sec: float = 15.0):
        """API 호출 간 사람처럼 불규칙한 지연. 봇 탐지 회피."""
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)


class MetaAPIError(Exception):
    """Meta API 오류."""
    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"Meta API {status_code}: {body}")