# 비개발dev 프로젝트 폴더 구조

목적: 내가 봐도, 에이전트가 봐도 빠르게 찾을 수 있게 폴더 단계를 줄인다.

## 최상위 원칙

- `app/`은 실행 코드만 둔다.
- `content/characters/`는 캐릭터 이미지 전용이다.
- `content/cardnews/`는 카드뉴스 게시물 전용이다. 날짜별 폴더 하나가 게시물 하나다.
- `content/templates/nodev-original-character-cardnews-30/`는 반복 사용 템플릿 30종이다. 기존 3D 캐릭터 외형을 유지한 상태에서 텍스트/말풍선/CTA 영역을 제공한다.
- 카드뉴스별 임시 Python 렌더러, 템플릿 실험본, ZIP은 최종 산출 후 삭제한다.
- 카드뉴스 게시 텍스트는 별도 posts 폴더에 두지 않고 해당 카드뉴스 폴더 안에 같이 둔다.
- 폐기본 `character_asset_set_20`은 복구하거나 다시 만들지 않는다.

## 현재 구조

```text
01_project_threads/
├── app/                         # Python 자동화 코드 전용
│   ├── src/                     # Meta/Threads/Instagram API 모듈
│   ├── scripts/                 # 실행 스크립트
│   ├── tests/                   # 테스트
│   ├── state/                   # 로컬 큐/응답 상태
│   └── requirements.txt
│
├── content/
│   ├── characters/
│   │   └── nodev-builder/
│   │       └── reference-locked-20/      # 유지: 공식 캐릭터 포즈 20개
│   │
│   ├── cardnews/
│   │   ├── 2026-05-04-character-best/   # 베스트 케이스 카드뉴스
│   │   │   ├── images/                  # card-01~06, contact-sheet
│   │   │   ├── card_script.json
│   │   │   └── notes.md
│   │   │
│   │   └── 2026-05-06-claude-first-asks/
│   │       ├── images/                  # card-01~07, contact-sheet
│   │       ├── caption-and-posting.md   # 게시 텍스트
│   │       └── card_script.json
│   │
│   ├── templates/
│   │   └── nodev-original-character-cardnews-30/
│   │       ├── images/                  # 기존 캐릭터 외형 유지 템플릿 30 PNG
│   │       ├── contact-sheets/          # 전체/cover/body/end 검수판
│   │       ├── manifest.json
│   │       └── README.md
│   │
│   └── README.md                        # content 사용법
│
├── guides/                              # 실제 HTML 가이드/리드마그넷 배포물
├── assets/                              # 브랜드/프로필 이미지
├── docs/                                # 장기 운영 문서
└── PROJECT_STRUCTURE.md                 # 이 파일
```

## 작업할 때 읽는 범위

### 캐릭터 카드뉴스를 만들거나 수정할 때

필수:
- `content/cardnews/<날짜-게시물>/`
- 필요 시 `content/characters/nodev-builder/reference-locked-20/`
- 필요 시 해당 작업 폴더에서 임시 렌더러를 새로 만든다.

기준:
- 베스트 케이스는 `content/cardnews/2026-05-04-character-best/`
- 캐릭터는 `content/characters/nodev-builder/reference-locked-20/`만 사용
- `character_asset_set_20`은 폐기본이라 사용 금지

피해야 할 것:
- 전체 이미지 폴더 일괄 분석
- 폐기본 캐릭터 세트 복구
- 과거 템플릿 실험본/대체 시안/ZIP 복구

### 자동화 코드를 수정할 때

필수:
- `app/src/`
- `app/scripts/`
- `app/tests/`

피해야 할 것:
- `content/cardnews/` 이미지 전체
- `content/characters/` 이미지 전체

## 날짜별 카드뉴스 폴더 규칙

새 카드뉴스는 항상 이렇게 만든다.

```text
content/cardnews/YYYY-MM-DD-short-title/
├── images/
│   ├── card-01.png
│   ├── card-02.png
│   └── contact-sheet.png
├── caption-and-posting.md   # 발행 텍스트/댓글 키워드/DM 문구
├── card_script.json         # 있으면 유지
└── notes.md                 # 제작 의도/수정 메모
```

## 2026-05-06 단순화 내역

- 캐릭터 이미지를 `content/characters/nodev-builder/`로 통합
- 카드뉴스를 `content/cardnews/` 날짜별 폴더로 통합
- 2026-05-08: 최종 산출물 기준으로 workflows, rejected/backup/대체 시안, 카드뉴스별 Python 렌더러를 삭제
- 2026-05-08: 이미지 ZIP은 만들거나 보관하지 않기로 결정. 업로드는 PNG를 직접 사용
- 2026-05-08: 잘못 생성한 템플릿 전량 삭제. 기존 캐릭터 외형을 유지하는 방향으로만 재시도
- 2026-05-08: `content/templates/nodev-original-character-cardnews-30/`에 기존 캐릭터 기반 카드뉴스 템플릿 30종 생성
- 기존 `content/instagram/`, `content/references/`, `content/planning/`, `app/cards/` 제거
- 베스트 케이스 경로를 `content/cardnews/2026-05-04-character-best/`로 고정
