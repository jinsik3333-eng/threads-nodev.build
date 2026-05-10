# 📋 결정 기록

## 2026-04-26

### D001: Hermes 기반 재구축
- **결정**: 기존 launchd 기반 자동화를 Hermes cronjob 기반으로 전환
- **이유**: launchd 의존성 제거, 자연어 제어 가능, 로깅 통합
- **영향**: launchd plist 제거, Hermes `threads` 프로필 생성

### D002: 계정 정지 원인 분석 기반 규칙
- **결정**: 6가지 안전 규칙 적용 (링크 제한, 랜덤 간격, Claude 답글 등)
- **이유**: 2회 계정 정지 경험 — 패턴 매칭이 주 원인
- **규칙**: [README 참조](../README.md)

### D003: app/docs 구조 분리
- **결정**: community_app과 동일한 구조로 통일
- **이유**: 프로젝트 간 일관성, 코드/문서 관심사 분리

### D004: 4채널 통합 메모리
- **결정**: 텔레그램·Hermes CLI·Claude Code CLI·Paperclip 4개 채널에서 동일 메모리 공유
- **방식**: docs/memory/ (마크다운) ← 모든 채널의 공통 진실 공급원
- **영향**: CLAUDE.md에 docs/memory/ 참조 추가, Paperclip 이슈↔로컬 문서 양방향 링크

### D005: Instagram 메인 + Threads 보조 전략 (2026-04-26)
- **결정**: Instagram을 메인 플랫폼, Threads를 보조 자동화 채널로 재편
- **이유**: 2회 계정 정지 경험 — 단일 플랫폼 의존도가 리스크. Instagram이 더 큰 오디언스 풀과 콘텐츠 다양성 제공
- **방식**: 공식 Meta Graph API만 사용 (graph.instagram.com + graph.threads.net). 비공식 크롤링 일체 배제
- **영향**: 코드베이스를 멀티 플랫폼으로 재구축 (meta_client.py, instagram.py, threads.py, generator.py, publisher.py, responder.py)

### D006: Instagram 토큰 별도 발급 (2026-04-26)
- **결정**: Instagram과 Threads API에 각각 별도 access token 사용
- **이유**: Meta Graph API 구조상 같은 App 아래에서도 서로 다른 제품군은 별도 인증 필요. 하나의 토큰으로 두 API 호출 불가
- **영향**: .env에 THREADS_ACCESS_TOKEN + INSTAGRAM_ACCESS_TOKEN 분리 관리 필요

### D007: 코드와 콘텐츠 제작 공간 분리 (2026-05-06)
- **결정**: `app/`은 실행 코드 전용으로 축소하고, 인스타 카드뉴스/포스트/레퍼런스/기획서는 `content/`로 이동
- **이유**: 카드뉴스 시안, 레퍼런스 DB, 출력물, 포스트 기획서가 `app/`에 섞여 에이전트 컨텍스트가 오염됨
- **구조**: `content/characters/nodev-builder/`, `content/cardnews/YYYY-MM-DD-title/`
- **원칙**: 카드뉴스 작업 시 해당 날짜별 카드뉴스 폴더만 먼저 읽고, 캐릭터가 필요할 때만 `content/characters/nodev-builder/reference-locked-20/`를 읽는다. 게시 텍스트는 해당 카드뉴스 폴더 안에 함께 둔다.
- **상세**: `PROJECT_STRUCTURE.md` 참조

### D008: 콘텐츠 폴더 단순화 (2026-05-06)
- **결정**: 이전 `content/instagram/cards/active/archive/posts`, `content/references`, `content/planning` 구조를 폐기하고 `characters`, `cardnews` 중심으로 단순화
- **이유**: 날짜/active/archive/episodes 단계가 많아 사용자가 보기 어렵고 에이전트도 빠르게 접근하기 어려움
- **베스트 케이스**: `content/cardnews/2026-05-04-character-best/`
- **폐기본**: `character_asset_set_20`은 사용/복구 금지

### D009: Hermes PM / OMX 실행 분리와 인스타 제작 게이트 (2026-05-08)
- **결정**: Hermes는 브리프/메모리/스킬/QA를 맡고, 실제 렌더링·파일 작업·자동화 구현은 OMX/Codex가 맡는다.
- **이유**: Hermes가 직접 긴 이미지 제작 루프를 수행하면 느리고, 브리프 오해/캐릭터 삽입 실패/레이아웃 실패가 반복됨.
- **방식**: `docs/ops/instagram-production-policy.md`에 방향보드 → 사용자 선택 → `card_script.json` → renderer → contact sheet QA → 최종 export 게이트를 고정.
- **영향**: 프로젝트 wrapper `.codex/skills/nodev-content-loop/SKILL.md` 사용. 세부 실패 사례는 새 micro-skill이 아니라 reference/정책 문서에 흡수.

### D010: 최종 산출물 중심 콘텐츠 폴더 정리 (2026-05-08)
- **결정**: 실제 게시에 쓰는 카드 이미지/캡션/공식 캐릭터만 남기고, 대체 시안·backup·템플릿 실험본·카드뉴스별 Python 렌더러·ZIP을 삭제한다.
- **이유**: 인스타 게시글 2개와 Threads 몇 개뿐인데 제작 중간 산출물이 많아 폴더와 에이전트 컨텍스트가 과도하게 커짐.
- **방식**: 업로드는 `images/card-*.png`를 직접 사용하고 ZIP은 만들거나 보관하지 않는다. 렌더러가 필요하면 해당 작업 범위에서 임시로 만들고 최종 산출 후 삭제한다.
- **영향**: `content/workflows/` 삭제. `content/cardnews/`와 `content/characters/nodev-builder/reference-locked-20/` 중심으로 단순화.

### D014: 잘못 만든 템플릿 전량 폐기 및 캐릭터 기준 복원 (2026-05-08)
- **결정**: `content/templates/` 아래에서 생성했던 모든 템플릿을 삭제한다.
- **이유**: 사용자가 원한 것은 기존 `content/characters/` 캐릭터의 귀여운 3D 외형을 유지하면서 카드뉴스용 텍스트/말풍선 틀로 확장하는 것이었는데, 새 시안들은 캐릭터 외형이 사라지거나 달라짐.
- **방식**: 기존 캐릭터 원본 `content/characters/`는 보존한다. 이후 템플릿화는 기존 캐릭터 외형/정체성을 유지하는 방향에서만 진행한다.
- **영향**: `nodev-clean-character-system-30`, `nodev-3d-object-textbox-30`, `nodev-scene-textbox-30`, `nodev-character-textbox-30` 모두 폐기 기준으로 기록한다.


### D015: 기존 캐릭터 기반 카드뉴스 템플릿 30종 재생성 (2026-05-08)
- **결정**: `content/templates/nodev-original-character-cardnews-30/`를 active 템플릿 세트로 둔다.
- **이유**: 사용자는 기존 귀여운 3D 캐릭터 외형은 유지하되, 카드뉴스 안에서 제목/본문/말풍선/CTA 텍스트 영역이 명확한 반복 사용 틀을 원했다.
- **방식**: `content/characters/nodev-builder/reference-locked-20/` 캐릭터 이미지를 템플릿의 의도된 캐릭터 영역에 배치하고, 2차 포스팅처럼 단순한 배경과 고정된 텍스트 박스 구조를 사용한다.
- **검증**: PNG 30개, 전부 1080x1350, ZIP/Python/cache 없음. `manifest.json`과 contact sheet 4종을 함께 둔다.
