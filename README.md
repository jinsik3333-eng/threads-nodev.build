# 비개발dev — Threads 자동화 프로젝트

> @nodev.build — Claude Code로 업무 도구 직접 만드는 비개발자 서사

## 📁 디렉토리 구조

```
01_project_threads/
├── app/                  ← 자동화 소스코드 (Python)
│   ├── src/              ← 핵심 모듈
│   │   ├── threads_client.py  ← Threads API
│   │   ├── generator.py       ← Claude 포스트 생성
│   │   ├── publisher.py       ← 발행 큐 관리
│   │   └── responder.py       ← 댓글 자동 응답
│   ├── scripts/          ← CLI 진입점
│   ├── tests/            ← 단위 테스트
│   └── state/            ← replied.json, queue.json
├── docs/                 ← 프로젝트 문서
│   ├── memory/           ← 결정, 리서치, 교훈
│   ├── hermes/           ← Hermes 연동 설정
│   ├── account/          ← 계정 관리 (비공개)
│   └── sessions/         ← 중요 세션 요약
├── guides/               ← 배포용 HTML 가이드
├── assets/               ← 이미지, 프로필 사진
├── .hermes-sync/         ← Hermes memory 미러
├── .env                  ← API 키 (gitignore)
└── .git/
```

## 🧠 메모리 3계층

| 계층 | 위치 | 용도 |
|------|------|------|
| 📝 영구 기록 | `docs/memory/` | 사람이 읽는 결정/교훈 |
| 🤖 AI 컨텍스트 | Hermes memory 도구 | 에이전트 세션 간 참조 |
| 🔄 동기화 미러 | `.hermes-sync/` | memory 도구 파일 미러 |

## 🛠 개발 도구

| 도구 | 용도 |
|------|------|
| **Hermes Agent** | `threads` 프로필 — AI 운영 어시스턴트 |
| **Threads API** | Meta 공식 API (포스트·댓글·대댓글) |
| **Claude API** | 포스트 생성, 댓글 답변 생성 |

## 🚀 빠른 시작

```bash
threads chat                  # Hermes 프로필 대화
threads config edit           # 설정 편집

# 로컬 테스트
cd app && python scripts/publish.py
cd app && python -m pytest tests/ -v
```

## 🚨 계정 정지 방지 규칙

| # | 규칙 | 이유 |
|---|------|------|
| 1 | 링크 5회 중 1회만 포함 | 스팸 시그널 회피 |
| 2 | 답글 간격 30~180초 랜덤 | 봇 패턴 회피 |
| 3 | 매번 Claude로 새 답글 생성 | 템플릿 반복 회피 |
| 4 | 하루 2~3회, 상위 5개만 | 과도한 활동 회피 |
| 5 | Hermes cronjob 사용 | launchd 탐지 회피 |
| 6 | API 간격 1시간 이상 | rate limit 준수 |

## 📋 진행 상황

| 상태 | 항목 |
|------|------|
| ✅ | 프로젝트 구조 재구성 (Hermes 통합) |
| ✅ | 자동화 코드 보존 (app/ 이관) |
| ⏳ | 새 계정 생성 (진행 예정) |
| ⏳ | Hermes cronjob 설정 |
| ⏳ | 안전한 자동화 패턴 적용 |