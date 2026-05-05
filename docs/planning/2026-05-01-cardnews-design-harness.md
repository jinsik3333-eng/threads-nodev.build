# 카드뉴스 디자인 하네스 v1

## 목적
카드뉴스를 만들 때 Hermes의 즉흥 미감에 맡기지 않고, 생성 전/중/후를 통과 기준으로 묶는다. 이 하네스는 특히 `폰트`, `후킹 이미지`, `레이아웃`을 평가한다.

## 전체 파이프라인

```text
Brief
→ Reference Intake
→ Direction Lock
→ Image Candidate Gate
→ Typography Gate
→ Layout Gate
→ Cover A/B/C Render
→ Vision Critique
→ User Pick
→ Carousel Expansion
→ Final QA
```

## 0. 금지 원칙

- 6장을 바로 만들지 않는다.
- 예쁜 배경 1장만 보고 전체 디자인을 확정하지 않는다.
- 둥근 박스/글래스모피즘으로 위계를 때우지 않는다.
- 한글 제목을 무조건 900 weight로 키우지 않는다.
- Adriana형과 Halfdoneclub형을 섞지 않는다.
- 비전 검수 없이 최종이라고 말하지 않는다.

---

## 1. Brief 입력 스키마

매 작업 시작 시 아래를 먼저 채운다.

```yaml
topic: "혼자 일하지만 팀처럼 보이는 법"
audience: "비개발자 직장인 / 1인 크리에이터"
primary_emotion: "나도 저렇게 일하고 싶다"
style_family: "adriana-premium | adriana-ad | halfdone-dark"
content_type: "cover-only | carousel-6"
cta: "댓글에 팀 남기면 워크플로우 보내드립니다"
forbidden: ["형광 노랑", "과한 박스", "가짜 UI 텍스트", "로고 남발"]
```

---

## 2. Reference Intake 하네스

레퍼런스 3개 이상을 보고 아래 표를 채운다.

```yaml
reference:
  account: "@adrianabubori"
  post_type: "cover / carousel / reel cover"
  first_second_hook: "무엇이 먼저 보이는가"
  image_subject: "인물 / 책상 / 제품 / 화면 / 공간 / 손 / 결과물"
  image_job: "장식 / 증거 / 욕망 / 대비 / 스토리"
  headline_position: "top-left / center / bottom / overlap"
  headline_type: "serif / sans / mixed"
  headline_weight: "light / regular / bold / black"
  layout_pattern: "magazine-cover / ad-poster / quote-editorial / split-grid"
  cta_treatment: "caption / capsule / button / none"
  why_it_hooks: "클릭하고 싶게 만드는 이유"
```

통과 기준:
- `why_it_hooks`를 말로 설명하지 못하면 아직 따라 만들면 안 된다.
- 표면 요소가 아니라 `image_job`이 명확해야 한다.

---

## 3. 이미지 후보 게이트

image2 또는 스톡/스크린샷 후보는 최소 3개를 만든다.
각 후보는 아래 점수로 평가한다.

```yaml
image_candidate:
  path: "...png"
  hook_score: 0        # 클릭 욕망/궁금증
  subject_score: 0     # 주제와 직접 연결되는가
  text_space_score: 0  # 제목 얹을 여백
  premium_score: 0     # 고급감
  ai_artifact_score: 0 # AI 티가 적을수록 높음
  contrast_score: 0    # 글자 대비 확보 가능성
  total: 0
  verdict: "use / revise / reject"
```

가중치:
- 후킹성 × 2
- 주제 적합성 × 2
- 텍스트 안전영역 × 1.5
- 고급감 × 1
- AI 티 × 1
- 대비 × 1

자동 탈락:
- 가짜 글자가 선명함
- 손/얼굴/노트북 키보드 왜곡이 눈에 띔
- 제목 넣을 공간이 없음
- 예쁘지만 주제와 무관함
- 이미지 안의 소품이 너무 많아 1초 후킹이 흐림

Adriana형 좋은 이미지 조건:
- 결과를 상상하게 하는 장면
- 작업/브랜드/콘텐츠 생산의 단서가 있음
- 여백과 오브제가 동시에 있음
- 감성 소품이 아니라 메시지와 연결되는 소품

---

## 4. 타이포그래피 게이트

커버마다 폰트 조합을 최소 3개 비교한다.

```yaml
type_test:
  headline_font: "Pretendard / Apple SD Gothic Neo / Noto Serif KR / ..."
  sub_font: "..."
  headline_size: 0
  headline_weight: 0
  line_height: 0
  letter_spacing: 0
  lines: ["혼자 일하지만", "팀처럼 보이는 법"]
  mobile_readability: 0
  premium_fit: 0
  korean_naturalness: 0
  verdict: "use / revise / reject"
```

통과 기준:
- 제목은 contact sheet 축소 상태에서도 읽혀야 한다.
- 한글 줄바꿈은 의미 단위여야 한다.
- 900 weight는 Halfdoneclub형이 아니면 기본 금지.
- Adriana형은 제목 무게보다 여백/사진/문장 리듬이 먼저다.

