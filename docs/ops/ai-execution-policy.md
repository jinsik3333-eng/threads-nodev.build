# AI 실행 정책 — nodev.builder / Threads·Instagram

Updated: 2026-05-08

## 목적

`01_project_threads`에서 Hermes의 기억/스킬/검증 장점은 유지하되, 실제 콘텐츠 렌더링·파일 작업·자동화 구현은 OMX/Codex 중심으로 빠르게 실행한다.

```text
Hermes = PM / memory / creative brief / skill governance / QA / report
OMX + Codex = renderer, file loop, automation implementation
Claude Code = UX/copy/architecture review when needed
Gemini = non-sensitive long-context / contact-sheet Vision QA
```

## 기본 라우팅

### Hermes가 직접 처리

- 계정/채널 전략, 제작 브리프, 금지사항, 실패 사례 관리
- `CLAUDE.md`, `PROJECT_MAP.md`, `PROJECT_STRUCTURE.md`, `docs/memory/*` 기반 작업 범위 설정
- 카드뉴스 방향 선택 게이트와 QA 기준 관리
- 결과물 readback, contact sheet/Vision QA, 짧은 보고
- 진행 상태는 `docs/memory/state.md`나 작업 폴더 문서에 남긴다.

### OMX/Codex에 위임

- `card_script.json` 작성/검증
- PIL/HTML/Playwright renderer 구현/수정
- 이미지/카드 export, contact sheet 생성
- app/src 자동화 코드 수정/테스트

권장 패턴:

```bash
omx exec -C /Users/jinsik/Desktop/Workspace/01_project_threads "<작고 구체적인 task packet>"
```

### Claude/Gemini 사용

- Claude: 카피/구조/리드마그넷/가이드 품질 리뷰
- Gemini: 공개 자료 요약, contact sheet/스크린샷 비전 QA
- 비공개 토큰, 인증, 내부 PRD, 계정 접근값은 외부 모델에 넘기지 않는다.

## 자동화/플랫폼 안전

- 공식 Meta Graph API만 사용한다.
- Instagram과 Threads access token은 별도다.
- 새 계정은 신뢰도 보호를 위해 초반 수동 운영 중심.
- ManyChat 키워드 DM은 초기 검증용으로 우선한다.
- 라이브 게시 검증은 로컬 파일/큐만으로 단정하지 않는다.
