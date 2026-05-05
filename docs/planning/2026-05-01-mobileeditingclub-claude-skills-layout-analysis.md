# Reference Breakdown — MobileEditingClub Claude Skills Post

Source: https://www.instagram.com/p/DXnAfxaDZ0C/?igsh=MTNzeWptejZvdnEwcA==
Date: 2026-05-01
Accounts: @mobileeditingclub + @adrianabubori

## 핵심 관찰

이 게시글은 예쁜 이미지를 단순히 나열한 게 아니라, 같은 문법을 반복한다.

1. Cover: 고급 인물 이미지 + 거대 키워드 + 짧은 효용 + CTA.
2. Problem card: 단색 배경 + 시간 라벨 + 작업명 + 문제 설명.
3. Skill card: 상단 기능 설명 + 하단 결과물 목업.
4. Problem card 반복.
5. Skill card 반복.
6. Final CTA: 댓글 키워드 + 도구/혜택 + 팔로우/DM 안내.

즉 구조는:

```text
Hook
→ Before problem
→ Skill solution
→ Before problem
→ Skill solution
→ Before problem
→ Skill solution
→ Before problem
→ Skill solution
→ Before problem
→ Skill solution
→ CTA
```

우리 v8 05번이 약했던 이유는 이 기준에서 `문제/해결/결과` 중 무엇인지 불명확했기 때문이다.

---

## 슬라이드별 구조 분석

### 01 Cover — Campaign Hero

텍스트:
- `MOBILE EDITING CLUB`
- `Claude Skills`
- `to automate your content pipeline`
- `OUR EXACT SKILLS →`

구조:
- 배경: 패션 캠페인형 인물 이미지.
- 중앙: 거대 흰색 키워드 2줄.
- 하단: 짧은 효용 설명 + 알약 CTA.
- 이미지와 텍스트가 겹치지만 얼굴을 완전히 죽이지 않음.

템플릿:
```text
[Top center] Brand
[Full background] Human/product campaign image
[Center] Huge topic keyword
[Lower center] Benefit sentence
[Bottom center] CTA pill
```

우리 적용:
- `Claude Skills` → `콘텐츠 시스템`
- `to automate your content pipeline` → `한 아이디어를 30일치로 바꾸는 구조`

---

### 02 Problem — Time Cost Card

텍스트:
- `3-5 hours`
- `Writing Creative Briefs`
- 긴 문제 설명 문단

구조:
- 이미지 없음.
- 짙은 브라운 단색 배경.
- 상단 캡슐 라벨로 시간 소모 강조.
- 중앙 대형 작업명.
- 그 아래 문제 설명.

템플릿:
```text
[Top capsule] Time / pain metric
[Center title] Task name
[Center paragraph] Why it is hard / slow / messy
[Bottom] small arrow or pagination
```

우리 적용:
- `3-5 hours` → `매번 2시간`
- `Writing Creative Briefs` → `콘텐츠 방향 잡기`
- 문제: 아이디어는 있는데 톤, 후킹, 이미지 방향이 매번 흔들림.

---

### 03 Skill — Feature + Output Board

텍스트:
- `creative-brief.skill`
- 기능 설명
- 하단 결과물 카드들
- `SWIPE`

구조:
- 상단 크림 배경: 아이콘 + 기능명 + 설명.
- 하단 다크 영역: 실제 산출물 목업/문서 카드.
- 손글씨 주석과 화살표로 결과물에 의미 부여.

템플릿:
```text
[Top left] Brand
[Top center] Tool icon
[Center] feature-name.skill
[Below] 2-3 line definition
[Bottom dark panel] Output mockup cards
[Bottom right] SWIPE pill
```

우리 적용:
- `content-brief.skill`
- 하단 목업: Hook / Visual Direction / Caption / CTA 카드.

---

### 04 Problem — Script Writing

구조는 02와 동일.
- 시간 라벨 + 작업명 + 문제 설명.
- 같은 템플릿을 반복해 시리즈 리듬을 만든다.

핵심:
- 반복 템플릿이 지루하지 않은 이유는 제목과 문제 문단이 선명하기 때문.
- 레이아웃을 바꾸지 않고도 콘텐츠 흐름이 유지된다.

---

### 05 Skill — Script Writer Output

구조는 03과 동일.
- 상단: `Script-writer.skill`
- 하단: 스크립트 문서 UI 3개.
- 주석: `BASED ON THE OUTPUT OF THE CREATIVE BRIEF`

핵심:
- 이전 solution의 결과가 다음 solution의 입력이 된다.
- 하단 주석이 페이지 간 연결을 만든다.

우리 적용:
- `caption-writer.skill`
- 주석: `BASED ON THE CONTENT DIRECTION`

---

### 06 Problem — Creative Direction

구조는 02/04와 동일.

핵심:
- 문제 카드에서 이미지가 없기 때문에 오히려 메시지가 명확하다.
- 배경, 라벨, 제목, 문단만으로 쉬어가는 리듬을 만든다.

---

### 07 Skill — Creative Direction Dashboard

구조:
- 상단: `creative-direction.skill`
- 하단: 다크 SaaS 대시보드 목업.
- 목업 안에 Palette / Lighting / Composition / Typography.

핵심:
- 단순 도구 나열이 아니라 `결정해야 할 항목`을 UI로 보여준다.
- 우리 05번처럼 도구 4개를 그냥 놓는 것보다 훨씬 명확하다.

우리 적용:
- `direction-board.skill`
- 하단 목업: Tone / Color / Layout / Reference / Do-not.

---

### 08 Problem — Storyboard

구조는 문제 카드 반복.

핵심:
- 이 게시글의 주제와 사용자의 최신 피드백이 정확히 맞는다.
- 좋은 콘텐츠는 스토리보드 없이 만들면 연결이 끊긴다는 메시지.

우리 적용:
- 문제 카드로 사용할 수 있음:
  - `스토리보드 없이 만들면`
  - `이미지는 예쁜데 흐름이 없다`

---

### 09 Skill — Storyboard Output

구조:
- 상단: `storyboard.skill`
- 하단: 스토리보드 문서 카드.
- 프레임 3개 썸네일 + 설명.

핵심:
- 스토리보드를 추상적으로 말하지 않고, 실제 결과물로 보여준다.
- 이게 우리가 만들어야 하는 05번의 좋은 방향이다.

우리 적용:
- `carousel-storyboard.skill`
- 하단: 01 Hook / 02 Bridge / 03 Prompt / 04 Assets / 05 Flow / 06 CTA 프레임.

---

### 10 Problem — Image Generation

구조는 문제 카드 반복.

메시지:
- 막연한 프롬프트는 브랜드와 맞지 않는 랜덤 이미지를 만든다.

우리 적용:
- `이미지 생성이 흔들리는 이유`
- `프롬프트보다 기준표가 먼저다`

---

### 11 Skill — Image Generation Asset Library

구조:
- 상단: `image-generation.skill`
- 하단: 파일 구조 + 이미지 썸네일 4개.
- 화살표와 주석으로 `생성 → 정리 → 에셋화`를 보여줌.

핵심:
- 이미지 4장을 그냥 배치하지 않고, 파일/라이브러리 구조로 묶어 의미를 만든다.
- 우리 콘텐츠에서도 4개 이미지를 쓰려면 반드시 `무엇의 묶음인지`를 라벨링해야 한다.

우리 적용:
- `asset-library.skill`
- 하단: Cover / Hook image / Product shot / CTA background.

---

### 12 Final CTA

텍스트:
- `Comment “scale”`
- `to learn how to use Claude for your brand`
- `P.S. don’t forget to follow @mobileeditingclub and check your DM requests.`

구조:
- 이미지 없음.
- 다크 브라운 배경.
- 중앙 대형 댓글 CTA.
- 댓글 키워드만 박스 처리.
- Claude 아이콘을 문장 중간에 삽입.
- 하단 작은 팔로우/DM 안내.

템플릿:
```text
[Top center] Brand
[Center huge] Comment “keyword”
[Center] to get / learn / use X for Y
[Keyword box] Highlight keyword
[Tool icon box] Optional
[Bottom] Follow + check DM
```

우리 적용:
- `댓글에 “30일치”`
- `Claude로 콘텐츠 시스템 만드는 법 받아가기`
- `P.S. @nodev.builder 팔로우하고 DM 요청함 확인`

---

## 추출한 레이아웃 템플릿 10개

### T01 Campaign Hero Cover
- 용도: 커버.
- 구성: 풀블리드 인물/제품 이미지 + 거대 키워드 + 효용 문장 + CTA pill.
- 주의: 이미지와 텍스트가 겹쳐도 주 피사체가 죽으면 실패.

### T02 Time Cost Problem Card
- 용도: Before / 문제 정의.
- 구성: 시간 라벨 + 작업명 + 문제 문단.
- 주의: 제목이 명확해야 한다. 이미지 필요 없음.

### T03 Skill Definition + Output Mockup
- 용도: 해결 기능 소개.
- 구성: 기능명.skill + 정의 문장 + 하단 산출물 목업.
- 주의: 하단 목업은 장식이 아니라 결과 증거여야 한다.

### T04 Linked Skill Output
- 용도: 이전 단계의 산출물이 다음 단계의 입력이 되는 흐름.
- 구성: 기능명 + 하단 결과물 + 주석 `BASED ON ...`.
- 주의: 페이지 간 연결 문구 필수.

### T05 Direction Dashboard
- 용도: 방향성/기준표/브랜드 룰 설명.
- 구성: 큰 기능명 + 하단 대시보드 UI + 4개 기준 카드.
- 주의: 도구명이 아니라 의사결정 항목을 보여줘야 한다.

### T06 Storyboard Preview
- 용도: 구조/프레임/시퀀스 설명.
- 구성: 기능명 + 하단 스토리보드 문서 + 프레임 썸네일 3~6개.
- 주의: 프레임 간 순서가 보여야 한다.

