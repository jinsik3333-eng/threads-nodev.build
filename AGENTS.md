# nodev.builder 프로젝트 운영 지침

## 프로젝트 범위

- 이 저장소는 `@nodev.builder` Instagram/Threads 콘텐츠·자동화 작업 전용이다.
- 작업 루트: `/Users/jinsik/Desktop/Workspace/01_project_threads`
- 기존 규칙은 `CLAUDE.md`, `PROJECT_MAP.md`, `PROJECT_STRUCTURE.md`, `docs/memory/*`를 우선한다.
- 모든 사용자 커뮤니케이션과 문서는 한국어를 기본으로 한다.

## 먼저 읽을 것

1. `CLAUDE.md`
2. `PROJECT_MAP.md`
3. `PROJECT_STRUCTURE.md`
4. `docs/memory/state.md`
5. `docs/memory/decisions.md`
6. 작업이 카드뉴스/이미지면 `docs/ops/instagram-production-policy.md`
7. 자동화/코드 작업이면 `docs/ops/ai-execution-policy.md`

## AI 실행 정책

- Hermes는 PM/메모리/스킬 관리/브리프/QA/보고를 담당한다.
- OMX/Codex는 렌더링, 파일 루프, 자동화 코드 구현의 메인 실행자다.
- Claude Code는 카피/UX/리드마그넷/아키텍처 리뷰에 선택적으로 사용한다.
- Gemini는 비민감 long-context와 contact-sheet Vision QA에만 사용한다.
- 상세 기준은 `docs/ops/ai-execution-policy.md`를 따른다.
- 스킬 추가/활성화 기준은 `docs/ops/skill-governance.md`를 따른다.

## 카드뉴스/이미지 제작 규칙

- 바로 최종 덱을 만들지 않는다.
- 방향보드/커버 2~3안 → 사용자 선택 → `card_script.json` → renderer → contact sheet QA → 최종 export 순서를 따른다.
- 이미지 모델에게 한국어 텍스트와 최종 레이아웃을 맡기지 않는다.
- 공식 캐릭터는 필요할 때만 `content/characters/nodev-builder/reference-locked-20/`에서 확인한다.
- `character_asset_set_20`은 폐기본이라 사용/복구하지 않는다.

## 플랫폼 안전

- 공식 Meta Graph API만 사용한다.
- Instagram을 메인, Threads를 보조 채널로 본다.
- 초기 계정은 수동 운영과 안전한 간격을 우선한다.
- 라이브 게시 검증은 로컬 파일/큐만으로 단정하지 않는다.
