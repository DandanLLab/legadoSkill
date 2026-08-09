# 无极书院

## 基本信息
- **书源名称**: 无极书院
- **书源地址**: http://m.wjzxchina.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

无极书院：http://m.wjzxchina.com
支持搜索/发现/详情/目录/正文，POST搜索，正文分页清洗

## 规则配置

### 搜索URL
```js
/search/,{"method":"POST","body":"q={{key}}"}
```

### 搜索规则
```js
{
  "author": ".bk-author@text",
  "bookList": "<js>\nvar html = String(result);\nvar doc = Packages.org.jsoup.Jsoup.parse(html);\nvar dls = doc.select('dl.B');\nvar sb = '<html><body><ul>';\nfor (var i = 0; i < dls.size(); i++) {\n    var dl = dls.get(i);\n    var dt = dl.selectFirst('dt a');\n    if (!dt) continue;\n    var name = String(dt.text());\n    var url = String(dt.attr('href'));\n    var img = dl.selectFirst('dd.imgB img');\n    var cover = '';\n    if (img) {\n        cover = String(img.attr('src'));\n        if (!cover) cover = String(img.attr('data-src'));\n    }\n    var author = '';\n    var intro = '';\n    var lastChapter = '';\n    var spans = dl.select('dd span');\n    for (var j = 0; j < spans.size(); j++) {\n        var sp = spans.get(j);\n        var sptext = String(sp.text());\n        if (sptext.indexOf('作者') >= 0) {\n            author = sptext.replace(/.*作者[：:]\\s*/, '');\n        }\n    }\n    var d2 = dl.selectFirst('dd.d2');\n    if (d2) intro = String(d2.text()).replace(/.*简介[：:]\\s*/, '');\n    var dds = dl.select('dd');\n    for (var k = 0; k < dds.size(); k++) {\n        var ddtext = String(dds.get(k).ownText());\n        if (ddtext.indexOf('最新章节') >= 0) {\n            var lcA = dds.get(k).selectFirst('a');\n            if (lcA) lastChapter = String(lcA.text());\n        }\n    }\n    sb += '<li>';\n    sb += '<div class=\"bk-name\"><a href=\"' + url + '\">' + name + '</a></div>';\n    sb += '<div class=\"bk-author\">' + author + '</div>';\n    sb += '<div class=\"bk-intro\">' + intro + '</div>';\n    sb += '<div class=\"bk-cover\"><img src=\"' + cover + '\"></div>';\n    sb += '<div class=\"bk-last\">' + lastChapter + '</div>';\n    sb += '</li>';\n}\nsb += '</ul></body></html>';\nsb;\n</js>\nul li",
  "bookUrl": ".bk-name a@href",
  "coverUrl": ".bk-cover img@src",
  "intro": ".bk-intro@text",
  "lastChapter": ".bk-last@text",
  "name": ".bk-name a@text"
}
```

### 发现URL
```js
[{"title": "分类", "url": "", "style": {"layout_flexGrow": 0, "layout_flexBasisPercent": 1}}, {"title": "玄幻奇幻", "url": "/wuji345/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "仙侠武侠", "url": "/wuji342/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "都市重生", "url": "/wuji341/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "科幻未来", "url": "/wuji343/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "女生言情", "url": "/wuji344/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "游戏竞技", "url": "/wuji347/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "二次元", "url": "/wuji346/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "灵异悬疑", "url": "/wuji349/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "历史军事", "url": "/wuji348/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "书库", "url": "/all/index/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "完本", "url": "/quanben/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}, {"title": "排行榜", "url": "/top/", "style": {"layout_flexGrow": 1, "layout_flexBasisPercent": 0.29}}]
```

