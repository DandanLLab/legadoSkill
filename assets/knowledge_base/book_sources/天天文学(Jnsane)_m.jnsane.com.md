# 天天文学(Jnsane)

## 基本信息
- **书源名称**: 天天文学(Jnsane)
- **书源地址**: https://m.jnsane.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

（无描述）

## 规则配置

### 搜索URL
```js
/search.html?4qhjh={{key}}
```

### 搜索规则
```js
{
  "author": ".s_list@text##.*/(.*)##$1###",
  "bookList": ".s_list",
  "bookUrl": "a@href",
  "lastChapter": ".title@text",
  "name": "a@text"
}
```

### 发现URL
```js
仙侠修真::/sort/20_0_0_0/?page={{page}}
都市言情::/sort/21_0_0_0/?page={{page}}
历史军事::/sort/22_0_0_0/?page={{page}}
现代言情::/sort/23_0_0_0/?page={{page}}
网游竞技::/sort/24_0_0_0/?page={{page}}
科幻灵异::/sort/25_0_0_0/?page={{page}}
武侠仙侠::/sort/26_0_0_0/?page={{page}}
侦探推理::/sort/62_0_0_0/?page={{page}}
```

### 发现规则
```js
{
  "author": ".s_list@text##.*/(.*)##$1###",
  "bookList": ".s_list",
  "bookUrl": "a@href",
  "name": "a@text"
}
```

### 详情规则
```js
{
  "author": ".synopsisArea_detail p.0@text",
  "coverUrl": ".synopsisArea_detail img@data-src",
  "intro": ".review@text",
  "kind": ".synopsisArea_detail p.1@text",
  "lastChapter": ".lastchapters a@text",
  "name": "h1.title@text",
  "tocUrl": "text.全部章节@href"
}
```

### 目录规则
```js
{
  "chapterList": ".directoryArea a",
  "chapterName": "@text",
  "chapterUrl": "@href"
}
```

### 正文规则
```js
{
  "content": "#htmlContent@html",
  "nextContentUrl": "#pb_next@href"
}
```

## 技术分析

### 核心技术点

- 正文分页处理（nextContentUrl）
- 自定义请求头

### 难度评估

**难度**: ⭐⭐
