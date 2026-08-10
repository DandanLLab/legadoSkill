# 领域书库

## 基本信息
- **书源名称**: 领域书库
- **书源地址**: http://www.lysxh.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

26.07.08@小说迷 修复cf验证 搜索列表
【网站】领域书库 (lysxh.com)
【技术实现】
搜索：HTML 搜索（GET /search.html?keyWord=关键词）
发现：HTML 发现（GET /fenlei/{分类全拼}/{{page}}/）
详情：Default 规则（class.top@tag.h1 精确定位书名）
目录：Default 规则（第二个 section-box）
正文：HTML 提取 + JS 清理

【局限性】
- 网站有 Cloudflare Turnstile 保护，首次访问可能需要验证
- 正文有分页，已配置 nextContentUrl 自动翻页
- 仅支持 HTTP（HTTPS 证书不兼容）

【规则说明】
- 搜索/发现列表：Default 格式（tag.a.0@text），表头行自动过滤
- 详情页书名：class.top@tag.h1 精确定位，避免匹配到 logo 的 h1
- 正文分页标题：全局正则删除所有 章节名(第X/Y页)<br><br> 标记
- 分类 URL 使用全拼：xuanhuan/wuxia/dushi/lishi/wangyou/kehuan/nvsheng
- 分页格式：/fenlei/分类/{{page}}/（目录式，非 .html 式）

## 规则配置

### 搜索URL
```js
/search.html?keyWord={{key}}
```

### 搜索规则
```js
{
  "author": "class.s4@text",
  "bookList": ".txt-list@li!0",
  "bookUrl": "tag.a.0@href",
  "kind": "class.s1@text",
  "lastChapter": "tag.a.1@text",
  "name": "tag.a.0@text"
}
```

### 发现URL
```js
玄幻奇幻::/fenlei/xuanhuan/{{page}}/
武侠仙侠::/fenlei/wuxia/{{page}}/
都市言情::/fenlei/dushi/{{page}}/
历史军事::/fenlei/lishi/{{page}}/
网游竞技::/fenlei/wangyou/{{page}}/
科幻灵异::/fenlei/kehuan/{{page}}/
女生频道::/fenlei/nvsheng/{{page}}/
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
  "chapterUrl": "a@href",
  "nextTocUrl": "option@value"
}
```

### 正文规则
```js
{
  "content": "#content@html@js:result.replace(/<script[\\s\\S]*?<\\/script>/g,'').replace(/[^<]*\\(第\\d+\\/\\d+页\\)<br><br>/g,'').replace(/（本章未完[\\s\\S]*?）/g,'')",
  "nextContentUrl": "text.下一页@href",
  "replaceRegex": "##.*?\\(第\\d+\\/\\d+页\\)##"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐
