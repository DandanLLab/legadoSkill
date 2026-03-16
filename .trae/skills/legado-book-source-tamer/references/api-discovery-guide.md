# API 发现核心技巧

本文档说明如何正确发现网站的 API 接口，包括搜索接口和其他 API。

## 目录

1. [核心原则](#核心原则)
2. [搜索接口发现流程](#搜索接口发现流程)
3. [其他 API 发现方法](#其他-api-发现方法)
4. [实战案例](#实战案例)
5. [常见问题与解决方案](#常见问题与解决方案)

---

## 核心原则

**API 发现是书源开发中最关键的一步，直接决定了书源的质量和性能。**

```
不要猜测，要分析！
盲目测试各种URL格式 → 浪费时间、效率低
分析HTML和JS代码找API → 精准定位、一次成功
```

---

## 搜索接口发现流程

创建书源时，搜索接口的发现是第一步关键工作。请严格按照以下顺序进行：

### 第一步：分析搜索表单（首选方法）

使用 Python 分析 HTML 结构，查找搜索表单：

**1. 查找 form 标签和 input 标签**

```python
from bs4 import BeautifulSoup

# 查找表单
forms = soup.find_all('form')
# 查找输入框
inputs = soup.find_all('input', {'type': ['text', 'search']})
```

**2. 常见搜索字段名（快速匹配）**

优先检查这些常见字段名：
```
['q', 'wd', 'query', 'search', 'key', 'keyword', 'value', 'searchkey', 's', 'word']
```

**3. 分析表单属性**

- `action` 属性：表单提交的 URL
- `method` 属性：GET 或 POST
- `name` 属性：输入框的字段名

**示例代码**：
```python
for form in forms:
    action = form.get('action', '')
    method = form.get('method', 'get').lower()
    input_tag = form.find('input', {'name': True})
    if input_tag:
        field_name = input_tag.get('name')
        print(f"URL: {action}, Method: {method}, Field: {field_name}")
```

### 第二步：分析 JavaScript 代码（备选方法）

如果第一步未找到表单，分析 JS 代码寻找 API：

**1. 查找内联 JS 代码**

```python
# 查找 script 标签中的内联代码
scripts = soup.find_all('script')
for script in scripts:
    if script.string:
        # 搜索关键词：search, ajax, fetch, api
        if any(kw in script.string.lower() for kw in ['search', 'ajax', 'fetch', 'api']):
            print(script.string[:500])  # 打印前500字符分析
```

**2. 查找外部 JS 文件**

```python
# 获取外部 JS 文件
external_scripts = soup.find_all('script', src=True)
for script in external_scripts:
    js_url = script.get('src')
    # 下载并分析 JS 文件内容
```

**3. JS 中常见的关键词**

| 类型 | 关键词 |
|------|--------|
| URL 相关 | `/search`, `/api/search`, `/ss`, `/s.php` |
| 参数相关 | `keyword`, `q`, `wd`, `searchkey` |
| 方法相关 | `$.ajax`, `fetch(`, `$.post`, `$.get` |

### 第三步：猜测测试常见格式（兜底方法）

如果前两步都失败，尝试常见搜索接口格式：

**常见 URL 格式**：
```
/search.php?keyword={{key}}
/search.php?q={{key}}
/search?key={{key}}
/s?q={{key}}
/modules/article/search.php?searchkey={{key}}
/search/{{key}}
```

**移动端常见格式**：
```
https://m.xxx.com/search?key={{key}}
https://m.xxx.com/ss,{'method':'POST','body':'searchkey={{key}}'}
```

### 第四步：参考实战案例（最后手段）

如果 3-5 次测试依旧失败，到实战案例库查找类似情况：

**参考位置**：`examples/README.md`

**常见特殊情况**：
- 移动端与 PC 端接口不同（如 22 笔趣阁）
- 需要 POST 请求而非 GET
- 需要特定请求头（Referer、Origin）
- 搜索接口在子域名上（如 m.xxx.com）
- 需要加密参数或 Token

### 搜索接口发现检查清单

- [ ] **第一步**：是否检查了 form 标签和 input 标签？
- [ ] **第一步**：是否匹配了常见字段名？
- [ ] **第二步**：是否分析了内联 JS 代码？
- [ ] **第二步**：是否分析了外部 JS 文件？
- [ ] **第三步**：是否测试了常见 URL 格式？
- [ ] **第三步**：是否测试了移动端接口？
- [ ] **第四步**：是否查阅了实战案例库？
- [ ] **验证**：是否实际请求接口并验证返回内容？

---

## 其他 API 发现方法

### API 发现三步法

```
第一步：获取首页HTML，先在里面的js代码里找api或某些特殊变量

第二步：在首页HTML,查找外部JS文件
  → <script src="/js/main.js">
  → <script src="/js/api.js">
  → 等等

第三步：分析JS文件，查找API调用
  → $.ajax('/api/chapter')
  → getJSON('/json_book?id=')
  → fetch('/api/content')
  → 等等形态

第四步：测试发现的API
  → 验证API是否可用
  → 分析返回数据格式
```

### 分析 JS 代码找 API

**错误做法**：盲目猜测测试
```python
# 不要这样做！效率低、浪费时间
search_urls = [
    '/search.php?q=xxx',      # 猜测1
    '/search?keyword=xxx',    # 猜测2
    '/api/search?q=xxx',      # 猜测3
]
```

**正确做法**：分析JS代码找API
```python
# 第一步：获取首页HTML
response = requests.get('https://www.bqgui.cc')
html = response.text

# 第二步：查找外部JS文件
import re
js_file_pattern = r'<script[^>]*src=["\']([^"\']+\.js[^"\']*)["\']'
js_files = re.findall(js_file_pattern, html)

# 第三步：分析JS文件，查找API调用
for js_file in js_files:
    js_response = requests.get(js_file)
    js_content = js_response.text
    
    # 查找API调用
    api_patterns = [
        r'\$\.ajax\(["\']([^"\']+)["\']',      # $.ajax('url')
        r'\$\.get\(["\']([^"\']+)["\']',       # $.get('url')
        r'\$\.post\(["\']([^"\']+)["\']',      # $.post('url')
        r'getJSON\(["\']([^"\']+)["\']',       # getJSON('url')
    ]
    
    for pattern in api_patterns:
        matches = re.findall(pattern, js_content)
        if matches:
            print(f"发现API: {matches}")
```

---

## 实战案例

### 案例：笔趣阁 API 发现

**问题**：主域名 `www.bqgui.cc` 的正文页有验证机制

**解决方法**：
```python
# 第一步：分析JS文件
js_file = 'https://www.bqgui.cc/js/compc.js?v=1.23'
js_content = requests.get(js_file).text

# 第二步：查找API调用
import re
pattern = r'getJSON\(["\']([^"\']+)["\']'
apis = re.findall(pattern, js_content)
# 发现：['/json_book?id=']

# 第三步：测试发现的API
api_url = 'https://www.bqgui.cc/json_book?id=66'
response = requests.get(api_url)
# 返回JSON数据
```

**关键发现**：
- `/json_book?id=` - 返回章节列表（JSON格式）
- 从JS代码中直接发现，无需猜测！

### 案例：22 笔趣阁搜索接口

**问题**：PC 端 `www.22biqu.com` 没有搜索表单

**解决方法**：
1. 分析 HTML 未找到搜索表单
2. 尝试常见 URL 格式均返回 404
3. 参考现有书源，发现移动端接口
4. 最终发现：`https://m.22biqu.com/ss` POST 请求

**教训**：移动端与 PC 端接口可能不同，优先检查移动端

---

## 常见问题与解决方案

### 1. 找不到搜索表单怎么办？

- 检查是否有隐藏的搜索按钮/图标
- 分析 JS 代码，搜索可能是动态加载的
- 尝试移动端网站（m.xxx.com）
- 查看网站是否有独立的搜索页面

### 2. API 需要特殊参数怎么办？

```python
# 常见需要的请求头
headers = {
    'Referer': 'https://www.xxx.com/',
    'Origin': 'https://www.xxx.com',
    'X-Requested-With': 'XMLHttpRequest',
}
```

### 3. 如何从验证页面发现备用域名？

```javascript
var html = java.webView(url, url, 'setTimeout(function(){window.legado.getHTML(document.documentElement.outerHTML);},5000);');
var match = html.match(/https?:\/\/([\w\-\.]+)\//);
if(match){
    source.setVariable(match[1]);  // 保存备用域名
}
```

### 4. 错误流程 vs 正确流程

**错误流程**：
```
看到变量 → 忽略 → 猜测API → 失败 → 再猜 → 再失败...
```

**正确流程**：
```
看到变量 → 追问用途 → 查找使用位置 → 发现ajax调用 → 仔细阅读 → 成功！
```

### 5. 核心技巧总结

| 技巧 | 说明 |
|------|------|
| 不要猜测，要分析 | 先分析 HTML 和 JS 代码 |
| 先内联，后外部 | 先分析内联 JS，再分析外部 JS 文件 |
| 关注变量 | 看到特殊变量一定要理解其作用 |
| 备用域名也有 API | 主域名失败时分析备用域名 |
| 注意请求头 | 有时需要特殊的请求头或 Cookie |
