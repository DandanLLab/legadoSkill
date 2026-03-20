# JavaScript开发完整指南

本文档详细说明Legado书源开发中的JavaScript使用方法。

## 目录

1. [环境配置](#环境配置)
2. [核心变量表](#核心变量表)
3. [网络请求方法](#网络请求方法)
4. [编码解码方法](#编码解码方法)
5. [加密解密方法](#加密解密方法)
6. [内容解析方法](#内容解析方法)
7. [缓存管理方法](#缓存管理方法)
8. [书源与书籍操作](#书源与书籍操作)
9. [Cookie管理](#cookie管理)
10. [文件操作方法](#文件操作方法)
11. [工具函数](#工具函数)
12. [登录相关方法](#登录相关方法)
13. [参数传递与多数据源合并](#参数传递与多数据源合并)
14. [动态获取发现规则](#动态获取发现规则高级技巧)
15. [jsLib 公共函数库](#jslib-公共函数库)
16. [多类型切换机制](#多类型切换机制)
17. [book.type 动态设置](#booktype-动态设置)

---

## 环境配置

| 配置项 | 说明 |
|--------|------|
| JavaScript引擎 | Rhino 1.8.0 |
| 变量声明 | 必须使用 `var`，避免使用 `const`/`let`（块级作用域问题） |
| Java调用 | 使用 `Packages.java.*` 访问Java包 |

---

## 核心变量表

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `java` | 当前类 | 主要功能入口，万能工具箱 |
| `baseUrl` | String | 当前页面URL |
| `result` | Any | 上一步结果 |
| `book` | Book类 | 书籍信息操作 |
| `chapter` | Chapter类 | 章节信息操作 |
| `source` | BaseSource类 | 书源配置操作 |
| `cookie` | CookieStore类 | Cookie管理 |
| `cache` | CacheManager类 | 缓存管理 |
**要注意这几个变量是阅读自带的，以后定义一个新变量时要避免使用这些变量名**
---

## 网络请求方法

```javascript
// 简单请求
java.ajax(url)                    // 返回字符串
java.connect(url)                 // 返回 StrResponse

// HTTP 方法
java.get(url, headers, timeout)   // GET 请求，返回字符串
java.post(url, body, headers, timeout) // POST 请求，返回字符串
java.head(url, headers, timeout)

// 并发请求
java.ajaxAll(urlList)             // 批量请求

// WebView 请求
java.webView(html, url, js)       // 执行 JS 获取内容
java.webViewGetOverrideUrl(html, url, js, regex)  // 获取跳转 URL
java.webViewGetSource(html, url, js, regex)       // 获取资源 URL
```

### 网络请求方法详细对比

| 方法 | 返回值 | 复杂度 | 适用场景 | 示例 |
|------|--------|--------|----------|------|
| `java.get(url)` | String | 简单 | 快速获取网页 HTML | `var html = java.get('https://example.com/');` |
| `java.ajax(url)` | String | 中等 | 需要书源配置支持的请求 | `var html = java.ajax('https://example.com/');` |
| `java.connect(url)` | StrResponse | 中等 | 需要获取状态码等元数据 | `var resp = java.connect(url); var html = resp.body;` |
| `java.get(url, headers, timeout)` | String | 复杂 | 需要自定义请求头 | `var html = java.get(url, headers, 10000);` |
| `java.post(url, body, headers, timeout)` | String | 复杂 | POST 请求 | `var html = java.post(url, body, headers, 10000);` |

**核心区别：**

1. **`java.get(url)`** - 最简单的 GET 请求，直接返回 HTML 字符串，适合快速抓取网页
2. **`java.ajax(url)`** - 功能更强大，支持书源配置（如 Cookie、请求头等），返回 HTML 字符串
3. **`java.connect(url)`** - 返回 StrResponse 对象，可访问 `body`（内容）、`code`（状态码）等属性
4. **`java.get(url, headers, timeout)`** - 可自定义请求头和超时时间的 GET 请求
5. **`java.post(url, body, headers, timeout)`** - POST 请求，用于提交数据

**选择建议：**
- 简单抓取网页 → 使用 `java.get(url)`
- 需要书源配置支持 → 使用 `java.ajax(url)`
- 需要检查状态码 → 使用 `java.connect(url)`
- 需要自定义请求头 → 使用 `java.get(url, headers, timeout)`
- 提交表单数据 → 使用 `java.post(url, body, headers, timeout)`
- 注意使用时要把url参数补全
---

## 编码解码方法

```javascript
// Base64编码
java.base64Encode(str)
java.base64Encode(str, flags)
java.base64Decode(str)
java.base64Decode(str, charset)

// 十六进制编码
java.hexEncodeToString(str)
java.hexDecodeToString(hex)
java.hexDecodeToByteArray(hex)

// URL编码
java.encodeURI(str)
java.encodeURI(str, "UTF8")

// 字符集转换
java.strToBytes(str, "UTF8")      // 字符串转字节
java.bytesToStr(bytes, "GBK")     // 字节转字符串
```

---

## 加密解密方法

```javascript
// 对称加密（AES等）
var cipher = java.createSymmetricCrypto("AES/CBC/PKCS5Padding", key, iv)
cipher.encryptHex(data)           // 加密为HEX
cipher.encryptBase64(data)        // 加密为Base64
cipher.decryptStr(encryptedData)  // 解密为字符串

// 非对称加密（RSA）
var rsa = java.createAsymmetricCrypto("RSA")
rsa.setPublicKey(publicKey)
rsa.encryptBase64(data, true)     // 使用公钥加密

// 摘要算法
java.md5Encode(str)               // MD5编码
java.md5Encode16(str)             // 16位MD5
java.digestHex(data, "SHA256")    // SHA256
java.digestBase64Str(data, "SHA1") // SHA1 Base64

// HMAC算法
java.HMacHex(data, "HmacSHA256", key)
java.HMacBase64(data, "HmacMD5", key)

// 签名验证
var sign = java.createSign("SHA256withRSA")
sign.setPrivateKey(privateKey)
sign.signHex(data)                // 生成签名
```

---

## 内容解析方法

```javascript
// 文本提取
java.getString(ruleStr, content, isUrl)
java.getStringList(ruleStr, content, isUrl)

// 元素提取
java.getElement(ruleStr)
java.getElements(ruleStr)

// 内容设置
java.setContent(content, baseUrl)

// 重新获取机制
java.reGetBook()                  // 重新搜索书籍
java.refreshTocUrl()              // 刷新目录URL
```

---

## 缓存管理方法

```javascript
// 数据库缓存
cache.put(key, value, saveTime)   // 保存（秒）
cache.get(key)                    // 读取
cache.delete(key)                 // 删除

// 文件缓存（大文件）
cache.putFile(key, value, saveTime)
cache.getFile(key)

// 内存缓存（临时）
cache.putMemory(key, value)
cache.getFromMemory(key)
```

---

## 书源与书籍操作

```javascript
// 书源操作
source.getKey()                   // 获取书源URL
source.getVariable()              // 获取书源变量
source.setVariable(data)          // 设置书源变量
source.put(key, value)            // 自定义变量存储
source.get(key)                   // 自定义变量读取

// 登录头管理
source.getLoginHeader()           // 获取登录头
source.putLoginHeader(header)     // 设置登录头
source.removeLoginHeader()        // 清除登录头

// 书籍属性
book.name                         // 书名
book.author                       // 作者
book.coverUrl                     // 封面
book.intro                       // 简介
book.bookUrl                      // 书籍URL
book.tocUrl                       // 目录URL
book.durChapterTitle              // 当前章节
book.durChapterIndex              // 章节索引
book.durChapterPos                // 阅读位置

// 章节属性
chapter.title                     // 章节标题
chapter.url                       // 章节URL
chapter.index                     // 章节序号
chapter.baseUrl                   // 基础URL
```

---

## Cookie管理

```javascript
cookie.getCookie(url)             // 获取Cookie
cookie.setCookie(url, cookieStr)  // 设置Cookie
cookie.replaceCookie(url, cookieStr) // 替换Cookie
cookie.removeCookie(url)          // 删除Cookie
```

---

## 文件操作方法

```javascript
// 下载与读取
java.downloadFile(url)            // 下载文件
java.readTxtFile(path)            // 读取文本文件
java.readTxtFile(path, "UTF8")    // 指定编码读取

// 压缩文件处理
java.unzipFile(zipPath)           // 解压ZIP
java.unrarFile(rarPath)           // 解压RAR
java.un7zFile(archivePath)        // 解压7Z
java.unArchiveFile(archivePath)   // 通用解压

// 文件夹操作
java.getTxtInFolder(folderPath)   // 读取文件夹内所有文本

// 压缩包内容读取
java.getZipStringContent(url, filePath)
java.getRarStringContent(url, filePath, "GBK")
java.get7zByteArrayContent(url, filePath)
```

---

## 工具函数

```javascript
// 调试输出
java.log("调试信息")              // 输出日志
java.logType(variable)            // 输出类型
java.toast("提示信息")            // 短时提示
java.longToast("长提示")          // 长时提示

// 浏览器操作
java.startBrowserAwait(url, title)  // 打开浏览器等待用户操作
```

---

## 登录相关方法

### 获取登录信息

```javascript
// 获取登录信息Map
var info = source.getLoginInfoMap();
var pwd = info.get('访问口令');  // 获取loginUi中定义的字段
pwd = pwd == null ? '' : String(pwd).trim();
```

### 登录UI配置（loginUi）

在书源JSON中配置登录界面：

```json
{
  "loginUi": "[{\"name\":\"访问口令\",\"type\":\"text\",\"style\":{\"layout_flexGrow\":1,\"layout_flexBasisPercent\":1}},\n{\"name\":\"加群获取密码\",\"type\":\"button\",\"action\":\"jq()\",\"style\":{\"layout_flexGrow\":1,\"layout_flexBasisPercent\":0.5}},\n{\"name\":\"请作者喝水\",\"type\":\"button\",\"action\":\"jk()\",\"style\":{\"layout_flexGrow\":1,\"layout_flexBasisPercent\":0.5}}]"
}
```

**loginUi 字段说明**：

| 字段 | 说明 |
|------|------|
| `name` | 显示名称 |
| `type` | 类型：`text`（文本输入）、`button`（按钮） |
| `action` | 按钮点击时执行的JS函数名 |
| `style.layout_flexGrow` | 弹性增长比例 |
| `style.layout_flexBasisPercent` | 基础宽度百分比 |

### 登录函数示例（loginUrl）

```javascript
function login() {
  var info = source.getLoginInfoMap();
  if (!info) throw new Error('请先输入访问口令');
  var pwd = info.get('访问口令');
  pwd = pwd == null ? '' : String(pwd).trim();
  if (!pwd) throw new Error('请先输入访问口令');
  
  var url = 'http://example.com/api?auth=login&pwd=' + encodeURIComponent(pwd);
  var body = java.ajax(url);
  if (!body) throw new Error('接口无响应');
  var res = JSON.parse(String(body));
  if (!res || res.code != 200) throw new Error(res && res.msg ? res.msg : '登录失败');
}

function jk() {
  java.startBrowserAwait("https://example.com/donate.jpg", "感谢支持");
}

function jq() {
  java.startBrowserAwait("https://example.com/group", "加群");
}
```

**关键技术点**：
1. `source.getLoginInfoMap()` 获取用户输入的登录信息
2. `throw new Error()` 抛出错误提示用户
3. `encodeURIComponent()` 对密码进行URL编码
4. `java.startBrowserAwait(url, title)` 打开浏览器供用户查看

---

## 参数传递与多数据源合并

### java.put/java.get 参数传递

在搜索URL中保存参数，供后续规则使用：

```javascript
// searchUrl 中保存参数
"searchUrl": "https://example.com/search?s={{key}}&page={{page}}\n@js:java.put('key',key);java.put('page',page);result"

// 后续规则中读取参数
<js>
key = java.get('key');
page = java.get('page');
// 使用参数进行额外请求
</js>
```

**应用场景**：当需要在多个规则之间共享搜索关键词或页码时使用。

### 多数据源合并技术

同时请求多个API并合并搜索结果：

```javascript
// 搜索规则 bookList 示例
"<js>" +
"key = java.get('key');" +
"page = java.get('page');" +
"" +
"// 创建空数组" +
"json = []; json2 = [];" +
"" +
"// 解析第一个API结果" +
"if(JSON.parse(result).info.Datas){" +
"  json = JSON.parse(result).info.Datas;" +
"}" +
"" +
"// 请求第二个API" +
"json1 = JSON.parse(java.ajax('https://example.com/api2?s=' + key + '&p=' + page));" +
"" +
"// 解析第二个API结果" +
"if(json1.info.Datas){" +
"  json2 = json1.info.Datas;" +
"}" +
"" +
"// 合并两个结果数组" +
"list = json.concat(json2);" +
"result = JSON.stringify(list);" +
"</js>" +
"$.[*]"
```

**关键技术点**：
1. 使用 `java.get()` 获取之前保存的参数
2. 使用 `JSON.parse()` 解析JSON响应
3. 使用 `java.ajax()` 发起额外请求
4. 使用 `concat()` 合并数组
5. 使用 `JSON.stringify()` 转回字符串供后续规则处理

### 条件判断URL生成

根据搜索结果类型动态生成不同的书籍URL：

```javascript
// bookUrl 规则示例
"<js>" +
"id = String(result).match(/id=(\\d+)/)[1];" +
"if(!String(result).match(/catalog_name/)){" +
"  // 单曲类型" +
"  result = 'https://example.com/sound?id=' + id;" +
"} else {" +
"  // 剧集类型" +
"  result = 'https://example.com/drama?id=' + id;" +
"}" +
"</js>"
```

**应用场景**：同一搜索结果中包含不同类型的内容（如有声书单曲vs剧集），需要跳转到不同的详情页。

### 动态目录URL生成

在书籍详情规则中根据当前URL动态生成目录URL：

```javascript
// ruleBookInfo.tocUrl 规则示例
"@js:" +
"if(baseUrl.match(/dramaapi|mdrama/)){" +
"  result = 'https://example.com/api/drama?id=' + baseUrl.match(/(\\d+)/)[1];" +
"}"
```

**应用场景**：详情页URL与目录页URL格式不同，需要根据详情页URL提取ID并构造目录API。

---

## 动态获取发现规则（高级技巧）

当网站分类较多或分类动态变化时，可以使用JavaScript动态获取发现分类：

### 基本结构

```javascript
"exploreUrl": "@js:\nvar result = [];\njava.toast(\"🔥动态获取发现中……\");\n \nvar push = (title, url, size) => result.push({\n    \"title\": title,\n    \"url\": url,\n    \"style\": {\n        \"layout_flexGrow\": 1,\n        \"layout_flexBasisPercent\": size \n    }\n});\n \nvar fl = java.ajax(source.key);\nif (fl) {\n    var a = org.jsoup.Jsoup.parse(fl).select(\".category-list a\");\n    push(\"༺ˇ»`ʚ分类导航ɞ´«ˇ༻\", null, 1);\n    \n    for(var i = 0; i < a.length; i++) {\n        var title = a[i].text();\n        var url = a[i].attr(\"href\");\n        var size = 0.25;\n        url = String(url).replace(/\\/$/, \"/{{page}}.html\");\n        push(title, url, size);\n    };\n} else {\n    java.toast(\"🚫发现获取失败……\");\n}\n \nJSON.stringify(result);"
```

### 关键技术详解

| 技术 | 说明 |
|------|------|
| `var result = []` | 创建空数组存储分类 |
| `java.toast()` | 显示提示信息 |
| `push()` 函数 | 封装添加分类的逻辑 |
| `org.jsoup.Jsoup.parse()` | 解析HTML |
| `source.key` | 获取书源URL |
| `JSON.stringify(result)` | 返回JSON数组 |

### push函数参数说明

```javascript
var push = (title, url, size) => result.push({
    "title": title,           // 分类名称
    "url": url,               // 分类URL（含{{page}}占位符）
    "style": {
        "layout_flexGrow": 1,
        "layout_flexBasisPercent": size  // 按钮宽度比例
    }
});
```

**size参数说明**：
- `1` = 占满一行（标题行）
- `0.5` = 半行宽（两个按钮一行）
- `0.25` = 四分之一行宽（四个按钮一行）
- `0.33` = 三分之一行宽（三个按钮一行）

### 完整示例（带标题分隔）

```javascript
"exploreUrl": "@js:\nvar result = [];\njava.toast(\"🔥动态获取发现中……\");\n \nvar push = (title, url, size) => result.push({\n    \"title\": title,\n    \"url\": url,\n    \"style\": {\n        \"layout_flexGrow\": 1,\n        \"layout_flexBasisPercent\": size \n    }\n});\n \nvar fl = java.ajax(source.key);\nif (fl) {\n    // 添加标题行（url为null，不跳转）\n    push(\"༺ˇ»`ʚ最近更新ɞ´«ˇ༻\", null, 1);\n    \n    // 解析分类列表\n    var a = org.jsoup.Jsoup.parse(fl).select(\".nav-list a\");\n    for(var i = 0; i < a.length; i++) {\n        var title = a[i].text();\n        var url = a[i].attr(\"href\");\n        // 添加分页参数\n        url = String(url).replace(/\\/$/, \"/{{page}}.html\");\n        push(title, url, 0.25);\n    };\n} else {\n    java.toast(\"🚫发现获取失败……\");\n}\n \nJSON.stringify(result);"
```

### URL格式转换技巧

```javascript
// 将 /category/ 转换为 /category/{{page}}.html
url = String(url).replace(/\\/$/, \"/{{page}}.html\");

// 将 /category 转换为 /category_{{page}}.html
url = String(url) + \"_{{page}}.html\";

// 将 /category/ 转换为 /category?page={{page}}
url = String(url).replace(/\\/$/, \"\") + \"?page={{page}}\";
```

### 适用场景

| 场景 | 说明 |
|------|------|
| 分类动态变化 | 网站分类经常更新，不适合写死 |
| 分类数量多 | 分类超过10个，手动编写繁琐 |
| 分类URL规律 | 分类URL格式统一，可程序生成 |
| 多级分类 | 需要从页面解析多级分类结构 |

### 注意事项

1. **性能考虑**：每次打开发现页都会请求一次，可能影响速度
2. **错误处理**：添加 `if (fl)` 判断请求是否成功
3. **用户提示**：使用 `java.toast()` 提示用户加载状态
4. **URL格式**：确保生成的URL包含 `{{page}}` 占位符

---

## jsLib 公共函数库

当多个规则需要共用相同的JavaScript函数时，可以使用 `jsLib` 字段定义公共函数库：

### 基本用法

```json
{
  "jsLib": "function normalizeId(raw, java) {\n    var s = String(raw || '');\n    if (/^\\d{8,}$/.test(s)) return s;\n    var m = s.match(/(\\d{8,})/);\n    return m ? String(m[1]) : '';\n}\n\nfunction formatTime(ts) {\n    ts = Number(ts || 0);\n    if (!isFinite(ts) || ts <= 0) return '刚刚';\n    var now = Math.floor(Date.now() / 1000);\n    var diff = now - ts;\n    if (diff < 60) return '刚刚';\n    if (diff < 3600) return Math.floor(diff / 60) + '分钟前';\n    if (diff < 86400) return Math.floor(diff / 3600) + '小时前';\n    return Math.floor(diff / 86400) + '天前';\n}"
}
```

### 在规则中调用

```javascript
// 在任意规则中直接调用jsLib中定义的函数
"bookId": "@js:normalizeId(result, java)"

"updateTime": "@js:formatTime(result)"
```

### 适用场景

| 场景 | 说明 |
|------|------|
| ID格式化 | 多处需要提取/格式化书籍ID |
| 时间格式化 | 多处需要转换时间戳 |
| HTML转义 | 多处需要转义/反转义HTML |
| 数据清洗 | 多处需要相同的清洗逻辑 |

### 注意事项

1. **函数必须接收java参数**：部分函数需要使用java对象的方法
2. **jsLib中的函数全局可用**：在所有规则中都可以直接调用
3. **避免命名冲突**：不要与Legado内置函数重名

---

## 多类型切换机制

当书源支持多种内容类型（小说/漫画/听书/短剧）时，可以使用类型切换机制：

### 类型存储与读取

```javascript
// 在loginUrl中定义切换函数
function configs(btnText) {
    var typeMap = {
        '小说': 'novel',
        '漫画': 'comic',
        '听书': 'audio',
        '短剧': 'video'
    };
    var type = typeMap[btnText];
    source.put('type', type);
    java.toast('已切换至' + btnText);
}

// 在searchUrl中读取类型
var type = source.get('type');
if (!type || type == "undefined") {
    tab = 3;  // 默认小说
} else {
    switch(type) {
        case 'novel': tab = 3; break;
        case 'comic': tab = 8; break;
        case 'audio': tab = 2; break;
        case 'video': tab = 11; break;
    }
}
```

### 登录界面配置

```json
{
  "loginUi": "[{\"name\":\"小说\",\"type\":\"button\",\"action\":\"configs('小说')\"},{\"name\":\"漫画\",\"type\":\"button\",\"action\":\"configs('漫画')\"},{\"name\":\"听书\",\"type\":\"button\",\"action\":\"configs('听书')\"},{\"name\":\"短剧\",\"type\":\"button\",\"action\":\"configs('短剧')\"}]"
}
```

### 搜索关键词前缀切换

```javascript
// 支持通过关键词前缀快速切换类型
if (String(key).startsWith("m:")) {
    tab = 8;  // 漫画
    source.put('type', 'comic');
    key = key.slice(2);
}
if (String(key).startsWith("t:")) {
    tab = 2;  // 听书
    source.put('type', 'audio');
    key = key.slice(2);
}
```

### 内容规则根据类型处理

```javascript
// 在ruleContent中根据类型返回不同内容
var type = source.get('type');
if (type == 'novel') {
    result = java.ajax(novelUrl);
} else if (type == 'comic') {
    result = java.ajax(comicUrl);
    result = JSON.parse(result).data.images.map(img => '<img src="' + img + '">').join('');
} else if (type == 'audio') {
    result = java.ajax(audioUrl);
    result = JSON.parse(result).data.raw.data[0].backup_url;
}
```

---

## book.type 动态设置

在目录规则中可以根据内容类型动态设置 `book.type`：

```javascript
// chapterUrl 规则
"$.itemId\n<js>\nvar type = source.get('type');\nif (type == 'comic') {\n    book.type = 64;  // 漫画类型\n} else if (type == 'audio') {\n    book.type = 32;  // 音频类型\n} else {\n    book.type = 8;   // 文本类型\n}\nresult = `data:;base64,${java.base64Encode(result)}`;\n</js>"
```

### book.type 值说明

| 值 | 类型 | 说明 |
|----|------|------|
| 0 | 文本 | 默认小说类型 |
| 1 | 音频 | 有声书 |
| 2 | 图片 | 漫画 |
| 8 | 文本 | 普通文本 |
| 32 | 音频 | 音频文件 |
| 64 | 图片 | 图片文件 |

### 应用场景

- 同一书源支持多种内容类型
- 需要根据类型使用不同的阅读器
- 漫画需要图片阅读器，听书需要音频播放器
