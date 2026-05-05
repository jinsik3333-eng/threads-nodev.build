# Claude in Chrome 수집 원문 붙여넣기용

아래 JSON 파일에 Claude in Chrome 결과를 그대로 넣으면 됩니다.

```text
/Users/jinsik/Desktop/Workspace/01_project_threads/app/references/instagram/claude-in-chrome-raw-input.json
```

## 권장 형식

```json
[
  {
    "account": "@mobileeditingclub",
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
]
```

## 주의

- JSON 전체가 완벽하지 않아도 괜찮습니다. 붙여넣은 뒤 제가 정리할 수 있습니다.
- 다만 가능하면 `[`로 시작해서 `]`로 끝나는 배열 형태가 가장 좋습니다.
- 중복 URL이 있어도 괜찮습니다. 제가 제거합니다.
- Claude in Chrome 결과가 너무 길면 계정별로 나눠 붙여도 됩니다.
