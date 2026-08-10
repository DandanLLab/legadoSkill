# 31书斋

## 基本信息
- **书源名称**: 31书斋
- **书源地址**: http://www.31sz.com
- **书源分组**: AI,优质
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

31书斋（www.31sz.com）
免费小说阅读网站，支持登录。

【技术实现】
搜索：GET /novelsearch/search/result.html?searchkey={{key}}
  - 搜索有60秒间隔限制
发现：分类目录（/type/{catId}_{subId}_{status}_{sort}_{page}.html）+ 全本分类 + 排行
  - 分类/全本支持 {{page}} 分页
  - 排行页为单页（总榜/月榜/周榜）
详情：/novel/{bookId}/ CSS 选择器
目录：/dir/{bookId}/（?page=N&sort=asc 分页）
正文：/read/{bookId}/{sourceId}/{chapterId}.html
  - 章节内分页：{chapterId}/{pageNum}.html
  - 已配置 nextContentUrl

【URL 规律】
书籍详情：/novel/{bookId}/
章节目录：/dir/{bookId}/
正文页面：/read/{bookId}/{sourceId}/{chapterId}.html
正文分页：/read/{bookId}/{sourceId}/{chapterId}/{pageNum}.html

【登录说明】
- 简单登录，无需验证码
- 登录表单：用户名、密码
- 登录后自动保存Cookie

【编码】UTF-8

## 规则配置

### 搜索URL
```js
http://www.31sz.com/novelsearch/search/result.html?searchkey={{key}}
```

### 搜索规则
```js
{
  "author": "tag.span.2@tag.a@text",
  "bookList": "<js>\nvar doc = org.jsoup.Jsoup.parse(result);\nvar errorEl = doc.select(\"p.error\");\nvar list;\nif (errorEl.size() > 0) {\n    java.longToast(\"⚠️ \" + errorEl.first().text());\n    list = doc.select(\"p\");\n} else {\n    list = doc.select(\"div.SHsectionThree-middle p\");\n}\nlist;\n</js>",
  "bookUrl": "tag.span.1@tag.a@href",
  "kind": "tag.span.0@tag.a@text",
  "name": "tag.span.1@tag.a@text"
}
```

### 发现URL
```js
————————分类——————————
玄幻::/type/1_0_0_lastupdate_{{page}}.html
仙侠::/type/2_0_0_lastupdate_{{page}}.html
都市::/type/3_0_0_lastupdate_{{page}}.html
职场::/type/4_0_0_lastupdate_{{page}}.html
历史::/type/5_0_0_lastupdate_{{page}}.html
军事::/type/6_0_0_lastupdate_{{page}}.html
科幻::/type/7_0_0_lastupdate_{{page}}.html
游戏::/type/8_0_0_lastupdate_{{page}}.html
灵异::/type/9_0_0_lastupdate_{{page}}.html
现言::/type/11_0_0_lastupdate_{{page}}.html
————————全本——————————
完本全部::/type/0_0_2_lastupdate_{{page}}.html
完本玄幻::/type/1_0_2_lastupdate_{{page}}.html
完本仙侠::/type/2_0_2_lastupdate_{{page}}.html
完本都市::/type/3_0_2_lastupdate_{{page}}.html
完本职场::/type/4_0_2_lastupdate_{{page}}.html
完本历史::/type/5_0_2_lastupdate_{{page}}.html
完本军事::/type/6_0_2_lastupdate_{{page}}.html
完本科幻::/type/7_0_2_lastupdate_{{page}}.html
完本游戏::/type/8_0_2_lastupdate_{{page}}.html
完本灵异::/type/9_0_2_lastupdate_{{page}}.html
完本现言::/type/11_0_2_lastupdate_{{page}}.html
————————排行——————————
总榜::/top_allvisit_1.html
月榜::/top_monthvisit_1.html
周榜::/top_weekvisit_1.html
```

### 发现规则
```js
{
  "author": "tag.p.1@tag.span@tag.a@text",
  "bookList": "div.CGsectionTwo-right-content-unit",
  "bookUrl": "tag.a.0@href",
  "intro": "tag.p.2@text",
  "lastChapter": "tag.p.3@tag.a@text",
  "name": "tag.a.0@text",
  "updateTime": "tag.p.3@text##.*(\\d{4}-\\d{2}-\\d{2})##$1"
}
```

### 详情规则
```js
{
  "author": ".BGsectionOne-top-right .author span a@text",
  "coverUrl": ".BGsectionOne-top-left img@data-original||.BGsectionOne-top-left img@src",
  "intro": ".BGsectionTwo-bottom p@text",
  "kind": ".BGsectionOne-top-right .category > span@text",
  "lastChapter": ".BGsectionOne-top-right .newestChapter span a@text",
  "name": ".BGsectionOne-top-right .title@text",
  "tocUrl": "a.sectionTwo-bottom@href",
  "updateTime": ".BGsectionOne-top-right .time span@text"
}
```

### 目录规则
```js
{
  "chapterList": "ol.BCsectionTwo-top li a",
  "chapterName": "text",
  "chapterUrl": "href",
  "nextTocUrl": "text.下一页@href"
}
```

### 正文规则
```js
{
  "content": ".RBGsectionThree-content@html##<script.*?</script>|-->.*|本章未完[\\s\\S]*",
  "nextContentUrl": "text.下一页@href"
}
```

### 登录配置
```js
loginUrl:
function getBaseUrl() { return 'http://www.31sz.com'; }

function login(b) {
    if (b == undefined) return true;
    var info = result;
    var username = info['用户名'];
    var password = info['密码'];
    if (!username || !password) {
        java.toast('请完整填写用户名和密码');
        return;
    }
    var url = getBaseUrl() + '/user/public/login.html';
    var body = 'username=' + encodeURIComponent(username) + '&password=' + encodeURIComponent(password) + '&action=login';
    var post = JSON.stringify({
        method: 'POST',
        body: body,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    var resp = java.ajax(url + ',' + post);
    try {
        if (resp.indexOf('登录成功') > -1 || resp.indexOf('success') > -1) {
            var cookieString = java.getCookie(getBaseUrl());
            if (cookieString) {
                source.putLoginHeader(cookieString);
            }
            java.toast('登录成功');
        } else {
            java.toast('登录失败，请检查用户名和密码');
        }
    } catch(e) {
        java.toast('登录异常：' + e.message);
    }
}

function logout() {
    source.removeLoginHeader();
    cookie.removeCookie(getBaseUrl());
    result['用户名'] = '';
    result['密码'] = '';
    source.putLoginInfo(JSON.stringify(result));
    java.toast('已登出');
}
```

### 登录UI
```js
[{"name":"用户名","type":"text"},{"name":"密码","type":"password"},{"name":"登 录","type":"button","action":"login(true)","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.5}},{"name":"登 出","type":"button","action":"logout()","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.5}}]
```

## 技术分析

### 核心技术点

- 需要登录（CookieJar + loginUrl）
- CookieJar已启用，自动管理登录状态
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）
- JSoup直接解析HTML
- bookUrlPattern: http://www\.31sz\.com/novel/\d+/
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐⭐
