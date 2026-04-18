# scripts/respond.py
"""launchd에서 30분마다 호출. 최근 발행 포스트의 댓글에 자동 응답한다."""
import os
import sys
import json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.threads_client import ThreadsClient
from src.responder import respond_to_post

QUEUE_PATH = Path(__file__).parent.parent / "posts/queue.json"

def main():
    user_id = os.environ.get("THREADS_USER_ID")
    access_token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not user_id or not access_token:
        print("[error] .env 파일에 THREADS_USER_ID, THREADS_ACCESS_TOKEN이 설정되어 있어야 합니다.")
        sys.exit(1)
    client = ThreadsClient(user_id=user_id, access_token=access_token)
    queue = json.loads(QUEUE_PATH.read_text()) if QUEUE_PATH.exists() else []
    published = [p for p in queue if p.get("published_at") and p.get("post_id")]
    if not published:
        print("[respond] 발행된 포스트가 없습니다.")
        return
    recent = sorted(published, key=lambda p: p["published_at"])[-2:]
    for item in recent:
        print(f"[respond] {item['post_id']} 댓글 처리 중...")
        reply_ids = respond_to_post(client, item["post_id"], item["content"])
        print(f"[respond] {len(reply_ids)}개 댓글 응답 완료")

if __name__ == "__main__":
    main()
