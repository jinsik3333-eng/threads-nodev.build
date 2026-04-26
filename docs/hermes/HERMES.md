# 비개발dev — Hermes Agent / Threads API 연동

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

## Threads API

| 항목 | 값 |
|------|-----|
| API Base | `https://graph.threads.net/v1.0` |
| 클라이언트 | `app/src/threads_client.py` |

### API 토큰 발급 방법

1. Meta for Developers에서 앱 생성 → Threads API 활성화
2. OAuth로 사용자 인증 → long-lived token 발급
3. `.env`에 저장:
   ```
   THREADS_ACCESS_TOKEN=...
   THREADS_USER_ID=...
   ANTHROPIC_API_KEY=...
   ```

## Hermes Cronjob (예정)

```bash
# 오전 포스트 발행 (07:30)
threads cron create "30 7 * * *" \
  --prompt "app/scripts/publish.py로 queue에서 다음 포스트 발행"

# 저녁 포스트 발행 (21:00)
threads cron create "0 21 * * *" \
  --prompt "app/scripts/publish.py로 queue에서 다음 포스트 발행"

# 댓글 응답 (1일 2회, 10:00 / 18:00)
threads cron create "0 10,18 * * *" \
  --prompt "app/scripts/respond.py로 최신 포스트 댓글 5개 선별 응답 (안전 규칙 준수)"
```

## 안전 체크리스트

- [ ] 답글에 링크 포함 비율 ≤ 20%
- [ ] 답글 간격 30~180초 랜덤
- [ ] API 호출 간격 ≥ 1시간
- [ ] 하루 응답 ≤ 15개
- [ ] 모든 답글 Claude API로 생성 (템플릿 금지)
- [ ] launchd 사용 금지 (Hermes cronjob만)