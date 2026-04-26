# 세션: 2026-04-26 Hermes 기반 재구축 + 4채널 아키텍처

**채널**: Telegram DM  
**주요 내용**:

1. `01_project_threads` 분석 — launchd 자동화, 2회 계정 정지
2. 정지 원인 분석: 패턴 반복 + 링크 스팸 + 규칙적 간격
3. Hermes `threads` 프로필 + 구조 재구성 (app/docs 분리)
4. 하이브리드 아키텍처: DeepSeek(생각) + Claude(실행)
5. OAuth Claude Max 계정 — 추가 키 불필요
6. **4채널 통합 메모리**:
   - ① Telegram DM → Hermes Gateway
   - ② Hermes CLI (`threads chat`)
   - ③ Claude Code CLI (`claude`)
   - ④ Paperclip 대시보드

## 4채널 공통 진실 공급원

```
어느 채널이든 → docs/memory/{state, decisions, lessons, architecture, research}.md
                 ├── 모든 채널이 같은 파일을 읽음
                 ├── 변경 시 모든 채널에 즉시 반영 (마크다운)
                 └── CLAUDE.md가 docs/memory/ 참조하도록 설정
```

## 결정사항
- [D001] Hermes cronjob 전환
- [D002] 6가지 안전 규칙
- [D003] app/docs 구조
- [D004] 4채널 통합 메모리

👉 [상태 확인](../memory/state.md)  👉 [모든 결정](../memory/decisions.md)