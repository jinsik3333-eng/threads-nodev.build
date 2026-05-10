# 비개발dev — Threads/Instagram 자동화 프로젝트

> @nodev.builder — Claude Code로 업무 도구를 직접 만드는 비개발자 서사

## 폴더 구조 핵심

이 프로젝트는 컨텍스트 오염을 줄이기 위해 코드와 콘텐츠를 분리한다.

```text
01_project_threads/
├── app/                  # 실행 코드 전용
│   ├── src/              # Meta/Threads/Instagram API 모듈
│   ├── scripts/          # CLI 진입점
│   ├── tests/            # 단위 테스트
│   └── state/            # 로컬 큐/응답 상태
├── content/              # 인스타 콘텐츠 제작 공간
│   ├── cardnews/         # 날짜별 최종 카드뉴스
│   └── characters/       # 공식 캐릭터 이미지
├── guides/               # 실제 배포용 HTML 리드마그넷
├── docs/                 # 운영 문서/메모리/결정 기록
├── assets/               # 브랜드 이미지
└── PROJECT_STRUCTURE.md  # 상세 폴더 규칙
```

작업 전에는 `PROJECT_STRUCTURE.md`와 `PROJECT_MAP.md`를 먼저 확인한다.

## 빠른 시작

```bash
# 로컬 테스트
cd app && python3 -m pytest tests/ -v

# 발행 스크립트 예시
cd app && python scripts/publish.py
```

## 메모리 3계층

| 계층 | 위치 | 용도 |
|------|------|------|
| 영구 기록 | `docs/memory/` | 사람이 읽는 결정/교훈/상태 |
| AI 컨텍스트 | Hermes memory 도구 | 에이전트 세션 간 핵심 정보 |
| 동기화 미러 | `.hermes-sync/` | memory 도구 파일 미러 |

## 계정 정지 방지 규칙

| # | 규칙 | 이유 |
|---|------|------|
| 1 | 링크 5회 중 1회만 포함 | 스팸 시그널 회피 |
| 2 | 답글 간격 30~180초 랜덤 | 봇 패턴 회피 |
| 3 | 매번 Claude로 새 답글 생성 | 템플릿 반복 회피 |
| 4 | 하루 2~3회, 상위 5개만 | 과도한 활동 회피 |
| 5 | Hermes cronjob 사용 | launchd 의존 제거 |
| 6 | API 간격 1시간 이상 | rate limit 준수 |

## 컨텍스트 로딩 원칙

- 코드 작업: `app/src`, `app/scripts`, `app/tests`만 우선.
- 카드뉴스 작업: 해당 `content/cardnews/{episode}`만 우선.
- 리드마그넷 작업: `guides/`와 관련 게시글 파일만 우선.
- 전체 이미지 폴더는 한 번에 읽지 않는다.
