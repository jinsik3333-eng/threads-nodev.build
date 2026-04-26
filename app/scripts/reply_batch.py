"""
세 개의 포스트에 미답변 댓글 일괄 답변.
--dry-run 플래그로 실제 발행 없이 미리보기.
"""
import os
import sys
import random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.threads_client import ThreadsClient
from src.responder import load_replied, save_replied

POST_SHORTCODES = [
    "DXTVrkCEWED",  # 첫 글
    "DXUICZvkTme",  # 두번째 글
    "DXVQJ09Eugm",  # 세번째 글
]

LINK = "https://jinsik3333-eng.github.io/threads-nodev.build/guides/"

TEMPLATES = [
    "{username} 고마워요! 😊 내일까지 최종 업데이트 있으니 참고해줘요! {link}",
    "{username} 감사해요! 🙏 링크 여기 있어요 → {link} (내일 최종본 올라올 예정이에요)",
    "{username} 고마워! 내일까지 최종 업데이트가 있다는 점 참고하고! {link}",
    "{username} 반가워요! 🙌 여기서 확인해보세요 → {link} 내일 업데이트 예정이에요",
]


def find_post_ids(client: ThreadsClient) -> dict[str, str]:
    """shortcode → numeric post ID 매핑"""
    threads = client.get_my_threads(limit=50)
    mapping = {}
    for post in threads:
        permalink = post.get("permalink", "")
        for code in POST_SHORTCODES:
            if code in permalink:
                mapping[code] = post["id"]
    return mapping


def main():
    dry_run = "--dry-run" in sys.argv

    user_id = os.environ.get("THREADS_USER_ID")
    access_token = os.environ.get("THREADS_ACCESS_TOKEN")
    if not user_id or not access_token:
        print("[error] .env에 THREADS_USER_ID, THREADS_ACCESS_TOKEN 필요")
        sys.exit(1)

    client = ThreadsClient(user_id=user_id, access_token=access_token)
    replied = load_replied()

    print("[1/3] 포스트 ID 조회 중...")
    post_ids = find_post_ids(client)
    for code in POST_SHORTCODES:
        if code not in post_ids:
            print(f"  [경고] {code} 포스트를 찾지 못했습니다.")
    print(f"  찾은 포스트: {len(post_ids)}개\n")

    total_replied = 0

    for code, post_id in post_ids.items():
        print(f"[포스트 {code}] 댓글 조회 중...")
        comments = client.get_replies(post_id)
        unreplied = []
        for c in comments:
            if c["id"] in replied or c.get("username") == "nodev.build":
                continue
            if client.has_owner_replied(c["id"]):
                replied.add(c["id"])
                continue
            unreplied.append(c)
        print(f"  전체 댓글 {len(comments)}개 / 미답변 {len(unreplied)}개")

        for c in unreplied:
            import time
            username = "@" + c.get("username", "")
            text = random.choice(TEMPLATES).format(username=username, link=LINK)
            print(f"  → {username}: {text[:60]}...")

            if not dry_run:
                try:
                    client.reply_to_comment(c["id"], text)
                    replied.add(c["id"])
                    save_replied(replied)
                    total_replied += 1
                    time.sleep(10)
                except Exception as e:
                    print(f"  [오류] {username} 답변 실패: {e}")
                    print("  잠시 후 재시도하세요. 이미 완료된 댓글은 저장됐습니다.")
                    break

    if dry_run:
        print("\n[dry-run] 실제 발행 없음. 발행하려면 --dry-run 없이 실행하세요.")
    else:
        save_replied(replied)
        print(f"\n완료: 총 {total_replied}개 댓글에 답변 달았습니다.")


if __name__ == "__main__":
    main()
