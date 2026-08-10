# 热门小说网

## 基本信息
- **书源名称**: 热门小说网
- **书源地址**: https://www.remexs.org
- **书源分组**: AI,18加
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

本书源难点：目录详情页60章，目录页61开始。正文加密。
【技术实现】
搜索：POST搜索（/search.html，body: s={{key}}），搜索前去cookie防间隔限制
发现：CSS选择器（分类页 .outdiv 卡片）
详情：og:novel 元数据
目录：详情页获取前60章 + nextTocUrl跳转至TOC页 + JS从select下拉菜单获取所有分页（跳过首项避免重复）
正文：webview加载（JS自动执行qsbs.bb Base64解码写入#article）+ java.ajax提取next_url

【目录流程】
1. 详情页：chapterList JS提取最后一个info-chapters div（前60章），nextTocUrl通过"查看更多章节"按钮跳转至TOC页
2. TOC页：chapterList JS从select下拉菜单获取所有分页URL，跳过第一项（详情页URL，避免与前60章重复），逐页ajax获取剩余章节
3. TOC页无"查看更多章节"文本，nextTocUrl返回空，自动停止

【正文流程】
- 正文通过document.writeln(qsbs.bb('Base64'))动态加载，需webview执行JS
- 章节分页：第1页URL:/book/ID/章节ID.html，第2页:/book/ID/章节ID/1.html，用/book/数字/数字/数字.html区分
- next_url在#article外的.read_nav中，用java.ajax单独获取

## 规则配置

### 搜索URL
```js
{{cookie.removeCookie(source.getKey())}}/search.html,{"method":"POST","body":"s={{key}}"}
```

### 搜索规则
```js
{
  "author": "span@text",
  "bookList": ".category-div",
  "bookUrl": "a@href",
  "coverUrl": "img@src",
  "intro": ".intro@text",
  "name": "h3@text"
}
```

### 发现URL
```js
玄幻修真::/fenlei1/{{page}}.html
重生穿越::/fenlei2/{{page}}.html
都市小说::/fenlei3/{{page}}.html
军史小说::/fenlei4/{{page}}.html
网游小说::/fenlei5/{{page}}.html
科幻小说::/fenlei6/{{page}}.html
灵异小说::/fenlei7/{{page}}.html
言情小说::/fenlei8/{{page}}.html
```

### 发现规则
```js
{
  "author": "span@text",
  "bookList": ".outdiv",
  "bookUrl": "a@href",
  "coverUrl": "img@src",
  "intro": ".intro@text",
  "name": "h3@text"
}
```

### 详情规则
```js
{
  "author": "meta[property=\"og:novel:author\"]@content",
  "coverUrl": "meta[property=\"og:image\"]@content",
  "intro": "meta[property=\"og:description\"]@content",
  "kind": "meta[property=\"og:novel:category\"]@content",
  "lastChapter": "meta[property=\"og:novel:latest_chapter_name\"]@content",
  "name": "meta[property=\"og:novel:book_name\"]@content"
}
```

### 目录规则
```js
{
  "chapterList": "<js>\nvar JsDom = Packages.org.jsoup.Jsoup;\nvar document = JsDom.parse(src);\nvar list = [];\nvar base = source.getKey();\n\nfunction toAbs(url) {\n    if (url && url.indexOf('http') != 0) {\n        return base + (url.indexOf('/') == 0 ? url : '/' + url);\n    }\n    return url;\n}\n\nvar select = document.select('select option');\nvar urls = [];\nfor (var i = 0; i < select.size(); i++) {\n    var url = select.get(i).attr('value');\n    if (url) urls.push(toAbs(url));\n}\n\nif (urls.length == 0) {\n    var divs = document.select('div.info-chapters.flex.flex-wrap');\n    if (divs.size() > 0) {\n        var last = divs.last();\n        var links = last.select('a[href*=.html]');\n        for (var i = 0; i < links.size(); i++) {\n            list.push({text: links.get(i).text(), url: links.get(i).attr('href')});\n        }\n    }\n}\n\nfor (var p = 1; p < urls.length; p++) {\n    var html = String(java.ajax(urls[p]));\n    var doc = JsDom.parse(html);\n    var divs = doc.select('div.info-chapters.flex.flex-wrap');\n    if (divs.size() > 0) {\n        var last = divs.last();\n        var links = last.select('a[href*=.html]');\n        for (var j = 0; j < links.size(); j++) {\n            var t = links.get(j).text();\n            if (t && t.indexOf('开始阅读') == -1 && t.indexOf('小说详情') == -1) {\n                list.push({text: t, url: links.get(j).attr('href')});\n            }\n        }\n    }\n}\nlist;\n</js>",
  "chapterName": "text",
  "chapterUrl": "url##$##,{\"webView\":true}",
  "nextTocUrl": "text.查看更多章节@href"
}
```

### 正文规则
```js
{
  "content": "#article@html",
  "nextContentUrl": "@js:var url=baseUrl.split(\",\")[0];if(url.indexOf('http')!=0){url=source.getKey()+url;}var html=String(java.ajax(url));var m=html.match(/id=\"next_url\"[^>]*href=\"([^\"]*)\"/);var n=m?m[1]:'';n&&/\\/book\\/\\d+\\/\\d+\\/\\d+\\.html/.test(n)?n:''##$##,{\"webView\": true}",
  "replaceRegex": "##www.novelser.com##"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）
- 搜索前清除Cookie（频率限制规避）

### 难度评估

**难度**: ⭐⭐⭐
