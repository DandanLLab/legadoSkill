# 搬山人小说网

## 基本信息
- **书源名称**: 搬山人小说网
- **书源地址**: https://www.banshanren.com
- **书源分组**: AI,18加
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

（无描述）

## 规则配置

### 搜索URL
```js
https://www.banshanren.com/search/index?keyword={{key}}&page={{page}},{"charset":"UTF-8"}
```

### 搜索规则
```js
{
  "author": ".info_box.1@text## ·.*",
  "bookList": "ul[class=\"novel_list\"] .novel_li",
  "bookUrl": ".title@href",
  "coverUrl": "img@data-src",
  "intro": ".novel_intro_box p@text",
  "kind": ".category_list a@text",
  "name": ".title@text##🔞",
  "wordCount": ".info_box.1@text##.*· "
}
```

### 发现URL
```js
全部小说::/all/0-0-0-0-0-0-1-{{page}}
奇幻玄幻::/all/0-4-0-0-0-0-1-{{page}}
BG言情::/all/0-5-0-0-0-0-1-{{page}}
BL耽美::/all/0-1-0-0-0-0-1-{{page}}
GL百合::/all/0-2-0-0-0-0-1-{{page}}
现代都市::/all/0-3-0-0-0-0-1-{{page}}
穿越重生::/all/0-7-0-0-0-0-1-{{page}}
武侠仙侠::/all/0-8-0-0-0-0-1-{{page}}
悬疑惊悚::/all/0-10-0-0-0-0-1-{{page}}
历史军事::/all/0-14-0-0-0-0-1-{{page}}
科幻::/all/0-6-0-0-0-0-1-{{page}}
校园::/all/0-13-0-0-0-0-1-{{page}}
同人::/all/0-15-0-0-0-0-1-{{page}}
轻小说::/all/0-16-0-0-0-0-1-{{page}}
最近更新::/all/0-0-0-0-0-1-1-{{page}}
最新上架::/all/0-0-0-0-0-2-1-{{page}}
```

### 发现规则
```js
{
  "author": ".info_box.1@text## ·.*",
  "bookList": "ul[class=\"novel_list\"] .novel_li",
  "bookUrl": ".title@href",
  "coverUrl": "img@data-src",
  "kind": ".category_list a@text",
  "name": ".title@text",
  "wordCount": ".info_box.1@text##.*· "
}
```

### 详情规则
```js
{
  "author": "[name=\"description\"]@content<js>\nvar m = String(result).match(/。.*《.*》是(.*?)创作/);\nif(!m)m=String(result).match(/。.*《.*》是(.*?)的作品/);\nresult=m?m[1]:'';\n</js>",
  "coverUrl": "[property=\"og:image\"]@content",
  "intro": "[property=\"og:description\"]@content",
  "kind": ".novel_tag_list a@title&&.category_list a@text##\\\\#",
  "lastChapter": ".catalog_top_box .hl@text",
  "name": "h1@text"
}
```

### 目录规则
```js
{
  "chapterList": "li[class~=volume_chapter] a&&ul[class~=chapter_list] a",
  "chapterName": "text",
  "chapterUrl": "href"
}
```

### 正文规则
```js
{
  "content": ".chapter_content_box p@html##\\<span.*\\>\\d+\\</span\\>",
  "nextContentUrl": "text.下一章@href"
}
```

### 登录配置
```js
loginUrl:
function login(b){
  if(b===undefined||b===false){
    var h=source.getLoginHeader();
    return h!=null&&h!='';
  }
  var url='https://www.banshanren.com/login';
  var body='loginName='+encodeURIComponent(result['用户名'])+'&password='+encodeURIComponent(result['密码']);
  var post=JSON.stringify({'method':'POST','body':body,'headers':{'Content-Type':'application/x-www-form-urlencoded'}});
  var res=java.ajax(url+','+post);
  java.log('登录响应:'+res);
  if(res&&res.indexOf('"result":"success"')>-1){
    var json=JSON.parse(res);
    source.putLoginHeader(json.model.token);
    java.toast('登录成功: '+json.model.nickName);
    return true;
  }else{
    var msg=res.match(/"msg":"([^"]+)"/);
    java.toast('登录失败: '+(msg?msg[1]:'未知错误'));
    return false;
  }
}
function logout(){
  source.removeLoginHeader();
  java.toast('已登出');
}
```

### 登录UI
```js
[{"name":"用户名","type":"text"},{"name":"密码","type":"password"},{"name":"登录","type":"button","action":"login(true)"},{"name":"登出","type":"button","action":"logout()"}]
```

## 技术分析

### 核心技术点

- 需要登录（CookieJar + loginUrl）
- CookieJar已启用，自动管理登录状态
- 正文分页处理（nextContentUrl）
- bookUrlPattern: https://www.banshanren.com/novel/.*
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐
