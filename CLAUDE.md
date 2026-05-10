# 비개발dev — Claude Code 프로젝트 컨텍스트

## ⚠️ 중요: 먼저 읽을 것
작업 시작 전에 반드시 아래 문서를 확인하세요:
- `docs/memory/state.md` — 현재 전체 상태 (한눈에 파악)
- `docs/memory/decisions.md` — 주요 결정과 이유
- `docs/memory/lessons.md` — 배운 점/교훈
- `docs/memory/architecture.md` — 4채널 아키텍처

## 프로젝트 정보
- **계정**: 비개발dev (@nodev.build → 새 계정 생성 예정)
- **타깃**: 코딩 경험 없는 비개발자 직장인
- **포지셔닝**: 도구를 "시키는" 사람이 아니라 직접 "만드는" 비개발자 서사
- **채널**: Threads + Instagram

## 디렉토리
```
app/                         ← 실행 코드 전용
├── src/                     ← 핵심 모듈 (threads_client, generator, publisher, responder)
├── scripts/                 ← CLI 진입점 (publish.py, respond.py)
├── tests/                   ← 단위 테스트
└── state/                   ← queue.json
content/                     ← 인스타/카드뉴스/레퍼런스 작업 공간
├── cardnews/                ← 날짜별 최종 카드뉴스
└── characters/              ← 공식 캐릭터 이미지
guides/                      ← 실제 배포용 HTML 리드마그넷
docs/
├── memory/                  ← 결정, 리서치, 교훈, 상태, 아키텍처
├── account/                 ← 계정 생성 체크리스트
└── hermes/                  ← Hermes 연동 설정
```

컨텍스트 오염 방지:
- 작업 전 `PROJECT_STRUCTURE.md`를 먼저 확인한다.
- 카드뉴스 작업은 `content/cardnews/` 아래의 해당 episode 폴더만 읽는다.
- PNG는 필요한 최종 파일만 직접 지정해서 확인한다. ZIP은 만들거나 보관하지 않는다.

## 계정 정지 방지 규칙 (반드시 준수)
1. 링크는 5회 중 1회만 포함
2. 답글 간격 30~180초 랜덤
3. 매번 다른 표현으로 답글 생성 (템플릿 금지)
4. 하루 응답 상위 5개만, 2~3회만 체크
5. API 호출 간격 최소 1시간

## 포스팅 톤
- 솔직하고 공감가는 직장인 말투
- 이모지 1~2개
- 200~350자
- 구조: [공감 상황] → [비개발자인데] → [해결] → [당신도 됩니다]

## 기술 스택
- Python + Threads API + Claude API
- `claude -p` 프린트 모드로 실행 (권장)
- Hermes cronjob으로 스케줄링
