# launchd 등록 방법

## 1. 경로 확인

```bash
pwd        # PROJECT_PATH
which python3  # PYTHON_PATH
```

## 2. plist 파일을 ~/Library/LaunchAgents/에 복사

```bash
cp launchd/*.plist ~/Library/LaunchAgents/
```

## 3. 등록

```bash
launchctl load ~/Library/LaunchAgents/build.nodev.morning.plist
launchctl load ~/Library/LaunchAgents/build.nodev.evening.plist
launchctl load ~/Library/LaunchAgents/build.nodev.comments.plist
```

## 4. 확인

```bash
launchctl list | grep nodev
```

## 5. 해제

```bash
launchctl unload ~/Library/LaunchAgents/build.nodev.morning.plist
launchctl unload ~/Library/LaunchAgents/build.nodev.evening.plist
launchctl unload ~/Library/LaunchAgents/build.nodev.comments.plist
```

## 스케줄

| plist | 실행 시간 | 스크립트 |
|-------|---------|---------|
| nodev.morning.plist | 매일 07:30 | scripts/publish.py |
| nodev.evening.plist | 매일 21:00 | scripts/publish.py |
| nodev.comments.plist | 매 30분 | scripts/respond.py |
