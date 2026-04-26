# 🔄 4채널 통합 메모리 아키텍처

## 채널별 역할

```
┌─────────────────────────────────────────────────────────┐
│                    docs/memory/ (진실 공급원)              │
│  decisions.md  │  research.md  │  lessons.md  │  state.md │
└────┬───────────────┬────────────────┬────────────────────┘
     │               │                │
     ▼               ▼                ▼
┌─────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐
│Telegram │  │  Hermes  │  │  Claude  │  │  Paperclip   │
│  (DM)   │  │   CLI    │  │Code CLI  │  │  (대시보드)   │
└────┬────┘  └────┬─────┘  └────┬─────┘  └──────┬───────┘
     │            │             │               │
     ▼            ▼             ▼               ▼
  DeepSeek    DeepSeek      Claude        Claude (runner)
  (NIM)       (NIM)         (Sonnet)      + CEO/CTO/CMO
```

## 각 채널별 컨텍스트 로딩

### ① Telegram → Hermes
```
[텔레그램 메시지]
    │
    ▼
[Hermes Gateway] → threads 프로필 로드
    │
    ├── SOUL.md (페르소나)
    ├── config.yaml
    ├── memory 도구 → 핵심 정보 자동 주입
    └── skills → 필요 시 로딩

[실행] → delegate_task → Claude Code
[결과 저장] → memory 도구 + docs/sessions/
```

### ② Hermes CLI (직접)
```bash
threads chat
# → SOUL.md + config.yaml + memory 도구 로드
# → docs/memory/는 수동 참조 또는 자동 스킬로 로딩
```

### ③ Claude Code CLI (직접)
```bash
claude
# → CLAUDE.md 로드 (docs/memory/ 참조 포함)
# → ~/.claude/CLAUDE.md (글로벌 규칙)
# → 직접 파일 읽기: docs/memory/decisions.md 등
```

### ④ Paperclip (대시보드)
```
Paperclip 이슈
    │
    ├── CEO 할당 → 작업 실행 (Claude Code runner)
    │
    ▼
[완료] → Hermes가 이슈 완료 감지
    │
    ├── docs/paperclip/issues/ 에 요약 저장
    └── docs/memory/ 관련 파일 업데이트
```

## 공유 데이터 흐름

```
어떤 채널에서든 작업 완료 시:

1. docs/memory/ 관련 파일 업데이트
   ├── 결정 → decisions.md
   ├── 교훈 → lessons.md
   ├── 리서치 → research.md
   └── 상태 변경 → state.md

2. Hermes memory 도구 업데이트 (핵심만 압축)
   └── .hermes-sync/memory.md 미러링

3. 해당 채널의 세션 기록
   ├── Telegram → Hermes sessions/
   ├── Hermes CLI → sessions/
   ├── Claude CLI → ~/.claude/projects/
   └── Paperclip → run-logs/

4. CLAUDE.md 동기화 (필요 시)
   └── Claude Code가 docs/memory/ 참조하도록 유지
```

## 현재 상태 (state.md 참조)

| 항목 | 값 |
|------|-----|
| 활성 채널 | Telegram ✅, Hermes CLI ✅, Claude CLI ✅, Paperclip ⏸️ |
| 계정 | 신규 생성 준비 중 |
| 자동화 | 코드 이관 완료, cronjob 미설정 |