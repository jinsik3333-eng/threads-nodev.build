# 비개발dev 프로젝트 맵

> 목적: 다음 세션에서 필요한 컨텍스트만 빠르게 읽기 위한 최소 지도.

## 먼저 읽을 파일

1. `CLAUDE.md` — 프로젝트 기본 규칙
2. `docs/memory/state.md` — 현재 운영 상태
3. `docs/memory/decisions.md` — 중요한 결정
4. `docs/memory/cleanup-20260505.md` — 2026-05-05 산출물 정리 기록

## 활성 작업 영역

### 코드

- `app/src/` — Threads/Instagram/Meta API 관련 핵심 모듈
- `app/scripts/` — CLI 실행 스크립트
- `app/tests/` — 테스트
- `app/state/` — 로컬 실행 상태. 민감/자동생성 파일은 Git/context 대상 아님

### 콘텐츠

- `app/posts/` — 게시글 문안/업로드 계획
- `guides/` — 실제 가이드 HTML/리소스
- `docs/` — 의사결정, 운영 메모리, 기획/디자인 문서

### 카드/영상 소스

- `app/cards/episodes/` — 카드뉴스 에피소드별 소스/스크립트/문안만 유지
- `app/cards/templates/` — 카드 템플릿
- `app/cards/layout-templates/` — 레이아웃 템플릿 소스
- `app/videos/*/render*.py` — 영상 재생성 스크립트
- `app/videos/*/captions-and-post-copy.md` — 업로드 문안

## 프로젝트 안에 두지 않는 것

아래는 컨텍스트와 용량을 많이 먹기 때문에 기본적으로 프로젝트 밖 아카이브로 이동한다.

- 렌더링 중간 프레임: `frames*/`
- Chrome/Playwright 임시 프로필: `chrome-profile/`, `chrome-cdp-profile/`
- 실패한 영상 버전 `.mp4`
- 카드뉴스 렌더 결과 `.png`, `.jpg`, `.zip`
- 실험 폴더: `app/cards/experiments/`
- 일회성 출력 폴더: `app/outputs/`

현재 아카이브 위치:

`/Users/jinsik/Desktop/Workspace/01_project_threads_archive_cleanup_20260505`

## 운영 원칙

- 활성 프로젝트에는 “소스, 문안, 결정 기록, 재현 스크립트”만 둔다.
- 이미지/영상 결과물은 업로드 직전 또는 검수 중에만 만들고, 끝나면 프로젝트 밖으로 이동한다.
- 다음 이미지/영상 작업 시 최종본만 명시적으로 보존하고 실패 버전은 남기지 않는다.
- 인스타/카드뉴스는 실제 레퍼런스 분석과 사용자 선택을 우선한다.
- @nodev.builder 영상은 AI 편집 그래픽보다 실제 가이드 스크롤형을 우선한다.
