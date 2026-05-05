# @nodev.builder 인스타그램 + ManyChat + Threads 런칭 플랜

전제: Claude Code 비개발자 9편 가이드는 순차 공개가 아니라 **한 번에 공개 완료된 리소스 허브**로 운영한다. 따라서 CTA는 “오늘 몇 편 공개”가 아니라, 사용자의 현재 막힘에 맞춰 필요한 편을 바로 보내주는 구조로 설계한다.

가이드 허브:
https://jinsik3333-eng.github.io/threads-nodev.build/guides/

---

## 1. ManyChat 기본 구조

### 목표
인스타그램 게시글/릴스 댓글 키워드를 받으면 DM으로 해당 가이드 링크를 자동 발송한다.

### ManyChat 사용 시 Meta API 필요 여부
- 직접 Meta API 구현은 필요 없음.
- ManyChat이 Meta 공식 연동/권한 처리를 대신한다.
- 필요한 계정 조건:
  - Instagram 프로페셔널 계정
  - Facebook Page 연결
  - ManyChat에서 Instagram 연결 및 권한 승인

### 직접 구현이 필요한 경우
나중에 자체 시스템으로 만들려면 Meta Developer App, Instagram Messaging API, Webhooks, Private Replies, 앱 검수/권한이 필요하다. 초기에는 ManyChat으로 검증한다.

---

## 2. 키워드 세트

### 1차 세팅 키워드
처음부터 9개 전부 만들지 말고, 반응이 큰 키워드부터 운영한다.

1. `가이드`
   - 전체 목차 발송
   - 모든 게시글 공통 fallback

2. `시작`
   - 1~3편 추천
   - “처음이면 이것만 먼저” 흐름

3. `설치`
   - 2편 발송
   - 터미널/설치 막힘용

4. `프로젝트`
   - 3편 발송
   - 첫 결과물 만들기용

5. `프롬프트`
   - 4편 발송
   - Claude에게 제대로 시키는 법

6. `워크스페이스`
   - 5편 발송
   - 내 AI 작업실 세팅

7. `MCP`
   - 6편 발송
   - Notion/Google Drive/GitHub/Slack 연결

8. `스킬`
   - 7편 발송
   - 반복 업무를 명령어처럼 만드는 흐름

9. `에이전트`
   - 8편 발송
   - 역할별 AI 도우미 만들기

10. `훅`
   - 9편 발송
   - 안전장치/자동화 보호 흐름

---

## 3. ManyChat DM 템플릿

### 공통 첫 문장 톤
너무 마케팅 메시지처럼 쓰지 않는다. “요청하신 자료입니다”보다 “막히는 지점 기준으로 보면 됩니다”가 더 자연스럽다.

---

### 키워드: 가이드

```text
Claude Code 비개발자 가이드 전체 링크입니다.

처음이라면 9편을 한 번에 다 보려고 하지 말고,
1~3편만 먼저 보세요.

1편: Claude Code 전에 계정/화면 감각 준비
2편: Claude Code 설치하기
3편: 첫 번째 프로젝트 만들기

전체 가이드:
https://jinsik3333-eng.github.io/threads-nodev.build/guides/
```

---

### 키워드: 시작

```text
처음 시작하는 분이면 여기부터 보면 됩니다.

1편: Claude Code 전에 계정/화면 감각 준비
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-01-desktop.html

2편: Claude Code 설치하기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-02-claude-code-install.html

3편: 첫 번째 프로젝트 만들기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-03-first-project.html

핵심은 코딩 공부가 아니라,
Claude에게 내 일을 어떻게 맡길지 감을 잡는 것입니다.
```

---

### 키워드: 설치

```text
Claude Code 설치에서 막힌 분은 이 편부터 보시면 됩니다.

2편: Claude Code 설치하기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-02-claude-code-install.html

터미널이 처음이어도 따라갈 수 있게
성공 화면 / 오류 화면 기준으로 정리해뒀습니다.
```

---

### 키워드: 프로젝트

```text
첫 프로젝트는 코딩이 아니라,
내 폴더에서 결과물 하나를 만들어보는 연습입니다.

3편: 첫 번째 프로젝트 만들기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-03-first-project.html

회의록 정리, 파일 정리, 콘텐츠 초안처럼
작은 업무부터 시작하면 됩니다.
```

---

### 키워드: 프롬프트

