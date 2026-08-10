# 菠萝猫（登录）

## 基本信息
- **书源名称**: 菠萝猫（登录）
- **书源地址**: https://www.boluomao1.com
- **书源分组**: AI,优质
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

原：www.boluomao.com
移动网用：www.boluomao1.com
【技术实现】
搜索：HTML 搜索（GET /search/?q={{key}}&page={{page}}）
发现：CSS 选择器（书库/分类/完结/排行/专题）
详情：CSS 选择器
目录：CSS 选择器（?cp=N 分页，已配置 nextTocUrl）
正文：CSS 选择器（章节内 ?p=N 分页，已配置 nextContentUrl 自动合并）

【登录说明】
- 登录需填写手机号、密码、图形验证码。
- 点击「刷新验证码」会在浏览器中打开验证码图片，查看后返回输入。
- 登录成功后自动保存 Cookie，后续请求自动携带。
- 登出按钮可清除 Cookie 和登录状态。
- ★ 「签 到」按钮：登录后点击即可完成每日签到，成功后 Toast 提示。
- ★ 搜索时自动检测登录状态，若已登录则自动签到，无需手动操作。

【局限性】
- 搜索需要登录：未登录访问 /search/ 会 302 跳转登录页，请先登录。
- 搜索每账号每天限 10 次。
- 网站有 WAF 防护，会封禁机房/代理 IP，请在正常网络环境使用。

## 规则配置

### 搜索URL
```js
<js>
var url = "https://www.boluomao.com/search/?q=" + encodeURIComponent(key);
if (page > 1) {
    url += "&page=" + page;
}
url + ',{"webView":true}';
</js>
```

### 搜索规则
```js
{
  "author": ".author@text",
  "bookList": "<js>\nvar doc = org.jsoup.Jsoup.parse(result);\nvar strongText = doc.select(\"span.searchRemain strong\").text();\n\n// 判断登录状态和搜索次数\nvar isLoggedIn = false;\nvar searchMsg = \"\";\nif (strongText && strongText.trim() !== \"\") {\n    isLoggedIn = true;\n    searchMsg = \"🔍 剩余搜索: \" + strongText.trim() + \" 次\";\n} else if (result.indexOf(\"次数已用完\") > -1 || result.indexOf(\"限制\") > -1) {\n    isLoggedIn = true;\n    searchMsg = \"⚠️ 今日搜索次数已耗尽\";\n} else if (result.indexOf(\"退出\") > -1) {\n    isLoggedIn = true;\n    searchMsg = \"🔍 剩余搜索: 12 次\";\n} else {\n    searchMsg = \"⚠️ 未检测到登录状态，请先登录！\";\n}\n\n// 已登录时自动签到\nvar signMsg = \"\";\nif (isLoggedIn) {\n    try {\n        var signPost = JSON.stringify({method: \"POST\", body: \"action=checkin\", headers: {\"Content-Type\": \"application/x-www-form-urlencoded\"}});\n        var signResp = java.ajax(\"https://www.boluomao1.com/api/checkin.php,\" + signPost);\n        var signJson = JSON.parse(signResp);\n        if (signJson.code === 0) {\n            signMsg = \" | 已自动签到 ✅\";\n        } else {\n            signMsg = \" | \" + (signJson.msg || \"已签到\");\n        }\n    } catch(e) {\n        // 签到异常不影响搜索\n    }\n}\n\njava.longToast(searchMsg + signMsg);\ndoc.select(\"div.picList ul li\");\n</js>",
  "bookUrl": ".name a@href",
  "coverUrl": ".pic img@src",
  "intro": ".intro@text",
  "kind": ".label@text",
  "name": ".name a@text",
  "wordCount": ".num@text"
}
```

### 发现URL
```js
————————二次元——————————
二次元书库::/gender/acg/page/{{page}}/
原生幻想::/gender/acg/category/22/page/{{page}}/
恋爱日常::/gender/acg/category/23/page/{{page}}/
衍生同人::/gender/acg/category/24/page/{{page}}/
搞笑吐槽::/gender/acg/category/25/page/{{page}}/


二次元完结::/full/gender/acg/page/{{page}}/
排行榜::/rank/
SF轻小说::/topic/1.html?p={{page}}
刺猬猫小说::/topic/2.html?p={{page}}
少年梦小说::/topic/3.html?p={{page}}
飞卢小说::/topic/4.html?p={{page}}
息壤小说::/topic/5.html?p={{page}}
次元姬小说::/topic/6.html?p={{page}}
————————男频———————————
男生书库::/gender/boy/page/{{page}}/
男生完结::/full/gender/boy/page/{{page}}/
玄幻::/gender/boy/category/1/page/{{page}}/
奇幻::/gender/boy/category/2/page/{{page}}/
武侠::/gender/boy/category/3/page/{{page}}/
仙侠::/gender/boy/category/4/page/{{page}}/
都市::/gender/boy/category/5/page/{{page}}/
军事::/gender/boy/category/6/page/{{page}}/
历史::/gender/boy/category/7/page/{{page}}/
游戏::/gender/boy/category/8/page/{{page}}/
体育::/gender/boy/category/9/page/{{page}}/
科幻::/gender/boy/category/10/page/{{page}}/
诸天无限::/gender/boy/category/11/page/{{page}}/
悬疑::/gender/boy/category/12/page/{{page}}/
————————女频———————————
女生书库::/gender/girl/page/{{page}}/
女生完结::/full/gender/girl/page/{{page}}/
古代言情::/gender/girl/category/13/page/{{page}}/
仙侠奇缘::/gender/girl/category/14/page/{{page}}/
现代言情::/gender/girl/category/15/page/{{page}}/
浪漫青春::/gender/girl/category/16/page/{{page}}/
玄幻言情::/gender/girl/category/17/page/{{page}}/
悬疑推理::/gender/girl/category/18/page/{{page}}/
科幻空间::/gender/girl/category/19/page/{{page}}/
游戏竞技::/gender/girl/category/20/page/{{page}}/
短篇言情::/gender/girl/category/21/page/{{page}}/
耽美::/gender/girl/category/32/page/{{page}}/
百合::/gender/girl/category/33/page/{{page}}/
轻小说::/gender/girl/category/34/page/{{page}}/
```

