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
    client = ThreadsClient(
        user_id=os.environ["THREADS_USER_ID"],
        access_token=os.environ["THREADS_ACCESS_TOKEN"],
    )
    post_id = publish_next(client)
    if post_id:
        print(f"[publish] 발행 완료: {post_id}")
    else:
        print("[publish] 큐가 비어 있습니다.")

if __name__ == "__main__":
    main()
