# 비개발dev — Hermes Agent / Threads API 연동

## 🧠 아키텍처: 하이브리드 (DeepSeek 생각 + Claude 실행)

```
[사용자/텔레그램] → [Hermes: DeepSeek(NIM)]
                         │
                         │ 생각/판단: "지금 포스트 발행할 시간이야"
                         │
                         ▼
                    [Claude Code (OAuth)]
                         │
                         │ 실제 실행: python publish.py 실행
                         │
                         ▼
                    [Threads API]
```

| 역할 | 모델 | 방식 |
|------|------|------|
| 🧠 **생각/판단** | DeepSeek-V4-Pro (NVIDIA NIM) | Hermes Agent |
| 🔧 **실행** | Claude Code (Sonnet) | `delegate_task` → `claude -p` |
| 🔑 **인증** | Claude Max OAuth | 추가 키 불필요 |

## Hermes Profile

```bash
threads chat           # 전용 CLI 대화
threads config edit    # 설정 편집
```

| 항목 | 경로 |
|------|------|
| Profile | `~/.hermes/profiles/threads/` |
| Config | `~/.hermes/profiles/threads/config.yaml` |
| Persona | `~/.hermes/profiles/threads/SOUL.md` |
| Skills | `~/.hermes/profiles/threads/skills/` |
| cwd | `.../01_project_threads/app` |

## 실행 패턴

### delegate_task로 Claude 호출 (권장)
```python
# Hermes 내부적으로 이렇게 동작
delegate_task(
    goal="queue에서 포스트 발행",
    context="app/scripts/publish.py 실행, .env에 Threads API 키 있음",
    toolsets=["terminal", "file"],
    acp_command="claude",
    acp_args=["-p", "python scripts/publish.py", "--allowedTools", "Bash,Read", "--max-turns", "5"]
)
```

### terminal로 직접 Claude 호출 (간단한 경우)
```bash
claude -p "python scripts/publish.py 실행" --max-turns 5
```

## Hermes Cronjob (예정)

```bash
# 오전 포스트 (07:30)
threads cron create "30 7 * * *" \
  --prompt "delegate_task로 Claude Code에게 app/scripts/publish.py 실행 지시"

# 댓글 응답 (1일 2회)
threads cron create "0 10,18 * * *" \
  --prompt "delegate_task로 Claude Code에게 새 댓글 선별 응답 지시 (안전 규칙 준수)"
```

## 안전 체크리스트
- [ ] 답글 링크 ≤ 20%
- [ ] 답글 간격 30~180초 랜덤
- [ ] 하루 응답 ≤ 15개
- [ ] Claude로 매번 새 답글 생성
- [ ] API 간격 ≥ 1시간