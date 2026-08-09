# 笔下文学

## 基本信息
- **书源名称**: 笔下文学
- **书源地址**: https://m.haishuxs.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

（无描述）

## 规则配置

### 发现URL
```js
玄幻魔法::/fenl/xuanhuan/{{page}}/
武侠修真::/fenl/wuxia/{{page}}/
都市言情::/fenl/doushi/{{page}}/
历史军事::/fenl/lishi/{{page}}/
网游动漫::/fenl/wangyou/{{page}}/
科幻小说::/fenl/kehuan/{{page}}/
其他类型::/fenl/qita/{{page}}/
全本小说::/full/{{page}}.html
```

### 发现规则
```js
{
  "author": "dd a@text",
  "bookList": "dl",
  "bookUrl": "dt a@href",
  "coverUrl": "img@data-src",
  "intro": "dd.0@text",
  "kind": "dd span@text",
  "name": "dt a@title"
}
```

### 详情规则
```js
{
  "author": ".book-meta:eq(1) a@text",
  "coverUrl": ".book-cover@src",
  "kind": ".book-meta:eq(2) a@text&&.book-meta:eq(3)@text&&.book-meta:eq(5)@text",
  "lastChapter": ".book-meta:eq(4) a@text",
  "name": "h1.book-title@text",
  "tocUrl": ".bookchaptermore@href"
}
```

### 目录规则
```js
{
  "chapterList": "#clist li",
  "chapterName": "a@text",
  "chapterUrl": "a@href",
  "nextTocUrl": ".listpage .right a@href"
}
```

### 正文规则
```js
{
  "content": "#chaptercontent@html##本章还未完.*##",
  "nextContentUrl": ".readpage a[rel=next]@href"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）
- bookUrlPattern: https://m.haishuxs.com/d/.*/*_.*/

### 难度评估

**难度**: ⭐⭐⭐