폰트 후보:
- Adriana 프리미엄: Apple SD Gothic Neo 700 + Playfair Display 영문 라벨
- Adriana 광고형: Pretendard 700/800 + 넓은 여백
- Editorial: Noto Serif KR 일부 테스트, 단 전통/신문 느낌 나면 탈락
- Halfdoneclub: Pretendard 900 + JetBrains Mono 라벨

---

## 5. 레이아웃 게이트

커버는 아래 4개 문법 중 하나를 명시적으로 선택한다.

### A. Magazine Cover
- 여백 40~60%
- 제목 2~3줄
- 사진은 분위기+욕망
- CTA는 작게
- 박스 거의 없음

### B. Brand Ad Poster
- 사진 주인공 60~70%
- 제목이 사진 일부를 덮음
- 작은 캡슐/로고처럼 CTA
- 설명문 최소화

### C. Editorial Quote
- 한 문장 중심
- 얇은 라인, 작은 캡션
- 여백과 리듬으로 설득
- 정보 박스 없음

### D. Dark Tech Thumbnail
- 강한 제목 1문장
- 강조 단어 1개 색 처리
- 인물/제품/로고/화면 중 하나를 크게
- 하단 정보보다 첫 후킹 우선

레이아웃 평가:
```yaml
layout_test:
  pattern: "Magazine Cover"
  first_read: "처음 읽히는 문장"
  second_read: "두 번째로 읽히는 요소"
  image_read: "이미지가 전달하는 의미"
  cta_read: "CTA가 보이는 방식"
  hierarchy_score: 0
  whitespace_score: 0
  tension_score: 0  # 시선 끌림
  template_smell_score: 0 # 템플릿 냄새 적을수록 높음
  verdict: "use / revise / reject"
```

자동 탈락:
- 모든 요소가 같은 힘으로 보임
- 제목보다 박스가 먼저 보임
- 카드뉴스 템플릿 냄새가 강함
- 여백 없이 꽉 참
- CTA가 광고 배너처럼 튐

---

## 6. 커버 3시안 의무화

6장 확장 전 반드시 커버 3개를 만든다.

```text
cover-a: Adriana Premium Magazine
cover-b: Adriana Brand Ad
cover-c: Halfdone Dark Tech 비교안
```

각 시안 산출물:
- `cover-a.html/png`
- `cover-b.html/png`
- `cover-c.html/png`
- `cover-contact-sheet.png`
- `cover-evaluation.md`

사용자에게 보여줄 때는 반드시 아래를 포함한다.

```text
A안: 장점 / 약점 / 언제 쓰면 좋은지
B안: 장점 / 약점 / 언제 쓰면 좋은지
C안: 장점 / 약점 / 언제 쓰면 좋은지
내 추천: X안, 이유 3가지
```

---

## 7. Vision Critique 프롬프트

### 커버 검수 프롬프트

```text
이 3개 인스타 카드뉴스 커버를 비교 검수해줘.
기준:
1. 첫 1초 후킹력
2. 한글 제목 가독성
3. 폰트의 고급감/촌스러움
4. 배경 이미지가 주제와 연결되는 정도
5. 레이아웃 위계
6. Adriana/Halfdone 스타일 적합성
7. 템플릿 냄새 여부
각 안을 10점 만점으로 평가하고, 가장 게시 가능성이 높은 안과 이유를 말해줘.
```

### 6장 검수 프롬프트

```text
이 6장 카드뉴스를 검수해줘.
기준:
1. 커버에서 약속한 후킹이 2~6장까지 이어지는가
2. 스타일 일관성
3. 폰트 위계
4. 정보 밀도
5. 이미지/배경 반복 피로도
6. CTA 자연스러움
7. 모바일 가독성
8. 촌스러운 요소
치명적 문제와 수정 우선순위 TOP 5를 말해줘.
```

---

## 8. 최종 QA 체크리스트

- [ ] 1080×1350 정확
- [ ] contact sheet 생성
- [ ] 커버 3시안 비교 완료
- [ ] 사용자가 방향 선택 또는 내가 명확한 추천 제시
- [ ] 제목이 축소 상태에서도 읽힘
- [ ] 배경 이미지가 주제의 욕망/결과/증거 중 하나를 담당함
- [ ] 박스가 위계의 주 수단이 아님
- [ ] CTA가 스타일을 깨지 않음
- [ ] vision 검수 1회 이상
- [ ] 수정 루프 1회 이상

---

## 다음 적용 작업

현재 `20260501_adriana-ai-creative-team` 6장 전체를 바로 고치지 말고, 먼저 커버 3시안만 다시 만든다.

주제:
`혼자 일하지만 팀처럼 보이는 법`

목표:
- 폰트 하네스 통과
- 이미지 후보 게이트 통과
- 레이아웃 게이트 통과
- 사용자 선택 후 6장 확장
