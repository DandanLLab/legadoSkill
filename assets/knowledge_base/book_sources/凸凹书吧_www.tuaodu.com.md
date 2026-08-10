# 凸凹书吧

## 基本信息
- **书源名称**: 凸凹书吧
- **书源地址**: https://www.tuaodu.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

凸凹书吧(tuaodu.com) - 全本小说在线阅读
单章全文

## 规则配置

### 搜索URL
```js
/Articles/Search?wd={{key}}
```

### 搜索规则
```js
{
  "author": ".index-imgcontent-title@text##.*作者[：:]\\s*",
  "bookList": ".index-imgs",
  "bookUrl": ".index-imgcontent-title@href",
  "coverUrl": "img@data-original||img@src",
  "intro": "a.index-imgcontent-img@title",
  "name": ".index-imgcontent-title@text## 作者[：:].*"
}
```

### 发现URL
```js
最新::/Articles?Page={{page}}
玄幻::/Articles/Categories/3?Page={{page}}
灵异::/Articles/Categories/6?Page={{page}}
穿越::/Articles/Categories/7?Page={{page}}
都市::/Articles/Categories/8?Page={{page}}
言情::/Articles/Categories/9?Page={{page}}
武侠::/Articles/Categories/10?Page={{page}}
其他::/Articles/Categories/11?Page={{page}}
```

### 发现规则
```js
{
  "author": ".index-imgcontent-title@text##.*作者[：:]\\s*",
  "bookList": ".index-imgs",
  "bookUrl": ".index-imgcontent-title@href",
  "coverUrl": "img.lazyimg@data-original||img@src",
  "intro": ".index-imgcontent-img@title",
  "name": ".index-imgcontent-title@text## 作者[：:].*"
}
```

### 详情规则
```js
{
  "author": ".content-title@text##.*作者[：:]\\s*",
  "coverUrl": "js:''",
  "intro": "meta[name='description']@content",
  "kind": ".breadcrumb li:nth-child(2) a@text",
  "name": ".content-title@text## 作者[：:].*"
}
```

### 目录规则
```js
{
  "chapterList": "@js:[{n:'全文',u:baseUrl}]",
  "chapterName": "n",
  "chapterUrl": "u"
}
```

### 正文规则
```js
{
  "content": "@js:\nvar m = result.match(/articleId.*? value=\"(\\d+)\"/);\nvar id=m?m[1]:'10909';var token=java.base64Encode(id);\njava.get('https://www.tuaodu.com/GetTxt.ashx?token='+token,{'Referer':'https://www.tuaodu.com/Articles/Content/'+id+'.html'}).body();"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐
