# Adriana 스타일 image2-high 카드뉴스 제작 계획

**Goal:** `비개발dev` 인스타그램용 Adriana Bubori 스타일 카드뉴스 6장을 image2-high 배경 이미지와 HTML 조판으로 제작한다.

**Style Direction:** 프리미엄 매거진/브랜드 광고형 AI 콘텐츠. AI/Claude를 기술 정보가 아니라 1인 사업가·크리에이터의 라이프스타일 생산성으로 포장한다.

**Output Path:** `/Users/jinsik/Desktop/Workspace/01_project_threads/app/cards/episodes/20260501_adriana-ai-creative-team/`

---

## 콘텐츠 콘셉트

주제: **Claude로 나만의 콘텐츠 팀 만들기**

핵심 후킹:
- 커버: `혼자 일하지만 팀처럼 보이는 법`
- 서브 메시지: `Claude를 비서가 아니라 크리에이티브 팀으로 쓰기`
- CTA: `댓글에 “팀” 남기면 워크플로우 보내드립니다`

## 카드 구성

1. **Cover** — 혼자 일하지만 팀처럼 보이는 법
2. **Problem** — 콘텐츠 만들 때 제일 힘든 건 아이디어가 아니라 반복이다
3. **Reframe** — Claude는 챗봇이 아니라 역할을 나눈 팀처럼 써야 한다
4. **Workflow** — 기획자 / 카피라이터 / 디자이너 / 편집장 역할 분리
5. **Result** — 1개 아이디어가 포스트·카드뉴스·릴스 대본으로 확장된다
6. **CTA** — 댓글에 “팀” 남기면 워크플로우 보내드립니다

## 디자인 규칙

- Adriana 스타일: 뉴트럴 베이지/브라운/크림 + 흰색 초대형 타이포 + 작은 캡슐 CTA
- 형광 노랑 금지, 하프던 스타일과 섞지 않기
- image2는 텍스트 없는 hero/background만 생성
- HTML에서 텍스트를 정확히 얹기
- 카드마다 이미지 전체를 배경으로 쓰되, 좌측/상단/하단에 타이포 안전 영역 확보
- 1080×1350 PNG 출력

## 실행 루프

1. image_gen provider/model을 `openai-codex` / `gpt-image-2-high`로 설정한다.
2. 공용 미디어킷 레퍼런스에서 poster/ad-creative 패턴을 확인한다.
3. image2-high로 텍스트 없는 Adriana형 hero 이미지 3장을 만든다.
4. vision으로 여백, 고급감, AI 티, 타이포 얹을 공간을 검수한다.
5. 가장 좋은 이미지를 중심으로 HTML 6장을 조판한다.
6. Playwright로 PNG 렌더링한다.
7. vision으로 최종 카드뉴스를 검수한다.
8. 문제 있으면 HTML/CSS 수정 후 재렌더링한다.
9. Telegram에 결과 PNG와 요약을 전달한다.
