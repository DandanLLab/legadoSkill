# JavaScript开发完整指南

本文档详细说明Legado书源开发中的JavaScript使用方法。

## 目录

1. [环境配置](#环境配置)
2. [核心变量表](#核心变量表)
3. [网络请求方法](#网络请求方法)
4. [编码解码方法](#编码解码方法)
5. [加密解密方法](#加密解密方法)
6. [内容解析方法](#内容解析方法)
7. [缓存管理方法](#缓存管理方法)
8. [书源与书籍操作](#书源与书籍操作)
9. [Cookie管理](#cookie管理)
10. [文件操作方法](#文件操作方法)
11. [工具函数](#工具函数)

---

## 环境配置

| 配置项 | 说明 |
|--------|------|
| JavaScript引擎 | Rhino 1.8.0 |
| 变量声明 | 必须使用 `var`，避免使用 `const`/`let`（块级作用域问题） |
| Java调用 | 使用 `Packages.java.*` 访问Java包 |

---

## 核心变量表

| 变量名 | 类型 | 说明 |
|--------|------|------|
| `java` | 当前类 | 主要功能入口，万能工具箱 |
| `baseUrl` | String | 当前页面URL |
| `result` | Any | 上一步结果 |
| `book` | Book类 | 书籍信息操作 |
| `chapter` | Chapter类 | 章节信息操作 |
| `source` | BaseSource类 | 书源配置操作 |
| `cookie` | CookieStore类 | Cookie管理 |
| `cache` | CacheManager类 | 缓存管理 |

---

## 网络请求方法

```javascript
// 简单请求
java.ajax(url)                    // 返回字符串
java.connect(url)                 // 返回StrResponse

// HTTP方法
java.get(url, headers, timeout)
java.post(url, body, headers, timeout)
java.head(url, headers, timeout)

// 并发请求
java.ajaxAll(urlList)             // 批量请求

// WebView请求
java.webView(html, url, js)       // 执行JS获取内容
java.webViewGetOverrideUrl(html, url, js, regex)  // 获取跳转URL
java.webViewGetSource(html, url, js, regex)       // 获取资源URL
```

---

## 编码解码方法

```javascript
// Base64编码
java.base64Encode(str)
java.base64Encode(str, flags)
java.base64Decode(str)
java.base64Decode(str, charset)

// 十六进制编码
java.hexEncodeToString(str)
java.hexDecodeToString(hex)
java.hexDecodeToByteArray(hex)

// URL编码
java.encodeURI(str)
java.encodeURI(str, "UTF8")

// 字符集转换
java.strToBytes(str, "UTF8")      // 字符串转字节
java.bytesToStr(bytes, "GBK")     // 字节转字符串
```

---

## 加密解密方法

```javascript
// 对称加密（AES等）
var cipher = java.createSymmetricCrypto("AES/CBC/PKCS5Padding", key, iv)
cipher.encryptHex(data)           // 加密为HEX
cipher.encryptBase64(data)        // 加密为Base64
cipher.decryptStr(encryptedData)  // 解密为字符串

// 非对称加密（RSA）
var rsa = java.createAsymmetricCrypto("RSA")
rsa.setPublicKey(publicKey)
rsa.encryptBase64(data, true)     // 使用公钥加密

// 摘要算法
java.md5Encode(str)               // MD5编码
java.md5Encode16(str)             // 16位MD5
java.digestHex(data, "SHA256")    // SHA256
java.digestBase64Str(data, "SHA1") // SHA1 Base64

// HMAC算法
java.HMacHex(data, "HmacSHA256", key)
java.HMacBase64(data, "HmacMD5", key)

// 签名验证
var sign = java.createSign("SHA256withRSA")
sign.setPrivateKey(privateKey)
sign.signHex(data)                // 生成签名
```

---

## 内容解析方法

```javascript
// 文本提取
java.getString(ruleStr, content, isUrl)
java.getStringList(ruleStr, content, isUrl)

// 元素提取
java.getElement(ruleStr)
java.getElements(ruleStr)

// 内容设置
java.setContent(content, baseUrl)

// 重新获取机制
java.reGetBook()                  // 重新搜索书籍
java.refreshTocUrl()              // 刷新目录URL
```

---

## 缓存管理方法

```javascript
// 数据库缓存
cache.put(key, value, saveTime)   // 保存（秒）
cache.get(key)                    // 读取
cache.delete(key)                 // 删除

// 文件缓存（大文件）
cache.putFile(key, value, saveTime)
cache.getFile(key)

// 内存缓存（临时）
cache.putMemory(key, value)
cache.getFromMemory(key)
```

---

## 书源与书籍操作

```javascript
// 书源操作
source.getKey()                   // 获取书源URL
source.getVariable()              // 获取书源变量
source.setVariable(data)          // 设置书源变量
source.put(key, value)            // 自定义变量存储
source.get(key)                   // 自定义变量读取

// 登录头管理
source.getLoginHeader()           // 获取登录头
source.putLoginHeader(header)     // 设置登录头
source.removeLoginHeader()        // 清除登录头

// 书籍属性
book.name                         // 书名
book.author                       // 作者
book.coverUrl                     // 封面
book.intro                       // 简介
book.bookUrl                      // 书籍URL
book.tocUrl                       // 目录URL
book.durChapterTitle              // 当前章节
book.durChapterIndex              // 章节索引
book.durChapterPos                // 阅读位置

// 章节属性
chapter.title                     // 章节标题
chapter.url                       // 章节URL
chapter.index                     // 章节序号
chapter.baseUrl                   // 基础URL
```

---

## Cookie管理

```javascript
cookie.getCookie(url)             // 获取Cookie
cookie.setCookie(url, cookieStr)  // 设置Cookie
cookie.replaceCookie(url, cookieStr) // 替换Cookie
cookie.removeCookie(url)          // 删除Cookie
```

---

## 文件操作方法

```javascript
// 下载与读取
java.downloadFile(url)            // 下载文件
java.readTxtFile(path)            // 读取文本文件
java.readTxtFile(path, "UTF8")    // 指定编码读取

// 压缩文件处理
java.unzipFile(zipPath)           // 解压ZIP
java.unrarFile(rarPath)           // 解压RAR
java.un7zFile(archivePath)        // 解压7Z
java.unArchiveFile(archivePath)   // 通用解压

// 文件夹操作
java.getTxtInFolder(folderPath)   // 读取文件夹内所有文本

// 压缩包内容读取
java.getZipStringContent(url, filePath)
java.getRarStringContent(url, filePath, "GBK")
java.get7zByteArrayContent(url, filePath)
```

---

## 工具函数

```javascript
// 调试输出
java.log("调试信息")              // 输出日志
java.logType(variable)            // 输出类型
java.toast("提示信息")            // 短时提示
java.longToast("长提示")          // 长时提示
```
