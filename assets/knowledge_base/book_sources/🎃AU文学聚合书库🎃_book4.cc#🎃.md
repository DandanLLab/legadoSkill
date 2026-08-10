# 🎃AU文学聚合书库🎃

## 基本信息
- **书源名称**: 🎃AU文学聚合书库🎃
- **书源地址**: https://book4.cc#🎃
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

AI修复，网站多个书源聚合

## 规则配置

### 搜索URL
```js
https://book4.cc/AU文学/searchword?q={{key}}
```

### 搜索规则
```js
{
  "author": "p.author.0@text##作者：",
  "bookList": "<js>\nvar html = String(result);\nvar m = html.match(/\"([A-Za-z0-9+\\/=]{50,})\"/);\nif (m) {\n    html = String(java.base64Decode(m[1]));\n}\nhtml.replace(/<!--|-->/g, \"\");\n</js>\n#book_list li",
  "bookUrl": "a.1@href",
  "coverUrl": "img@src",
  "intro": "p.-1@html##简介：",
  "kind": "p.author.1:-2@text",
  "lastChapter": "a.-1@text",
  "name": "a.1@text##《|》"
}
```

### 发现URL
```js
@js:
var result = [];
var src = String(java.ajax(source.getKey()));
var b = src.match(/"([A-Za-z0-9+\/=]{50,})"/);
if (b) {
    src = String(java.base64Decode(b[1]));
}
var JsDom = Packages.org.jsoup.Jsoup;
var doc = JsDom.parse(src);
var a = doc.select('ul.nav.nav-pills li a');
for (var i = 1; i < a.size(); i++) {
    result.push({
        title: a.get(i).text(),
        url: a.get(i).attr('href') + '{{page}}',
        style: {
            layout_flexGrow: 1,
            layout_flexBasisPercent: 0.2
        }
    });
}
JSON.stringify(result);
```

### 发现规则
```js
{
  "author": "p.author.0@text##作者：",
  "bookList": "<js>\nvar html = String(result);\nvar m = html.match(/\"([A-Za-z0-9+\\/=]{50,})\"/);\nif (m) {\n    html = String(java.base64Decode(m[1]));\n}\nhtml.replace(/<!--|-->/g, \"\");\n</js>\n#main li",
  "bookUrl": "a.1@href",
  "coverUrl": "img@src",
  "intro": "p.-1@text##简介：",
  "kind": "p.author.1:3:4@text",
  "lastChapter": "a.-2@text",
  "name": "h3 a@text##《|》"
}
```

### 详情规则
```js
{
  "author": "$.author",
  "coverUrl": "$.cover",
  "init": "<js>\nvar html = String(result);\nvar m = html.match(/\"([A-Za-z0-9+\\/=]{50,})\"/);\nif (m) {\n    html = String(java.base64Decode(m[1]));\n}\n\nvar data = {}, n = 0, so = 1;\nvar v = book.getVariable(\"custom\");\nvar b = html.match(/book=(\\{[\\s\\S]*?\\})\\s*[;<\\n]/) || [];\ntry {\n    data = JSON.parse(b[1]);\n} catch (err) {\n    try {\n        data = eval(\"(\" + b[1] + \")\");\n    } catch (e2) {\n        data = {};\n    }\n}\n\nvar img = java.getString(\".book-img img@src\", html);\nvar origin = data[\"同书名作者其他阅读源\"] || [];\n\nif (v != \"\" && v != null) {\n    so = n;\n    n = Number(v) - 1;\n}\n\nvar obj = origin[n] || data;\nvar info = '<br>当前源：【' + so + '】状态：' + (obj.isok ? '可用' : '异常') + '\\n最新章节：' + (obj.last_chapter_name || '') + '\\n更新时间：' + (obj.time_update || '') + '\\n源列表（设置书籍变量custom刷新切换源）\\n' + origin.map(function(o, i) {\n    return '源接口：〔' + (i + 1) + '〕状态：' + (o.isok ? '可用' : '异常') + '\\n  最新：' + (o.last_chapter_name || '') + '\\n  更新：' + (o.time_update || '');\n}).join('\\n');\n\nobj.intro = info + ' <br>本书《' + (obj.book_name || book.name) + '》简介：\\n' + (obj.intro || '');\n\nvar load = html.match(/load_js\\('(.+?)'/);\nvar kind = (obj.type_name || '') + ',' + (obj.time_update || '');\nvar last = (obj.last_chapter_name || '') + '•' + (obj.time_update || '');\nobj.kind = kind;\nobj.last = last;\nobj.dir = ((load && load[1]) || '/show_jsload_book_info/') + obj.book_yun_path;\nobj.cover = img || obj.cover || '';\nJSON.stringify(obj);\n</js>",
  "intro": "$.intro",
  "kind": "$.kind",
  "lastChapter": "$.last",
  "name": "$.book_name",
  "tocUrl": "$.dir"
}
```

### 目录规则
```js
{
  "chapterList": "<js>\nvar raw = String(result);\nvar data;\ntry {\n    data = JSON.parse(raw);\n} catch (e) {\n    var m = raw.match(/dstr\\s*=\\s*\"([^\"]+)\"/);\n    if (m) {\n        var step1 = String(java.base64Decode(m[1]));\n        var step2;\n        try {\n            step2 = decodeURIComponent(step1);\n        } catch (e2) {\n            step2 = step1;\n        }\n        data = JSON.parse(step2);\n    } else {\n        data = { chapter_list: [] };\n    }\n}\nvar chapters = data.chapter_list || [];\nvar list = [];\nvar bookUrl = String(book.bookUrl);\nif (bookUrl.charAt(bookUrl.length - 1) !== '/') bookUrl += '/';\nfor (var i = 0; i < chapters.length; i++) {\n    list.push({\n        text: chapters[i].name,\n        url: bookUrl + chapters[i].file_name,\n        info: String(chapters[i].len + '字')\n    });\n}\nlist;\n</js>",
  "chapterName": "text",
  "chapterUrl": "url",
  "preUpdateJs": "java.refreshTocUrl()",
  "updateTime": "info"
}
```

### 正文规则
```js
{
  "content": "<js>\nvar html = String(result);\nvar m = html.match(/\"([A-Za-z0-9+\\/=]{50,})\"/);\nif (m) {\n    html = String(java.base64Decode(m[1]));\n}\nhtml;\n</js>\n.entry-content p@html##<p style.*?/p>|<a[^>]*>[\\s\\S]*?</a>|请各位大哥.*?感谢支持|正在阅读.*|当前章节.*"
}
```

## 技术分析

### 核心技术点

- CookieJar已启用，自动管理登录状态
- JS init动态提取参数
- bookUrlPattern: https?://book4\.cc/AU文学/.{1,3}/\d+/
- 自定义请求头
- 自定义JS库（jsLib）

### 难度评估

**难度**: ⭐⭐⭐⭐⭐
