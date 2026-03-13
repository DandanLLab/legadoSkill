# 验证码检测与处理指南

本文档详细说明如何检测和处理各类网站验证码（WAF保护/验证码识别/Cloudflare盾）。

---

## 目录

1. [检测方法](#检测方法)
2. [常见WAF类型及特征](#常见waf类型及特征)
3. [处理方法](#处理方法)
4. [检测流程](#检测流程)

---

## 检测方法

### 1. 实际访问测试

**必须通过实际访问网站来确认是否存在验证码**，而不是凭经验猜测！

执行以下测试：
- 访问网站首页
- 尝试执行搜索请求
- 尝试访问书籍详情页

### 2. 响应特征识别

检查返回的HTML内容：

1. **HTTP状态码异常**：
   - 403 Forbidden
   - 502 Bad Gateway
   - 503 Service Unavailable

2. **页面内容特征**：
   - 验证码输入表单
   - 滑动验证元素
   - 特定WAF标识

---

## 常见WAF类型及特征

### Cloudflare

**特征关键词**：
- "Just a moment"
- "Checking your browser"
- "cloudflare"

**检测代码**：
```javascript
o.includes('Just a moment') || o.includes('Checking your browser')
```

---

### GoEdge WAF

**特征关键词**：
- "Verify Yourself"
- "GOEDGE_WAF_CAPTCHA"
- "WAF/VERIFY/CAPTCHA"

**检测代码**：
```javascript
o.includes('Verify Yourself') || o.includes('GOEDGE_WAF_CAPTCHA')
```

---

### 常见WAF标识

| WAF类型 | 特征关键词 |
|---------|-----------|
| Cloudflare | "Just a moment", "Checking your browser" |
| GoEdge WAF | "Verify Yourself", "GOEDGE_WAF_CAPTCHA" |
| 百度云加速 | "yunjiasu", "safety.baidu.com" |
| 阿里云WAF | "aliyun", "waf.aliyun.com" |
| 腾讯云WAF | "waf.qcloud.com" |
| 安全狗 | "safedog", "cloud.safedog.cn" |

---

## 处理方法

### 1. loginCheckJs 字段

在书源JSON中添加 `loginCheckJs` 字段来处理验证码：

```javascript
"loginCheckJs": "(function(a){var r=a.url(),o=a.body(),t=a.code();if(o&&(403===t||503===t||502===t||200===t&&(o.includes('Just a moment')||o.includes('Checking your browser')||o.includes('Verify Yourself')||o.includes('GOEDGE_WAF_CAPTCHA')))){var c=source.get('cf_count')||'0';c=parseInt(c)+1;source.put('cf_count',c);if(c<=3){for(var i=0;i<2;i++){try{var h=java.webView(r,r,'setTimeout(function(){window.legado.getHTML(document.documentElement.outerHTML);},5000);');if(h&&!h.includes('Just a moment')&&!h.includes('Verify Yourself')&&200===java.connect(r).code()){source.put('cf_count','0');return a}}catch(e){}}}java.toast('需要验证码验证');java.startBrowserAwait(r,'验证');source.put('cf_count','0');return java.connect(r)}return a})(result)"
```

### 2. 代码逻辑说明

1. **检测验证页面**：检查响应中是否包含验证码特征关键词
2. **自动重试**：最多重试3次，每次等待5秒
3. **WebView处理**：使用WebView加载页面让用户手动完成验证
4. **验证成功**：返回正常页面内容

### 3. 自定义检测关键词

根据实际检测到的WAF类型，添加相应的检测关键词：

```javascript
// 在条件判断中添加新的WAF检测
o.includes('Your_WAF_Keyword')
```

---

## 检测流程

### 建议的检测顺序

1. **第一步：访问首页**
   ```bash
   curl -L "https://example.com/"
   ```

2. **第二步：测试搜索**
   ```bash
   curl -X POST -d "keyword=test" "https://example.com/search/"
   ```

3. **第三步：检查响应**
   - 检查HTTP状态码
   - 检查HTML内容是否包含验证特征
   - 记录检测到的WAF类型

4. **第四步：配置处理**
   - 根据WAF类型选择合适的处理代码
   - 添加相应的检测关键词

---

## 注意事项

1. **不要凭经验猜测** - 必须实际访问网站进行测试
2. **不同页面可能不同** - 首页、搜索页、详情页可能有不同的验证机制
3. **IP可能被封** - 频繁访问可能导致临时封禁
4. **WebView不是万能的** - 某些高级验证可能无法通过脚本处理
