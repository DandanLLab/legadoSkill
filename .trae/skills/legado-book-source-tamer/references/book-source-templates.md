# 书源模板参考

本文档包含多个真实书源模板，供创建书源时参考。

## 目录

1. [模板1：笔趣阁（Default推荐）](#模板1笔趣阁default推荐)
2. [模板2：69书吧（POST请求）](#模板269书吧post请求)
3. [模板3：qs中文网（JSONPath，API型）](#模板3qs中文网jsonpathapi型)
4. [模板4：新笔趣阁（XPath）](#模板4新笔趣阁xpath)
5. [模板5：猫耳FM（有声书，WebView）](#模板5猫耳fm有声书webview)
6. [有"下一章"按钮的书源](#有下一章按钮的书源)
7. [错误示例](#错误示例)

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

## 模板5：猫耳FM（有声书，WebView）

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
