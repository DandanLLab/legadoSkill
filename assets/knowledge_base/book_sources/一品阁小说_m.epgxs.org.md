# 一品阁小说

## 基本信息
- **书源名称**: 一品阁小说
- **书源地址**: https://m.epgxs.org
- **书源分组**: AI,18加
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

正文文字图大，右上角图片样式选TEXT
网址发布邮箱：Ltxsba@gmail.com
【技术实现】
搜索：POST 搜索（/search/，body: searchkey={{key}}）
发现：CSS 选择器（分类页 .item 卡片）
详情：CSS 选择器 + og:novel 元数据
目录：XPath 章节列表（第二个 section-box 为完整列表）+ text.下一页 逐页分页
正文：webview 加载章节页（JS 自动执行 AJAX 加载内容+文字图片）+ #content@html 提取

【局限性】
- 章节链接使用 webView 加载，依赖 JS 执行加载正文内容
- 详情页 URL 从 /bookcv/ 重定向到 /html/
- 每页有两个 section-box，第一个是最新章节（倒序），第二个是完整列表（正序），用 XPath [2] 选取第二个

## 规则配置

### 搜索URL
```js
{{cookie.removeCookie(source.getKey())}}/search/,{"method":"POST","body":"searchkey={{key}}"}
```

### 搜索规则
```js
{
  "author": ".s4@text",
  "bookList": ".txt-list li",
  "bookUrl": ".s2 a@href",
  "kind": ".s1@text",
  "lastChapter": ".s3 a@text",
  "name": ".s2 a@text"
}
```

### 发现URL
```js
玄幻小说::/sort/1/{{page}}/
武侠小说::/sort/2/{{page}}/
都市小说::/sort/3/{{page}}/
历史小说::/sort/4/{{page}}/
侦探小说::/sort/5/{{page}}/
网游小说::/sort/6/{{page}}/
科幻小说::/sort/7/{{page}}/
恐怖小说::/sort/8/{{page}}/
辣文小说::/sort/10/{{page}}/
```

### 发现规则
```js
{
  "author": "dt span@text",
  "bookList": ".item",
  "bookUrl": "dt a@href",
  "coverUrl": "img@src",
  "intro": "dd@text",
  "name": "dt a@text"
}
```

### 详情规则
```js
{
  "author": "meta[property=\"og:novel:author\"]@content",
  "coverUrl": ".imgbox img@src",
  "intro": ".desc@text",
  "kind": "meta[property=\"og:novel:category\"]@content",
  "lastChapter": "meta[property=\"og:novel:lastest_chapter_name\"]@content",
  "name": "meta[property=\"og:novel:book_name\"]@content"
}
```

### 目录规则
```js
{
  "chapterList": "//div[@class=\"section-box\"][2]//li/a",
  "chapterName": "@text",
  "chapterUrl": "@href##$##,{\"webView\":true}",
  "nextTocUrl": "text.下一页@href"
}
```

### 正文规则
```js
{
  "content": "#content@html",
  "nextContentUrl": "text.下一页@href"
}
```

## 技术分析

### 核心技术点

- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）
- 搜索前清除Cookie（频率限制规避）

### 难度评估

**难度**: ⭐⭐⭐
