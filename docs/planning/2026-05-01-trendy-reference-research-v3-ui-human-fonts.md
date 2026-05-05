# 트렌디형 카드뉴스 재탐색 v3 — Human + UI + Font Mix

## 왜 다시 탐색했나

이전 v2는 `@mobileeditingclub + @adrianabubori`의 큰 인물 이미지와 에디토리얼 타이포를 일부 반영했지만, 실제 예시를 보면 트렌디형은 단순히 “고급 인물 이미지 + 큰 제목”만이 아니다.

실제 패턴은 다음이 섞인다.

1. 감도 높은 생성형 인물/제품 이미지
2. 흰색/반투명 텍스트 박스 또는 프레임
3. Claude, Notion, Figma, Instagram 등 툴 아이콘/네트워크
4. Claude 데스크톱/프롬프트 입력창 같은 UI 화면
5. 굵은 산세리프 + 세리프/이탤릭/스크립트 폰트 믹스
6. 슬라이드마다 다른 포맷: 커버, UI, 프롬프트, 결과, 비교, CTA

따라서 다음 트렌디형은 “전체 슬라이드가 같은 에디토리얼 포스터”가 아니라 **브랜드 캠페인 + AI 툴 UI + 저장 가능한 프롬프트 템플릿**의 혼합 구조로 가야 한다.

---

## 실제 레퍼런스에서 확인한 패턴

### 1. Mobile Editing Club 계열

핵심: **AI 튜토리얼을 정보 카드가 아니라 패션/뷰티 캠페인 썸네일처럼 보이게 함.**

관찰 패턴:

- 풀블리드 인물/제품 이미지
- 얼굴 초근접 크롭 또는 상반신 화보 컷
- 흰색 초대형 산세리프 타이틀
- 특정 단어만 세리프/이탤릭으로 강조
- 작은 상단 로고 반복
- 하단 pill CTA: `SEE FOR YOURSELF →`, `OUR WORKFLOWS →`, `COPY THE PROMPT →`
- 전통적 설명 박스는 적고, 결과물/툴명을 제목처럼 사용

가져갈 요소:

- 커버는 Claude UI가 아니라 “Claude를 쓰는 사람/브랜드 장면”으로 시작
- Claude, GPT Image, Figma 같은 툴명은 설명이 아니라 메인 타이틀로 사용
- 생성형 인물은 장식이 아니라 “AI로 가능한 결과”의 증거 이미지로 사용

---

### 2. Adriana Bubori 계열

핵심: **Claude 생산성 콘텐츠를 라이프스타일/비즈니스 매거진처럼 패키징.**

보이는 게시물 제목 패턴:

- `I save 4 hours a day with Claude cowork`
- `Claude Skills`
- `Claude prompts to build your creative team`
- `How to scale content production with Claude`
- `What if Claude could create your content on autopilot?`
- `I hired a full creative team with Claude`
- `Prompt less Edit more`
- `Claude for Brands`
- `AI agent`
- `fonts of the week`

핵심 카피 패턴:

- `I save X hours with ...`
- `I hired/built ... with Claude`
- `What if Claude could ...?`
- `Claude for Brands`
- `Prompt less. Edit more.`
- `... of the week`

가져갈 요소:

- Claude를 단순 챗봇이 아니라 `coworker`, `creative team`, `agent`, `content pipeline`, `autopilot`으로 포지셔닝
- 첫 장은 결과/상상/베네핏을 먼저 던짐
- 2~5장에서 Claude UI, 프롬프트, 결과물 예시, 툴 연결을 보여줌

---

## 기존 v2의 한계

v2 장점:

- 에디토리얼 톤은 이전보다 좋아짐
- 설명형으로 퇴화하지 않도록 문구를 압축함
- 인물 이미지와 큰 타이포 조합은 통과

v2 한계:

1. 모든 장이 비슷한 포스터형이라 실제 계정들의 슬라이드 변주가 부족함
2. Claude 데스크톱/프롬프트 입력창 UI가 없음
3. 텍스트 박스, 흰색 프레임, 툴 아이콘 네트워크가 부족함
4. 폰트가 산세리프 + 세리프 이탤릭 정도에 머물고, 스크립트/컨덴스드/모노 UI 폰트의 역할 분화가 부족함
5. 저장 가능한 프롬프트/워크플로우 템플릿으로서의 실용성이 약함
6. 트렌디한 “감도”는 있으나 실제 예시처럼 “AI 작업 화면을 쓰는 듯한 현실감”이 약함

---

## 새 트렌디형 제작 원칙 v3

### 원칙 1. 커버는 캠페인, 내부는 UI/프롬프트

- 1장: 감도 높은 생성형 인물/브랜드 장면 + 큰 후킹 카피
- 2장: 문제/욕망을 짧게 제시
- 3장: Claude 데스크톱/프롬프트 입력창 UI
- 4장: Claude output/result UI
- 5장: 툴 아이콘 네트워크 또는 content pipeline
- 6장: 복붙 프롬프트 / 저장 CTA

### 원칙 2. 슬라이드마다 형식이 달라야 한다

같은 포스터 6장을 만들지 않는다. 다음 포맷을 섞는다.

- Magazine cover
- White framed portrait card
- Claude desktop prompt window
- Dark UI command panel
- Tool icon network
- Before/After 또는 Output preview
- Copy-this-prompt template

### 원칙 3. 폰트는 역할별로 분리한다

- 메인 영문 헤드라인: 굵은 산세리프/컨덴스드 느낌
- 감성 강조 단어: 세리프 이탤릭 또는 스크립트
- 한글 보조문: Pretendard/SUIT 계열, 가볍게
- 프롬프트/UI 텍스트: 모노스페이스 계열
- 로고/라벨/CTA: 작고 단단한 uppercase 산세리프

### 원칙 4. 텍스트 박스는 설명 박스가 아니라 UI 장치여야 한다

좋은 텍스트 박스:

- Claude 입력창
- 프롬프트 카드
- 브라우저/데스크톱 윈도우
- 미니 캡션 박스
- 흰색 프레임 속 인물 카드
- 툴 아이콘 라벨

나쁜 텍스트 박스:

- 설명문을 길게 담는 강의 슬라이드 박스
- 역할/공식/목록을 지나치게 설명하는 워크시트 박스
- 장식용 라벨

### 원칙 5. 생성형 인물 이미지는 목적별로 다르게 쓴다

- 커버: 얼굴/상반신 화보로 후킹
- 문제 카드: 업무 중인 크리에이터/브랜드 오너
- UI 카드: 배경은 어둡게 흐리고 Claude 창이 주인공
- 결과 카드: 인물보다 결과물/콘텐츠 조각이 주인공
- CTA: 다시 인물 또는 프롬프트 템플릿을 크게 보여줌

---

## 다음 제작용 추천 구조

### 카드뉴스 제목 후보

1. `I Built a Content Team with Claude`
2. `Claude Prompts to Build Your Creative Team`
3. `What if Claude Planned Your Next 30 Posts?`
4. `Prompt Less. Brief Better.`
5. `Claude Workflows of the Week`

### 추천안 A — Adriana식 Claude cowork

1. Cover: 인물 화보 + `I built a content team with Claude`
2. Problem: 콘텐츠 팀 업무 6개를 흰색 카드로 분해
3. Prompt UI: Claude 데스크톱 입력창
4. Output UI: Claude 결과 카드 3개
5. Tool Network: Claude → Notion → Figma/Canva → Instagram
6. Copy Prompt: 복붙용 프롬프트 박스 + CTA

### 추천안 B — Mobile Editing Club식 AI campaign

1. Cover: 초근접 인물/제품 이미지 + `This is not a content team. This is Claude.`
2. Prompt: 프롬프트 입력창을 화보 위에 작게 얹기
3. Result: 콘텐츠 조각들이 floating card처럼 보이기
4. Compare: Before/After 또는 Solo vs System
5. Format: Feed/Reels/Caption/Email을 UI 카드로 보여주기
6. CTA: `COPY THIS WORKFLOW →`

### 추천안 C — of the week 연재형

1. Cover: `Claude Workflows of the Week`
2. Workflow 01: Research
3. Workflow 02: Hooks
4. Workflow 03: Carousel outline
5. Workflow 04: Caption/CTA
6. Save: 복붙 프롬프트

---

## QA 체크리스트 v3

- [ ] 1장은 감도 높은 생성형 인물/제품 이미지로 후킹하는가?
- [ ] 2~5장 중 최소 2장은 Claude/UI/프롬프트/툴 네트워크를 포함하는가?
- [ ] 모든 장이 같은 포스터형으로 반복되지 않는가?
- [ ] 폰트 역할이 분리되어 있는가? 헤드라인/감성/한글/UI/CTA
- [ ] 프롬프트 텍스트는 모노 또는 UI 폰트처럼 보이는가?
- [ ] 텍스트 박스가 설명문 박스가 아니라 UI 장치로 보이는가?
- [ ] Claude를 챗봇이 아니라 coworker/team/agent/workflow로 포지셔닝하는가?
- [ ] 긴 설명 대신 저장 가능한 프롬프트/워크플로우가 있는가?
- [ ] 인물 얼굴을 불필요하게 가리지 않는가?
- [ ] 1px 겹침/침범이 없는가?

---

## 결론

다음 트렌디형은 v2처럼 “에디토리얼 포스터 6장”으로 가면 부족하다. 실제 레퍼런스는 다음 조합이다.

> 생성형 인물 캠페인 컷 + 초대형 감각 타이포 + Claude/프롬프트 UI + 툴 네트워크 + 저장 가능한 프롬프트 템플릿

따라서 다음 제작은 먼저 **A/B/C 방향 커버만 만드는 게 아니라**, 커버 3안과 함께 **내부 슬라이드 형식 보드**까지 같이 만들어야 한다.
