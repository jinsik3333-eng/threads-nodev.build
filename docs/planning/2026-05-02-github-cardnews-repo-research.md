# GitHub 카드뉴스 제작 레포 리서치 — 2026-05-02

## 목적

한국어 카드뉴스/인스타 캐러셀 제작에 참고할 수 있는 공개 GitHub 레포를 찾고, 우리 파이프라인에 가져올만한 구조를 분리한다.

## 검색 쿼리

- `카드뉴스 language:JavaScript`
- `카드뉴스 language:TypeScript`
- `카드뉴스 language:Python`
- `인스타그램 카드뉴스`
- `카드뉴스 생성기`
- `카드뉴스 템플릿 language:TypeScript`
- `인스타 카드 만들기 language:TypeScript`

## 참고 가치가 있는 레포

### 1. fivetaku/content-pipeline

- URL: https://github.com/fivetaku/content-pipeline
- 설명: 주제 하나로 리서치 → 카드뉴스 → 영상까지 자동 생성하는 Claude Code 스킬.
- Stars: 68
- 언어: Python
- 참고 가치:
  - 한국어 카드뉴스 파이프라인 구조가 잘 정리됨.
  - `01-리서치-보고서.md`, `02-카드뉴스-기획서.md`, `card-news.html`, `output.mp4` 식의 산출물 단계 구분이 명확함.
  - 카드뉴스 가이드에 모바일 가독성, 행간, 여백, 본문 2~3줄 제한, 1080×1350 기준 등이 있음.
- 우리 적용:
  - 디자인 품질보다는 `리서치 → 기획서 → 카드뉴스 → 영상화` 전체 파이프라인 참고.
  - 카드뉴스 기획서 포맷을 우리 스토리보드 하네스와 결합 가능.

### 2. leedonwoo2827-ship-it/instagram-cardweaver-canva

- URL: https://github.com/leedonwoo2827-ship-it/instagram-cardweaver-canva
- 설명: 책/교육과정/GitHub 소스 → `card_script.json` → FlowGenie JSON + Canva Bulk CSV + 프리뷰 PNG 생성.
- 언어: JavaScript
- 참고 가치:
  - 8장 인스타 카드뉴스 시리즈를 `card_script.json` 중심으로 조립.
  - `photo-overlay`, `typo-minimal` 같은 템플릿 개념이 있음.
  - Canva Bulk CSV로 넘기는 구조가 실무적.
- 우리 적용:
  - `storyboard.md`와 별도로 `card_script.json` 스키마를 만들면 템플릿 재사용성이 올라감.
  - Canva 연동은 지금 당장 필요 없지만, CSV/JSON 기반 분리 구조는 참고 가치 있음.

### 3. l2juhan/card-news-app

- URL: https://github.com/l2juhan/card-news-app
- 설명: Instagram 카드뉴스 생성/편집/내보내기 Electron 데스크톱 앱.
- 언어: TypeScript
- 참고 가치:
  - 터미널 기반 Claude Code 워크플로우의 한계를 GUI로 보완하려는 방향.
  - 1080×1080 / 1080×1350 프리뷰, PhoneMockup, 편집/내보내기 앱 구조.
  - `SRS.md`, `PLAN.md`, `docs/DESIGN.md` 등 제품화 문서가 있음.
- 우리 적용:
  - 바로 코드 차용보다는, 장기적으로 카드뉴스 QA/템플릿 선택 UI를 만들 때 참고.

### 4. Monkkim/cardnews-agent

- URL: https://github.com/Monkkim/cardnews-agent
- 설명: Pillow 단독 인스타 카드뉴스 PNG 생성기. mono/glow 2가지 스타일.
- 언어: Python
- 참고 가치:
  - PretendardVariable, NotoSansKR 폰트를 직접 포함한 한국어 렌더링 구조.
  - JSON 입력 → PNG 출력 구조.
  - 다크 모노톤 에세이형/독백형 카드뉴스에 적합.
- 우리 적용:
  - 한국어 줄바꿈/하이라이트 태그/로컬 폰트 렌더링 참고.
  - 단, 현재 우리 트렌디형 프리미엄 캠페인과는 스타일이 다름.

### 5. wade8908/lbcc-card-generator

- URL: https://github.com/wade8908/lbcc-card-generator
- 설명: Claude + Gemini Imagen + Playwright 기반 LBCC 인스타그램 카드뉴스 자동화 툴.
- 언어: Python
- 참고 가치:
  - HTML 템플릿이 1080×1350 기준.
  - SUIT + ZEN Serif 조합 사용.
  - hook/body/closing 카드 템플릿 분리.
  - 프롬프트 규칙: 짧고 여백 있는 문장, hook 1장, body 3~6장, closing 1장.
- 우리 적용:
  - 한국어 트렌디형에서 SUIT + 세리프 포인트 조합 검증 참고.
  - hook/body/closing 템플릿 분리 방식 참고.

### 6. MIKA5KR/cardnews-skill

- URL: https://github.com/MIKA5KR/cardnews-skill
- 설명: Claude Code용 인스타그램 마케팅 카드뉴스 자동 기획·작성 스킬.
- 참고 가치:
  - 국내 인스타그램 바이럴용 카드뉴스 카피를 리서치/팩트체크/작성하는 방향.
  - 디자인보다는 기획/카피 스킬에 가까움.
- 우리 적용:
  - 콘텐츠 주제별 타깃/후킹/카피 생성 절차 참고.

### 7. happyhappy82/blinked-cardnews-kit

- URL: https://github.com/happyhappy82/blinked-cardnews-kit
- 설명: 블링크애드 카드뉴스 제작 키트. Pencil 디자인 + Remotion 영상화.
- 언어: TypeScript
- 참고 가치:
  - 1080×1350 정적 PNG + MP4 영상화.
  - 레이아웃 패턴: 상단 63% 이미지, 하단 37% 검정 배경 + 텍스트.
  - 이미지 모션/텍스트 고정 방식이 명확함.
- 우리 적용:
  - 스타일리쉬형에서 중간 전체 이미지/상하분할 템플릿을 영상화할 때 참고.

### 8. 기타 후보

- https://github.com/gor031/cardnews-generator-v2
  - AI 기반 SNS 카드뉴스 제작 도구. Google AI Studio 앱 기반. 디자인 참고보다는 앱 구조 참고.
- https://github.com/boxtvstar/auto-cardnews
  - Next.js 자동 카드뉴스 생성기. 기본 템플릿 구조 확인 후보.
- https://github.com/oh-namgyu/insta-card-maker
  - 3초 카드뉴스 제조기. Before/After 인스타 카드 만들기.
- https://github.com/eogus13/zombiepark-cardnews
  - 특정 브랜드/장소용 인스타 카드뉴스 자동 발행 시스템. 콘텐츠 운영 자동화 참고.
- https://github.com/phamcucvinh/card-news-generator
  - Node.js + Canvas 기반 SNS 카드뉴스 생성기.
- https://github.com/soochul331/sermon-cardnews
  - 설교 원고 → AI 카드뉴스. 긴 원고를 카드로 나누는 구조 참고.

## 현재 결론

공개 레포 중에서 바로 디자인 퀄리티를 가져올만한 완성형은 많지 않다. 대부분 0-star 개인 프로젝트/프로토타입이다. 하지만 구조적으로는 참고할 포인트가 있다.

가져올 것:
- `fivetaku/content-pipeline`: 리서치 → 기획서 → 카드뉴스 → 영상 파이프라인.
- `instagram-cardweaver-canva`: `card_script.json` 중심의 중간 스키마.
- `wade8908/lbcc-card-generator`: SUIT + 세리프, hook/body/closing 분리, 1080×1350 HTML 템플릿.
- `Monkkim/cardnews-agent`: Pretendard/NotoSansKR 기반 한국어 PNG 렌더링과 하이라이트 태그.
- `l2juhan/card-news-app`: 장기적으로 템플릿/QA/프리뷰 GUI 참고.
- `blinked-cardnews-kit`: 상단 이미지 63% + 하단 텍스트 37%, Remotion 영상화.

버릴 것/주의할 것:
- 스타 수가 낮고 실사용 검증이 약한 레포가 많다.
- 디자인 감도 자체는 우리 기준보다 낮을 가능성이 큼.
- 한국어 폰트/줄바꿈/모바일 가독성은 참고하되, 미감은 레퍼런스 기반 하네스에서 다시 검증해야 함.
- 자동화 구조가 좋아도 결과물이 유치하거나 템플릿 티가 나면 채택 금지.

## 우리 파이프라인에 추가할 만한 개선안

1. `card_script.json` 도입
   - 스토리보드와 렌더 코드 사이에 중간 JSON을 둔다.
   - 필드 예시: `slide_id`, `role`, `template_id`, `headline`, `support_copy`, `image_role`, `elements`, `qa_rules`.

2. 템플릿 ID 체계화
   - `T01 Campaign Hero`
   - `T03 Skill Output Mockup`
   - `T06 Storyboard Preview`
   - `T11 Full Image Breaker`
   - 이런 식으로 슬라이드가 템플릿을 참조하게 한다.

3. 한국어 줄바꿈/폰트 하네스 강화
   - SUIT/Pretendard/IBM Plex Sans KR 별도 역할 고정.
   - 1080×1350 기준 최소 22px 규칙 유지.
   - 제목은 의미 단위 2줄 우선.

4. 영상화 가능성 열어두기
   - 카드뉴스 PNG를 Remotion/영상으로 변환할 수 있게 이미지 영역/텍스트 영역을 분리해두면 확장 가능.