```text
Claude Code가 잘 안 되는 이유는 보통
AI가 부족해서가 아니라 지시가 흐릿해서입니다.

4편: Claude 잘 쓰는 법
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-04-better-prompts.html

프롬프트를 개발 지식이 아니라
업무 지시서처럼 쓰는 방법으로 정리했습니다.
```

---

### 키워드: 워크스페이스

```text
워크스페이스는 개발자 세팅이 아니라,
내 업무별 AI 작업실을 만드는 과정입니다.

5편: 나만의 워크스페이스
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-05-workspace.html

한 번 잡아두면 Claude에게 매번 같은 설명을 반복하지 않아도 됩니다.
```

---

### 키워드: MCP

```text
MCP는 설정을 외우는 게 아니라,
Claude Code에게 “이 앱 연결해줘”라고 맡기는 흐름으로 보면 됩니다.

6편: MCP 연결, 외우지 말고 Claude Code에게 시키기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-06-mcp.html

처음에는 Notion, Google Drive, GitHub, Slack 같은 서비스 연결부터 보면 됩니다.
```

---

### 키워드: 스킬

```text
매번 같은 설명을 반복한다면 Skills를 보면 됩니다.

7편: Skills — 반복 작업을 명령어처럼 만들기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-07-skills.html

직접 파일을 외워서 만드는 방식이 아니라,
Claude Code에게 skill-creator로 만들게 하는 흐름으로 정리했습니다.
```

---

### 키워드: 에이전트

```text
작업이 많아지면 Claude 하나에게 다 시키는 것보다
역할별 AI 도우미를 나누는 게 편합니다.

8편: Sub-agents — 역할별 AI 도우미
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-08-agents.html

비개발자도 에이전트 파일을 직접 쓰는 게 아니라,
Claude Code에게 “이런 팀원 만들어줘”라고 시키는 방식으로 시작하면 됩니다.
```

---

### 키워드: 훅

```text
자동화가 편해질수록 안전장치가 필요합니다.

9편: Hooks — 내 작업 지키는 안전장치
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-09-hooks.html

위험한 명령을 실행하기 전에 멈추게 하거나,
작업 결과를 알림으로 받는 흐름을 이해하는 편입니다.
```

---

## 4. 인스타그램 첫 5개 게시글 CTA

### 게시글 1 — 런칭/정체성

주제:
`코딩 몰라도 Claude Code를 시작할 수 있습니다`

본문 CTA:
```text
Claude Code를 처음 시작하는 분이라면
댓글에 `시작`이라고 남겨주세요.

1~3편만 먼저 볼 수 있는 링크를 DM으로 보내드릴게요.
```

DM 키워드:
`시작`

연결 가이드:
1~3편

---

### 게시글 2 — 설치 장벽

주제:
`터미널이 무서워서 Claude Code 설치를 미루고 있다면`

본문 CTA:
```text
설치 화면을 보면서 따라가고 싶다면
댓글에 `설치`라고 남겨주세요.

성공 화면 / 오류 화면 기준으로 정리한 2편을 보내드릴게요.
```

DM 키워드:
`설치`

연결 가이드:
2편

---

### 게시글 3 — 첫 프로젝트

주제:
`비개발자의 첫 Claude Code 프로젝트는 코딩이 아닙니다`

본문 CTA:
```text
처음 만들 프로젝트 예시가 필요하면
댓글에 `프로젝트`라고 남겨주세요.

회의록 정리, 파일 정리, 콘텐츠 초안처럼
작게 시작하는 3편 링크를 보내드릴게요.
```

DM 키워드:
`프로젝트`

연결 가이드:
3편

---

### 게시글 4 — 프롬프트/지시서

주제:
`AI가 못하는 게 아니라, 시키는 방식이 문제일 수 있습니다`

본문 CTA:
```text
Claude에게 어떻게 말해야 할지 모르겠다면
댓글에 `프롬프트`라고 남겨주세요.

비개발자용 업무 지시서 방식으로 정리한 4편을 보내드릴게요.
```

DM 키워드:
`프롬프트`

연결 가이드:
4편

---

### 게시글 5 — 워크스페이스/반복 설명 제거

주제:
`Claude에게 매번 같은 설명을 반복하고 있다면`

본문 CTA:
```text
내 업무별 AI 작업실을 만들고 싶다면
댓글에 `워크스페이스`라고 남겨주세요.

5편 링크를 DM으로 보내드릴게요.
```

DM 키워드:
`워크스페이스`

연결 가이드:
5편

