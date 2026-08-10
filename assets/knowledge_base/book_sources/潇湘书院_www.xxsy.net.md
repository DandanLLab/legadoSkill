# 潇湘书院

## 基本信息
- **书源名称**: 潇湘书院
- **书源地址**: https://www.xxsy.net
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

（无描述）

## 规则配置

### 搜索URL
```js
/search?s_wd={{key}}
```

### 搜索规则
```js
{
  "author": "@css:.info .subtitle > a@text##\\n.*|^[^\\u4e00-\\u9fff]+",
  "bookList": "@css:.result-list li",
  "bookUrl": "@css:a.book.commonbook@href",
  "coverUrl": "@css:.book-cover img@src",
  "intro": "@css:.detail@text",
  "kind": "@css:.info .subtitle > span@text##,.+",
  "name": "@css:.info h4 > a@text",
  "wordCount": "@css:.number span@text"
}
```

### 发现URL
```js
古代言情::/search?tag=古代言情&page={{page}}
现代言情::/search?tag=现代言情&page={{page}}
玄幻仙侠::/search?tag=玄幻仙侠&page={{page}}
浪漫青春::/search?tag=浪漫青春&page={{page}}
悬疑::/search?tag=悬疑&page={{page}}
排行::/rank
完本::/rank/finish
```

### 发现规则
```js
{
  "author": "@css:.info .subtitle > a@text##\\n.*|^[^\\u4e00-\\u9fff]+",
  "bookList": "@css:.result-list li",
  "bookUrl": "@css:a.book.commonbook@href",
  "coverUrl": "@css:.book-cover img@src",
  "intro": "@css:.detail@text",
  "kind": "@css:.info .subtitle > span@text##,.+",
  "name": "@css:.info h4 > a@text",
  "wordCount": "@css:.number span@text"
}
```

### 详情规则
```js
{
  "author": ".bookprofile dd .title span@text##文 / |文/",
  "coverUrl": ".bookprofile .book-cover img@src",
  "intro": "#book_intro@text",
  "kind": ".sub-cols span:eq(2)@text##类别：",
  "lastChapter": ".sub-newest p:eq(0) a@text",
  "name": ".bookdetail h1@text",
  "tocUrl": ".click-hd h3 a@href",
  "wordCount": ".sub-data span@text##字数："
}
```

### 目录规则
```js
{
  "chapterList": "@css:.profile-main ul li a[href*='/chapter/']",
  "chapterName": "@title",
  "chapterUrl": "@href"
}
```

### 正文规则
```js
{
  "content": "#content@text",
  "nextContentUrl": ".nav-btn-group a:last-of-type@href",
  "title": "h1@text"
}
```

## 技术分析

### 核心技术点

- 正文分页处理（nextContentUrl）
- bookUrlPattern: xxsy\.net/book/\d+

### 难度评估

**难度**: ⭐⭐
