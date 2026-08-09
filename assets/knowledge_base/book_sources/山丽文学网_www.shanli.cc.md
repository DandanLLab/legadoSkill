# 山丽文学网

## 基本信息
- **书源名称**: 山丽文学网
- **书源地址**: https://www.shanli.cc
- **书源分组**: 验证码,AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

山丽文学网书源 (https://www.shanli.cc)

搜索时自动弹出验证码图片，输入后自动搜索。
获取一次验证码后缓存，一段时间内无需再次输入。
验证码过期会自动重新弹出。

发现包含8大分类和7个排行榜。

## 规则配置

### 搜索URL
```js
@js:
java.put('search_key',key);
var sUrl=String(source.bookSourceUrl);
result=sUrl+'/search.php,{"method":"POST","body":"keyword='+encodeURIComponent(key)+'&code="}';
```

### 搜索规则
```js
{
  "author": ".info .author@text##.* / | / .*",
  "bookList": "<js>\nif(result.indexOf('searchcode')>-1){\n    var sUrl=String(source.bookSourceUrl);\n    var sk=java.get('search_key')||'';\n    var captchaUrl=sUrl+'/searchcode.php?t='+Date.now();\n    function doPost(code){\n        var u=sUrl+'/search.php,{\"method\":\"POST\",\"body\":\"keyword='+encodeURIComponent(sk)+'&code='+code+'\"}';\n        return java.ajax(u);\n    }\n    var yzco=source.getVariable();\n    if(yzco&&yzco!=''){\n        result=doPost(yzco);\n        if(result.indexOf('searchcode')>-1){\n            java.longToast('验证码过期，请重新输入');\n            var yzm=java.getVerificationCode(captchaUrl);\n            result=doPost(yzm);\n            source.setVariable(yzm);\n        }\n    }else{\n        var yzm=java.getVerificationCode(captchaUrl);\n        result=doPost(yzm);\n        source.setVariable(yzm);\n    }\n}\nresult;\n</js>\n.list .row",
  "bookUrl": ".info .name@href",
  "coverUrl": ".cover img@src",
  "intro": ".info .intro@text",
  "kind": ".info .author@text## / .* / ",
  "name": ".info .name@text"
}
```

### 发现URL
```js
玄幻魔法::https://www.shanli.cc/0oxm/xuanhuan/{{page}}/
武侠修真::https://www.shanli.cc/0oxm/wuxia/{{page}}/
都市言情::https://www.shanli.cc/0oxm/dushi/{{page}}/
历史军事::https://www.shanli.cc/0oxm/lishi/{{page}}/
网游竞技::https://www.shanli.cc/0oxm/wangyou/{{page}}/
科幻小说::https://www.shanli.cc/0oxm/kehuan/{{page}}/
恐怖灵异::https://www.shanli.cc/0oxm/kongbu/{{page}}/
其他小说::https://www.shanli.cc/0oxm/qita/{{page}}/
总点击榜::https://www.shanli.cc/5wb04g/allvisit/{{page}}.html
总推荐榜::https://www.shanli.cc/5wb04g/allvote/{{page}}.html
最近更新::https://www.shanli.cc/5wb04g/lastupdate/{{page}}.html
最新入库::https://www.shanli.cc/5wb04g/postdate/{{page}}.html
日点击榜::https://www.shanli.cc/5wb04g/dayvisit/{{page}}.html
周点击榜::https://www.shanli.cc/5wb04g/weekvisit/{{page}}.html
月点击榜::https://www.shanli.cc/5wb04g/monthvisit/{{page}}.html
```

### 发现规则
```js
{
  "author": "dd.author@text",
  "bookList": ".list-index-2 .item",
  "bookUrl": "dl dt a@href",
  "coverUrl": ".cover img@data-src",
  "intro": "dd.intro@text",
  "kind": "dd.more@span.1@text",
  "name": "dl dt a@text",
  "wordCount": "dd.more@span.0@text"
}
```

### 详情规则
```js
{
  "author": ".book .right h2 span.0@text##作者：",
  "coverUrl": ".book .cover img@src",
  "intro": ".intro@text##小说简介：|关键词[\\s\\S]*",
  "kind": ".book .cover span@text## / [\\s\\S]*",
  "lastChapter": ".status a@text",
  "name": ".right h1 a@text",
  "tocUrl": "@js:baseUrl"
}
```

### 目录规则
```js
{
  "chapterList": "ul.chapterlist1 li a",
  "chapterName": "@text",
  "chapterUrl": "@href"
}
```

### 正文规则
```js
{
  "content": "#chapter@html",
  "nextContentUrl": "#next_url@href"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 正文分页处理（nextContentUrl）

### 难度评估

**难度**: ⭐⭐⭐
