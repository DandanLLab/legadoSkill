# POST 请求配置规范

本文档详细说明 POST 请求的配置方法。

## 目录

1. [简单 POST 格式](#简单-post-格式)
2. [关键要点](#关键要点)
3. [复杂 POST 格式（使用 JavaScript）](#复杂-post-格式使用-javascript)

---

## 简单 POST 格式

```
https://www.example.com/search,{"method":"POST","body":"keyword={{key}}&page={{page}}","charset":"gbk"}
```

---

## 关键要点

1. **URL格式注意**：URL与请求参数用逗号分隔时，URL末尾不加斜线
   - 正确：`https://m.example.com/ss,{"method":"POST",...}`
   - 错误：`https://m.example.com/ss/,{"method":"POST",...}`
2. `body` 必须保证是 JavaScript 的 `String` 类型
3. 变量尽量用 `String()` 强转类型
4. `charset` 为 utf-8 时可省略
5. 无特殊情况不需要请求头和 webView
6. POST 参数顺序很重要 - 某些网站会验证参数的顺序，必须保持与原始网站一致
   - 例如：`"body": "q={{key}}&vw={{vw}}&abw={{abw}}&sign={{sign}}"`
   - 参数顺序错误可能导致服务器拒绝请求
7. IP 封禁检测 - 如果多次 API 请求无数据或刚开始有数据后面没数据，可能被网站封禁 IP
   - 症状：返回空数据、固定错误提示、HTTP 状态码异常
   - 解决方法：更换 IP、使用代理、降低请求频率、添加随机延迟
   - 预防：设置合理的 `concurrentRate`（并发率），避免高频请求，并发率是毫秒为单位
   - 给用户返回这个信息："如果POST请求返回空数据或固定错误提示，请检查IP是否被封禁。"

---

## 复杂 POST 格式（使用 JavaScript）

```javascript
@js:
var headers = {"User-Agent": "Mozilla/5.0..."};
var body = "keyword=" + String(key) + "&page=" + String(page);
var option = {"charset": "gbk", "method": "POST", "body": String(body), "headers": headers};
"https://www.example.com/search," + JSON.stringify(option)
```
