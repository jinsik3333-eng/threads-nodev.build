# scripts/publish.py
"""launchd에서 07:30 / 21:00에 호출. 큐의 다음 포스트를 발행한다."""
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.threads_client import ThreadsClient
from src.publisher import publish_next

def main():
    user_id = os.environ.get("THREADS_USER_ID")
    access_token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not user_id or not access_token:
        print("[error] .env 파일에 THREADS_USER_ID, THREADS_ACCESS_TOKEN이 설정되어 있어야 합니다.")
        sys.exit(1)
    client = ThreadsClient(user_id=user_id, access_token=access_token)
    post_id = publish_next(client)
    if post_id:
        print(f"[publish] 발행 완료: {post_id}")
    else:
        print("[publish] 큐가 비어 있습니다.")

if __name__ == "__main__":
    main()
