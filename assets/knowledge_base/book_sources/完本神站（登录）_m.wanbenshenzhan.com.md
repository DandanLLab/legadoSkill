# 完本神站（登录）

## 基本信息
- **书源名称**: 完本神站（登录）
- **书源地址**: https://m.wanbenshenzhan.com
- **书源分组**: AI,优质
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

完本神站（m.wanbenshenzhan.com）
搜索通过搜搜书(sososhu.com)搜索引擎进行，需登录后使用。

【技术实现】
搜索：sososhu.com 搜索（GET /?s={{key}}&web=38kanshu）
  - 搜索结果由 JS 从 Base64 编码的 JSON 动态渲染
  - bookList 规则直接从 HTML 提取 Base64 数据并解码，不依赖 WebView
  - 搜索结果链接指向 m.wanbenshenzhan.com
发现：wanbenshenzhan.com 书库/排行榜（表格+卡片两种布局）
详情：wanbenshenzhan.com CSS 选择器
目录：wanbenshenzhan.com CSS 选择器（?chapter_page=N 分页）
正文：wanbenshenzhan.com CSS 选择器

【登录说明】
- 登录需填写手机号、密码、图形验证码。
- 点击「刷新验证码」会在浏览器中打开验证码图片，查看后返回输入。
- 登录成功后自动保存 Cookie，后续请求自动携带。
- 登出按钮可清除 Cookie 和登录状态。
- ★ 「签 到」按钮：登录后点击即可完成每日签到，成功后 Toast 提示。
- ★ 搜索时自动检测签到状态，若未签到则自动签到。

【局限性】
- 搜索需要登录：未登录访问搜索会跳转登录页，请先登录。
- 搜索每账号每天限 8 次。
- 搜索结果搜索次数提示会自动 Toast 显示剩余次数和签到状态。
- 搜索结果 URL 中的 token 参数已自动去除，避免过期问题。

## 规则配置

### 搜索URL
```js
<js>
var url = "https://www.sososhu.com/?s=" + encodeURIComponent(key) + "&web=38kanshu";
if (page > 1) {
    url += "&page=" + page;
}
url;
</js>
```

