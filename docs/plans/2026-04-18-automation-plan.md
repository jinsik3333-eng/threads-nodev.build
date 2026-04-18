# 비개발dev 자동화 운영 시스템 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 비개발dev Threads 계정의 경험 포스트 생성·발행·댓글 자동 응답 파이프라인을 Python + launchd로 구축한다.

**Architecture:** Threads 공식 API를 래핑한 클라이언트 위에, Claude API로 포스트/댓글을 생성하는 generator와 댓글 필터링 로직을 가진 responder를 얹는다. launchd plist 3개(오전 발행, 저녁 발행, 댓글 체크)가 스크립트를 트리거하며, 발행 대기열은 `posts/queue.json`, 이미 답한 댓글은 `state/replied.json`으로 상태를 관리한다.

**Tech Stack:** Python 3.11+, `requests`, `anthropic`, `python-dotenv`, `pytest`, macOS launchd

**Phase 범위:** 이 플랜은 Phase 1(경험 포스트 + 무료 자료 배포 + 댓글 응답)만 다룬다. 트렌드 수집(collector.py)은 Phase 2 별도 플랜에서 작성한다.

---

## 파일 구조

```
threads/
├── src/
│   ├── threads_client.py    # Threads API 래퍼 (인증 확인, 포스트, 댓글 조회·작성)
│   ├── generator.py         # Claude API로 경험 포스트 / 무료 자료 포스트 생성
│   ├── publisher.py         # queue.json에서 다음 포스트를 꺼내 발행
│   └── responder.py         # 댓글 조회 → 필터링 → Claude로 답변 생성 → 발행
├── scripts/
│   ├── publish.py           # launchd 트리거용 CLI (publisher.py 호출)
│   └── respond.py           # launchd 트리거용 CLI (responder.py 호출)
├── launchd/
│   ├── nodev.morning.plist  # 07:30 daily → publish.py
│   ├── nodev.evening.plist  # 21:00 daily → publish.py
│   └── nodev.comments.plist # 매 30분 → respond.py
├── posts/
│   └── queue.json           # 발행 대기열 [{type, content, queued_at, published_at|null}]
├── state/
│   └── replied.json         # 이미 답한 댓글 ID 목록
├── .env                     # API 키 (gitignore)
├── .env.example             # 키 템플릿
├── requirements.txt
└── tests/
    ├── test_threads_client.py
    ├── test_generator.py
    └── test_responder.py
```

---

### Task 1: 프로젝트 초기 설정

**Files:**
- Create: `requirements.txt`
- Create: `.env.example`
- Create: `.gitignore`
- Create: `posts/queue.json`
- Create: `state/replied.json`

- [ ] **Step 1: requirements.txt 작성**

```
requests==2.32.3
anthropic==0.49.0
python-dotenv==1.1.0
pytest==8.3.5
pytest-mock==3.14.0
```

- [ ] **Step 2: .env.example 작성**

```
THREADS_ACCESS_TOKEN=your_long_lived_access_token_here
THREADS_USER_ID=your_numeric_user_id_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here
```

- [ ] **Step 3: .gitignore 작성**

```
.env
__pycache__/
.pytest_cache/
*.pyc
state/replied.json
```

- [ ] **Step 4: posts/queue.json 초기화**

```json
[]
```

- [ ] **Step 5: state/replied.json 초기화**

```json
[]
```

- [ ] **Step 6: 의존성 설치**

```bash
pip install -r requirements.txt
```

Expected: Successfully installed anthropic-0.49.0 python-dotenv-1.1.0 requests-2.32.3 (버전은 유사하면 OK)

- [ ] **Step 7: 커밋**

```bash
git add requirements.txt .env.example .gitignore posts/queue.json state/replied.json
git commit -m "🎉 프로젝트 초기 설정"
```

---

### Task 2: Threads API 클라이언트

**Files:**
- Create: `src/threads_client.py`
- Create: `tests/test_threads_client.py`

Threads API 흐름:
1. 포스트 발행: `POST /v1.0/{user_id}/threads` → container_id 획득 → `POST /v1.0/{user_id}/threads_publish`
2. 댓글 조회: `GET /v1.0/{post_id}/replies?fields=id,text,username,timestamp`
3. 댓글 작성: `POST /v1.0/{user_id}/threads` (reply_to_id 포함) → publish

- [ ] **Step 1: 실패하는 테스트 작성**

```python
# tests/test_threads_client.py
import pytest
from unittest.mock import patch, MagicMock
from src.threads_client import ThreadsClient

BASE = "https://graph.threads.net/v1.0"

@pytest.fixture
def client():
    return ThreadsClient(user_id="123", access_token="tok")

def test_create_post_calls_correct_endpoints(client):
    with patch("src.threads_client.requests.post") as mock_post:
        mock_post.side_effect = [
            MagicMock(ok=True, json=lambda: {"id": "container_1"}),
            MagicMock(ok=True, json=lambda: {"id": "post_1"}),
        ]
        post_id = client.create_post("안녕하세요")
        assert post_id == "post_1"
        assert mock_post.call_count == 2
        first_call = mock_post.call_args_list[0]
        assert first_call[0][0] == f"{BASE}/123/threads"
        assert first_call[1]["data"]["text"] == "안녕하세요"

def test_get_replies_returns_list(client):
    with patch("src.threads_client.requests.get") as mock_get:
        mock_get.return_value = MagicMock(ok=True, json=lambda: {
            "data": [{"id": "r1", "text": "감사합니다", "username": "user1", "timestamp": "2026-04-18T07:30:00Z"}]
        })
        replies = client.get_replies("post_1")
        assert len(replies) == 1
        assert replies[0]["id"] == "r1"

def test_reply_to_comment_publishes(client):
    with patch("src.threads_client.requests.post") as mock_post:
        mock_post.side_effect = [
            MagicMock(ok=True, json=lambda: {"id": "container_r"}),
            MagicMock(ok=True, json=lambda: {"id": "reply_1"}),
        ]
        reply_id = client.reply_to_comment("comment_1", "도움이 되셨나요?")
        assert reply_id == "reply_1"
        first_call = mock_post.call_args_list[0]
        assert first_call[1]["data"]["reply_to_id"] == "comment_1"

def test_create_post_raises_on_api_error(client):
    with patch("src.threads_client.requests.post") as mock_post:
        mock_post.return_value = MagicMock(ok=False, status_code=400, text="Bad Request")
        with pytest.raises(RuntimeError, match="Threads API 오류"):
            client.create_post("테스트")
```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

```bash
pytest tests/test_threads_client.py -v
```

Expected: ModuleNotFoundError 또는 ImportError (src/threads_client.py 없음)

- [ ] **Step 3: threads_client.py 구현**

```python
# src/threads_client.py
import requests

BASE = "https://graph.threads.net/v1.0"

class ThreadsClient:
    def __init__(self, user_id: str, access_token: str):
        self.user_id = user_id
        self.token = access_token

    def _post(self, path: str, data: dict) -> dict:
        data["access_token"] = self.token
        resp = requests.post(f"{BASE}/{path}", data=data)
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
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
pytest tests/test_threads_client.py -v
```

Expected: 4 passed

- [ ] **Step 5: 커밋**

```bash
git add src/threads_client.py tests/test_threads_client.py
git commit -m "✨ Threads API 클라이언트 구현"
```

---

### Task 3: 포스트 생성기 (Claude API)

**Files:**
- Create: `src/generator.py`
- Create: `tests/test_generator.py`

경험 포스트와 무료 자료 배포 포스트 두 가지를 생성한다.

- [ ] **Step 1: 실패하는 테스트 작성**

```python
# tests/test_generator.py
import pytest
from unittest.mock import patch, MagicMock
from src.generator import generate_experience_post, generate_free_content_post

def make_mock_response(text: str):
    mock = MagicMock()
    mock.content = [MagicMock(text=text)]
    return mock

def test_generate_experience_post_returns_string(mocker):
    mocker.patch("src.generator.anthropic.Anthropic").return_value.messages.create.return_value = \
        make_mock_response("개발팀한테 요청했더니 백로그에 넣었습니다.\n코딩 몰라도 하루만에 만들었습니다.")
    result = generate_experience_post("엑셀 자동화 도구가 필요했던 상황")
    assert isinstance(result, str)
    assert len(result) > 10

def test_generate_experience_post_includes_idea_in_prompt(mocker):
    mock_create = mocker.patch("src.generator.anthropic.Anthropic").return_value.messages.create
    mock_create.return_value = make_mock_response("포스트 내용")
    generate_experience_post("보고서 자동화")
    call_args = mock_create.call_args
    prompt_text = call_args[1]["messages"][0]["content"]
    assert "보고서 자동화" in prompt_text

def test_generate_free_content_post_returns_string(mocker):
    mocker.patch("src.generator.anthropic.Anthropic").return_value.messages.create.return_value = \
        make_mock_response("무료 가이드 드립니다. 팔로우+댓글 남겨주세요.")
    result = generate_free_content_post("Claude Code 설치 가이드", "https://example.com/guide.html")
    assert isinstance(result, str)
    assert len(result) > 10
```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