### 发现规则
```js
{
  "author": ".bk-author@text",
  "bookList": "<js>\nvar html = String(result);\nvar doc = Packages.org.jsoup.Jsoup.parse(html);\nvar dls = doc.select('dl.B');\nvar sb = '<html><body><ul>';\nfor (var i = 0; i < dls.size(); i++) {\n    var dl = dls.get(i);\n    var dt = dl.selectFirst('dt a');\n    if (!dt) continue;\n    var name = String(dt.text());\n    var url = String(dt.attr('href'));\n    var img = dl.selectFirst('dd.imgB img');\n    var cover = '';\n    if (img) {\n        cover = String(img.attr('src'));\n        if (!cover) cover = String(img.attr('data-src'));\n    }\n    var author = '';\n    var intro = '';\n    var lastChapter = '';\n    var spans = dl.select('dd span');\n    for (var j = 0; j < spans.size(); j++) {\n        var sp = spans.get(j);\n        var sptext = String(sp.text());\n        if (sptext.indexOf('作者') >= 0) {\n            author = sptext.replace(/.*作者[：:]\\s*/, '');\n        }\n    }\n    var d2 = dl.selectFirst('dd.d2');\n    if (d2) intro = String(d2.text()).replace(/.*简介[：:]\\s*/, '');\n    var dds = dl.select('dd');\n    for (var k = 0; k < dds.size(); k++) {\n        var ddtext = String(dds.get(k).ownText());\n        if (ddtext.indexOf('最新章节') >= 0) {\n            var lcA = dds.get(k).selectFirst('a');\n            if (lcA) lastChapter = String(lcA.text());\n        }\n    }\n    sb += '<li>';\n    sb += '<div class=\"bk-name\"><a href=\"' + url + '\">' + name + '</a></div>';\n    sb += '<div class=\"bk-author\">' + author + '</div>';\n    sb += '<div class=\"bk-intro\">' + intro + '</div>';\n    sb += '<div class=\"bk-cover\"><img src=\"' + cover + '\"></div>';\n    sb += '<div class=\"bk-last\">' + lastChapter + '</div>';\n    sb += '</li>';\n}\nsb += '</ul></body></html>';\nsb;\n</js>\nul li",
  "bookUrl": ".bk-name a@href",
  "coverUrl": ".bk-cover img@src",
  "intro": ".bk-intro@text",
  "lastChapter": ".bk-last@text",
  "name": ".bk-name a@text"
}
```

### 详情规则
```js
{
  "author": "class.B@tag.dd.1@text##.*作者[：:]\\s*##",
  "coverUrl": "dl.B dd.imgB img@src",
  "intro": ".nrjj .e@text",
  "kind": "class.B@tag.dd.2@tag.span.0@text##.*类别[：:]\\s*##",
  "lastChapter": "class.B@tag.dd.4@tag.a@text",
  "name": "dl.B dt@text",
  "tocUrl": ".nrbt .F a@href"
}
```

### 目录规则
```js
{
  "chapterList": "ul.MLlist li a",
  "chapterName": "@text",
  "chapterUrl": "@href"
}
```

### 正文规则
```js
{
  "content": "<js>\nvar html = String(result);\nvar doc = Packages.org.jsoup.Jsoup.parse(html);\nvar content = doc.selectFirst('div.TxtContent');\nvar lines = [];\nif (content) {\n    var ps = content.select('p');\n    for (var i = 0; i < ps.size(); i++) {\n        var t = String(ps.get(i).text()).replace(/\\u00a0/g, ' ').trim();\n        if (t && !/温馨提示|本章.*完.*继续阅读|wjzxchina/.test(t)) {\n            lines.push(t);\n        }\n    }\n    if (lines.length === 0) {\n        var text = String(content.text()).replace(/\\u00a0/g, ' ').trim();\n        if (text) lines.push(text);\n    }\n}\nlines.join('\\n');\n</js>",
  "nextContentUrl": "text.下一页@href"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- 正文分页处理（nextContentUrl）
- JSoup直接解析HTML
- bookUrlPattern: https?://m\.wjzxchina\.com/wuji/\d+/?
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐
