# 验证码检测与处理指南

本文档详细说明如何检测和处理各类网站验证码（WAF保护/验证码识别/Cloudflare盾）。

---

## 目录

1. [检测方法](#检测方法)
2. [常见WAF类型及特征](#常见waf类型及特征)
3. [处理方法](#处理方法)
4. [检测流程](#检测流程)

---

## 检测方法

### 1. 实际访问测试

**必须通过实际访问网站来确认是否存在验证码**，而不是凭经验猜测！

执行以下测试：
- 访问网站首页
- 尝试执行搜索请求
- 尝试访问书籍详情页

### 2. 响应特征识别

检查返回的HTML内容：

1. **HTTP状态码异常**：
   - 403 Forbidden
   - 502 Bad Gateway
   - 503 Service Unavailable

2. **页面内容特征**：
   - 验证码输入表单
   - 滑动验证元素
   - 特定WAF标识

---

## 常见WAF类型及特征

### Cloudflare

**特征关键词**：
- "Just a moment"
- "Checking your browser"
- "cloudflare"

**检测代码**：
```javascript
o.includes('Just a moment') || o.includes('Checking your browser')
```

---

### GoEdge WAF

**特征关键词**：
- "Verify Yourself"
- "GOEDGE_WAF_CAPTCHA"
- "WAF/VERIFY/CAPTCHA"

**检测代码**：
```javascript
o.includes('Verify Yourself') || o.includes('GOEDGE_WAF_CAPTCHA')
```

---

### 常见WAF标识

| WAF类型 | 特征关键词 |
|---------|-----------|
| Cloudflare | "Just a moment", "Checking your browser" |
| GoEdge WAF | "Verify Yourself", "GOEDGE_WAF_CAPTCHA" |
| 百度云加速 | "yunjiasu", "safety.baidu.com" |
| 阿里云WAF | "aliyun", "waf.aliyun.com" |
| 腾讯云WAF | "waf.qcloud.com" |
| 安全狗 | "safedog", "cloud.safedog.cn" |

---

## 处理方法

### 1. loginCheckJs 字段

在书源JSON中添加 `loginCheckJs` 字段来处理验证码：

```javascript
"loginCheckJs": "(function(a){var r=a.url(),o=a.body(),t=a.code();if(o&&(403===t||503===t||502===t||200===t&&(o.includes('Just a moment')||o.includes('Checking your browser')||o.includes('Verify Yourself')||o.includes('GOEDGE_WAF_CAPTCHA')))){var c=source.get('cf_count')||'0';c=parseInt(c)+1;source.put('cf_count',c);if(c<=3){for(var i=0;i<2;i++){try{var h=java.webView(r,r,'setTimeout(function(){window.legado.getHTML(document.documentElement.outerHTML);},5000);');if(h&&!h.includes('Just a moment')&&!h.includes('Verify Yourself')&&200===java.connect(r).code()){source.put('cf_count','0');return a}}catch(e){}}}java.toast('需要验证码验证');java.startBrowserAwait(r,'验证');source.put('cf_count','0');return java.connect(r)}return a})(result)"
```

### 2. 代码逻辑说明

1. **检测验证页面**：检查响应中是否包含验证码特征关键词
2. **自动重试**：最多重试3次，每次等待5秒
3. **WebView处理**：使用WebView加载页面让用户手动完成验证
4. **验证成功**：返回正常页面内容

### 3. 自定义检测关键词

根据实际检测到的WAF类型，添加相应的检测关键词：

```javascript
// 在条件判断中添加新的WAF检测
o.includes('Your_WAF_Keyword')
```

---

## 检测流程

### 建议的检测顺序

1. **第一步：访问首页**
   ```bash
   curl -L "https://example.com/"
   ```

2. **第二步：测试搜索**
   ```bash
   curl -X POST -d "keyword=test" "https://example.com/search/"
   ```

3. **第三步：检查响应**
   - 检查HTTP状态码
   - 检查HTML内容是否包含验证特征
   - 记录检测到的WAF类型

4. **第四步：配置处理**
   - 根据WAF类型选择合适的处理代码
   - 添加相应的检测关键词

---

## 注意事项

1. **不要凭经验猜测** - 必须实际访问网站进行测试
2. **不同页面可能不同** - 首页、搜索页、详情页可能有不同的验证机制
3. **IP可能被封** - 频繁访问可能导致临时封禁
4. **WebView不是万能的** - 某些高级验证可能无法通过脚本处理

---

## 搜索结果中的人机验证处理

当搜索请求触发人机验证时，可以在 bookList 规则中检测并处理：

### 检测验证标记

某些网站在触发验证时会返回特定标记：

```javascript
// bookList 规则示例
"<js>\nif(result.match(/_____tmd_____/)){\n\tvar xb = baseUrl;\n\tjava.startBrowserAwait(xb, \"验证\");\n\tresult = java.ajax(xb);\n}\nresult\n</js>\n.qk-card a"
```

**处理流程**：
1. 检测返回内容中是否包含验证标记（如 `_____tmd_____`）
2. 如果触发验证，调用 `java.startBrowserAwait()` 打开浏览器让用户手动验证
3. 验证完成后重新请求获取正常结果

### 常见验证标记

| 验证类型 | 特征标记 |
|----------|----------|
| 自定义验证 | `_____tmd_____`, `verify`, `captcha` |
| Cloudflare | `Just a moment`, `cf-browser-verification` |
| GoEdge WAF | `GOEDGE_WAF_CAPTCHA` |

### 完整示例

```json
{
  "ruleSearch": {
    "bookList": "<js>\nif(result.match(/_____tmd_____/)){\n\txb=baseUrl\n\tjava.startBrowserAwait(xb,\"验证\")\n\tresult=java.ajax(xb)\n}\nresult\n</js>\n.qk-card a\n@js:\nvar list = [];\nfor (var i = 0; i < result.length; i++) {\n\tvar e = result[i];\n\tvar se = String(e);\n\tif (se.includes(\"libahao.com\")) {\n\t\tlist.push(e)\n\t}\n}\nlist"
  }
}
```

### 注意事项

1. **验证标记需要实际测试确定** - 不同网站的验证标记不同
2. **验证后需要重新请求** - 使用 `java.ajax()` 重新获取结果
3. **用户体验** - 在书源注释中提醒用户可能触发验证

---

## loginCheckJs 验证检测

使用 `loginCheckJs` 字段可以在每次请求时自动检测验证码：

### 百度安全验证检测

```javascript
"loginCheckJs": "var src = result.body();\nif (src.match(/百度安全验证/)) {\n    cookie.removeCookie(source.bookSourceUrl);\n    let url = result.url();\n    java.startBrowserAwait(url, \"验证\");\n    result = java.connect(url);\n}\nresult;"
```

**处理流程**：
1. 获取响应内容 `result.body()`
2. 检测是否包含"百度安全验证"
3. 如果触发验证：
   - 清除Cookie：`cookie.removeCookie(source.bookSourceUrl)`
   - 打开浏览器让用户验证：`java.startBrowserAwait(url, "验证")`
   - 验证后重新请求：`result = java.connect(url)`
4. 返回处理后的结果

### loginCheckJs 与 bookList 验证处理的区别

| 方式 | 适用场景 | 触发时机 |
|------|----------|----------|
| `loginCheckJs` | 全局验证检测 | 每次请求都会检测 |
| `bookList` 中的JS | 搜索结果验证 | 仅搜索时检测 |

### 常见验证检测关键词

| 验证类型 | 检测关键词 |
|----------|------------|
| 百度安全验证 | `百度安全验证` |
| Cloudflare | `Just a moment`, `Checking your browser` |
| GoEdge WAF | `GOEDGE_WAF_CAPTCHA`, `Verify Yourself` |
| 自定义验证 | `_____tmd_____`, `captcha`, `verify` |

### 完整示例

```json
{
  "loginCheckJs": "var src = result.body();\nif (src.match(/百度安全验证/)) {\n    cookie.removeCookie(source.bookSourceUrl);\n    let url = result.url();\n    java.startBrowserAwait(url, \"验证\");\n    result = java.connect(url);\n}\nresult;",
  "header": "{\"User-Agent\": \"Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36\"}"
}
```

**注意事项**：
1. `loginCheckJs` 会增加每次请求的处理时间
2. 需要配合 `webView: true` 使用
3. 清除Cookie后需要用户重新验证

---

## 频繁刷新检测与提示

当网站对频繁访问有限制时，可以在规则中检测并提示用户：

### 检测频繁刷新限制

```javascript
// bookList 规则示例
"<js>\nif(result.match(/Tis/)){\n\tjava.toast('请不要频繁刷新，请休息几秒再试吧');\n}\nif(result.match(/Just a moment/)){\n\tjava.startBrowserAwait(baseUrl, \"验证\");\n\tresult = java.ajax(baseUrl);\n}\nresult;\n</js>\n.x-book"
```

### 多种检测组合

```javascript
// 同时检测多种情况
"<js>\n" +
"// 检测频繁刷新\n" +
"if(result.match(/Tis|频繁|请稍候/)){\n" +
"\tjava.toast('请不要频繁刷新，请休息几秒再试吧');\n" +
"}\n" +
"// 检测Cloudflare验证\n" +
"if(result.match(/Just a moment/)){\n" +
"\tjava.startBrowserAwait(baseUrl, \"验证\");\n" +
"\tresult = java.ajax(baseUrl);\n" +
"}\n" +
"result;\n" +
"</js>\n.x-book"
```

### 常见限制检测关键词

| 限制类型 | 检测关键词 | 处理方式 |
|----------|------------|----------|
| 频繁刷新 | `Tis`, `频繁`, `请稍候` | 提示用户等待 |
| Cloudflare | `Just a moment` | 打开浏览器验证 |
| 自定义验证 | `_____tmd_____`, `验证` | 打开浏览器验证 |
| IP封禁 | `禁止访问`, `blocked` | 提示用户更换网络 |

### 正文页验证检测

在正文规则中同样可以检测验证：

```javascript
// ruleContent.content 规则示例
"<js>\nif(result.match(/请稍候/)){\n\tjava.startBrowserAwait(baseUrl, \"验证\");\n\tresult = java.ajax(baseUrl);\n}\nresult;\n</js>\n.read-section@p@html"
```

### 完整示例

```json
{
  "ruleSearch": {
    "bookList": "<js>\nif(result.match(/Tis/)){\n\tjava.toast('请不要频繁刷新，请休息几秒再试吧');\n}\nif(result.match(/Just a moment/)){\n\tjava.startBrowserAwait(baseUrl, \"验证\");\n\tresult = java.ajax(baseUrl);\n}\nresult;\n</js>\n.x-book"
  },
  "ruleContent": {
    "content": "<js>\nif(result.match(/请稍候/)){\n\tjava.startBrowserAwait(baseUrl, \"验证\");\n\tresult = java.ajax(baseUrl);\n}\nresult;\n</js>\n.read-section@p@html"
  }
}
```

### 处理流程

```
请求页面
    ↓
检测响应内容
    ↓
┌─────────────────┐
│ 频繁刷新提示？   │──是──→ java.toast() 提示用户
└─────────────────┘
    │否
    ↓
┌─────────────────┐
│ 验证码页面？     │──是──→ java.startBrowserAwait() 打开浏览器
└─────────────────┘         ↓
    │否                 重新请求 java.ajax()
    ↓
返回正常内容
```

### 注意事项

1. **提示信息要明确**：告诉用户具体原因和解决方法
2. **验证后重新请求**：使用 `java.ajax(baseUrl)` 重新获取内容
3. **多个检测按顺序**：先检测提示，再检测验证
4. **书源注释提醒**：在 `bookSourceComment` 中提醒用户可能遇到的情况