```bash
pytest tests/test_generator.py -v
```

Expected: ImportError (src/generator.py 없음)

- [ ] **Step 3: generator.py 구현**

```python
# src/generator.py
import anthropic

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
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        system=EXPERIENCE_SYSTEM,
        messages=[{"role": "user", "content": f"다음 상황을 바탕으로 Threads 포스트를 작성해주세요:\n{idea}"}],
    )
    return resp.content[0].text.strip()

def generate_free_content_post(resource_name: str, resource_url: str) -> str:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=400,
        system=FREE_CONTENT_SYSTEM,
        messages=[{"role": "user", "content": f"자료명: {resource_name}\n링크: {resource_url}\n\n위 무료 자료를 배포하는 Threads 포스트를 작성해주세요."}],
    )
    return resp.content[0].text.strip()
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
pytest tests/test_generator.py -v
```

Expected: 3 passed

- [ ] **Step 5: 커밋**

```bash
git add src/generator.py tests/test_generator.py
git commit -m "✨ Claude API 포스트 생성기 구현"
```

---

### Task 4: 발행 큐 & Publisher

**Files:**
- Create: `src/publisher.py`
- Modify: `posts/queue.json` (런타임에 변경됨, 구조 확정)

queue.json 항목 구조:
```json
{
  "id": "uuid",
  "type": "experience | free_content",
  "content": "포스트 본문",
  "queued_at": "2026-04-18T07:00:00",
  "published_at": null
}
```

- [ ] **Step 1: publisher.py 구현 (로직이 단순해 테스트 후 구현)**

```python
# src/publisher.py
import json
import uuid
from datetime import datetime
from pathlib import Path

QUEUE_PATH = Path("posts/queue.json")

def load_queue() -> list[dict]:
    if not QUEUE_PATH.exists():
        return []
    return json.loads(QUEUE_PATH.read_text())

def save_queue(queue: list[dict]) -> None:
    QUEUE_PATH.write_text(json.dumps(queue, ensure_ascii=False, indent=2))

def enqueue(content: str, post_type: str) -> dict:
    queue = load_queue()
    item = {
        "id": str(uuid.uuid4()),
        "type": post_type,
        "content": content,
        "queued_at": datetime.now().isoformat(),
        "published_at": None,
    }
    queue.append(item)
    save_queue(queue)
    return item

def pop_next() -> dict | None:
    queue = load_queue()
    pending = [item for item in queue if item["published_at"] is None]
    if not pending:
        return None
    return pending[0]

def mark_published(item_id: str) -> None:
    queue = load_queue()
    for item in queue:
        if item["id"] == item_id:
            item["published_at"] = datetime.now().isoformat()
            break
    save_queue(queue)

def publish_next(client) -> str | None:
    item = pop_next()
    if not item:
        return None
    post_id = client.create_post(item["content"])
    mark_published(item["id"])
    return post_id
```

- [ ] **Step 2: publisher 단위 테스트 작성**

```python
# tests/test_publisher.py
import json
import pytest
from unittest.mock import MagicMock
from src.publisher import enqueue, pop_next, mark_published, publish_next, QUEUE_PATH

@pytest.fixture(autouse=True)
def clean_queue(tmp_path, monkeypatch):
    monkeypatch.setattr("src.publisher.QUEUE_PATH", tmp_path / "queue.json")
    (tmp_path / "queue.json").write_text("[]")

def test_enqueue_adds_item():
    from src.publisher import load_queue
    enqueue("테스트 포스트", "experience")
    queue = load_queue()
    assert len(queue) == 1
    assert queue[0]["content"] == "테스트 포스트"
    assert queue[0]["published_at"] is None

def test_pop_next_returns_pending():
    enqueue("첫 번째", "experience")
    enqueue("두 번째", "experience")
    item = pop_next()
    assert item["content"] == "첫 번째"

def test_mark_published_sets_timestamp():
    item = enqueue("포스트", "experience")
    mark_published(item["id"])
    from src.publisher import load_queue
    queue = load_queue()
    assert queue[0]["published_at"] is not None

def test_publish_next_calls_client_and_marks_published():
    enqueue("발행할 포스트", "experience")
    mock_client = MagicMock()
    mock_client.create_post.return_value = "post_123"
    post_id = publish_next(mock_client)
    assert post_id == "post_123"
    from src.publisher import load_queue
    queue = load_queue()
    assert queue[0]["published_at"] is not None

def test_publish_next_returns_none_when_empty():
    mock_client = MagicMock()
    result = publish_next(mock_client)
    assert result is None
```

- [ ] **Step 3: 테스트 실행**

```bash
pytest tests/test_publisher.py -v
```

Expected: 5 passed

- [ ] **Step 4: 커밋**

```bash
git add src/publisher.py tests/test_publisher.py
git commit -m "✨ 발행 큐 및 publisher 구현"
```

---

### Task 5: 댓글 응답기 (Responder)

**Files:**
- Create: `src/responder.py`
- Create: `tests/test_responder.py`

필터 규칙:
- 상위 10개 댓글 (timestamp 기준 최신순)
- 키워드 트리거: "자료", "어떻게", "저도", "링크", "공유", "주세요", "보내"
- 이미 replied.json에 있는 댓글은 건너뜀

- [ ] **Step 1: 실패하는 테스트 작성**

```python
# tests/test_responder.py
import pytest
from src.responder import select_comments_to_reply, KEYWORD_TRIGGERS

SAMPLE_COMMENTS = [
    {"id": "c1", "text": "자료 주시면 감사합니다", "username": "user1", "timestamp": "2026-04-18T08:00:00Z"},
    {"id": "c2", "text": "좋은 내용이네요", "username": "user2", "timestamp": "2026-04-18T08:01:00Z"},
    {"id": "c3", "text": "저도 해보고 싶어요", "username": "user3", "timestamp": "2026-04-18T08:02:00Z"},
    {"id": "c4", "text": "어떻게 시작하나요", "username": "user4", "timestamp": "2026-04-18T08:03:00Z"},
    {"id": "c5", "text": "그냥 구경 중", "username": "user5", "timestamp": "2026-04-18T08:04:00Z"},
]

def test_keyword_comments_are_included():
    selected = select_comments_to_reply(SAMPLE_COMMENTS, already_replied=set())
    ids = [c["id"] for c in selected]
    assert "c1" in ids  # "자료"
    assert "c3" in ids  # "저도"
    assert "c4" in ids  # "어떻게"

def test_top_10_limit():
    many = [{"id": str(i), "text": f"댓글 {i}", "username": f"u{i}", "timestamp": f"2026-04-18T08:{i:02d}:00Z"} for i in range(15)]
    selected = select_comments_to_reply(many, already_replied=set())
    assert len(selected) <= 10

def test_already_replied_are_excluded():
    selected = select_comments_to_reply(SAMPLE_COMMENTS, already_replied={"c1", "c3"})
    ids = [c["id"] for c in selected]
    assert "c1" not in ids
    assert "c3" not in ids

def test_keyword_triggers_cover_expected_words():
    for word in ["자료", "어떻게", "저도", "링크", "공유", "주세요", "보내"]:
        assert word in KEYWORD_TRIGGERS
```

- [ ] **Step 2: 테스트 실행 — 실패 확인**

```bash
pytest tests/test_responder.py -v
```

Expected: ImportError

- [ ] **Step 3: responder.py 구현**

```python
# src/responder.py
import json
from pathlib import Path
import anthropic

KEYWORD_TRIGGERS = ["자료", "어떻게", "저도", "링크", "공유", "주세요", "보내"]
REPLIED_PATH = Path("state/replied.json")

REPLY_SYSTEM = """당신은 @nodev.build(비개발dev) Threads 계정 운영자입니다.
비개발자 직장인 팔로워의 댓글에 따뜻하고 실용적으로 답합니다.
1~2문장, 이모지 1개, 구어체."""

def load_replied() -> set[str]:
    if not REPLIED_PATH.exists():
        return set()
    return set(json.loads(REPLIED_PATH.read_text()))

def save_replied(replied: set[str]) -> None:
    REPLIED_PATH.parent.mkdir(exist_ok=True)
    REPLIED_PATH.write_text(json.dumps(list(replied), ensure_ascii=False, indent=2))

def _has_keyword(text: str) -> bool:
    return any(kw in text for kw in KEYWORD_TRIGGERS)

def select_comments_to_reply(comments: list[dict], already_replied: set[str]) -> list[dict]:
    sorted_comments = sorted(comments, key=lambda c: c["timestamp"])
    top10 = sorted_comments[:10]
    keyword_rest = [c for c in sorted_comments[10:] if _has_keyword(c["text"])]
    candidates = top10 + keyword_rest
    return [c for c in candidates if c["id"] not in already_replied]

def generate_reply(post_content: str, comment_text: str) -> str:
    client = anthropic.Anthropic()
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        system=REPLY_SYSTEM,
        messages=[{"role": "user", "content": f"포스트 내용:\n{post_content}\n\n댓글:\n{comment_text}\n\n답변을 작성해주세요."}],
    )
    return resp.content[0].text.strip()

def respond_to_post(threads_client, post_id: str, post_content: str) -> list[str]:
    replied = load_replied()
    comments = threads_client.get_replies(post_id)
    to_reply = select_comments_to_reply(comments, replied)
    reply_ids = []
    for comment in to_reply:
        text = generate_reply(post_content, comment["text"])
        reply_id = threads_client.reply_to_comment(comment["id"], text)
        replied.add(comment["id"])
        reply_ids.append(reply_id)
    save_replied(replied)
    return reply_ids
```

- [ ] **Step 4: 테스트 통과 확인**

```bash
pytest tests/test_responder.py -v
```

Expected: 4 passed

- [ ] **Step 5: 커밋**

```bash
git add src/responder.py tests/test_responder.py state/replied.json
git commit -m "✨ 댓글 필터링 및 자동 응답기 구현"
```

---

### Task 6: CLI 스크립트 (launchd 트리거용)

**Files:**
- Create: `scripts/publish.py`
- Create: `scripts/respond.py`

- [ ] **Step 1: publish.py 작성**

```python
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
```

- [ ] **Step 2: respond.py 작성**

```python
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

QUEUE_PATH = Path("posts/queue.json")

def main():
    client = ThreadsClient(
        user_id=os.environ["THREADS_USER_ID"],
        access_token=os.environ["THREADS_ACCESS_TOKEN"],
    )
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
```

- [ ] **Step 3: publisher.py에 post_id 저장 추가**

`src/publisher.py`의 `publish_next` 함수와 `mark_published`를 다음과 같이 수정:

```python
def mark_published(item_id: str, post_id: str) -> None:
    queue = load_queue()
    for item in queue:
        if item["id"] == item_id:
            item["published_at"] = datetime.now().isoformat()
            item["post_id"] = post_id
            break
    save_queue(queue)

def publish_next(client) -> str | None:
    item = pop_next()
    if not item:
        return None
    post_id = client.create_post(item["content"])
    mark_published(item["id"], post_id)
    return post_id
```

- [ ] **Step 4: 스크립트 동작 확인 (dry run — .env 없이 import만 체크)**

```bash
python -c "import scripts.publish; import scripts.respond; print('OK')"
```

Expected: OK (또는 sys.path 설정으로 인해 직접 실행 권장)

- [ ] **Step 5: 커밋**

```bash
git add scripts/publish.py scripts/respond.py src/publisher.py
git commit -m "✨ launchd 트리거용 CLI 스크립트 추가"
```

---

### Task 7: launchd 스케줄러 설정

**Files:**
- Create: `launchd/nodev.morning.plist`
- Create: `launchd/nodev.evening.plist`
- Create: `launchd/nodev.comments.plist`

`{PROJECT_PATH}`를 실제 절대 경로로 교체해야 한다. `{PYTHON_PATH}`는 `which python3`로 확인.

- [ ] **Step 1: nodev.morning.plist 작성**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>build.nodev.morning</string>
    <key>ProgramArguments</key>
    <array>
        <string>{PYTHON_PATH}</string>
        <string>{PROJECT_PATH}/scripts/publish.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{PROJECT_PATH}</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>7</integer>
        <key>Minute</key>
        <integer>30</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{PROJECT_PATH}/logs/morning.log</string>
    <key>StandardErrorPath</key>
    <string>{PROJECT_PATH}/logs/morning.err</string>
