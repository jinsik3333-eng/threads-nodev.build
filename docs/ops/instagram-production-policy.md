# Instagram / Card-news Production Policy — nodev.builder

Updated: 2026-05-08

## 목적

`@nodev.builder` 인스타/카드뉴스 제작에서 Hermes가 느리게 직접 실행하거나, 이미지 모델이 브리프를 오해해 이상한 결과물을 만드는 문제를 줄인다.

핵심:

```text
Hermes = creative director / memory / brief / QA
OMX + Codex = renderer / file loop / PNG export
Image model = textless background, scene, character pose asset only
```

## 절대 규칙

1. 바로 최종 6장 덱을 만들지 않는다.
2. 먼저 방향보드 또는 커버 2~3안만 만든다.
3. 사용자가 방향을 선택하기 전에는 전체 덱으로 확장하지 않는다.
4. `card_script.json` 없이 렌더링하지 않는다.
5. 이미지 모델에게 한국어 텍스트와 최종 레이아웃을 맡기지 않는다.
6. 한국어 텍스트, 박스, 페이지 번호, CTA는 HTML/PIL/renderer가 담당한다.
7. 캐릭터 PNG를 나중에 대충 붙이지 않는다. 캐릭터가 들어갈 이유와 영역이 먼저 있어야 한다.
8. contact sheet + Vision/Gemini QA 전에는 최종본이라고 말하지 않는다.
9. ZIP은 만들거나 보관하지 않는다. 업로드는 최종 PNG를 직접 사용한다.

## 제작 순서

1. Brief gate
   - 목적, 타깃, 슬라이드 수, 톤, 금지 요소, 레퍼런스 계열, CTA 확정
2. Direction board
   - Warm Minimal / Premium Campaign / Dark Briefing 등 2~3안
   - cover-only 또는 template-only
3. User selection
   - 사용자가 고르기 전 확장 금지
4. `card_script.json`
   - slide role, message, visual job, text safe area, character usage 명시
5. OMX/Codex render
   - PIL/HTML/Playwright renderer로 PNG export
6. Asset generation
   - 이미지 모델은 텍스트 없는 배경/장면/pose만 생성
7. QA
   - contact sheet, 개별 risk card, 모바일 가독성, 한국어 줄바꿈, 캐릭터 삽입감, 레퍼런스 문법 확인
8. Patch and final PNG export

## 캐릭터 정책

- 공식 캐릭터는 `content/characters/nodev-builder/reference-locked-20/`를 우선한다.
- 같은 커버 캐릭터 반복은 피한다.
- 본문 슬라이드는 정보 중심이면 캐릭터를 빼도 된다.
- 캐릭터가 필요하면 장면/말풍선/도구/CTA 행동 등 역할을 가진다.
- 상자 안에 가둔 느낌, 스티커처럼 붙은 느낌, opaque 배경이 카드와 어긋난 경우 실패다.

## QA 체크

- 모바일에서 읽히는가?
- 한국어가 자연스럽고 번역투가 아닌가?
- 작은 보조 텍스트가 장식처럼 죽지 않았는가?
- 레퍼런스 문법과 실제 결과가 맞는가?
- 캐릭터가 슬라이드 메시지에 기여하는가?
- 배경/캐릭터/카드 표면이 따로 노는가?
- 동일한 얼굴/포즈가 반복되어 피로하지 않은가?