### 发现规则
```js
{
  "author": ".author@text",
  "bookList": ".picList li||.fullCardList li",
  "bookUrl": ".name a@href",
  "coverUrl": ".pic img@src",
  "intro": ".intro@text",
  "kind": ".label@text",
  "name": ".name a@text",
  "wordCount": ".num@text||.words@text"
}
```

### 详情规则
```js
{
  "author": ".bookTitleLeft .author@text",
  "coverUrl": ".picb .pic img.0@src",
  "intro": ".intro.font16@text",
  "kind": "class.info@tag.dl.0@tag.dd@text&&class.info@tag.dl.1@tag.dd@text&&class.tags-line@tag.a@text",
  "lastChapter": ".latest-link@text",
  "name": ".bookTitleRow h1@text",
  "wordCount": ".num.font14@text"
}
```

### 目录规则
```js
{
  "chapterList": "#chapters .direList li",
  "chapterName": ".name a@text",
  "chapterUrl": ".name a@href",
  "nextTocUrl": ".page-range-list .cur+a@href"
}
```

### 正文规则
```js
{
  "content": ".content@html@js:var html = result; var matches = html.match(/data-obf=\\\"([^\\\"]*)\\\"/g); var decoded = ''; if (matches) { for (var i = 0; i < matches.length; i++) { var obf = matches[i].match(/data-obf=\\\"([^\\\"]*)\\\"/)[1]; var bytes = java.base64DecodeToByteArray(obf); for (var j = 0; j < bytes.length; j++) { bytes[j] = bytes[j] ^ ((j % 127) + 1); } decoded += java.bytesToStr(bytes, 'utf-8') + '\\n'; } } decoded;",
  "nextContentUrl": "text.下一页@href"
}
```

### 登录配置
```js
loginUrl:
function getBaseUrl() { return 'https://www.boluomao1.com'; }

function refreshCaptcha() {
    var url = getBaseUrl() + '/api/captcha.php?r=' + Math.random();
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
    var url = getBaseUrl() + '/api/auth.php';
    var body = 'action=login&mobile=' + encodeURIComponent(mobile) + '&password=' + encodeURIComponent(password) + '&captcha=' + encodeURIComponent(captcha);
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
                java.toast('登录成功');
            } else {
                java.toast('登录成功但未获取到Cookie，请重试');
            }
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
    // 可选清除cookie
    // java.removeCookie(getBaseUrl());
    result['手机号'] = '';
    result['密码'] = '';
    result['验证码'] = '';
    source.putLoginInfo(JSON.stringify(result));
    java.toast('已登出');
}

// ★ 新增签到函数
function checkin() {
    var url = getBaseUrl() + '/api/checkin.php';
    var body = 'action=checkin';
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
            java.toast('✅ 签到成功：' + json.msg);
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
[{"name":"手机号","type":"text"},{"name":"密码","type":"password"},{"name":"验证码","type":"text"},{"name":"刷新验证码","type":"button","action":"refreshCaptcha()"},{"name":"登 录","type":"button","action":"login(true)","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.5}},{"name":"登 出","type":"button","action":"logout()","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.5}},{"name":"签 到","type":"button","action":"checkin()","style":{"layout_flexGrow":1,"layout_flexBasisPercent":0.5}}]
```

## 技术分析

### 核心技术点

- WebView浏览器模式，用于处理JS渲染或验证
- 需要登录（CookieJar + loginUrl）
- 支持签到功能
- 验证码处理（图形验证码弹窗）
- CookieJar已启用，自动管理登录状态
- data-obf属性加密（Base64+XOR）
- 目录分页处理（nextTocUrl）
- 正文分页处理（nextContentUrl）
- JSoup直接解析HTML
- bookUrlPattern: https://www.boluomao.*?\.com/book/\d+.html

### 难度评估

**难度**: ⭐⭐⭐⭐⭐
