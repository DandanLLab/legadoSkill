# POST请求配置规范

本文档详细说明POST请求的配置方法。

## 目录

1. [简单POST格式](#简单post格式)
2. [关键要点](#关键要点)
3. [复杂POST格式（使用JavaScript）](#复杂post格式使用javascript)

---

## 简单POST格式

```
https://www.example.com/search,{"method":"POST","body":"keyword={{key}}&page={{page}}","charset":"gbk"}
```

---

## 关键要点

1. `body`必须保证是JavaScript的`String`类型
2. 变量尽量用`String()`强转类型
3. `charset`为utf-8时可省略
4. 无特殊情况不需要请求头和webView

---

## 复杂POST格式（使用JavaScript）

```javascript
@js:
var headers = {"User-Agent": "Mozilla/5.0..."};
var body = "keyword=" + String(key) + "&page=" + String(page);
var option = {"charset": "gbk", "method": "POST", "body": String(body), "headers": headers};
"https://www.example.com/search," + JSON.stringify(option)
```
