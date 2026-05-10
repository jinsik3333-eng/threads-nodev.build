---
name: nodev-content-loop
description: @nodev.builder Threads/Instagram 콘텐츠 제작 wrapper. Hermes는 브리프/기억/QA, OMX/Codex는 렌더링·파일 작업 실행자.
version: 1.0.0
---

# nodev-content-loop

## 역할

`01_project_threads`에서 인스타 카드뉴스, Threads/Instagram 게시, 리드마그넷, 콘텐츠 자동화 작업을 처리하는 프로젝트 전용 wrapper다.

```text
Hermes = creative PM / memory / skill governance / QA / report
OMX + Codex = renderer / scripts / file operations / implementation
Claude Code = copy/UX/resource review
Gemini = non-sensitive Vision QA / public-reference review
```

## 먼저 읽을 문서

1. `CLAUDE.md`
2. `PROJECT_MAP.md`
3. `PROJECT_STRUCTURE.md`
4. `docs/memory/state.md`
5. `docs/memory/decisions.md`
6. `docs/ops/ai-execution-policy.md`
7. `docs/ops/skill-governance.md`
8. `docs/ops/instagram-production-policy.md`

## 요청 분류

### 카드뉴스/이미지 제작

`docs/ops/instagram-production-policy.md`를 따른다.

- 바로 최종본 금지
- 방향보드/커버 2~3안 먼저
- 사용자 선택 전 전체 확장 금지
- `card_script.json` 필수
- 이미지 모델은 텍스트 없는 asset만
- 텍스트/레이아웃은 renderer 담당
- contact sheet + Vision QA 필수
- ZIP 생성/보관 금지. 최종 PNG를 직접 사용

권장 실행:

```bash
omx exec -C /Users/jinsik/Desktop/Workspace/01_project_threads "<card_script/render/png export task packet>"
```

### 콘텐츠 전략/게시 문안

- `docs/memory/state.md`, `docs/memory/decisions.md`를 우선한다.
- Instagram 메인, Threads 보조 전략을 따른다.
- 초기 계정 신뢰도 보호: 과도한 자동화/링크 반복 금지.

### 자동화 코드

- 공식 Meta Graph API만 사용한다.
- Instagram/Threads 토큰은 별도다.
- 로컬 파일/큐 상태를 라이브 게시 증거로 말하지 않는다.
- 민감정보는 출력하지 않는다.

## 보고

짧게:

- 만든 파일/이미지
- QA 결과
- 사용자 선택 필요 여부
- 다음 액션
