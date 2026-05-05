# Card Script JSON Pipeline — 2026-05-02

## 목적

카드뉴스 제작을 `감으로 바로 렌더링`하지 않고, 아래 중간 스키마를 거치게 한다.

```text
reference research
→ structural storyboard.md
→ card_script.json
→ template renderer
→ PNG/contact sheet
→ vision QA
→ patch
```

이 문서의 핵심은 **스토리보드와 렌더링 코드 사이에 사람이 검토 가능한 JSON 계약을 두는 것**이다.

---

## 왜 필요한가

기존 문제:
- JS 렌더 파일 안에 카피, 역할, 레이아웃, QA 기준이 섞임.
- 05번처럼 `도구 네트워크인지 / 프로세스인지 / 스토리보드인지`가 흐려질 수 있음.
- 디자인 수정 때 구조적 이유보다 위치값 패치에 매몰됨.

새 방식:
- 각 슬라이드가 먼저 `role`, `template_id`, `message`, `image_role`, `element_jobs`를 가진다.
- 렌더러는 이 계약을 시각화한다.
- QA는 계약 대비 실패 여부를 본다.

---

## 파일 위치 규칙

권장 폴더:

```text
app/cards/episodes/{YYYYMMDD_slug}/
├── storyboard.md
├── card_script.json
├── render.js
├── output/
│   ├── card-01.png
│   ├── ...
│   └── contact-sheet.png
└── qa-report.md
```

템플릿/스키마 공용 자산:

```text
app/cards/templates/
├── card-script.schema.json
├── template-registry.json
└── validate-card-script.mjs
```

---

## card_script.json 최상위 구조

```json
{
  "version": "1.0.0",
  "project": "nodev-builder",
  "format": {
    "width": 1080,
    "height": 1350,
    "platform": "instagram-carousel"
  },
  "style_profile": "trendy-mec-adriana-kr",
  "brand": {
    "account_name": "NODEV BUILDER",
    "account_position": "top-center",
    "required_on_all_slides": true
  },
  "font_policy": {
    "headline": "SUIT ExtraBold",
    "body": "Pretendard SemiBold",
    "ui": "IBM Plex Sans KR or mono",
    "min_readable_px": 22
  },
  "global_qa_rules": [
    "no_unintentional_overlap_1px",
    "small_text_must_be_readable_on_mobile",
    "each_element_must_have_job",
    "no_repeated_hero_image_without_reason",
    "korean_copy_must_be_semantic_two_line_when_possible"
  ],
  "slides": []
}
```

---

## slide 객체 필드

### 필수 필드

```json
{
  "slide_id": "01",
  "role": "cover_hook",
  "template_id": "T01_CAMPAIGN_HERO",
  "message": "콘텐츠 30일치를 Claude가 짜준다는 결과 약속",
  "headline": ["콘텐츠 30일치", "Claude가 짜줌"],
  "support_copy": "",
  "image_role": "desire_hook",
  "visual_direction": "premium human campaign image, bright editorial tone",
  "elements": [],
  "qa_rules": []
}
```

### 필드 정의

- `slide_id`
  - `01`, `02` 같은 문자열.
- `role`
  - 슬라이드의 서사 역할.
  - 예: `cover_hook`, `campaign_bridge`, `prompt_setup`, `generated_assets`, `storyboard_preview`, `final_cta`.
- `template_id`
  - 템플릿 레지스트리의 ID.
  - 예: `T01_CAMPAIGN_HERO`, `T06_STORYBOARD_PREVIEW`, `T11_FULL_IMAGE_BREAKER`.
- `message`
  - 이 장이 전달해야 하는 한 문장.
- `headline`
  - 제목 줄 배열. 한국어는 의미 단위 줄바꿈 우선.
- `support_copy`
  - 보조 문장. 없으면 빈 문자열.
- `image_role`
  - 이미지가 하는 일.
  - 허용 예: `none`, `desire_hook`, `proof`, `transition`, `comparison`, `detail_check`, `asset_mockup`, `mood_bridge`.
- `visual_direction`
  - 이미지/레이아웃 톤 설명.
- `elements`
  - 실제 구성요소와 역할.
- `qa_rules`
  - 이 슬라이드에 추가로 적용할 QA.

---

## element 객체

```json
{
  "id": "headline",
  "type": "text",
  "job": "hook_message",
  "content": "콘텐츠 30일치 / Claude가 짜줌",
  "priority": 1,
  "must_be_readable": true,
  "notes": "30일치만 컬러 강조"
}
```

### element.job 허용값

- `brand_identification`
- `hook_message`
- `story_progression`
- `proof_result`
- `content_preview`
- `instruction`
- `comparison_basis`
- `cta_action`
- `visual_rhythm_break`
- `decoration_only`

규칙:
- `decoration_only`는 최소화한다.
- 정보성 요소는 `must_be_readable: true`여야 한다.
- `job`을 설명할 수 없는 요소는 삭제한다.

---

## 권장 role 흐름 — 트렌디형 6장

```text
01 cover_hook
02 campaign_bridge
03 prompt_setup
04 generated_assets
05 storyboard_preview or process_ladder
06 final_cta
```

05번 선택 규칙:
- 구조/흐름이 핵심이면 `T06_STORYBOARD_PREVIEW`.
- 단계 실행이 핵심이면 `T10_PROCESS_LADDER`.
- 중간 리듬 전환이면 `T11_FULL_IMAGE_BREAKER`.
- 결과/품질 증명이 핵심이면 `T12_DETAIL_CLOSEUP_CHECKLIST`.

---

## QA 체크리스트

렌더링 전 JSON 단계에서 확인:

- [ ] 모든 슬라이드에 `role`이 있다.
- [ ] 모든 슬라이드에 `template_id`가 있다.
- [ ] 모든 슬라이드의 `message`가 한 문장으로 명확하다.
- [ ] 이미지가 있는 장은 `image_role`이 `none`이 아니다.
- [ ] `elements`의 모든 항목은 `job`을 가진다.
- [ ] 읽혀야 하는 텍스트는 `must_be_readable: true`다.
- [ ] 05번은 도구/프로세스/스토리보드가 섞이지 않는다.
- [ ] CTA는 댓글 키워드/DM 자료/팔로우 중 하나 이상을 명확히 요구한다.

렌더링 후 PNG 단계에서 확인:

- [ ] 1px라도 의도치 않은 겹침 없음.
- [ ] 가장 작은 정보성 텍스트가 모바일에서 읽힘.
- [ ] 계정명은 모든 슬라이드 상단 중앙.
- [ ] 이미지가 텍스트를 죽이지 않음.
- [ ] 같은 이미지 반복 없음. 반복 시 이유가 JSON에 명시돼야 함.

---

## 다음 구현 단위

1. `template-registry.json` 생성.
2. `card-script.schema.json` 생성.
3. 샘플 `card_script.json` 생성.
4. `validate-card-script.mjs`로 구조 검증.
5. 기존 v8/v9 렌더러가 `card_script.json`을 읽도록 점진 전환.
