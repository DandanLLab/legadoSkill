# API发现核心技巧

本文档说明如何正确发现网站的API接口。

## 目录

1. [核心原则](#核心原则)
2. [正确方法：分析JS代码找API](#正确方法分析js代码找api)
3. [实战案例：笔趣阁API发现](#实战案例笔趣阁api发现)
4. [API发现三步法](#api发现三步法)
5. [核心技巧](#核心技巧)

---

## 核心原则

**API发现是书源开发中最关键的一步，直接决定了书源的质量和性能。**

---


## API发现三步法

```
第一步：获取首页HTML，先在里面的js代码里找api或某些特殊变量

第二步：在首页HTML,查找外部JS文件
  → <script src="/js/main.js">
  → <script src="/js/api.js">
  → 等等

第二步：分析JS文件，查找API调用
  → $.ajax('/api/chapter')
  → getJSON('/json_book?id=')
  → fetch('/api/content')
  → 等等形态

第三步：测试发现的API
  → 验证API是否可用
  → 分析返回数据格式
```
---

## 正确方法：分析JS代码找API

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

## 实战案例：笔趣阁API发现

**问题**：主域名 `www.bqgui.cc` 的正文页有验证机制

**正确方法**：
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


---

## 核心技巧

1. **不要猜测，要分析**
   ```
   盲目测试各种URL格式
   分析JS代码找API调用
   先分析html中的内联js代码，再分析外部js文件
   不要忽略关键线索，比如看到了特殊的变量一定要理解其作用。动态加载一定要注意变量
   仔细阅读代码，尤其是ajax相关的代码
   ```

2. **备用域名也有API**
   ```
   主域名API失败 → 分析备用域名的JS代码
   备用域名往往有惊喜
   ```

3. **从验证页面发现备用域名**
   ```javascript
   var html = java.webView(url, url, 'setTimeout(function(){window.legado.getHTML(document.documentElement.outerHTML);},5000);');
   var match = html.match(/https?:\/\/([\w\-\.]+)\//);
   if(match){
       source.setVariable(match[1]);  // 保存备用域名
   }
   ```
  
4. **有时可能需要特殊的请求头或者需要cookie**

5. **错误流程**：
  看到变量 → 忽略 → 猜测API → 失败 → 再猜 → 再失败...

  **正确流程**：
  看到变量 → 追问用途 → 查找使用位置 → 发现ajax调用 → 仔细阅读 → 成功！
