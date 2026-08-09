# kk笔趣阁新站

## 基本信息
- **书源名称**: kk笔趣阁新站
- **书源地址**: http://www.kkbiquge.net
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

调出真实浏览器过人机验证

## 规则配置

### 搜索URL
```js
{{url=source.getKey();
cookie.removeCookie(url);}}{{(function(){
    var baseUrl = 'http://www.kkbiquge.net';
    var html = java.ajax(baseUrl + '/');
    var match = html.match(/<form[^>]*id="search"[^>]*action="([^"]+)"/);
    var action = match ? match[1] : '/search21.html';
    return baseUrl + action + '?searchkey=' + java.encodeURI(key);
})()}}
```

### 搜索规则
```js
{
  "author": "div.btm a@text",
  "bookList": "div.item",
  "bookUrl": "dt a@href",
  "coverUrl": "img@data-original||img@src",
  "intro": "dd@text",
  "name": "dt a@text",
  "wordCount": "div.btm em.orange@text"
}
```

### 发现URL
```js
玄幻::/class/xuanhuanmofa/{{page}}/
仙侠::/class/xianxiaxiuzhen/{{page}}/
都市::/class/dushuyanqing/{{page}}/
历史::/class/lishijunshi/{{page}}/
网游::/class/wangyoudongman/{{page}}/
科幻::/class/kehuanxiaoshuo/{{page}}/
女生::/class/nvshengxiaoshuo/{{page}}/
其他::/class/qitaxiaoshuo/{{page}}/
```

### 发现规则
```js
{
  "author": "div.btm a@text",
  "bookList": "div.item",
  "bookUrl": "dt a@href",
  "coverUrl": "img@data-original||img@src",
  "intro": "dd@text",
  "name": "dt a@text"
}
```

### 详情规则
```js
{
  "author": "#info p a@text",
  "coverUrl": "img[data-original]@data-original||#fmimg img@src",
  "intro": "#intro@text",
  "kind": "p.sort@text##类别：|\\s*",
  "lastChapter": "#info a[rel=\"chapter\"]@text",
  "name": "#info h1@text"
}
```

### 目录规则
```js
{
  "chapterList": "#list dl a[href]",
  "chapterName": "dd@text",
  "chapterUrl": "@href"
}
```

### 正文规则
```js
{
  "content": "#chaptercontent #booktxt@html##<p[^>]*>\\s*</p>",
  "nextContentUrl": "a#next_url@href"
}
```

### 登录配置
```js
loginUrl:
http://www.kkbiquge.net/
```

## 技术分析

### 核心技术点

- 需要登录（CookieJar + loginUrl）
- 正文分页处理（nextContentUrl）
- 搜索前清除Cookie（频率限制规避）
- bookUrlPattern: http://www.kkbiquge.net/\d+_\d+/
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐
