# 书源模板参考

本文档包含多个真实书源模板，供创建书源时参考。

## 目录

1. [模板1：笔趣阁（Default推荐）](#模板1笔趣阁default推荐)
2. [模板2：69书吧（POST请求）](#模板269书吧post请求)
3. [模板3：qs中文网（JSONPath，API型）](#模板3qs中文网jsonpathapi型)
4. [模板4：新笔趣阁（XPath）](#模板4新笔趣阁xpath)
5. [模板5：猫耳FM（有声书，WebView搜索）](#模板5猫耳fm有声书webview搜索)
6. [模板6：狗耳听书（有声书，多数据源合并）](#模板6狗耳听书有声书多数据源合并)
7. [模板7：星辰书库（登录验证，发现页JSON数组）](#模板7星辰书库登录验证发现页json数组)
8. [有"下一章"按钮的书源](#有下一章按钮的书源)
9. [错误示例](#错误示例)

---

## 模板1：笔趣阁（Default推荐）

**特点**：
- 使用Default语法（推荐）
- 简洁的选择器
- 复杂选择器使用@css前缀
- 正则表达式清理内容

```js
{
  "bookSourceName": "笔趣阁",
  "bookSourceUrl": "https://www.biquge.com",
  "bookSourceType": 0,
  "searchUrl": "/search.php?q={{key}}",
  "ruleSearch": {
    "bookList": "class.result-list@class.result-item",
    "name": "class.result-game-item-title-link@text",
    "author": "@css:.result-game-item-info-tag:nth-child(1)@text##作\\s*者：",
    "bookUrl": "class.result-game-item-title-link@href",
    "coverUrl": "class.result-game-item-pic@tag.img@src",
    "intro": "class.result-game-item-desc@text"
  },
  "ruleBookInfo": {
    "name": "id.info@tag.h1@text",
    "author": "@css:#info p:nth-child(1)@text##作.*?：",
    "coverUrl": "id.fmimg@tag.img@src",
    "intro": "id.intro@text",
    "lastChapter": "@css:#info p:nth-child(4) a@text"
  },
  "ruleToc": {
    "chapterList": "id.list@tag.dd@tag.a",
    "chapterName": "text",
    "chapterUrl": "href"
  },
  "ruleContent": {
    "content": "id.content@html##<script[\\s\\S]*?</script>|请收藏.*"
  }
}
```

---

## 模板2：69书吧（POST请求）

**特点**：
- 使用POST请求
- body必须用String()类型
- 支持GBK编码
- 使用Default+XPath语法

```js
{
  "bookSourceName": "69书吧",
  "bookSourceUrl": "https://www.69shuba.com",
  "bookSourceType": 0,
  "searchUrl": "/modules/article/search.php,{\"method\":\"POST\",\"body\":\"searchkey={{key}}&searchtype=all\",\"charset\":\"gbk\"}",
  "ruleSearch": {
    "bookList": "class.newbox@tag.li",
    "name": "tag.a.0@text",
    "author": "tag.span.-1@text##.*：",
    "bookUrl": "tag.a.0@href",
    "coverUrl": "tag.img@src"
  },
  "ruleBookInfo": {
    "name": "class.booknav2@tag.h1@text",
    "author": "class.booknav2@tag.a.0@text",
    "coverUrl": "class.bookimg2@tag.img@src",
    "intro": "class.navtxt@tag.p.-1@text",
    "kind": "class.booknav2@tag.a.1@text",
    "lastChapter": "class.qustime@tag.a@text"
  },
  "ruleToc": {
    "chapterList": "id.catalog@tag.li",
    "chapterName": "tag.a@text",
    "chapterUrl": "tag.a@href"
  },
  "ruleContent": {
    "content": "class.txtnav@html##<p>.*?</p>|<script[\\s\\S]*?</script>"
  }
}
```

---

## 模板3：qs中文网（JSONPath，API型）

```json
{
  "bookSourceName": "qs中文网",
  "bookSourceUrl": "https://m.qidian.com",
  "bookSourceType": 0,
  "searchUrl": "https://m.qidian.com/majax/search/list?kw={{key}}&pageNum={{page}}",
  "ruleSearch": {
    "bookList": "$.data.records",
    "name": "$.bName",
    "author": "$.bAuth",
    "bookUrl": "https://m.qidian.com/book/{{$.bid}}",
    "coverUrl": "https://bookcover.yuewen.com/qdbimg/349573/{{$.bid}}/150"
  },
  "ruleToc": {
    "chapterList": "$.data.vs[*].cs[*]",
    "chapterName": "$.cN",
    "chapterUrl": "https://m.qidian.com/book/{{$.bid}}/{{$.id}}"
  },
  "ruleContent": {
    "content": "$.data.content"
  }
}
```

---

## 模板4：新笔趣阁（XPath）

```json
{
  "bookSourceName": "新笔趣阁",
  "bookSourceUrl": "https://www.xbiquge.la",
  "bookSourceType": 0,
  "searchUrl": "/search.php?keyword={{key}}",
  "ruleSearch": {
    "bookList": "//div[@class=\"result-item\"]",
    "name": "//h3/a/text()",
    "author": "//p[@class=\"result-game-item-info-tag\"][1]/span[2]/text()",
    "bookUrl": "//h3/a/@href"
  },
  "ruleToc": {
    "chapterList": "//div[@id=\"list\"]/dl/dd/a",
    "chapterName": "/text()",
    "chapterUrl": "/@href"
  },
  "ruleContent": {
    "content": "//div[@id=\"content\"]"
  }
}
```

---

## 模板5：猫耳FM（有声书，WebView搜索）

```json
{
  "bookSourceName": "猫耳FM",
  "bookSourceUrl": "https://www.missevan.com",
  "bookSourceType": 1,
  "searchUrl": "https://www.missevan.com/dramaapi/search?s={{key}}&page=1",
  "ruleSearch": {
    "bookList": "$.info.Datas",
    "name": "$.name",
    "author": "$.author",
    "bookUrl": "https://www.missevan.com/mdrama/drama/{{$.id}},{\"webView\":true}"
  },
  "ruleContent": {
    "content": "https://static.missevan.com/{{//*[contains(@class,\"pld-sound-active\")]/@data-soundurl64}}",
    "sourceRegex": ".*\\.(mp3|m4a).*"
  }
}
```

---

## 模板6：狗耳听书（有声书，多数据源合并）

**特点**：
- bookSourceType = 1（有声书）
- 多数据源合并：同时搜索剧集和单曲
- java.put/get 参数传递
- 条件判断URL生成
- 动态目录URL生成

```json
{
  "bookSourceName": "狗耳听书",
  "bookSourceUrl": "https://www.abcd.com",
  "bookSourceType": 1,
  "enabledCookieJar": true,
  "searchUrl": "https://www.abcd.com/dramaapi/search?s={{key}}&page={{page}}\n@js:java.put('key',key);java.put('page',page);result",
  "ruleSearch": {
    "author": "$.username||$.author",
    "bookList": "<js>\nkey=java.get('key');\npage=java.get('page');\n\njson=[];json2=[];\n\nif(JSON.parse(result).info.Datas){\njson=JSON.parse(result).info.Datas;\n}\n\njson1=JSON.parse(java.ajax('https://www.abcd.com/sound/getsearch?s='+key+'&type=3&page_size=10&p='+page));\n\nif(json1.info.Datas){\njson2=json1.info.Datas\n}\n\nlist=json.concat(json2);\nresult=JSON.stringify(list)\n</js>\n$.[*]",
    "bookUrl": "<js>\nid=String(result).match(/id=(\\d+)/)[1];\nif(!String(result).match(/catalog_name/)){\nresult='https://www.abcd.com/sound/getsound?soundid='+id\n}else{result='https://www.abcd.com/dramaapi/getdrama?drama_id='+id}\n</js>",
    "coverUrl": "$.front_cover||$.cover",
    "intro": "$.abstract",
    "kind": "{$.type_name},{$.catalog_name}##\\{.*?\\}",
    "lastChapter": "$.newest",
    "name": "$.soundstr||$.name"
  },
  "ruleBookInfo": {
    "intro": "class.intro-content@html||$.info.sound.intro",
    "kind": "class.detail-count@text&&class.detail-newest@text&&class.detail-author@text&&class.detail-type@text&&class.detail-tags@text##类型：|标签：无|标签：",
    "tocUrl": "@js:\nif(baseUrl.match(/dramaapi|mdrama/)){\nresult='https://www.abcd.com/dramaapi/getdrama?drama_id='+baseUrl.match(/(\\d+)/)[1]\n}"
  },
  "ruleContent": {
    "content": "$.info.sound.soundurl_128||$.info.sound.soundurl"
  },
  "ruleExplore": {
    "bookList": "$.info.Datas",
    "bookUrl": "https://www.abcd.com/mdrama/drama/{{$.id}},{\"webView\":true}",
    "coverUrl": "$.cover",
    "kind": "$.type_name",
    "lastChapter": "$.newest",
    "name": "$.name"
  },
  "ruleToc": {
    "chapterList": "<js>'['+result+']'</js>\n$..info.episodes.episode[*]||$..info.episodes.music[*]||$.[*]",
    "chapterName": "$.name||$.info.sound.soundstr",
    "chapterUrl": "https://www.abcd.com/sound/getsound?soundid={{$.sound_id||$.info.sound.id}}"
  }
}
```

**关键技术详解**：

| 技术 | 说明 |
|------|------|
| `java.put('key',key)` | 在searchUrl中保存搜索关键词 |
| `java.get('key')` | 在后续规则中读取保存的关键词 |
| `json.concat(json2)` | 合并两个搜索结果数组 |
| `$.field1||$.field2` | JSONPath多字段备选 |
| `if(!match())` | 条件判断生成不同URL |
| `baseUrl.match()` | 根据当前URL动态生成目录URL |

---

## 模板7：星辰书库（登录验证，发现页JSON数组）

**特点**：
- 自定义登录UI（loginUi）
- 登录验证函数（loginUrl）
- 发现页使用JSON数组格式
- 预设关键词搜索作为发现页
- 自定义请求头（header）
- 并发率控制（concurrentRate）

```json
{
  "bookSourceName": "星辰书库",
  "bookSourceUrl": "http://example.com/api.php",
  "bookSourceType": 0,
  "concurrentRate": "1200",
  "enabledCookieJar": true,
  "enabledExplore": true,
  "header": "{\"X-HDS-Client\":\"xingchen-legado\",\"X-HDS-Version\":\"20260320\"}",
  "loginUi": "[{\"name\":\"访问口令\",\"type\":\"text\",\"style\":{\"layout_flexGrow\":1,\"layout_flexBasisPercent\":1}},{\"name\":\"加群获取密码\",\"type\":\"button\",\"action\":\"jq()\",\"style\":{\"layout_flexGrow\":1,\"layout_flexBasisPercent\":0.5}},{\"name\":\"请作者喝水\",\"type\":\"button\",\"action\":\"jk()\",\"style\":{\"layout_flexGrow\":1,\"layout_flexBasisPercent\":0.5}}]",
  "loginUrl": "function login(){var info=source.getLoginInfoMap();if(!info)throw new Error('请先输入访问口令');var pwd=info.get('访问口令');pwd=pwd==null?'':String(pwd).trim();if(!pwd)throw new Error('请先输入访问口令');var url='http://example.com/api?auth=login&pwd='+encodeURIComponent(pwd);var body=java.ajax(url);if(!body)throw new Error('接口无响应');var res=JSON.parse(String(body));if(!res||res.code!=200)throw new Error(res&&res.msg?res.msg:'登录失败');}\nfunction jk(){java.startBrowserAwait(\"https://example.com/donate.jpg\",\"感谢支持\")}\nfunction jq(){java.startBrowserAwait(\"https://example.com/group\",\"加群\")}",
  "exploreUrl": "[{\"title\":\"都市\",\"url\":\"http://example.com/api?kw=%E9%83%BD%E5%B8%82&page={{page}}\"},{\"title\":\"总裁\",\"url\":\"http://example.com/api?kw=%E6%80%BB%E8%A3%81&page={{page}}\"},{\"title\":\"穿越\",\"url\":\"http://example.com/api?kw=%E7%A9%BF%E8%B6%8A&page={{page}}\"}]",
  "searchUrl": "http://example.com/api?kw={{key}}&page={{page}}",
  "ruleSearch": {
    "author": "author",
    "bookList": "data[*]",
    "bookUrl": "detail_url",
    "coverUrl": "cover_url",
    "intro": "intro",
    "kind": "cate_name",
    "name": "title"
  },
  "ruleBookInfo": {
    "author": "data.novel_info.author",
    "coverUrl": "data.novel_info.cover_url",
    "intro": "data.novel_info.intro",
    "kind": "data.novel_info.cate_name",
    "lastChapter": "data.novel_info.last_chapter_title.chapter_title",
    "name": "data.novel_info.title"
  },
  "ruleToc": {
    "chapterList": "data.novel_detail.list[*]",
    "chapterName": "chapter_title",
    "chapterUrl": "chapter_url"
  },
  "ruleContent": {
    "content": "all"
  },
  "ruleExplore": {
    "author": "author",
    "bookList": "data[*]",
    "bookUrl": "detail_url",
    "coverUrl": "cover_url",
    "intro": "intro",
    "kind": "cate_name",
    "name": "title"
  }
}
```

**关键技术详解**：

| 技术 | 说明 |
|------|------|
| `loginUi` | JSON数组配置登录界面，支持文本输入和按钮 |
| `loginUrl` | 登录验证函数，使用 `source.getLoginInfoMap()` 获取输入 |
| `exploreUrl` JSON数组 | 每个分类包含 `title` 和 `url` 字段 |
| `header` | 自定义请求头，JSON字符串格式 |
| `concurrentRate` | 并发率控制，单位毫秒 |
| `throw new Error()` | 抛出错误提示用户 |
| `java.startBrowserAwait()` | 打开浏览器供用户查看图片或链接 |
| `%E9%83%BD%E5%B8%82` | URL编码的中文关键词（都市） |

**发现页JSON数组格式**：
```json
[
  {"title": "分类名", "url": "分类URL_{{page}}"},
  {"title": "分类名2", "url": "分类URL2_{{page}}"}
]
```

---

## 有"下一章"按钮的书源

```js
{
  "bookSourceName": "示例书源",
  "bookSourceUrl": "https://example.com",
  "bookSourceType": 0,
  "ruleContent": {
    "content": "#chaptercontent@html##广告[\\s\\S]*?##",
    "nextContentUrl": "text.下一章@href"  // 正确：使用 text.文本 格式
  }
}
```

---

## 错误示例

**错误示例（不要模仿）**：
```js
{
  "ruleContent": {
    "content": "#chaptercontent@html##广告[\\s\\S]*?##",
    "nextContentUrl": "a:contains(下一章)@href",  // 错误：不能使用 :contains()
    "prevContentUrl": "text.上一章@href"           // 错误：Legado中没有 prevContentUrl
  }
}
```

---

## 真实书源分析结果要点（134个书源）

### 最常用CSS选择器（Top 10）
- `img` (40次) - 图片元素（封面）
- `h1` (30次) - 一级标题（书名）
- `div` (13次) - 通用容器
- `content` (12次) - 内容区域（正文）
- `intro` (11次) - 简介
- `h3` (9次) - 三级标题（章节名）
- `span` (9次) - 通用行内元素
- `a` (多次) - 链接元素

### 最常用提取类型（Top 5）
- `@href` (81次) - 链接地址
- `@text` (72次) - 文本内容
- `@src` (60次) - 图片地址
- `@html` (33次) - HTML结构
- `@js` (25次) - JavaScript处理

### 常见书源结构模式
1. **标准小说站**：有封面、完整信息、独立标签
2. **笔趣阁类**：无封面、信息合并、需要正则拆分
3. **聚合源（API型）**：返回JSON、使用JSONPath提取
4. **漫画站点**：图片封面、漫画专属字段

### 特殊功能使用
- 正则表达式：42次（清理前缀后缀、提取特定内容）
- XPath：24次（复杂选择）
- JavaScript处理：8次（复杂逻辑）
- JSONPath：6次（API型书源）
