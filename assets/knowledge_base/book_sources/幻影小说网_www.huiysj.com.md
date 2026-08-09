# 幻影小说网

## 基本信息
- **书源名称**: 幻影小说网
- **书源地址**: https://www.huiysj.com
- **书源分组**: AI,18加
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

Tips：
1、修复目录拼接缺章、乱序问题
2、优化目录加载慢（一定程度上）
3、修复部分章节内容获取失败
目前存在问题：
个别书籍的个别章节加载失败（如天衍录第3章），原因未找到

## 规则配置

### 搜索URL
```js
https://www.huiysj.com/search.html,{"method":"POST","body":"s={{key}}","charset":"utf-8"}
```

### 搜索规则
```js
{
  "author": ".s3 a@text",
  "bookList": "#novel-search li",
  "bookUrl": ".s2 a@href",
  "checkKeyWord": "我的",
  "kind": ".s1@text",
  "lastChapter": ".s4 a@text",
  "name": ".s2 a@text"
}
```

### 发现URL
```js
玄幻修真::https://www.huiysj.com/book/1/{{page}}.html
重生穿越::https://www.huiysj.com/book/2/{{page}}.html
都市小说::https://www.huiysj.com/book/3/{{page}}.html
军史小说::https://www.huiysj.com/book/4/{{page}}.html
网游小说::https://www.huiysj.com/book/5/{{page}}.html
科幻小说::https://www.huiysj.com/book/6/{{page}}.html
灵异小说::https://www.huiysj.com/book/7/{{page}}.html
言情小说::https://www.huiysj.com/book/8/{{page}}.html
其他小说::https://www.huiysj.com/book/9/{{page}}.html
```

### 发现规则
```js
{
  "author": ".s4@text",
  "bookList": ".list_l2 li",
  "bookUrl": ".s2 a@href",
  "kind": ".s1@text",
  "lastChapter": ".s2 a@title##最新章节：",
  "name": ".s2 a@text"
}
```

### 详情规则
```js
{
  "author": ".details .p a@text",
  "coverUrl": ".img img@src",
  "intro": ".details .p2@text",
  "kind": "meta[property=og:novel:category]@content",
  "lastChapter": "meta[property=og:novel:latest_chapter_name]@content",
  "name": ".details h2@text"
}
```

### 目录规则
```js
{
  "chapterList": "@js:\nvar url='https://www.huiysj.com/kuaishou/';\nvar bookId = baseUrl.match(/kuaishou\\/(\\d+)/)[1];\nvar list = new Packages.java.util.ArrayList();\nfirstPage();\notherPage();\n\nfunction firstPage() {\n    var doc = org.jsoup.Jsoup.parse(result.toString());\n    var sections = doc.select('div.info_dv3');\n    for (var s = 0; s < sections.size(); s++) {\n        var sec = sections.get(s);\n        var title = sec.select('div.title').text();\n        if (title.indexOf('\\u7ae0\\u8282\\u5217\\u8868') >= 0) {\n            var links = sec.select('a[href*=/kuaishou/]');\n            for (var i = 0; i < links.size(); i++) {\n                var a = links.get(i);\n                var name = a.text();\n                var hr = a.attr('abs:href');\n                if (name && hr && hr.indexOf('all_') < 0) {\n                    addChap(name, hr);\n                }\n            }\n        }\n    }\n}\n\nfunction otherPage() {\n    for (var p = 1; p < 100; p++) {\n        var pageUrl = url + bookId + '/all_' + p + '/index.html';\n        var html = String(java.ajax(pageUrl));\n        if (!html || html.indexOf('章节列表（第1页）') > 0) {\n            break;\n        }\n        var d2 = org.jsoup.Jsoup.parse(html);\n        var str = d2.select('style').toString();\n        var nthChildCount = (str.match(/ul\\.yanqing_list>li:nth-child\\(/g) || []).length;\n        var nthLastChildCount = (str.match(/ul\\.yanqing_list>li:nth-last-child\\(/g) || []).length;\n        var items = d2.select('ul.yanqing_list li a');\n        if (items.size() === 0) break;\n        for (var k = nthChildCount; k < items.size() - nthLastChildCount; k++) {\n            var a2 = items.get(k);\n            var name = a2.text();\n            var oc = a2.attr('onclick');\n            var m = oc.match(/read_tz\\((\\d+)\\)/);\n            if (m) {\n                addChap(name, url + bookId + '/' + m[1] + '.html');\n            }\n        }\n    }\n}\n\nfunction addChap(name, url) {\n    if (url && url.indexOf('kuaishou') >= 0) {\n        var map = new Packages.java.util.HashMap();\n        map.put(\"name\", name);\n        map.put(\"url\", url);\n        list.add(map);\n    }\n}\n\nlist;",
  "chapterName": "$.name",
  "chapterUrl": "$.url"
}
```

### 正文规则
```js
{
  "content": "@js:\nvar src = String(result);\nvar doc = org.jsoup.Jsoup.parse(src);\n\nfunction decode(d) {\n    var scripts = d.select('script');\n    var s = '';\n    for (var i = 0; i < scripts.size(); i++) {\n        var data = scripts.get(i).data();\n        var m = data.match(/qsbs\\.bb\\('([^']+)'\\)/);\n        if (m) {\n                var bytes = Packages.java.util.Base64.getDecoder().decode(m[1]);\n                s += new Packages.java.lang.String(bytes, 'UTF-8');\n        }\n    }\nif(null == s || s==''){\nvar str=doc.select('div.info_dv1');\nvar pList=str.select('p');\ns=pList.toString();\n}\n    return s;\n}\nvar content = decode(doc);\n\nvar m = baseUrl.match(/kuaishou\\/(\\d+)\\/(\\d+)(?:_\\d+)?\\.html/);\nif (m) {\n    var bid = m[1];\n    var cid = m[2];\n    for (var p = 1; p < 50; p++) {\n            var url = 'https://www.huiysj.com/kuaishou/' + bid + '/' + cid + '_' + p + '.html';\n            var html = String(java.ajax(url));\n            if (!html || html.indexOf('（第1页）') > 0) break;\n            var nextContent = decode(org.jsoup.Jsoup.parse(html));\n            if (!nextContent || nextContent === '') break;\n            content += nextContent;\n    }\n}\n\ncontent;",
  "replaceRegex": "##<p>.*?幻影小说.*?</p>|请关闭浏览器阅读模式.*|手机浏览器扫描.*##"
}
```

## 技术分析

### 核心技术点

- JSoup直接解析HTML
- bookUrlPattern: https://www.huiysj.com/kuaishou/.*/index.html
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐
