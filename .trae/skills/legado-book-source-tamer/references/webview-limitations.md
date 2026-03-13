# WebView的JavaScript限制

本文档说明java.webView()的JavaScript使用限制。

## 目录

1. [核心原则](#核心原则)
2. [原因说明](#原因说明)
3. [关键理解](#关键理解)
4. [正确用法示例](#正确用法示例)
5. [最佳实践](#最佳实践)
6. [记忆口诀](#记忆口诀)

---

## 核心原则

**java.webView() 的 js 参数只能写纯 JavaScript ES5 和部分 ES6 代码，不能使用 DOM 和 BOM API。**

---

## 原因说明

Legado 使用 **Rhino 1.8.0** JavaScript 引擎执行代码，有以下限制：

| 特性 | 支持 | 说明 |
|------|------|------|
| **ES5 语法** | 完全支持 | var、function、基本语法 |
| **部分 ES6** | 部分支持 | let、const（有作用域问题）、箭头函数 |
| **DOM API** | 不支持 | document、window、getElementById等 |
| **BOM API** | 不支持 | location、history、navigator等 |

---

## 关键理解

**执行环境切换**：
```
js参数在浏览器环境中执行 → 可以使用DOM/BOM
返回后在Rhino环境中处理 → 只能用ES5语法
Webview不是指的webjs，而是指的Legado的webView函数。
```

---

## 正确用法示例

```javascript
// 正确：js参数在浏览器环境中执行
java.webView(html, url, 
    'setTimeout(function(){' +
    '  var html = document.documentElement.outerHTML;' +  // 浏览器环境，可以使用DOM
    '  window.legado.getHTML(html);' +
    '}, 5000);'
);

// 正确：返回后在Rhino环境中处理
var html = java.webView(html, url, js);
var content = html.replace(/<script[\s\S]*?<\/script>/g, '');  // Rhino环境，只能用ES5
```

---

## 最佳实践

1. **使用 var 而不是 let/const**（避免作用域问题）
2. **使用传统函数而不是箭头函数**（更稳定）
3. **在 js 参数中使用浏览器 API，返回后在 Rhino 中处理**

---

## 记忆口诀

```
WebView的js参数，
浏览器环境执行。
返回后的处理，
Rhino环境执行。
只能用ES5语法，
var和function最稳。
环境分清楚，
各司其职好！
```
