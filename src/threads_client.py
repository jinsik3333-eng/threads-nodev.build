import requests

BASE = "https://graph.threads.net/v1.0"

class ThreadsClient:
    def __init__(self, user_id: str, access_token: str):
        self.user_id = user_id
        self.token = access_token

    def _post(self, path: str, data: dict) -> dict:
        resp = requests.post(f"{BASE}/{path}", data={**data, "access_token": self.token})
        if not resp.ok:
            raise RuntimeError(f"Threads API 오류: {resp.status_code} {resp.text}")
        return resp.json()

    def _get(self, path: str, params: dict = None) -> dict:
        p = {"access_token": self.token, **(params or {})}
        resp = requests.get(f"{BASE}/{path}", params=p)
        if not resp.ok:
            raise RuntimeError(f"Threads API 오류: {resp.status_code} {resp.text}")
        return resp.json()

    def create_post(self, text: str) -> str:
        container = self._post(f"{self.user_id}/threads", {
            "media_type": "TEXT",
            "text": text,
        })
        result = self._post(f"{self.user_id}/threads_publish", {
            "creation_id": container["id"],
        })
        return result["id"]

    def get_replies(self, post_id: str) -> list[dict]:
        data = self._get(f"{post_id}/replies", {
            "fields": "id,text,username,timestamp"
        })
        return data.get("data", [])

    def reply_to_comment(self, comment_id: str, text: str) -> str:
        container = self._post(f"{self.user_id}/threads", {
            "media_type": "TEXT",
            "text": text,
            "reply_to_id": comment_id,
        })
        result = self._post(f"{self.user_id}/threads_publish", {
            "creation_id": container["id"],
        })
        return result["id"]
