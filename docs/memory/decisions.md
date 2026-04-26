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