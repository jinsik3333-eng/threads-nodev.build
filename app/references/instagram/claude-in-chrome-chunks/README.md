# Claude in Chrome Instagram 수집 결과 붙여넣기용 분할 파일

Telegram/JSON 한 번에 붙여넣으면 길어서 끊기므로 계정별로 나눠 저장합니다.

## 파일

- `01-mobileeditingclub.json`
- `02-adrianabubori.json`
- `03-sebia-ai.json`
- `04-gymcoding.json`

## 붙여넣기 규칙

각 파일은 아래 형태만 유지하면 됩니다.

```json
{
  "account": "@계정명",
  "posts": [
    {
      "url": "https://www.instagram.com/p/.../",
      "cover_headline": "",
      "slide_count": 0,
      "slide_roles": [],
      "design_features": [],
      "patterns_for_nodev_builder": [],
      "avoid": []
    }
  ]
}
```

- 계정 하나씩만 넣으면 됩니다.
- 중복 URL 있어도 괜찮습니다. 나중에 제가 제거합니다.
- JSON이 깨질 것 같으면 `.json` 구조 신경 쓰지 말고, 같은 폴더에 `raw-계정명.md`로 원문 그대로 저장해도 됩니다.
- 특히 `@sebia.ai`, `@gymcoding`은 따로 넣는 것을 추천합니다.
