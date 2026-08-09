# 🍉owllook聚合小说搜索引擎

## 基本信息
- **书源名称**: 🍉owllook聚合小说搜索引擎
- **书源地址**: https://www.owlook.com.cn
- **书源分组**: AI
- **书源类型**: 文本 (0)
- **创建时间**: 2026-08-09 21:26:04

## 书源描述

备用网址：www1.owlook.com.cn
owllook开源小说搜索引擎聚合书源

v16 根本性优化发现加载速度：
问题: v15在bookUrl中用java.ajax()搜索，Legado显示发现列表时对每本书
      都执行ajax(1.5s/本)，80本书=120秒
修复: bookUrl只编码中文参数(瞬时)，不做ajax搜索
      改用ruleBookInfo.tocUrl在用户点击后才搜索提取详情页链接

流程对比:
  v15: 发现页→80本书各ajax搜索(120s)→显示列表
  v16: 发现页→编码URL(瞬时)→显示列表→点击→访问搜索页→提取详情页→目录
  v16.1:搜索增加cookie.removeCookie

v14修复（已保留）：
- content: @js:遍历选择器(#txt→#htmlContent→#content→#booktxt→.show-content)
- chapterUrl: 纯URL逻辑(不依赖#content_url)
- chapterList: CSS逗号兼容6种源站结构
全程零WebView

## 规则配置

### 搜索URL
```js
{{url=source.getKey();
cookie.removeCookie(url);}}/search?wd={{key}}
```

### 搜索规则
```js
{
  "author": "li > a@text##.*--##",
  "bookList": ".result_item",
  "bookUrl": "a.0@href@js:var u = String(result || ''); u = u.replace(/&amp;/g, '&'); var m = u.match(/^(.*?novels_name=)([^&]*)$/); if (m) { u = m[1] + java.encodeURI(m[2]); } if (u.indexOf('http') !== 0) { u = 'https://www.owlook.com.cn' + (u.charAt(0) === '/' ? u : '/' + u); } result = u;",
  "name": "li > a@text##.*?--(.*?)--.*##$1"
}
```

### 发现URL
```js
起点月票榜::/md/qidian
起点玄幻::/md/qidian?type=玄幻
起点奇幻::/md/qidian?type=奇幻
起点武侠::/md/qidian?type=武侠
起点仙侠::/md/qidian?type=仙侠
起点都市::/md/qidian?type=都市
起点现实::/md/qidian?type=现实
起点军事::/md/qidian?type=军事
起点历史::/md/qidian?type=历史
起点游戏::/md/qidian?type=游戏
起点体育::/md/qidian?type=体育
起点科幻::/md/qidian?type=科幻
起点悬疑::/md/qidian?type=悬疑
起点轻小说::/md/qidian?type=轻小说
起点诸天无限::/md/qidian?type=诸天无限
纵横人气榜::/md/zongheng
```

### 发现规则
```js
{
  "bookList": "table.mdui-table tbody tr",
  "bookUrl": "td a@href@js:var s=String(result||'');if(s.indexOf('http')!==0){s='https://www.owlook.com.cn'+(s.charAt(0)==='/'?s:'/'+s);}var m=s.match(/^(.*?wd=)(.*)$/);if(m){s=m[1]+java.encodeURI(m[2]);}result=s;",
  "name": "td a@text"
}
```

### 详情规则
```js
{
  "author": "@js:if(baseUrl.indexOf('/search?')>=0){var t=String(java.getString('.result_item a.0@text')||'');var m=t.match(/.*--(.*)$/);result=m?m[1]:'';}else{result='';}",
  "name": "@js:if(baseUrl.indexOf('/search?')>=0){var m=baseUrl.match(/wd=([^&]+)/);result=m?decodeURIComponent(m[1]):'';}else{result=java.getString('#novels_name@value');}",
  "tocUrl": "@js:if(baseUrl.indexOf('/search?')>=0){var u=String(java.getString('.result_item a.0@href')||'');u=u.replace(/&amp;/g,'&');var m=u.match(/^(.*?novels_name=)([^&]*)$/);if(m){u=m[1]+java.encodeURI(m[2]);}if(u.indexOf('http')!==0){u='https://www.owlook.com.cn'+(u.charAt(0)==='/'?u:'/'+u);}result=u;}else{result='';}"
}
```

### 目录规则
```js
{
  "chapterList": "ul.info li, .dirlist li, .book_list li, .chapterlist li, dd,ul li,.result_item li,.list dl dd,.list-chapterAll dd",
  "chapterName": "a@text",
  "chapterUrl": "a@href@js:var h=String(result||'');var n=java.getString('a@text');var b='https://www.owlook.com.cn';var u=String(baseUrl);var m1=u.match(/[?&]url=([^&]+)/);var m2=u.match(/[?&]novels_name=([^&]+)/);var bu='',bn='';if(m1){bu=m1[1];}if(m2){bn=m2[1];try{bn=decodeURIComponent(bn);}catch(e){}}if(!h){result=baseUrl;}else{h=h.replace(/&amp;/g,'&');var fullUrl='';if(h.indexOf('http')===0){fullUrl=h;}else if(h.charAt(0)==='/'){var md=bu.match(new RegExp('^(https?://[^/]+)'));fullUrl=md?md[1]+h:bu+h;}else{fullUrl=bu.charAt(bu.length-1)==='/'?bu+h:bu+'/'+h;}result=b+'/owllook_content?url='+java.encodeURI(fullUrl)+'&name='+java.encodeURI(n)+'&chapter_url='+java.encodeURI(bu)+'&novels_name='+java.encodeURI(bn);}"
}
```

### 正文规则
```js
{
  "content": "@js:var s=['#txt','#htmlContent','#content','#booktxt','.show-content'];var c='';for(var i=0;i<s.length;i++){c=java.getString(s[i]+'@html');if(c&&c.length>100){break;}}result=c;",
  "replaceRegex": "##&nbsp;## "
}
```

### 登录配置
```js
loginUrl:
https://www.owlook.com.cn
```

## 技术分析

### 核心技术点

- 需要登录（CookieJar + loginUrl）
- 搜索前清除Cookie（频率限制规避）
- 自定义请求头

### 难度评估

**难度**: ⭐⭐⭐⭐
