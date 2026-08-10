# 38看书

## 基本信息
- **书源名称**: 38看书
- **书源地址**: https://www.38ksw.com
- **书源分组**: AI,优质
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

原：www.38ksw.com
搜索通过搜搜书(sososhu.com)搜索引擎进行，需登录后使用。

【技术实现】
搜索：sososhu.com 搜索（GET /?s={{key}}&web=38kanshu，WebView 模式）
发现：CSS 选择器（排行/分类/全本）
详情：CSS 选择器
目录：CSS 选择器（分页已配置 nextTocUrl）
正文：CSS 选择器（章节内 _N 分页，已配置 nextContentUrl）

【登录说明】
- 登录需填写手机号、密码、图形验证码。
- 点击「刷新验证码」会在浏览器中打开验证码图片，查看后返回输入。
- 登录成功后自动保存 Cookie，后续请求自动携带。
- 登出按钮可清除 Cookie 和登录状态。
- ★ 新增「签 到」按钮：登录后点击即可完成每日签到，成功后 Toast 提示。

【局限性】
- 搜索需要登录：未登录访问搜索会跳转登录页，请先登录。
- 搜索每账号每天限 8 次。
- 搜索通过 sososhu.com 搜索引擎进行，搜索结果链接到 38 看书网。
- 网站自身搜索已关闭，原来通过必应搜索，现改用 sososhu.com 搜索。

## 规则配置

### 搜索URL
```js
<js>
var url = "https://www.sososhu.com/?s=" + encodeURIComponent(key) + "&web=38kanshu";
if (page > 1) {
    url += "&page=" + page;
}
url + ',{"webView":true}';
</js>
```

### 搜索规则
```js
{
  "bookList": "<js>\nvar doc = org.jsoup.Jsoup.parse(result);\nvar bodyText = doc.text();\n\n// 搜索次数检测\nif (bodyText.indexOf(\"已用完\") > -1) {\n    var match = bodyText.match(/(\\d+)次[\\/每]天/);\n    java.longToast(match ? \"⚠️ 今日搜索次数已用完（\" + match[1] + \"次/天），明天再来吧！\" : \"⚠️ 今日搜索次数已用完，明天再来吧！\");\n} else if (bodyText.indexOf(\"需要登录\") > -1 || result.indexOf(\"action=login\") > -1) {\n    java.longToast(\"⚠️ 未检测到登录状态，请先登录！\");\n} else {\n    // 尝试从 profile API 获取搜索次数\n    try {\n        var profile = java.ajax(\"https://www.sososhu.com/?action=user_api&act=profile\");\n        var pJson = JSON.parse(profile);\n        if (pJson.code === 0 && pJson.data) {\n            var d = pJson.data;\n            java.longToast(\"🔍 今日剩余搜索: \" + d.searchRemaining + \"/\" + d.searchMax + \" 次\" + (d.signedToday ? \" | 今日已签到 ✅\" : \" | 今日未签到 ❌\"));\n        }\n    } catch(e) {}\n}\n\n// 提取书籍结果 - 查找指向 38ksw.com 的链接\nvar bookLinks = doc.select(\"a[href*=38ksw]\");\nvar sb = \"\";\nvar seen = {};\nfor (var i = 0; i < bookLinks.size(); i++) {\n    var link = bookLinks.get(i);\n    var href = link.attr(\"abs:href\");\n    if (href.match(/38ksw\\.com\\/\\d+/) && !seen[href]) {\n        seen[href] = true;\n        var name = link.text().trim();\n        name = name.replace(/最新章节.*|全文阅读.*|,.*|_.*/g, \"\").trim();\n        if (name) {\n            sb += '<div class=\"book-item\"><a href=\"' + href + '\">' + name + '</a></div>';\n        }\n    }\n}\nresult = sb;\n</js>\n.book-item",
  "bookUrl": "a@href",
  "name": "a@text##最新章节.*|全文阅读.*|,.*|_.*"
}
```

### 发现URL
```js
总排行榜::/rank/allvisit/
月排行榜::/rank/monthvisit/
周排行第::/rank/weekvisit/
收藏榜::/rank/goodnum/
全部::/quanben/fenlei/{{page}}/
玄幻::/fenlei/1/{{page}}/
奇幻::/fenlei/2/{{page}}/
武侠::/fenlei/3/{{page}}/
仙侠::/fenlei/4/{{page}}/
都市::/fenlei/5/{{page}}/
军事::/fenlei/6/{{page}}/
历史::/fenlei/7/{{page}}/
游戏::/fenlei/8/{{page}}/
竞技::/fenlei/9/{{page}}/
科幻::/fenlei/10/{{page}}/
悬疑::/fenlei/11/{{page}}/
灵异::/fenlei/12/{{page}}/
其他::/fenlei/13/{{page}}/
古代言情::/fenlei/14/{{page}}/
仙侠奇缘::/fenlei/15/{{page}}/
现代言情::/fenlei/16/{{page}}/
浪漫青春::/fenlei/17/{{page}}/
玄幻言情::/fenlei/18/{{page}}/
悬疑灵异::/fenlei/19/{{page}}/
科幻空间::/fenlei/20/{{page}}/
游戏竞技::/fenlei/21/{{page}}/
二次元::/fenlei/24/{{page}}/
```

### 发现规则
```js
{
  "author": "class.author@text##作者：|（.*?）",
  "bookList": "class.hot_sale",
  "bookUrl": "tag.a@href",
  "intro": "class.review@text##简介：",
  "name": "class.title@text"
}
```

### 详情规则
```js
{
  "author": "class.author@text##作者：",
  "coverUrl": "class.synopsisArea_detail tag.img@src",
  "intro": "class.review@text",
  "kind": "class.sort@text##类别：",
  "lastChapter": "class.lastchapter tag.a@text",
  "name": "class.title@text"
}
```

### 目录规则
```js
{
  "chapterList": "class.recommend.1@class.directoryArea@tag.p@tag.a",
  "chapterName": "text",
  "chapterUrl": "href",
  "nextTocUrl": "text.下一页@href"
}
```

### 正文规则
```js
{
  "content": "id.chaptercontent@html##<p class=\"chapter-page-info\">[\\s\\S]*?</p>|<div style=\"width:100%;text-align:center;\">[\\s\\S]*?</div>|<span>\\d+</span>|<script[\\s\\S]*?</script>|谨记我们的网址[\\s\\S]*?宣传宣传。|本章未完[\\s\\S]*?继续阅读。",
  "nextContentUrl": "text.下一页@href"
}
```

### 登录配置
```js
loginUrl:
function getBaseUrl() { return 'https://www.sososhu.com'; }

function refreshCaptcha() {
    var url = getBaseUrl() + '/?action=captcha_api&t=' + Math.random();
    java.startBrowser(url, '验证码');
}

function login(b) {
    if (b == undefined) return true;
    var info = result;
    var mobile = info['手机号'];
    var password = info['密码'];
    var captcha = info['验证码'];
    if (!mobile || !password || !captcha) {
        java.toast('请完整填写手机号、密码和验证码');
        return;
    }
    var url = getBaseUrl() + '/?action=user_api&act=login';
    var body = 'mobile=' + encodeURIComponent(mobile) + '&password=' + encodeURIComponent(password) + '&captcha=' + encodeURIComponent(captcha);
    var post = JSON.stringify({
        method: 'POST',
        body: body,
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    var resp = java.ajax(url + ',' + post);
    try {
        var json = JSON.parse(resp);
        if (json.code === 0) {
            var cookieString = java.getCookie(getBaseUrl());
            if (cookieString) {
                source.putLoginHeader(cookieString);
            }
            java.toast('登录成功');
        } else {
            java.toast('登录失败：' + json.msg);
            refreshCaptcha();
        }
    } catch(e) {
        java.toast('登录异常：' + e.message);
    }
}

function logout() {
    source.removeLoginHeader();
    cookie.removeCookie(getBaseUrl());
    result['手机号'] = '';
    result['密码'] = '';
    result['验证码'] = '';
    source.putLoginInfo(JSON.stringify(result));
    java.toast('已登出');
}

function checkin() {
    var url = getBaseUrl() + '/?action=user_api&act=sign_in';
    var post = JSON.stringify({
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
    });
    var resp = java.ajax(url + ',' + post);
    try {
        var json = JSON.parse(resp);
        if (json.code === 0) {
            java.toast('✅ 签到成功：' + (json.msg || ''));
        } else {
            java.toast('❌ 签到失败：' + json.msg);
        }
    } catch(e) {
        java.toast('签到异常：' + e.message);
    }
}
```

### 登录UI
```js
[{"name": "手机号", "type": "text"}, {"name": "密码", "type": "password"}, {"name": "验证码", "type": "text"}, {"name": "刷新验证码", "type": "button", "action": "refreshCaptcha()"}, {"name": "登 录", "type": "button", "action": "login(true)", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.5}}, {"name": "登 出", "type": "button", "action": "logout()", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.5}}, {"name": "签 到", "type": "button", "action": "checkin()", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.5}}]
```

## 技术分析

### 核心技术点

- WebView浏览器模式，用于处理JS渲染或验证
- 需要登录（CookieJar + loginUrl）
- 支持签到功能
- 验证码处理（图形验证码弹窗）
- CookieJar已启用，自动管理登录状态
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）
- 第三方搜索引擎集成（sososhu.com）
- JSoup直接解析HTML
- bookUrlPattern: https://www.38ksw.com/\d+/
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐⭐
