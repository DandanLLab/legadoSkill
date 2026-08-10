# 初五小说

## 基本信息
- **书源名称**: 初五小说
- **书源地址**: https://www.clljcw.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

搜索间隔20秒

## 规则配置

### 搜索URL
```js
https://www.clljcw.com/search.html,{"method":"POST","body":"s={{key}}"}
```

### 搜索规则
```js
{
  "author": ".s5@text##^\\s+",
  "bookList": ".sort_list li",
  "bookUrl": ".s2 a@href",
  "name": ".s2 a@text"
}
```

### 发现URL
```js
[{"title": "玄幻小说", "url": "/list/lastupdate_1_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}, {"title": "武侠小说", "url": "/list/lastupdate_2_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}, {"title": "都市小说", "url": "/list/lastupdate_3_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}, {"title": "军史小说", "url": "/list/lastupdate_4_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}, {"title": "网游小说", "url": "/list/lastupdate_5_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}, {"title": "科幻小说", "url": "/list/lastupdate_6_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}, {"title": "灵异小说", "url": "/list/lastupdate_7_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}, {"title": "其他小说", "url": "/list/lastupdate_8_0_0_{{page}}.html", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.25}}]
```

### 发现规则
```js
{
  "author": ".s4@text",
  "bookList": ".sort_list li",
  "bookUrl": ".s2 a@href",
  "kind": ".s1@text##\\[|\\]",
  "lastChapter": ".s2 a@title##最新章节：",
  "name": ".s2 a@text"
}
```

### 详情规则
```js
{
  "author": "[property=\"og:novel:author\"]@content",
  "coverUrl": "[property=\"og:image\"]@content",
  "intro": "[property=\"og:description\"]@content",
  "kind": "[property=\"og:novel:category\"]@content",
  "lastChapter": "[property=\"og:novel:latest_chapter_name\"]@content",
  "name": "[property=\"og:novel:book_name\"]@content"
}
```

### 目录规则
```js
{
  "chapterList": "<js>\nvar html = String(result);\nvar url = String(baseUrl);\nvar isMl = url.indexOf('/ml') !== -1;\nvar su = source.getKey();\nvar bookPath = url.replace(su, '').replace(/^\\//, '').split('/')[0];\nvar base = su + '/' + bookPath + '/';\nif (!isMl) {\n    html = String(java.ajax(base + 'ml1.html'));\n}\nvar opts = html.match(/ml(\\d+)\\.html/g);\nvar maxPage = 1;\nif (opts) {\n    for (var i = 0; i < opts.length; i++) {\n        var p = parseInt(opts[i].match(/\\d+/)[0]);\n        if (p > maxPage) maxPage = p;\n    }\n}\nvar allItems = '';\nfor (var p = 1; p <= maxPage; p++) {\n    var pageHtml = (p === 1) ? html : String(java.ajax(base + 'ml' + p + '.html'));\n    var ulMatch = pageHtml.match(/<ul class=\"chapter-list\">([\\s\\S]*?)<\\/ul>/);\n    if (ulMatch) {\n        allItems += ulMatch[1];\n    }\n}\nresult = allItems;\n</js>li a",
  "chapterName": "text",
  "chapterUrl": "href"
}
```

### 正文规则
```js
{
  "content": "<js>\nvar html = String(result);\nvar blocks = html.match(/writeln\\([^;]*?'([A-Za-z0-9+/=]+)'\\)/g);\nvar content = '';\nif (blocks) {\n    for (var i = 0; i < blocks.length; i++) {\n        var m = blocks[i].match(/'([A-Za-z0-9+/=]+)'/);\n        if (m) {\n            content += String(java.base64Decode(m[1], 'utf-8'));\n        }\n    }\n}\ncontent = content.replace(/\\[split\\]/g, '');\nvar nm = html.match(/var hhekgsv='([^']+)'/);\nif (nm) {\n    var nextUrl = nm[1];\n    var curFile = String(baseUrl).split('/').pop();\n    var nextFile = nextUrl.split('/').pop();\n    var curBase = curFile.replace(/_\\d+\\.html.*/, '.html');\n    var nextBase = nextFile.replace(/_\\d+\\.html.*/, '.html');\n    java.put('clljcw_next', curBase === nextBase ? nextUrl : '');\n} else {\n    java.put('clljcw_next', '');\n}\nresult = content;\n</js>",
  "nextContentUrl": "<js>\nresult = java.get('clljcw_next') || '';\n</js>"
}
```

### 登录配置
```js
loginUrl:
https://www.clljcw.com/login.html
```

## 技术分析

### 核心技术点

- 需要登录（CookieJar + loginUrl）
- CookieJar已启用，自动管理登录状态
- writeln加密（JS动态输出正文）
- 正文分页处理（nextContentUrl）
- bookUrlPattern: https://www.clljcw.com/.*/
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐⭐
