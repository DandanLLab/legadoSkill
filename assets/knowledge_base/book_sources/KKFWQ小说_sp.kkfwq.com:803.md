# KKFWQ小说

## 基本信息
- **书源名称**: KKFWQ小说
- **书源地址**: http://sp.kkfwq.com:803
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

（无描述）

## 规则配置

### 搜索URL
```js
@js:'/modules/article/search.php,'+JSON.stringify({method:'POST',body:'searchtype=articlename&searchkey='+key,charset:'GBK'})
```

### 搜索规则
```js
{
  "author": "tr:nth-child(2) td:nth-child(2)@text##.*[：:]",
  "bookList": "table[width=\"96%\"][align=\"center\"]",
  "coverUrl": "img[src*=\"/files/article/image/\"]@src",
  "intro": "td:contains(内容简介)[1]@text##.*?内容简介：|作品关键字：.*##",
  "kind": "tr:nth-child(2) td:nth-child(1)@text##.*[：:]",
  "lastChapter": "span.hottext:contains(最近章节) + a@text",
  "name": "span[style*=\"font-size:16px\"]@text",
  "wordCount": "tr:nth-child(2) td:nth-child(4)@text##.*[：:]"
}
```

### 发现URL
```js
全部文章::/modules/article/articlelist.php?class=&page={{page}}
玄幻奇幻::/modules/article/articlelist.php?class=1&page={{page}}
武侠仙侠::/modules/article/articlelist.php?class=2&page={{page}}
都市言情::/modules/article/articlelist.php?class=3&page={{page}}
历史军事::/modules/article/articlelist.php?class=4&page={{page}}
推理灵异::/modules/article/articlelist.php?class=5&page={{page}}
科幻网游::/modules/article/articlelist.php?class=6&page={{page}}
同人小说::/modules/article/articlelist.php?class=7&page={{page}}
其他类型::/modules/article/articlelist.php?class=8&page={{page}}
总排行榜::/modules/article/toplist.php?sort=allvisit&page={{page}}
总推荐榜::/modules/article/toplist.php?sort=allvote&page={{page}}
月排行榜::/modules/article/toplist.php?sort=monthvisit&page={{page}}
月推荐榜::/modules/article/toplist.php?sort=monthvote&page={{page}}
周排行榜::/modules/article/toplist.php?sort=weekvisit&page={{page}}
周推荐榜::/modules/article/toplist.php?sort=weekvote&page={{page}}
最新入库::/modules/article/toplist.php?sort=postdate&page={{page}}
最近更新::/modules/article/toplist.php?sort=lastupdate&page={{page}}
总收藏榜::/modules/article/toplist.php?sort=goodnum&page={{page}}
字数排行::/modules/article/toplist.php?sort=size&page={{page}}
```

### 发现规则
```js
{
  "author": "td:nth-child(3)@text",
  "bookList": "table.grid tr:has(td.odd)",
  "bookUrl": "td.odd a@href",
  "lastChapter": "td:nth-child(2) a@text",
  "name": "td.odd a@text",
  "wordCount": "td:nth-child(4)@text"
}
```

### 详情规则
```js
{
  "author": "table[width=\"96%\"][align=\"center\"] tr:nth-child(2) td:nth-child(2)@text##.*[：:]",
  "coverUrl": "img[src*=\"/files/article/image/\"]@src",
  "intro": "td:contains(内容简介)[1]@text##.*?内容简介：|作品关键字：.*##",
  "kind": "table[width=\"96%\"][align=\"center\"] tr:nth-child(2) td:nth-child(1)@text##.*[：:]",
  "lastChapter": "span.hottext:contains(最近章节) + a@text",
  "name": "span[style*=\"font-size:16px\"]@text",
  "tocUrl": "a.btnlink[href*=\"reader.php\"]@href",
  "wordCount": "table[width=\"96%\"][align=\"center\"] tr:nth-child(2) td:nth-child(4)@text##.*[：:]"
}
```

### 目录规则
```js
{
  "chapterList": "table.acss a",
  "chapterName": "@text",
  "chapterUrl": "@href"
}
```

### 正文规则
```js
{
  "content": "#content@textNodes",
  "nextContentUrl": "a:contains(下一页)@href"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 正文分页处理（nextContentUrl）
- bookUrlPattern: http://sp.kkfwq.com:803/modules/article/articleinfo.php?id=\d+

### 难度评估

**难度**: ⭐⭐⭐
