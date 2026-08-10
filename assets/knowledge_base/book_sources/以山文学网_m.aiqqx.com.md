# 以山文学网

## 基本信息
- **书源名称**: 以山文学网
- **书源地址**: https://m.aiqqx.com
- **书源分组**: AI,验证码
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

以山文学网书源 (https://m.aiqqx.com)

搜索时自动弹出验证码图片，输入后自动搜索。
获取一次验证码后缓存，一段时间内无需再次输入。
验证码过期会自动重新弹出。

发现包含8大分类、12个排行榜和全本小说。
目录从详情页开始，章节按最新更新排列。
分类：玄幻魔法、仙侠修真、都市言情、历史军事、网游竞技、科幻小说、恐怖灵异、其他小说
排行：日/周/月/总点击榜、日/周/月/总推荐榜、总收藏榜、字数排行、最新入库、最近更新

## 规则配置

### 搜索URL
```js
@js:
java.put('search_key',key);
var sUrl=String(source.bookSourceUrl);
result=sUrl+'/s.php,{"method":"POST","body":"keyword='+encodeURIComponent(key)+'&code="}';
```

### 搜索规则
```js
{
  "author": "span.author a@text",
  "bookList": "<js>\nif(result.indexOf('searchcode')>-1){\n    var sUrl=String(source.bookSourceUrl);\n    var sk=java.get('search_key')||'';\n    var captchaUrl=sUrl+'/searchcode.php?t='+Date.now();\n    function doPost(code){\n        var u=sUrl+'/s.php,{\"method\":\"POST\",\"body\":\"keyword='+encodeURIComponent(sk)+'&code='+code+'\"}';\n        return java.ajax(u);\n    }\n    var yzco=source.getVariable();\n    if(yzco&&yzco!=''){\n        result=doPost(yzco);\n        if(result.indexOf('searchcode')>-1){\n            java.longToast('验证码过期，请重新输入');\n            var yzm=java.getVerificationCode(captchaUrl);\n            result=doPost(yzm);\n            source.setVariable(yzm);\n        }\n    }else{\n        var yzm=java.getVerificationCode(captchaUrl);\n        result=doPost(yzm);\n        source.setVariable(yzm);\n    }\n}\nresult;\n</js>\np.sone",
  "bookUrl": "a@href",
  "name": "a.0@text"
}
```

### 发现URL
```js
玄幻魔法::https://m.aiqqx.com/xuanhuan/{{page}}.html
仙侠修真::https://m.aiqqx.com/xianxia/{{page}}.html
都市言情::https://m.aiqqx.com/dushi/{{page}}.html
历史军事::https://m.aiqqx.com/lishi/{{page}}.html
网游竞技::https://m.aiqqx.com/wangyou/{{page}}.html
科幻小说::https://m.aiqqx.com/kehuan/{{page}}.html
恐怖灵异::https://m.aiqqx.com/kongbu/{{page}}.html
其他小说::https://m.aiqqx.com/qita/{{page}}.html
日点击榜::https://m.aiqqx.com/top/dayvisit_{{page}}/
周点击榜::https://m.aiqqx.com/top/weekvisit_{{page}}/
月点击榜::https://m.aiqqx.com/top/monthvisit_{{page}}/
总点击榜::https://m.aiqqx.com/top/allvisit_{{page}}/
日推荐榜::https://m.aiqqx.com/top/dayvote_{{page}}/
周推荐榜::https://m.aiqqx.com/top/weekvote_{{page}}/
月推荐榜::https://m.aiqqx.com/top/monthvote_{{page}}/
总推荐榜::https://m.aiqqx.com/top/allvote_{{page}}/
总收藏榜::https://m.aiqqx.com/top/goodnum_{{page}}/
字数排行::https://m.aiqqx.com/top/size_{{page}}/
最新入库::https://m.aiqqx.com/top/postdate_{{page}}/
最近更新::https://m.aiqqx.com/top/lastupdate_{{page}}/
全本小说::https://m.aiqqx.com/full/{{page}}/
```

### 发现规则
```js
{
  "author": ".newbook_author a@text##作者：",
  "bookList": "<js>\nif(result.indexOf('newbook_list')==-1){\n    result=result.replace(/<div class=\"(articlegeneral|full_content)\">[\\s\\S]*?<p class=\"p1\">\\[(.*?)\\]<\\/p>[\\s\\S]*?<a href=\"([^\"]*)\" class=\"blue\">([^<]*)<\\/a>[\\s\\S]*?<p class=\"p3\">[\\s\\S]*?<a href=\"[^\"]*\">([^<]*)<\\/a>[\\s\\S]*?<\\/div>/g,'<div class=\"newbook_list\"><div class=\"newbook_novel\"><div class=\"newbook_title\"><a href=\"$3\">$4</a><\\/div><div class=\"newbook_author\">作者：<a href=\"$3\">$5<\\/a><\\/div><div class=\"wanben_serial_novelsort\"><span class=\"s1\">$2<\\/span><\\/div><\\/div><\\/div>');\n}\nresult;\n</js>\n.newbook_list",
  "bookUrl": ".newbook_title a@href",
  "coverUrl": ".newbook_pic img@src",
  "intro": ".newbook_intor@text",
  "kind": ".wanben_serial_novelsort span@text",
  "name": ".newbook_title a@text"
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
  "tocUrl": "@js:baseUrl"
}
```

### 目录规则
```js
{
  "chapterList": "-.info_newest ul li a",
  "chapterName": "@text",
  "chapterUrl": "@href",
  "nextTocUrl": "text.下一页@href"
}
```

### 正文规则
```js
{
  "content": "#nr1@text##本章未完[\\s\\S]*##",
  "nextContentUrl": "text.下一页@href"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）

### 难度评估

**难度**: ⭐⭐⭐