---

## 5. Threads 동시 운영 원칙

Threads는 인스타그램 카드뉴스를 그대로 옮기지 않는다.

역할:
- 인스타그램: 카드뉴스 + 댓글 키워드 DM 전환
- Threads: 짧은 생각/기록/실험 로그 + 가이드 허브 보조 유입

운영 원칙:
- 링크는 너무 자주 넣지 않는다.
- 3~5개 중 1개 정도만 직접 링크 포함.
- 나머지는 “인스타에 정리해둠”, “댓글 달면 알려드림” 정도로 부드럽게 유도.
- 새 Threads 계정은 초반 자동화 강도를 낮춘다.

---

## 6. Threads 첫 5개 텍스트 버전

### Threads 1 — 시작

```text
Claude Code를 처음 시작하는 사람은
처음부터 9편을 다 볼 필요 없다.

1. Claude 화면 감각 익히기
2. Claude Code 설치하기
3. 내 폴더에서 첫 결과물 만들기

이 3개만 먼저 해도
“아 이게 이런 식으로 돌아가는구나” 감이 온다.

코딩 공부가 아니라,
AI에게 내 일을 맡기는 감각부터 익히는 게 먼저다.
```

---

### Threads 2 — 설치

```text
비개발자가 Claude Code에서 제일 먼저 막히는 건
대부분 코딩이 아니라 설치 화면이다.

터미널이 뭔지 모르겠고,
뭐가 성공 화면인지 모르겠고,
에러가 뜨면 어디서부터 봐야 할지 모른다.

그래서 설치 가이드는 명령어보다
“이 화면이 보이면 정상” 기준으로 보는 게 훨씬 낫다.
```

---

### Threads 3 — 첫 프로젝트

```text
Claude Code 첫 프로젝트는
거창한 앱 만들기가 아니어도 된다.

회의록 정리
폴더 안 파일 이름 바꾸기
CSV 요약하기
콘텐츠 초안 만들기

이런 작은 것부터 해보면 된다.

중요한 건 코딩을 이해하는 게 아니라
내 업무를 Claude가 읽을 수 있게 설명하는 것.
```

---

### Threads 4 — 프롬프트

```text
프롬프트를 주문처럼 쓰면 결과가 흔들린다.

“이거 해줘”보다

목표는 뭐고
자료는 어디 있고
조건은 뭐고
끝났다는 증거는 뭔지

이렇게 업무 지시서처럼 말해야 한다.

비개발자에게 필요한 건 개발 문법보다
일을 구조화해서 설명하는 능력에 가깝다.
```

---

### Threads 5 — 워크스페이스

```text
Claude Code를 계속 쓰다 보면
매번 같은 설명을 반복하게 된다.

“이 폴더는 이런 프로젝트고”
“결과물은 이런 형식이고”
“이건 건드리지 말고”

이걸 줄이려면 업무별 워크스페이스를 만들어두는 게 좋다.

개발자 세팅이라기보다
내 AI 작업실을 정리하는 느낌에 가깝다.
```

---

## 7. Threads 자동화 방향

### 지금 당장
- 완전 자동 게시보다 수동/반자동 추천.
- Hermes가 인스타 게시글에서 Threads 버전을 자동 생성해 큐에 넣고, 사용자가 확인 후 올리는 방식.
- 링크 포함은 제한적으로.

### 토큰 안정화 후
공식 Threads API로 가능:
- 텍스트 게시 자동화
- 게시물 목록 조회
- 답글 조회
- 댓글 답글 작성

이미 코드 구조상 `app/src/threads.py`에 공식 Threads API 클라이언트 방향이 잡혀 있다.

### 주의
새 계정은 초반에 링크 반복/댓글 자동응답을 강하게 걸면 봇 시그널이 될 수 있다. Threads는 인스타 DM 자동화처럼 전환 채널로 쓰기보다, 기록형 보조 채널로 운영한다.

---

## 8. 추천 실행 순서

1. ManyChat 연결
2. 키워드 `가이드`, `시작`, `설치`, `프로젝트`, `프롬프트`, `워크스페이스` 먼저 세팅
3. 인스타 첫 5개 게시글 제작
4. 각 게시글 하단 CTA에 키워드 삽입
5. 같은 주제로 Threads 텍스트 버전 수동/반자동 업로드
6. 반응 좋은 키워드 확인 후 `MCP`, `스킬`, `에이전트`, `훅` 추가