### 搜索规则
```js
{
  "author": "class.book-meta@class.author@text##作者：",
  "bookList": "<js>\nvar doc = org.jsoup.Jsoup.parse(result);\nvar bodyText = doc.text();\n\n// 搜索次数检测\nif (bodyText.indexOf(\"已用完\") > -1) {\n    var match = bodyText.match(/(\\d+)次[\\/每]天/);\n    java.longToast(match ? \"⚠️ 今日搜索次数已用完（\" + match[1] + \"次/天），明天再来吧！\" : \"⚠️ 今日搜索次数已用完，明天再来吧！\");\n} else if (bodyText.indexOf(\"需要登录\") > -1 || result.indexOf(\"action=login\") > -1) {\n    java.longToast(\"⚠️ 未检测到登录状态，请先登录！\");\n} else {\n    // 从页面提取剩余搜索次数\n    var quotaEl = doc.select(\"#quota-remaining\");\n    if (quotaEl && quotaEl.size() > 0) {\n        var remaining = quotaEl.first().text();\n        // 尝试从 profile API 获取更详细的信息\n        try {\n            var profile = java.ajax(\"https://www.sososhu.com/?action=user_api&act=profile\");\n            // 处理BOM字符\n            if (profile.charCodeAt(0) === 0xFEFF) profile = profile.substring(1);\n            var pJson = JSON.parse(profile);\n            if (pJson.code === 0 && pJson.data) {\n                var d = pJson.data;\n                var signMsg = \"\";\n                if (!d.signedToday) {\n                    // 未签到，自动签到\n                    try {\n                        var signPost = JSON.stringify({method: \"POST\", headers: {\"Content-Type\": \"application/x-www-form-urlencoded\"}});\n                        var signResp = java.ajax(\"https://www.sososhu.com/?action=user_api&act=sign_in,\" + signPost);\n                        if (signResp.charCodeAt(0) === 0xFEFF) signResp = signResp.substring(1);\n                        var signJson = JSON.parse(signResp);\n                        signMsg = signJson.code === 0 ? \" | 已自动签到 ✅\" : \" | 签到失败: \" + signJson.msg;\n                    } catch(e2) {\n                        signMsg = \" | 自动签到异常\";\n                    }\n                } else {\n                    signMsg = \" | 今日已签到 ✅\";\n                }\n                java.longToast(\"🔍 今日剩余搜索: \" + d.searchRemaining + \"/\" + d.searchMax + \" 次\" + signMsg);\n            } else {\n                java.longToast(\"🔍 今日剩余搜索: \" + remaining + \" 次\");\n            }\n        } catch(e) {\n            java.longToast(\"🔍 今日剩余搜索: \" + remaining + \" 次\");\n        }\n    }\n}\n\n// 从HTML中提取Base64编码的书籍数据（不依赖WebView渲染）\nvar match = result.match(/var books = JSON\\.parse\\(d\\(\"([^\"]+)\"\\)\\)/);\nif (match) {\n    var b64 = match[1];\n    // 使用Legado的Base64解码（Android默认UTF-8）\n    var decoded = java.base64Decode(b64);\n    var books = JSON.parse(decoded);\n\n    // HTML转义函数\n    function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }\n    // 构造HTML元素列表（用数组拼接，不用StringBuilder）\n    var htmlArr = [\"<html><body>\"];\n    for (var i = 0; i < books.length; i++) {\n        var b = books[i];\n        var cleanUrl = b.url.replace(/\\?token=.*$/, \"\");\n        var tag = b.fullflag ? '<span class=\"tag tag-end\">完结</span>' : '<span class=\"tag tag-serial\">连载</span>';\n        var lastHtml = b.lastchap ? '<p class=\"book-last\">最新：' + esc(b.lastchap) + '</p>' : '';\n        htmlArr.push('<div class=\"book-card\">');\n        htmlArr.push('<a href=\"' + cleanUrl + '\" class=\"book-cover\"><img src=\"' + b.cover + '\"></a>');\n        htmlArr.push('<div class=\"book-info\">');\n        htmlArr.push('<h3><a href=\"' + cleanUrl + '\">' + esc(b.name) + '</a>' + tag + '</h3>');\n        htmlArr.push('<p class=\"book-meta\"><span class=\"author\">作者：' + esc(b.author) + '</span>');\n        htmlArr.push('<span class=\"count\">' + b.chapters + '章 · ' + b.allvisit + '阅读</span></p>');\n        htmlArr.push('<p class=\"book-intro\">' + esc(b.intro) + '</p>');\n        htmlArr.push(lastHtml);\n        htmlArr.push('</div></div>');\n    }\n    htmlArr.push(\"</body></html>\");\n    org.jsoup.Jsoup.parse(htmlArr.join(\"\")).select(\"div.book-card\");\n} else {\n    // 如果Base64提取失败，尝试直接从DOM中查找（兼容WebView模式）\n    doc.select(\"div.book-card\");\n}\n</js>",
  "bookUrl": "class.book-info@tag.h3@tag.a@href##\\?token=.*$",
  "coverUrl": "class.book-cover@tag.img@src",
  "intro": "class.book-intro@text",
  "kind": "class.book-info@tag.h3@tag.span@text",
  "lastChapter": "class.book-last@text##最新：",
  "name": "class.book-info@tag.h3@tag.a@text",
  "wordCount": "class.book-meta@class.count@text##.*章 · |阅读"
}
```

### 发现URL
```js
————————书库——————————
全部::/all/0_lastupdate_0_0_{{page}}.html
玄幻::/all/1_lastupdate_0_0_{{page}}.html
奇幻::/all/2_lastupdate_0_0_{{page}}.html
武侠::/all/3_lastupdate_0_0_{{page}}.html
仙侠::/all/4_lastupdate_0_0_{{page}}.html
都市::/all/5_lastupdate_0_0_{{page}}.html
军事::/all/6_lastupdate_0_0_{{page}}.html
历史::/all/7_lastupdate_0_0_{{page}}.html
游戏::/all/8_lastupdate_0_0_{{page}}.html
竞技::/all/9_lastupdate_0_0_{{page}}.html
科幻::/all/10_lastupdate_0_0_{{page}}.html
悬疑::/all/11_lastupdate_0_0_{{page}}.html
灵异::/all/12_lastupdate_0_0_{{page}}.html
————————言情——————————
古代言情::/all/14_lastupdate_0_0_{{page}}.html
仙侠奇缘::/all/15_lastupdate_0_0_{{page}}.html
现代言情::/all/16_lastupdate_0_0_{{page}}.html
浪漫青春::/all/17_lastupdate_0_0_{{page}}.html
玄幻言情::/all/18_lastupdate_0_0_{{page}}.html
悬疑灵异::/all/19_lastupdate_0_0_{{page}}.html
科幻空间::/all/20_lastupdate_0_0_{{page}}.html
游戏竞技::/all/21_lastupdate_0_0_{{page}}.html
BL文::/all/22_lastupdate_0_0_{{page}}.html
GL文::/all/23_lastupdate_0_0_{{page}}.html
二次元::/all/24_lastupdate_0_0_{{page}}.html
————————完本——————————
完本全部::/all/0_lastupdate_1_0_{{page}}.html
完本玄幻::/all/1_lastupdate_1_0_{{page}}.html
完本仙侠::/all/4_lastupdate_1_0_{{page}}.html
完本都市::/all/5_lastupdate_1_0_{{page}}.html
完本历史::/all/7_lastupdate_1_0_{{page}}.html
————————排行——————————
点击榜::/top/allvisit.html
周点击::/top/weekvisit.html
收藏榜::/top/goodnum.html
推荐榜::/top/allvote.html
新书榜::/top/postdate.html
更新榜::/top/lastupdate.html
```

### 发现规则
```js
{
  "author": "class.author@text||class.rank-book-info@class.meta@tag.span.0@text##作者：",
  "bookList": "class.data-table@tag.tbody@tag.tr||class.rank-item",
  "bookUrl": "class.book-name@tag.a@href||class.rank-cover@tag.a@href",
  "coverUrl": "class.rank-cover@tag.img@src",
  "intro": "class.desc@text",
  "kind": "class.sort@text||class.rank-book-info@class.meta@tag.span.1@text##分类：|\\[|\\]",
  "lastChapter": "class.chapter@tag.a@text||class.latest@tag.a@text",
  "name": "class.book-name@tag.a@text||class.rank-book-info@tag.h4@tag.a@text",
  "wordCount": "class.words@text"
}
```

### 详情规则
```js
{
  "author": "class.book-meta@tag.span.0@text##作者：",
  "coverUrl": "class.book-cover-large@tag.img@src",
  "intro": "class.book-intro@tag.p@text",
  "kind": "class.book-meta@tag.span.1@text##分类：",
  "lastChapter": "class.latest-chapter-link@tag.a@text",
  "name": "class.book-info-detail@tag.h1@text##编辑",
  "wordCount": "class.book-meta@tag.span.3@text##字数："
}
```

### 目录规则
```js
{
  "chapterList": "id.chapter-list@class.chapter-list@tag.a",
  "chapterName": "text",
  "chapterUrl": "href",
  "nextTocUrl": "text.下一页@href"
}
```

### 正文规则
```js
{
  "content": "class.chapter-content@html##<p>【完本神站】[^<]*</p>|<p>\\s*</p>"
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
        // 处理BOM字符
        var respText = resp;
        if (respText.charCodeAt(0) === 0xFEFF) respText = respText.substring(1);
        var json = JSON.parse(respText);
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
        var respText = resp;
        if (respText.charCodeAt(0) === 0xFEFF) respText = respText.substring(1);
        var json = JSON.parse(respText);
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

- 需要登录（CookieJar + loginUrl）
- 支持签到功能
- 验证码处理（图形验证码弹窗）
- CookieJar已启用，自动管理登录状态
- Base64编码/解码处理
- 目录分页处理（nextTocUrl）
- 第三方搜索引擎集成（sososhu.com）
- JSoup直接解析HTML
- bookUrlPattern: https://m\.wanbenshenzhan\.com/\d+/
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐⭐
