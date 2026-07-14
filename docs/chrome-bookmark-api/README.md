크롬 북마크에 프로그래밍 방식으로 접근하는 방법은 크게 두 가지입니다.

**1. Chrome Extension API (`chrome.bookmarks`)**

확장 프로그램을 만든다면 공식 API가 있습니다.

```javascript
// manifest.json에 "permissions": ["bookmarks"] 필요

chrome.bookmarks.getTree((tree) => {
  console.log(tree);
});

// 검색
chrome.bookmarks.search("query", (results) => { ... });

// 특정 노드
chrome.bookmarks.getChildren("0", (children) => { ... });
```

주요 메서드: `getTree`, `getSubTree`, `getChildren`, `search`, `create`, `move`, `update`, `remove`.

**2. 로컬 Bookmarks 파일 직접 파싱 (서버/백엔드용)**

확장 프로그램이 아니라 백엔드에서 처리한다면, 크롬은 북마크를 JSON 파일로 저장하므로 그걸 읽으면 됩니다.

- macOS: `~/Library/Application Support/Google/Chrome/Default/Bookmarks`
- Windows: `%LOCALAPPDATA%\Google\Chrome\User Data\Default\Bookmarks`
- Linux: `~/.config/google-chrome/Default/Bookmarks`

확장자 없는 JSON 파일이라 그냥 파싱하면 됩니다.

```python
import json, os

path = os.path.expanduser("~/.config/google-chrome/Default/Bookmarks")
with open(path, encoding="utf-8") as f:
    data = json.load(f)

def walk(node):
    if node["type"] == "url":
        yield node["name"], node["url"]
    for child in node.get("children", []):
        yield from walk(child)

for root in data["roots"].values():
    if isinstance(root, dict):
        for name, url in walk(root):
            print(name, url)
```

---

방식은 위 2가지고 실제로는 2번 방식 사용할 듯, 항상 확장을 사용하는 방식은 아니기 때문