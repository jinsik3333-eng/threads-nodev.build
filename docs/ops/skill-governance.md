# Skill Governance — nodev.builder / Threads·Instagram

Updated: 2026-05-08

## 목적

카드뉴스/소셜 자동화 작업에서 스킬과 레퍼런스가 과도하게 늘어나 컨텍스트가 오염되는 것을 막는다.

## 분류

### Active skill

자동 적용 대상. 최소화한다.

- Hermes 전역: `instagram-card-news`, `social-platform-automation`, `omx-hermes-orchestration`, `codex`, `claude-code`, `multimodel-session-end`
- 프로젝트 wrapper: `.codex/skills/nodev-content-loop/SKILL.md`

### Reference

필요할 때만 읽는다.

- `docs/memory/*`
- `PROJECT_MAP.md`, `PROJECT_STRUCTURE.md`
- `content/characters/nodev-builder/reference-locked-20/`
- `content/cardnews/<episode>/`
- `content/templates/nodev-original-character-cardnews-30/`
- `content/characters/`
- Hermes `instagram-card-news`의 references

### Archive

과거 실패본/폐기본. 자동 발동 금지.

- `character_asset_set_20`은 폐기본이며 사용/복구 금지.
- 대량 삭제된 legacy `app/cards`, `app/posts`, `app/references` 파일은 현재 active context로 복원하지 않는다.
- 삭제된 `content/workflows`, 대체 시안, backup, ZIP은 복원하지 않는다.

## 운영 원칙

1. 프로젝트 wrapper는 `nodev-content-loop` 1개만 유지한다.
2. 카드뉴스/이미지 실패 사례는 새 skill로 쪼개지 말고 `instagram-production-policy.md`나 Hermes `instagram-card-news` reference에 흡수한다.
3. 자동 발동 skill을 여러 개 붙이지 않는다. `nodev-content-loop`가 상황별로 reference를 선택한다.
4. 진행 상태는 Hermes memory가 아니라 `docs/memory/state.md`, 해당 episode `notes.md`, `caption-and-posting.md`에 남긴다.
5. 민감한 계정/API 정보는 memory·문서·프롬프트에 쓰지 않는다.