</dict>
</plist>
```

- [ ] **Step 2: nodev.evening.plist 작성**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>build.nodev.evening</string>
    <key>ProgramArguments</key>
    <array>
        <string>{PYTHON_PATH}</string>
        <string>{PROJECT_PATH}/scripts/publish.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{PROJECT_PATH}</string>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>21</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>{PROJECT_PATH}/logs/evening.log</string>
    <key>StandardErrorPath</key>
    <string>{PROJECT_PATH}/logs/evening.err</string>
</dict>
</plist>
```

- [ ] **Step 3: nodev.comments.plist 작성 (매 30분)**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>build.nodev.comments</string>
    <key>ProgramArguments</key>
    <array>
        <string>{PYTHON_PATH}</string>
        <string>{PROJECT_PATH}/scripts/respond.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>{PROJECT_PATH}</string>
    <key>StartInterval</key>
    <integer>1800</integer>
    <key>StandardOutPath</key>
    <string>{PROJECT_PATH}/logs/comments.log</string>
    <key>StandardErrorPath</key>
    <string>{PROJECT_PATH}/logs/comments.err</string>
</dict>
</plist>
```

- [ ] **Step 4: logs 디렉토리 생성 및 .gitignore에 추가**

```bash
mkdir -p logs
echo "logs/" >> .gitignore
```

- [ ] **Step 5: launchd에 등록하는 방법 메모 작성**

`launchd/README.md`에 아래 내용을 작성:

```markdown
# launchd 등록 방법

1. PROJECT_PATH와 PYTHON_PATH를 실제 경로로 치환한다
   - PROJECT_PATH: `pwd` 로 확인
   - PYTHON_PATH: `which python3` 로 확인

2. plist 파일을 ~/Library/LaunchAgents/에 복사한다
   ```
   cp launchd/*.plist ~/Library/LaunchAgents/
   ```

3. 등록한다
   ```
   launchctl load ~/Library/LaunchAgents/build.nodev.morning.plist
   launchctl load ~/Library/LaunchAgents/build.nodev.evening.plist
   launchctl load ~/Library/LaunchAgents/build.nodev.comments.plist
   ```

4. 확인한다
   ```
   launchctl list | grep nodev
   ```

5. 해제할 때
   ```
   launchctl unload ~/Library/LaunchAgents/build.nodev.morning.plist
   ```
```

- [ ] **Step 6: 커밋**

```bash
git add launchd/ logs/.gitkeep .gitignore
git commit -m "🔧 launchd 스케줄러 plist 설정 추가"
```

---

### Task 8: 전체 테스트 및 수동 발행 검증

- [ ] **Step 1: 전체 테스트 실행**

```bash
pytest tests/ -v
```

Expected: 모든 테스트 통과 (최소 16개)

- [ ] **Step 2: 포스트 큐에 샘플 항목 추가**

```bash
python -c "
import sys; sys.path.insert(0, '.')
from src.publisher import enqueue
enqueue('개발팀한테 요청했더니 백로그에 넣었습니다. 6개월을 기다렸습니다.\n\n코딩 몰라도 Claude Code로 하루만에 만들었습니다.\n\n비개발자도 됩니다. 진짜로요 🙌', 'experience')
print('큐에 추가 완료')
"
```

- [ ] **Step 3: .env 파일 생성 (실제 토큰으로)**

```bash
cp .env.example .env
# .env 파일에 실제 토큰 입력
```

- [ ] **Step 4: 수동 발행 테스트**

```bash
python scripts/publish.py
```

Expected: `[publish] 발행 완료: {post_id}` 출력

- [ ] **Step 5: 댓글 응답 테스트**

```bash
python scripts/respond.py
```

Expected: `[respond] {post_id} 댓글 처리 중...` 출력 또는 `발행된 포스트가 없습니다.`

- [ ] **Step 6: 최종 커밋**

```bash
git add .
git commit -m "✅ 전체 검증 완료 — Phase 1 자동화 시스템"
```

---

## Phase 2 예고 (이 플랜 범위 밖)

- `src/collector.py` — Anthropic RSS + 한국 AI 계정 트렌드 수집
- 트렌드 → 포스트 자동 생성 후 큐 추가
- launchd에 06:00 수집 트리거 추가
