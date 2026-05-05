# 🎨 인스타그램 카드뉴스 자동 생성 (Claude Code Skill)

> Claude Code + Playwright로 HTML→PNG 카드뉴스 자동 생성

## 개요

비개발dev 인스타그램 계정용 카드뉴스를 자동 생성하는 워크플로우입니다.  
참고: 유튜브 영상 "클로드 코드 스킬로 인스타 카드뉴스 자동 생성"

## 작동 방식

```
① 컨텐츠 URL/텍스트 → ② Claude Code가 HTML 생성 → ③ Playwright 스크린샷 → ④ PNG 이미지 완성
```

## 디렉토리 구조

```
app/cards/
├── template.css        ← 공통 스타일
├── logo.png            ← 비개발dev 로고
├── generate.sh         ← 실행 스크립트
└── episodes/
    └── YYYYMMDD_주제/  ← 주제별 카드뉴스
        ├── source.txt  ← 원본 텍스트
        └── cards/      ← 생성된 이미지
```

## 브랜드 가이드

| 항목 | 값 |
|------|-----|
| 색상 | 메인 #2D3748, 포인트 #4299E1, 배경 #F7FAFC |
| 폰트 | Noto Sans KR (본문), Noto Sans KR Bold (헤더) |
| 로고 | assets/비개발dev_image.png → 80x80px로 축소 |
| CTA | "비개발dev — Claude Code로 만드는 나만의 도구" |

## 카드뉴스 구성 (6~8장)

| 순서 | 유형 | 내용 |
|------|------|------|
| 1 | 커버 | 주제 + "비개발dev" 로고 |
| 2~N-1 | 본문 | 핵심 내용 1포인트/1카드 |
| N | CTA | "팔로우하고 업무 자동화 꿀팁 받아가세요 🚀" |

## 실행 방법

### 1. 자료 수집
```
claude code에서: "@카드뉴스 [URL] 이 내용으로 카드뉴스 만들어줘"
```

### 2. HTML 생성
```
- 비율: 1080x1350 (인스타그램 4:5)
- 순수 HTML + CSS
- 첫 번째: 커버 (제목 + 로고)
- 중간: 내용 카드 (헤더 + 바디 + 푸터)
- 마지막: CTA
```

### 3. 이미지로 변환
```bash
npx playwright screenshot --viewport-size=1080,1350 \
  "file://$(pwd)/episodes/20260426_클로드4.7/card-01.html" card-01.png
```

### 4. Skill 등록
```
Skill Creator로 등록 → 다음부터 @카드뉴스 한마디로 자동 생성
```

## 활용 예시

```bash
# 첫 번째 카드뉴스
claude -p "
@카드뉴스 다음 내용으로 인스타 카드뉴스 제작:

주제: Claude Code로 엑셀 업무 자동화하기
내용:
- 매주 3시간 걸리던 엑셀 작업이 5분으로
- VBA 몰라도 됨
- '이 데이터로 피벗테이블 만들어줘' 한마디면 끝
- 비개발자도 할 수 있다

브랜드 가이드와 템플릿을 참고하여 제작해줘.
app/cards/episodes/20260426_엑셀자동화/ 에 저장.
" --allowedTools "Write,Bash" --max-turns 10
```