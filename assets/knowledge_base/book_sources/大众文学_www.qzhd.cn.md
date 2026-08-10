# 大众文学

## 基本信息
- **书源名称**: 大众文学
- **书源地址**: http://www.qzhd.cn
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

间隔20秒

## 规则配置

### 搜索URL
```js
@js:
var su = source.getKey();
source.put('searchKey', String(key));
su + '/search.html,{"method":"POST","body":"s=' + encodeURIComponent(key) + '"}'
```

### 搜索规则
```js
{
  "author": ".s3 a@text##\\{.*?\\}##",
  "bookList": ".txt-list li:has(.s3)",
  "bookUrl": ".s2 a@href",
  "kind": ".s1@text##\\{.*?\\}##",
  "lastChapter": ".s4 a@text",
  "name": ".s2 a@text"
}
```

### 发现URL
```js
[{"title":"玄幻魔法","url":"/sort/1/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}},{"title":"武侠修真","url":"/sort/2/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}},{"title":"都市言情","url":"/sort/3/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}},{"title":"历史军事","url":"/sort/4/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}},{"title":"侦探推理","url":"/sort/5/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}},{"title":"网游动漫","url":"/sort/6/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}},{"title":"女生耽美","url":"/sort/7/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}},{"title":"其他小说","url":"/sort/8/{{page}}.html","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.25}}]
```

### 发现规则
```js
{
  "author": ".s4@text||.s5 a@text",
  "bookList": ".txt-list li",
  "bookUrl": ".s2 a@href",
  "kind": ".s1@text",
  "lastChapter": ".s3 a@text",
  "name": ".s2 a@text"
}
```

### 详情规则
```js
{
  "author": "[property=\"og:novel:author\"]@content",
  "coverUrl": "[property=\"og:image\"]@content",
  "intro": "[property=\"og:description\"]@content",
  "kind": "[property~=og:novel:category|og:novel:status|og:novel:update_time]@content",
  "lastChapter": "[property=\"og:novel:latest_chapter_name\"]@content",
  "name": "[property=\"og:novel:book_name\"]@content"
}
```

### 目录规则
```js
{
  "chapterList": ".row-section .layout-col1 li a",
  "chapterName": "text",
  "chapterUrl": "href"
}
```

### 正文规则
```js
{
  "content": ".word_read p@html",
  "nextContentUrl": "text.下一章@href"
}
```

### 登录配置
```js
loginUrl:
http://www.qzhd.cn/login.html
```

## 技术分析

### 核心技术点

- 需要登录（CookieJar + loginUrl）
- CookieJar已启用，自动管理登录状态
- 正文分页处理（nextContentUrl）
- bookUrlPattern: http://www.qzhd.cn/biquge/\d+/
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐
