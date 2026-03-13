# User-Agent检测问题排查经验

## 🔍 排查方法

当搜索无结果时，按以下顺序测试：

```python
import requests
from bs4 import BeautifulSoup

url = 'https://example.com/search'
data = {'key': '测试'}

# 1. 不带UA
r1 = requests.post(url, data=data)
# 2. 简单UA
r2 = requests.post(url, data=data, headers={'User-Agent': 'Mozilla/5.0'})
# 3. 完整UA
r3 = requests.post(url, data=data, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0...)'})

# 对比结果数量
for name, r in [('不带UA', r1), ('简单UA', r2), ('完整UA', r3)]:
    soup = BeautifulSoup(r.text, 'html.parser')
    results = soup.find_all('li', class_='result')
    print(f'{name}: {len(results)} 个结果')
```

## 📊 常见检测结果

| User-Agent | 结果 | 原因 |
|-----------|------|------|
| 不带UA | ✅ 有 | 网站未检测 |
| `Mozilla/5.0` | ✅ 有 | 网站过滤完整UA |
| 完整浏览器UA | ❌ 无 | 网站过滤完整UA |
| 移动端UA | ❌ 无 | 网站过滤移动端 |
| `python-requests` | ❌ 无 | 网站过滤爬虫 |

## ✅ 解决方案

在searchUrl中指定简单UA：

```json
{
  "searchUrl": "/search,{\"method\":\"POST\",\"body\":\"key={{key}}\",\"headers\":{\"User-Agent\":\"Mozilla/5.0\"}}"
}
```

## 💡 排查口诀

```
搜索无果先测UA，
不带请求头先试。
简单UA再测试，
对比结果找规律。
```

---
**更新时间**：2026-03-13
