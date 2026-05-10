# 콘텐츠 폴더 사용법 (단순 구조)

이 프로젝트에서 카드뉴스 작업할 때는 아래 2곳만 보면 된다.

## 1. 캐릭터 이미지
`content/characters/nodev-builder/`

- `reference-locked-20/` — 유지할 공식 캐릭터 포즈 20개
- 초기 테스트 6개 세트는 `reference-locked-20/`와 중복이라 삭제했다.
- `character_asset_set_20/`은 폐기본이라 만들거나 복구하지 않는다.

## 2. 카드뉴스
`content/cardnews/`

날짜별 폴더 하나가 게시물 하나다.

예시:
- `2026-05-04-character-best/` — 현재 베스트 케이스 캐릭터 카드뉴스
- `2026-05-06-claude-first-asks/` — 2026-05-06 제작 카드뉴스

각 폴더 안 규칙:
- `images/` — 업로드용 카드 이미지와 contact-sheet
- `caption-and-posting.md` 또는 `notes.md` — 게시 텍스트/기획/메모
- `card_script.json` — 카드 구조가 있으면 같이 둔다
- ZIP은 만들거나 보관하지 않는다. 업로드는 `images/card-*.png`를 직접 사용한다.

## 3. 카드뉴스 템플릿
`content/templates/nodev-original-character-cardnews-30/`

- 기존 `content/characters/nodev-builder/reference-locked-20/` 캐릭터 외형을 유지한 카드뉴스 템플릿 30종
- `images/` — 1080x1350 PNG 템플릿 30개
- `contact-sheets/` — 전체/cover/body/end 검수용 contact sheet
- `manifest.json` — 템플릿별 역할, 팔레트, 캐릭터 소스 기록
- ZIP은 만들거나 보관하지 않는다.

## 에이전트 접근 규칙

카드뉴스를 만들거나 수정할 때 전체 폴더를 다 읽지 말고:
1. `content/cardnews/<날짜-게시물>/` 해당 폴더만 먼저 본다.
2. 반복 사용할 카드뉴스 틀이 필요하면 `content/templates/nodev-original-character-cardnews-30/`를 본다.
3. 캐릭터가 필요할 때만 `content/characters/nodev-builder/reference-locked-20/`를 본다.
4. 렌더링이 필요하면 기존 캐릭터 외형을 유지해 새 작업 범위 안에서 임시 렌더러를 만들고, 최종 산출 후 삭제한다.
