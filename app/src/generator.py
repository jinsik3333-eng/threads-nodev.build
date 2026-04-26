import anthropic

MODEL = "claude-sonnet-4-6"
_client = anthropic.Anthropic()

EXPERIENCE_SYSTEM = """당신은 @nodev.build(비개발dev) Threads 계정의 콘텐츠 작성자입니다.
타깃: 코딩 경험 없는 비개발자 직장인.
톤: 솔직하고 공감가는 직장인 말투. 이모지 1~2개 사용.
길이: 200~350자.
구조: [공감 상황] → [나는 비개발자인데] → [이렇게 해결했다] → [당신도 됩니다]"""

FREE_CONTENT_SYSTEM = """당신은 @nodev.build(비개발dev) Threads 계정의 콘텐츠 작성자입니다.
타깃: 코딩 경험 없는 비개발자 직장인.
톤: 친근하고 실용적. 이모지 1~2개.
길이: 150~250자.
구조: [무료 자료 소개] → [이걸 보면 뭘 할 수 있나] → [팔로우+댓글 남기시면 드립니다]"""

def generate_experience_post(idea: str) -> str:
    resp = _client.messages.create(
        model=MODEL,
        max_tokens=500,
        system=EXPERIENCE_SYSTEM,
        messages=[{"role": "user", "content": f"다음 상황을 바탕으로 Threads 포스트를 작성해주세요:\n{idea}"}],
    )
    return resp.content[0].text.strip()

def generate_free_content_post(resource_name: str, resource_url: str) -> str:
    resp = _client.messages.create(
        model=MODEL,
        max_tokens=400,
        system=FREE_CONTENT_SYSTEM,
        messages=[{"role": "user", "content": f"자료명: {resource_name}\n링크: {resource_url}\n\n위 무료 자료를 배포하는 Threads 포스트를 작성해주세요."}],
    )
    return resp.content[0].text.strip()
