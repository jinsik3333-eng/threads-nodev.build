# @nodev.builder Instagram Professional + ManyChat 플로우 세팅 체크리스트

목표: Instagram을 메인 전환 채널로 만들고, 댓글 키워드 → DM 가이드 발송을 ManyChat으로 빠르게 검증한다.

가이드 허브: https://jinsik3333-eng.github.io/threads-nodev.build/guides/

---

## 0. 오늘의 완료 기준

- Instagram 계정이 Professional 계정으로 전환됨
- Facebook Page가 생성/연결됨
- ManyChat에 Instagram 계정이 연결됨
- 댓글 키워드 6개가 DM 플로우로 연결됨
- 테스트 게시물에서 댓글 키워드 입력 → DM 수신까지 확인됨

---

## 1. Instagram Professional 계정 전환

### 권장 선택값

- 계정 유형: Creator 우선
  - 이유: 개인 브랜드/콘텐츠 계정에 자연스러움
  - Business도 가능하지만, 초기 `비개발dev` 개인 실험/교육 콘텐츠 톤에는 Creator가 적합
- 카테고리 후보:
  - Digital Creator
  - Education
  - Entrepreneur
  - Software Company는 초기에는 딱딱하므로 비추천
- 프로필 표시: 카테고리 노출은 초기에 켜도 무방. 어색하면 나중에 끄기

### 앱에서 진행

1. Instagram 앱 → 프로필
2. 우측 상단 메뉴
3. Settings and privacy
4. Account type and tools
5. Switch to professional account
6. Creator 선택
7. 카테고리 선택: `Digital Creator` 또는 `Education`
8. Professional dashboard가 보이면 완료

### 프로필 기본값

- 이름: 비개발dev
- 사용자명: nodev.builder
- 소개문 1안:
  ```text
  비개발자를 위한 Claude Code 실험실
  코딩 공부보다, AI에게 일을 맡기는 법
  ↓ 처음이면 1~3편부터
  ```
- 링크: https://jinsik3333-eng.github.io/threads-nodev.build/guides/

---

## 2. Facebook Page 생성/연결

ManyChat Instagram 자동화는 Facebook Page 연결이 사실상 필수다.

### Page 권장값

- Page name: 비개발dev
- Category:
  - Education website
  - Digital creator
  - Personal blog
- Bio:
  ```text
  코딩 경험 없는 사람도 Claude Code로 자기 일을 자동화할 수 있게 정리합니다.
  ```

### 연결 확인

Instagram 앱 또는 Meta Accounts Center에서 Facebook Page와 Instagram 계정이 연결되어야 한다.

완료 기준:
- Instagram Professional dashboard에서 연결된 Facebook Page가 보임
- Meta Business Suite에서 Instagram 계정과 Page가 함께 보임

---

## 3. ManyChat 연결

### 연결 순서

1. ManyChat 접속
2. Instagram 채널 추가
3. Facebook 로그인
4. `비개발dev` Page 선택
5. `@nodev.builder` Instagram 계정 선택
6. 권한 전체 승인
7. ManyChat Inbox/Automation에서 Instagram 채널이 Active인지 확인

### 주의

- 권한 승인 중 Page만 선택하고 Instagram 계정을 빼먹으면 댓글 자동화가 작동하지 않을 수 있음
- 연결 실패 시 Facebook 로그인 계정이 Page 관리자 권한을 갖고 있는지 확인
- 초기에는 과도한 자동 DM보다 “댓글 요청자에게 요청한 자료를 보내는 흐름”만 사용

---

## 4. 1차 키워드 플로우

처음에는 6개만 만든다.

### 키워드 1: 가이드 / 전체

트리거:
- `가이드`
- `전체`

DM:
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

### 키워드 2: 시작

DM:
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

### 키워드 3: 설치

DM:
```text
Claude Code 설치에서 막힌 분은 이 편부터 보시면 됩니다.

2편: Claude Code 설치하기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-02-claude-code-install.html

터미널이 처음이어도 따라갈 수 있게
성공 화면 / 오류 화면 기준으로 정리해뒀습니다.
```

### 키워드 4: 프로젝트

DM:
```text
첫 프로젝트는 코딩이 아니라,
내 폴더에서 결과물 하나를 만들어보는 연습입니다.

3편: 첫 번째 프로젝트 만들기
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-03-first-project.html

회의록 정리, 파일 정리, 콘텐츠 초안처럼
작은 업무부터 시작하면 됩니다.
```

### 키워드 5: 프롬프트

DM:
```text
Claude Code가 잘 안 되는 이유는 보통
AI가 부족해서가 아니라 지시가 흐릿해서입니다.

4편: Claude 잘 쓰는 법
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-04-better-prompts.html

프롬프트를 개발 지식이 아니라
업무 지시서처럼 쓰는 방법으로 정리했습니다.
```

### 키워드 6: 워크스페이스

DM:
```text
워크스페이스는 개발자 세팅이 아니라,
내 업무별 AI 작업실을 만드는 과정입니다.

5편: 나만의 워크스페이스
https://jinsik3333-eng.github.io/threads-nodev.build/guides/guide-05-workspace.html

한 번 잡아두면 Claude에게 매번 같은 설명을 반복하지 않아도 됩니다.
```

---

## 5. ManyChat 안에서 만드는 방식

각 키워드마다 아래 구조로 만든다.

1. Automation 생성
2. Trigger: Instagram Comments
3. Post 범위:
   - 초기 테스트: 특정 테스트 게시물 1개
   - 안정화 후: 전체 게시물 또는 캠페인 게시물별 지정
4. Keyword condition:
   - exact match 또는 contains는 테스트 후 선택
   - 한국어 키워드는 오타 가능성이 낮아 exact/contains 둘 다 가능
5. Action:
   - Send Message
   - 위 DM 템플릿 입력
6. Optional:
   - 태그 부여: `ig_kw_가이드`, `ig_kw_시작` 등
   - 사용자 입력 대기/추가 질문은 초기에는 넣지 않음

---

## 6. 테스트 절차

### 테스트 게시물 캡션

```text
Claude Code를 처음 시작하는 분들을 위해
비개발자 기준으로 1~3편만 먼저 볼 수 있게 정리했습니다.

필요하시면 댓글에 `시작`이라고 남겨주세요.
DM으로 링크 보내드릴게요.
```

### 테스트 순서

1. 테스트 게시물 업로드
2. 개인 계정 또는 지인 계정으로 댓글 `시작` 입력
3. DM 수신 확인
4. 링크 클릭 확인
5. ManyChat에서 contact/tag 기록 확인
6. `가이드`, `설치`도 각각 테스트

완료 기준:
- 댓글 후 DM이 1분 이내 도착
- 링크가 정상 접속됨
- 중복 메시지가 과도하게 발송되지 않음

---

## 7. 첫 운영 규칙

- 첫 1주일은 키워드 6개만 운영
- 댓글 자동 DM은 사용자가 직접 키워드를 남긴 경우만 발송
- 게시글마다 CTA 키워드는 1개만 명확하게 제시
- Threads에는 자동 DM 유도보다 “인스타에 정리해둠” 정도로 부드럽게 연결
- 링크 반복/무관한 DM/반복 홍보 메시지 금지

---

## 8. 다음 확장

1차 테스트 후 반응이 있으면 추가 키워드:

- `MCP` → 6편
- `스킬` → 7편
- `에이전트` → 8편
- `훅` → 9편

그 다음 자체 Meta API 구현 검토:
- Instagram Messaging API
- Webhooks
- Private Replies
- `instagram_manage_comments`
- `pages_messaging`

초기에는 ManyChat으로 충분하다.
