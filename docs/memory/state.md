# 📊 현재 상태

> 언제 어디서 보더라도, 이 파일 하나로 현재 상태를 한눈에 파악.

- **최종 업데이트**: 2026-05-08 KST
- **작업자**: Jinsik

## 계정

| 항목 | 상태 |
|------|------|
| 이전 계정 @nodev.build | ❌ 정지 (2회) |
| **새 계정 @nodev.builder** | 🟢 활성 — 수동 운영 중 |
| 첫 포스트 | ✅ 완료 |
| 토큰 발급 | ⏳ 4주차 예정 (5/18~) |
| 체크리스트 | [docs/account/checklist.md](../account/checklist.md) |

## 운영 계획

| 주차 | 기간 | 계획 |
|------|------|------|
| 1주차 | 4/27 ~ 5/3 | 수동 1일 1포스트 (week1-posts.md) |
| 2주차 | 5/4 ~ 5/10 | 수동 2포스트 + 소통 |
| 3~4주차 | 5/11 ~ 5/24 | Meta 앱 생성 → 토큰 발급 |
| 5주차~ | 5/25 ~ | 점진적 자동화 |

## 코드/폴더

| 항목 | 상태 |
|------|------|
| app/src/ (자동화 모듈) | ✅ 코드 전용으로 정리 |
| app/scripts/ (CLI) | ✅ 유지 |
| app/tests/ | ✅ 유지 |
| content/characters/nodev-builder/ | ✅ 캐릭터 이미지 통합 |
| content/cardnews/ | ✅ 날짜별 카드뉴스 통합 |
| content/characters/ | ✅ 기존 캐릭터 외형 유지 필요 |
| content/templates/nodev-original-character-cardnews-30/ | ✅ 기존 캐릭터 외형 유지 카드뉴스 템플릿 30종 |
| content/workflows/ | ❌ 삭제 — 최종 산출 후 임시 렌더러/템플릿/노트는 보관하지 않음 |
| 베스트 케이스 | ✅ content/cardnews/2026-05-04-character-best/ |
| 구조 규칙 | ✅ PROJECT_STRUCTURE.md 갱신 |

## 문서

| 파일 | 상태 |
|------|------|
| state.md (이 파일) | ✅ |
| decisions.md | ✅ D001~D007 |
| architecture.md | ✅ 4채널 |
| PROJECT_STRUCTURE.md | ✅ 폴더/컨텍스트 규칙 |
| PROJECT_MAP.md | ✅ 최신 구조 반영 |
| account/checklist.md | ✅ 업데이트 완료 |

## 다음 할 일

| # | 작업 | 우선순위 |
|---|------|----------|
| 1 | 2번째/3번째 인스타 카드뉴스 최종 검수/업로드 | 🔴 진행 중 |
| 2 | ManyChat/프로필 링크 리드마그넷 연결 점검 | 🟡 필요 |
| 3 | Meta 앱 생성 및 토큰 발급 준비 (5/18~) | 🟢 예정 |
| 4 | 콘텐츠 폴더 구조 규칙 유지 | 🟢 상시 |

## 2026-05-08 운영 정책

- Hermes/OMX 실행 분리 적용: Hermes는 브리프·메모리·스킬·QA, OMX/Codex는 렌더링·파일 작업·자동화 구현.
- 인스타 카드뉴스는 `docs/ops/instagram-production-policy.md`의 방향보드 → 선택 → `card_script.json` → renderer → QA 순서를 따른다.
- 카드뉴스 ZIP은 만들거나 보관하지 않는다. 업로드는 최종 PNG를 직접 사용한다.
- 프로젝트 wrapper: `.codex/skills/nodev-content-loop/SKILL.md`.

## 2026-05-08 템플릿 기준

- 현재 반복 사용 템플릿은 `content/templates/nodev-original-character-cardnews-30/` 하나만 active로 본다.
- 기존 캐릭터 외형은 `content/characters/nodev-builder/reference-locked-20/`를 기준으로 유지한다.
- 템플릿은 1080x1350 PNG 30개이며 ZIP은 만들지 않는다.
