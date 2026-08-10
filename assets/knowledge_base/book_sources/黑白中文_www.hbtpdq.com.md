# 黑白中文

## 基本信息
- **书源名称**: 黑白中文
- **书源地址**: https://www.hbtpdq.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

【网站】黑白中文 (hbtpdq.com)
【技术实现】
搜索：HTML 搜索（GET /so.html?keyWord=关键词）
发现：HTML 发现（GET /fenlei/{分类}/{{page}}.html）
详情：Default 规则（class.top@tag.h1 精确定位书名）
目录：Default 规则（第二个 section-box）
正文：HTML 提取 + JS 清理

【局限性】
- 网站有 Cloudflare 保护，首次访问可能需要验证
- 正文有分页，已配置 nextContentUrl 自动翻页
- 搜索结果无封面图

【v2 修复记录】
- 搜索/发现列表：改用 Default 格式（tag.a.0@text）替代 CSS 格式，解决字段提取失败问题
- 搜索表头行：tag.a.0 对表头行返回空值，自动过滤
- 详情页书名：改用 class.top@tag.h1 精确定位，避免匹配到 logo 的 h1

【v3 修复记录】
- 正文分页标题：用全局正则删除所有 章节名(第X/Y页)<br><br> 标记，避免多页拼接后残留

## 规则配置

### 搜索URL
```js
/so.html?keyWord={{key}}
```

### 搜索规则
```js
{
  "author": "class.s4@text",
  "bookList": ".txt-list-row5 li:not(:first-child)",
  "bookUrl": "tag.a.0@href",
  "kind": "class.s1@text",
  "lastChapter": "tag.a.1@text",
  "name": "tag.a.0@text"
}
```

### 发现URL
```js
玄幻奇幻::/fenlei/xh/{{page}}.html
武侠仙侠::/fenlei/wx/{{page}}.html
都市言情::/fenlei/ds/{{page}}.html
历史军事::/fenlei/ls/{{page}}.html
网游竞技::/fenlei/wy/{{page}}.html
科幻灵异::/fenlei/kh/{{page}}.html
女生频道::/fenlei/ns/{{page}}.html
```

### 发现规则
```js
{
  "author": "class.s4@text",
  "bookList": ".txt-list li",
  "bookUrl": "tag.a.0@href",
  "kind": "class.s1@text",
  "lastChapter": "tag.a.1@text",
  "name": "tag.a.0@text"
}
```

### 详情规则
```js
{
  "author": "class.fix@tag.p.0@text##.*者：##",
  "coverUrl": ".imgbox img@src",
  "intro": ".desc@text##^\\s*##",
  "kind": "class.fix@tag.p.1@text##.*别：##",
  "lastChapter": "class.fix@tag.p.-1@tag.a@text",
  "name": "class.top@tag.h1@text"
}
```

### 目录规则
```js
{
  "chapterList": "class.section-box.-1@class.section-list@tag.li",
  "chapterName": "a@text",
  "chapterUrl": "a@href"
}
```

### 正文规则
```js
{
  "content": "#content@html@js:result.replace(/<script[\\s\\S]*?<\\/script>/g,'').replace(/[^<]*\\(第\\d+\\/\\d+页\\)<br><br>/g,'').replace(/（本章未完[\\s\\S]*?）/g,'')",
  "nextContentUrl": "text.下一页@href",
  "replaceRegex": "##.*\\(第\\d+\\/\\d+页\\)##"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 正文分页处理（nextContentUrl）
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐
