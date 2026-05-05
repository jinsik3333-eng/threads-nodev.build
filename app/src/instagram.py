"""
Instagram Graph API 클라이언트.
공식 graph.instagram.com API만 사용.

제한사항 (공식):
  - Creator/Business Account 필요 (개인 계정 전환)
  - 이미지/릴스 게시: 24시간 내 25건 제한
  - 스토리: 별도 rate limit
  - 댓글 관리, 인사이트 조회 가능
  - DM 자동화는 공식 API에서 지원 안 함 (별도 Messenger API 필요)

Reference:
  - https://developers.facebook.com/docs/instagram-api
  - https://developers.facebook.com/docs/instagram-api/reference
"""

import time
import random
from typing import Optional

import requests

# Instagram Graph API 기본 URL
BASE_URL = "https://graph.instagram.com/v20.0"


class InstagramClient:
    """Instagram 공식 Graph API 클라이언트."""

    def __init__(self, access_token: str, business_account_id: str):
        self.token = access_token
        self.ig_account_id = business_account_id

    def _get(self, path: str, params: dict = None) -> dict:
        p = {"access_token": self.token, **(params or {})}
        resp = requests.get(f"{BASE_URL}/{path}", params=p)
        if not resp.ok:
            raise Exception(f"Instagram API 오류 {resp.status_code}: {resp.text}")
        return resp.json()

    def _post(self, path: str, data: dict) -> dict:
        payload = {**data, "access_token": self.token}
        resp = requests.post(f"{BASE_URL}/{path}", data=payload)
        if not resp.ok:
            raise Exception(f"Instagram API 오류 {resp.status_code}: {resp.text}")
        return resp.json()

    # ── 미디어 게시 ──────────────────────────────────────

    def create_image_container(
        self, image_url: str, caption: str = ""
    ) -> str:
        """
        이미지 미디어 컨테이너 생성.
        이미지 URL은 공개 접근 가능해야 함 (S3, CDN 등).
        """
        result = self._post(f"{self.ig_account_id}/media", {
            "image_url": image_url,
            "caption": caption,
            "media_type": "IMAGE",
        })
        return result["id"]

    def create_carousel_container(
        self, children: list[str], caption: str = ""
    ) -> str:
        """
        캐러셀(여러 이미지) 컨테이너 생성.
        children: image_container_id 배열.
        """
        result = self._post(f"{self.ig_account_id}/media", {
            "media_type": "CAROUSEL",
            "children": ",".join(children),
            "caption": caption,
        })
        return result["id"]

    def publish_media(self, creation_id: str) -> str:
        """미디어 컨테이너 발행. 실제 Instagram에 게시."""
        result = self._post(f"{self.ig_account_id}/media_publish", {
            "creation_id": creation_id,
        })
        return result["id"]

    def get_media_status(self, creation_id: str) -> dict:
        """미디어 컨테이너 상태 확인."""
        return self._get(f"{creation_id}", {
            "fields": "status_code,status",
        })

    # ── 댓글 관리 ──────────────────────────────────────

    def get_media_comments(self, media_id: str, limit: int = 50) -> list[dict]:
        """미디어 댓글 조회."""
        data = self._get(f"{media_id}/comments", {
            "fields": "id,text,username,timestamp",
            "limit": limit,
        })
        return data.get("data", [])

    def reply_to_comment(self, comment_id: str, message: str) -> str:
        """댓글에 답글 작성."""
        result = self._post(f"{comment_id}/replies", {
            "message": message,
        })
        return result["id"]

    def hide_comment(self, comment_id: str) -> bool:
        """댓글 숨김."""
        result = self._post(f"{comment_id}", {"hide": "true"})
        return result.get("success", False)

    # ── 인사이트 ───────────────────────────────────────

    def get_user_insights(self, period: str = "day", since: str = None, until: str = None) -> dict:
        """계정 인사이트 (팔로워 수, 도달 등)."""
        params = {"metric": "follower_count,impressions,reach,profile_views", "period": period}
        if since:
            params["since"] = since
        if until:
            params["until"] = until
        return self._get(f"{self.ig_account_id}/insights", params)

    # ── 검색 ───────────────────────────────────────────

    def search_hashtag(self, hashtag_id: str) -> dict:
        """해시태그 정보 조회."""
        return self._get(f"{hashtag_id}", {
            "fields": "id,name",
        })

    @staticmethod
    def safe_delay():
        """사람 같은 랜덤 지연 (5~20초)."""
        time.sleep(random.uniform(5, 20))