### T07 Asset Library
- 용도: 이미지/콘텐츠 결과 묶음 설명.
- 구성: 파일 구조 + 이미지 썸네일 + 화살표 주석.
- 주의: 이미지를 그냥 나열하지 말고 라이브러리/세트로 묶어야 한다.

### T08 CTA Comment Keyword
- 용도: 마지막 페이지.
- 구성: 댓글 키워드 대형 문장 + 키워드 박스 + DM/팔로우 안내.
- 주의: 키워드와 받을 자료가 분명해야 한다.

### T09 Side-by-side Before/After
- 용도: 문제 → 해결 비교.
- 구성: 왼쪽 Before 문장/이미지, 오른쪽 After 산출물.
- 주의: 비교 기준 1개만 잡는다.

### T10 Process Ladder
- 용도: 우리 v8 05번 대체.
- 구성: 01 Draft → 02 Direction → 03 Asset → 04 Publish.
- 주의: 2×2 도구 나열 금지. 좌→우 또는 상→하 흐름으로 읽히게 한다.

---

## 우리 05번 대체안

기존 v8 05번은 `도구 네트워크`처럼 보였고 강조점이 흐렸다.

새 05번은 아래 둘 중 하나로 간다.

### Option A — Storyboard Preview형

제목:
```text
초안이 콘텐츠가 되는 순서
```

구조:
```text
[상단] NODEV BUILDER
[제목] 초안이 콘텐츠가 되는 순서
[서브] Claude 결과를 바로 올리는 게 아니라, 프레임으로 나눈다.
[하단 문서 목업]
01 Hook / 02 Bridge / 03 Prompt / 04 Assets / 05 Flow / 06 CTA
[CTA] SEE THE BOARD →
```

장점:
- 사용자가 말한 `구조적인 스토리보드`와 가장 잘 맞음.
- 5번이 정확히 전체 흐름을 정리하는 장이 됨.

### Option B — Process Ladder형

제목:
```text
아이디어가 업로드되는 4단계
```

구조:
```text
01 Draft       Claude       초안 만들기
02 Direction   Board        톤과 장면 고정
03 Asset       Canva/Figma  카드로 변환
04 Publish     Instagram    업로드
```

장점:
- 흐름이 즉시 읽힘.
- 도구와 단계가 충돌하지 않음.

결론:
- 지금 우리 캐러셀에는 Option A가 더 맞다.
- 이유: 이번 콘텐츠의 핵심 교훈이 `스토리보드를 먼저 짜야 좋은 콘텐츠가 나온다`이기 때문.

---

## 추가 관찰 — Stylish Full Image / Visual Break 패턴

추가로 @mobileeditingclub의 다른 게시글들을 보면, 스타일리쉬형은 커버뿐 아니라 중간 슬라이드에도 **이미지를 전체로 깔아 넣는 패턴**을 자주 쓴다.

관찰한 패턴:
- 풀블리드 인물/제품/클로즈업 이미지 위에 큰 흰색 타이포를 얹는다.
- 상단 중앙 작은 브랜드 로고는 유지한다.
- 커버는 `큰 후킹 문장 + CTA pill` 중심이다.
- 내부 슬라이드는 `Eyes`, `Nose`처럼 하나의 디테일을 크게 보여주고, 아래에 짧은 체크리스트를 얹는다.
- 이미지가 장식이 아니라 `증거 / 결과물 / 분위기 전환` 역할을 한다.

추가 템플릿:

### T11 Full Image Breaker
- 용도: 캐러셀 중간 리듬 전환.
- 구성: 전체 이미지 + 하단 큰 2줄 제목 + 작은 CTA pill.
- 주의: 정보 설명 장이 아니라 `잠깐 멈추게 하는 장`이어야 한다.

### T12 Detail Close-up Checklist
- 용도: 이미지 품질/프롬프트 기준 설명.
- 구성: 풀블리드 클로즈업 이미지 + 큰 키워드 + 3~4개 체크리스트.
- 주의: 한 장에서 하나의 디테일만 다룬다. 체크리스트는 모바일에서 읽혀야 한다.

### T13 Section Opener
- 용도: 다음 파트로 넘어가는 전환 페이지.
- 구성: 전체 이미지 + 얇은 프레임 + 중앙 대형 타이틀 + 짧은 전환 문장.
- 주의: 프레임/로고/제목이 서로 겹치지 않게 안전영역을 둔다.

### T14 Visual Comparison
- 용도: Before/After 또는 모델/도구 비교.
- 구성: 좌우 풀 이미지 비교 + 하단 흰 caption strip.
- 주의: 긴 본문 금지. 설명은 하단 스트립 한 덩어리로만 둔다.

수정 사항:
- T03 하단 흰 박스 2개의 상단 기준선을 맞춤. 레이아웃상 이쪽이 맞다.
- 템플릿 보드는 10개에서 14개로 확장했다.
