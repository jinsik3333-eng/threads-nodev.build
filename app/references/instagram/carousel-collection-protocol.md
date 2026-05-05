# Carousel Collection Protocol for @nodev.builder References

작성일: 2026-05-03

## 목적

Instagram 레퍼런스는 커버 1장만 분석하면 실패한다. 게시글 하나가 여러 장의 이미지/영상으로 구성되므로, 반드시 캐러셀 내부 슬라이드 흐름까지 기록한다.

## 수집 단위

### Account

- 계정명
- 계정 포지션
- 그리드 전체 톤
- 반복 색/폰트/CTA/라벨

### Post

- 게시글 URL
- 게시글 유형: carousel / reel / single
- 게시글 주제
- 커버 카피
- CTA 방식
- 캡션 내 댓글 키워드/링크 유도

### Slide

각 캐러셀은 슬라이드별로 아래를 기록한다.

```json
{
  "slide_no": 1,
  "role": "cover | problem | proof | process | output | cta",
  "screenshot": "assets/...png",
  "layout": "텍스트/이미지/프레임 배치",
  "image_role": "인물 | 제품 | UI | 결과물 | 분위기 | 증거",
  "text_role": "후킹 | 설명 | 라벨 | CTA | 저장 포인트",
  "copy": "보이는 핵심 문구",
  "transition_from_prev": "이전 장에서 왜 넘어오는지",
  "reusable_rule": "@nodev.builder에 가져올 규칙",
  "avoid_rule": "그대로 따라 하면 안 되는 점"
}
```

## 캡처 기준

1. 커버 이미지는 피드 그리드와 게시글 상세 두 버전 모두 가능하면 저장한다.
2. 캐러셀 내부는 1장씩 넘기며 전체 캡처한다.
3. 릴스는 커버 + 영상 첫 3초 + CTA 프레임을 우선 캡처한다.
4. 캡션은 댓글 키워드/DM 유도/프로필 링크 유무만 요약한다.
5. 이미지 생성에 쓸 수 있는 레퍼런스는 `good_reference`로 태깅한다.
6. 보기에는 예쁘지만 @nodev.builder와 안 맞으면 `avoid_reference`로 태깅한다.

## 로그인 필요 시점

비로그인 Instagram 웹은 다음이 불안정하다.

- 게시글 상세 URL 안정 수집
- 캐러셀 내부 슬라이드 전체 열람
- 다음/이전 슬라이드 버튼 조작
- 고화질 이미지 확인
- 댓글/캡션 전체 보기

따라서 내부 슬라이드까지 DB를 쌓으려면 사용자가 브라우저에서 Instagram 로그인해주거나, 게시글 링크/스크린샷을 직접 보내주는 방식이 필요하다.

## 우선순위

1. `@mobileeditingclub`: 커버 감도와 내부 이미지/CTA 흐름
2. `@adrianabubori`: Claude/AI workflow를 라이프스타일로 포장하는 방식
3. `@sebia.ai`: 한국어 후킹/DM 퍼널/정보계정 구조
4. `@gymcoding`: 한국어 AI 개발 교육의 정보 위계/저장형 구조

## 완료 기준

- 계정당 최소 10개 게시글
- 게시글당 커버 + 내부 슬라이드 기록
- 총 40개 post JSON
- 각 post에 최소 3개 이상 reusable_rule/avoid_rule
- @nodev.builder 템플릿 후보와 연결
