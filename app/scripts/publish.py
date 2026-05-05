#!/usr/bin/env python3
"""멀티 플랫폼 발행 CLI. Instagram + Threads 동시 발행 지원.

사용법:
  python scripts/publish.py                    # 큐의 다음 항목 발행
  python scripts/publish.py --platform threads  # Threads만 발행
  python scripts/publish.py --platform instagram # Instagram만 발행
"""

import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.threads import ThreadsClient
from src.instagram import InstagramClient
from src.publisher import pop_next, mark_published
from src.generator import generate_cross_platform, generate_threads_post


def _get_threads_client():
    user_id = os.environ.get("THREADS_USER_ID")
    token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not user_id or not token:
        print("[error] .env에 THREADS_USER_ID, THREADS_ACCESS_TOKEN이 필요합니다.")
        return None
    return ThreadsClient(user_id=user_id, access_token=token)


def _get_instagram_client():
    token = os.environ.get("INSTAGRAM_ACCESS_TOKEN")
    acct_id = os.environ.get("INSTAGRAM_BUSINESS_ACCOUNT_ID")
    if not token or not acct_id:
        print("[error] .env에 INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_BUSINESS_ACCOUNT_ID가 필요합니다.")
        return None
    return InstagramClient(access_token=token, business_account_id=acct_id)


def publish_threads(item: dict) -> str | None:
    client = _get_threads_client()
    if not client:
        return None

    # Instagram 캡션이 따로 있으면 그것을, 없으면 content 그대로
    text = item.get("threads_content") or item.get("content", "")
    post_id = client.create_post(text)
    mark_published(item["id"], "threads", post_id)
    print(f"[threads] 발행 완료: {post_id}")
    return post_id


def publish_instagram(item: dict) -> str | None:
    """Instagram 발행 — 현재는 캡션만 준비하고 이미지 URL은 추후 추가."""
    client = _get_instagram_client()
    if not client:
        return None

    caption = item.get("instagram_caption") or item.get("content", "")
    # NOTE: 이미지 URL이 아직 없으면 실제 발행 불가
    # 추후 image_url이 item에 포함되면 create_image_container + publish_media 호출
    img_url = item.get("image_url")
    if img_url:
        container_id = client.create_image_container(img_url, caption)
        post_id = client.publish_media(container_id)
        mark_published(item["id"], "instagram", post_id)
        print(f"[instagram] 발행 완료: {post_id}")
        return post_id
    else:
        print("[instagram] 이미지 URL이 없어 발행 건너뜀")
        return None


def main():
    parser = argparse.ArgumentParser(description="멀티 플랫폼 발행")
    parser.add_argument("--platform", choices=["threads", "instagram", "all"],
                        default="all", help="발행할 플랫폼 (기본: all)")
    parser.add_argument("--topic", "-t", help="새 콘텐츠 생성해서 발행 (큐 무시)")
    args = parser.parse_args()

    # --topic이 있으면 즉시 생성 + 발행
    if args.topic:
        contents = generate_cross_platform(args.topic)
        print("[generate] 크로스 플랫폼 콘텐츠 생성 완료")
        print(f"\n--- Instagram ---\n{contents['instagram']}")
        print(f"\n--- Threads ---\n{contents['threads']}")
        # 큐에 넣지 않고 즉시 발행하려면 enqueue 생략 가능
        return

    item = pop_next()
    if not item:
        print("[publish] 큐가 비어 있습니다.")
        return

    print(f"[publish] 발행 시작: {item['id']}")

    published = []
    if args.platform in ("all", "threads") and "threads" in item.get("platforms", []):
        pid = publish_threads(item)
        if pid:
            published.append(("threads", pid))

    if args.platform in ("all", "instagram") and "instagram" in item.get("platforms", []):
        pid = publish_instagram(item)
        if pid:
            published.append(("instagram", pid))

    if published:
        print(f"[publish] 총 {len(published)}개 플랫폼 발행 완료")
    else:
        print("[publish] 발행된 플랫폼 없음")


if __name__ == "__main__":
    main()