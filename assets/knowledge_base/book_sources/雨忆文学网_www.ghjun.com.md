# 雨忆文学网

## 基本信息
- **书源名称**: 雨忆文学网
- **书源地址**: https://www.ghjun.com
- **书源分组**: 验证码,AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

雨忆文学网书源 (https://www.ghjun.com)

搜索时自动弹出验证码图片，输入后自动搜索。
获取一次验证码后缓存，一段时间内无需再次输入。
验证码过期会自动重新弹出。

发现包含8大分类、8个排行榜和全本小说。
分类：玄幻、仙侠、都市、历史、网游、科幻、灵异、其他
排行：总排行、周榜、日榜、月榜、更新榜、新书上架、收藏榜、字数榜

## 规则配置

### 搜索URL
```js
@js:
java.put('search_key',key);
var sUrl=String(source.bookSourceUrl);
result=sUrl+'/s/search/?keyword='+encodeURIComponent(key);
```

### 搜索规则
```js
{
  "author": "@css:td:nth-child(4)@text",
  "bookList": "<js>\nif(result.indexOf('searchcode')>-1){\n    var sUrl=String(source.bookSourceUrl);\n    var sk=java.get('search_key')||'';\n    var captchaUrl=sUrl+'/searchcode.php?t='+Date.now();\n    function doPost(code){\n        var u=sUrl+'/s/search/,{\"method\":\"POST\",\"body\":\"keyword='+encodeURIComponent(sk)+'&code='+code+'\"}';\n        return java.ajax(u);\n    }\n    var yzco=source.getVariable();\n    if(yzco&&yzco!=''){\n        result=doPost(yzco);\n        if(result.indexOf('searchcode')>-1){\n            java.longToast('验证码过期，请重新输入');\n            var yzm=java.getVerificationCode(captchaUrl);\n            result=doPost(yzm);\n            source.setVariable(yzm);\n        }\n    }else{\n        var yzm=java.getVerificationCode(captchaUrl);\n        result=doPost(yzm);\n        source.setVariable(yzm);\n    }\n}\nresult;\n</js>\ntable.table tr",
  "bookUrl": "a[title]@href",
  "kind": "@css:td:nth-child(1)@text",
  "lastChapter": "a.text-muted@text",
  "name": "a[title]@title",
  "wordCount": "@css:td:nth-child(5)@text"
}
```

### 发现URL
```js
玄幻小说::https://www.ghjun.com/sort/1/{{page}}.html
仙侠小说::https://www.ghjun.com/sort/2/{{page}}.html
都市小说::https://www.ghjun.com/sort/3/{{page}}.html
历史小说::https://www.ghjun.com/sort/4/{{page}}.html
网游小说::https://www.ghjun.com/sort/5/{{page}}.html
科幻小说::https://www.ghjun.com/sort/6/{{page}}.html
灵异小说::https://www.ghjun.com/sort/7/{{page}}.html
其他小说::https://www.ghjun.com/sort/8/{{page}}.html
总排行榜::https://www.ghjun.com/top/allvisit/{{page}}.html
周排行榜::https://www.ghjun.com/top/weekvisit/{{page}}.html
日排行榜::https://www.ghjun.com/top/dayvisit/{{page}}.html
月排行榜::https://www.ghjun.com/top/monthvisit/{{page}}.html
更新榜::https://www.ghjun.com/top/lastupdate/{{page}}.html
新书上架::https://www.ghjun.com/top/postdate/{{page}}.html
收藏榜::https://www.ghjun.com/top/goodnum/{{page}}.html
字数榜::https://www.ghjun.com/top/size/{{page}}.html
全本小说::https://www.ghjun.com/full/{{page}}.html
```

### 发现规则
```js
{
  "author": "@css:td:nth-child(4)@text",
  "bookList": "table.table tr",
  "bookUrl": "a[title]@href",
  "kind": "@css:td:nth-child(1)@text",
  "lastChapter": "a.text-muted@text",
  "name": "a[title]@title",
  "wordCount": "@css:td:nth-child(5)@text"
}
```

### 详情规则
```js
{
  "author": "meta[property~=og:novel:author]@content",
  "coverUrl": "meta[property~=og:image]@content",
  "intro": "meta[property~=og:description]@content",
  "kind": "meta[property~=og:novel:category]@content",
  "lastChapter": "meta[property~=og:novel:latest_chapter_name]@content",
  "name": "meta[property~=og:novel:book_name]@content",
  "tocUrl": "@js:baseUrl.replace(/\\/$/, '') + '/1/'"
}
```

### 目录规则
```js
{
  "chapterList": "dl.panel-chapterlist dd a",
  "chapterName": "@text",
  "chapterUrl": "@href",
  "nextTocUrl": "text.下一页@href"
}
```

### 正文规则
```js
{
  "content": "#chapter@html##\\[.*?】.*?\\]##",
  "nextContentUrl": "text.下一章@href"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）

### 难度评估

**难度**: ⭐⭐⭐
