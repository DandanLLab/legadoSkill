# 格格看书

## 基本信息
- **书源名称**: 格格看书
- **书源地址**: https://www.ggkshu.com
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

目录乱序修正逻辑说明：
1. 
正则提取  <dd><a href="...">章节名</a></dd>  所有章节
2. 
按URL中的数字（ /az_xxx/数字.html ）从小到大排序
3. 
去重后输出为  <ol><li><a href="...">...</a></li></ol> 
4. 
CSS选择器  li a  提取排序后的章节

## 规则配置

### 搜索URL
```js
/search.html?az={{key}}
```

### 搜索规则
```js
{
  "author": "td:eq(3)@text",
  "bookList": "table.search-list tr",
  "bookUrl": "td:eq(1) a@href",
  "kind": "td:eq(0)@text##\\[|\\]",
  "lastChapter": "td:eq(2) a@text",
  "name": "td:eq(1) a@text"
}
```

### 发现URL
```js
仙侠修真::/sort/20_0_0_0/?page={{page}}
都市言情::/sort/21_0_0_0/?page={{page}}
历史军事::/sort/22_0_0_0/?page={{page}}
现代言情::/sort/23_0_0_0/?page={{page}}
网游竞技::/sort/24_0_0_0/?page={{page}}
科幻灵异::/sort/25_0_0_0/?page={{page}}
武侠仙侠::/sort/26_0_0_0/?page={{page}}
侦探推理::/sort/62_0_0_0/?page={{page}}
```

### 发现规则
```js
{
  "author": ".s5@text&&.s4@text##\\d+-\\d+",
  "bookList": ".bd ul li",
  "bookUrl": ".s2 a@href",
  "kind": ".s1@text",
  "lastChapter": ".s3 a@text",
  "name": ".s2 a@text"
}
```

### 详情规则
```js
{
  "author": "div.small span:eq(0) a@text",
  "coverUrl": "div.cover img@data-src",
  "intro": "div.intro@text##简介：|推荐地址：.*手机阅读",
  "kind": "div.small span:eq(1) a@text",
  "lastChapter": "div.small span.last a@text",
  "name": "div.info h2@text"
}
```

### 目录规则
```js
{
  "chapterList": "<js>\nvar sUrl=String(source.bookSourceUrl);\nvar base=baseUrl.replace(/\\?.*$/,'');\nvar html=java.ajax(baseUrl);\nvar chapters=[];\nvar seen={};\n\n// 获取总页数\nvar pageMatch=html.match(/<select[^>]*>([\\s\\S]*?)<\\/select>/);\nvar totalPages=1;\nif(pageMatch){\n    var optRe=/<option[^>]*value=\"[^\"]*\\?page=(\\d+)/g;\n    var om;\n    while((om=optRe.exec(pageMatch[1]))!==null){\n        var p=parseInt(om[1]);\n        if(p>totalPages)totalPages=p;\n    }\n}\n\n// 循环获取每一页\nfor(var page=1;page<=totalPages;page++){\n    if(page>1){\n        html=java.ajax(base+'?page='+page);\n    }\n    var re=/<dd><a\\s+href\\s*=\\s*\"([^\"]+)\"[^>]*>([^<]+)<\\/a><\\/dd>/g;\n    var m;\n    while((m=re.exec(html))!==null){\n        var href=m[1];\n        if(href.indexOf('http')!==0){\n            href=(href.indexOf('/')===0)?sUrl+href:base+'/'+href;\n        }\n        if(!seen[href]){\n            seen[href]=true;\n            chapters.push({name:m[2],url:href});\n        }\n    }\n}\n\n// 按URL中的数字排序\nchapters.sort(function(a,b){\n    var na=parseInt((a.url.match(/\\/(\\d+)(?:_\\d+)?\\.html/)||[0,0])[1]);\n    var nb=parseInt((b.url.match(/\\/(\\d+)(?:_\\d+)?\\.html/)||[0,0])[1]);\n    return na-nb;\n});\n\n// 输出\nvar out='<ol>';\nfor(var i=0;i<chapters.length;i++){\n    out+='<li><a href=\"'+chapters[i].url+'\">'+chapters[i].name+'</a></li>';\n}\nout+='</ol>';\nresult=out;\n</js>\nli a",
  "chapterName": "a@text",
  "chapterUrl": "a@href"
}
```

### 正文规则
```js
{
  "content": "div#htmlContent@html",
  "nextContentUrl": "a.Readpage_down@href"
}
```

## 技术分析

### 核心技术点

- 正文分页处理（nextContentUrl）
- bookUrlPattern: https://www\.ggkshu\.com/az_\d+/

### 难度评估

**难度**: ⭐⭐
