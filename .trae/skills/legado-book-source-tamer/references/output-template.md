# 书源输出模板

本文档定义书源JSON的输出格式规范。

## 目录

1. [JSON格式要求](#json格式要求)
2. [书源级别必填字段](#书源级别必填字段)
3. [书源级别可选字段](#书源级别可选字段)
4. [规则级别必填字段](#规则级别必填字段)
5. [输出格式示例](#输出格式示例)
6. [nextContentUrl判断规则](#nextcontenturl判断规则)
7. [严禁使用的字段和选择器](#严禁使用的字段和选择器)

---

## JSON格式要求

**必须**：
- 输出必须是**标准JSON数组格式**（最外层必须是数组）
- 可以直接导入Legado APP
- 不包含任何注释
- 不包含Markdown代码块标记（```json或```js）
- 每个书源对象符合Legado官方规范

**禁止**：
- 输出单个JSON对象（必须是数组）
- 包含注释
- 包含Markdown代码块
- 使用Mock数据
- 缺少必填字段

---

## 书源级别必填字段

```js
{
  "bookSourceUrl": "必填",    // 书源地址（字符串，不能为空）
  "bookSourceName": "必填",   // 书源名称（字符串，不能为空）
  "searchUrl": "必填",        // 搜索URL（字符串，不能为空）
}
```

---

## 书源级别可选字段

```js
{
  "loginCheckJs": "可选",     // Cloudflare验证检测JS（字符串，用于处理CF验证）
  "loginUrl": "可选",         // 登录URL（字符串，用于需要登录的网站）
  "loginUi": "可选",          // 登录界面配置（字符串，自定义登录表单）
  "bookSourceType": "可选",   // 书源类型（数字，0=文字，1=音频，2=图片）
  "bookSourceComment": "可选", // 书源说明（字符串，书源描述信息）
  "enabled": "可选",          // 是否启用（布尔值，默认true）
  "enabledExplore": "可选",   // 是否启用发现（布尔值，默认true）
  "exploreUrl": "可选",       // 发现URL（字符串，分类导航配置）
  "ruleExplore": "可选",      // 发现规则（对象，分类页面解析规则）
}
```

### loginCheckJs 字段详解

用于处理Cloudflare等反爬验证，当网站返回验证页面时自动处理。

| 字段 | 类型 | 说明 | 使用场景 |
|------|------|------|----------|
| `loginCheckJs` | String | 验证检测JS代码 | 网站有Cloudflare保护 |

**使用示例**：
```json
{
  "bookSourceName": "受保护网站",
  "bookSourceUrl": "https://example.com",
  "loginCheckJs": "(function(a){var r=a.url(),o=a.body(),t=a.code();if(o&&(403===t||503===t||502===t||200===t&&(o.includes('Just a moment')||o.includes('Checking your browser')))){...}return a})(result)"
}
```

**重要区分**：
- `loginCheckJs`：用于Cloudflare等验证码/反爬处理
- `loginUrl` + `loginUi`：用于需要账号登录的网站

---

## 规则级别必填字段

```js
{
  "ruleSearch": {
    "bookList": "必填",       // 书籍列表选择器（字符串，不能为空）
    "name": "必填",           // 书名提取规则（字符串，不能为空）
    "bookUrl": "必填"         // 书籍URL提取规则（字符串，不能为空）
  },
  "ruleToc": {
    "chapterList": "必填",    // 章节列表选择器（字符串，不能为空）
    "chapterName": "必填",    // 章节名提取规则（字符串，不能为空）
    "chapterUrl": "必填"      // 章节URL提取规则（字符串，不能为空）
  },
  "ruleContent": {
    "content": "必填"         // 正文内容提取规则（字符串，不能为空）
  }
}
```

---

## 输出格式示例

**正确格式**（标准JSON数组）：

```js
[
  {
    "bookSourceName": "示例书源",
    "bookSourceUrl": "https://www.example.com",
    "searchUrl": "/search?q={{key}}",
    "ruleSearch": {
      "bookList": ".book-item",
      "name": ".title@text",
      "author": ".author@text",
      "coverUrl": "img@src",
      "bookUrl": "a@href"
    },
    "ruleToc": {
      "chapterList": "#chapter-list li",
      "chapterName": "a@text",
      "chapterUrl": "a@href"
    },
    "ruleContent": {
      "content": "#content@html"
    }
  }
]
```

---

## nextContentUrl判断规则

### 核心原则

`nextContentUrl` 字段的设置取决于按钮的**实际功能**，而不是按钮的文字！

### 三种使用场景

**场景1：真正的"下一章"（必须设置 nextContentUrl）**

**适用情况**：
- 按钮链接到**真正的下一章节**内容
- 例如：从"第一章"跳转到"第二章"
- 按钮文字可能是："下一章"、"下章"、"下一节"、"下节"、"下一话"等

**选择器格式**：
- `text.下一章@href` - 如果按钮文字是"下一章"
- `text.下章@href` - 如果按钮文字是"下章"
- `text.下一@href` - 如果按钮文字是"下一"（简写）
- `text.下一节@href` - 如果按钮文字是"下一节"

**场景2：同一章节分页（必须设置 nextContentUrl！）**

**适用情况**：
- 按钮是**同一章节的分页**
- 例如：第一章太长，分成"第一页"、"第二页"显示
- 按钮文字可能是："下一页"、"下一页阅读"、"继续阅读"、"翻到下一页"等
- URL变化方式：/chapter/1_1.html → /chapter/1_2.html（章节号不变，页码变化）

**重要**：`nextContentUrl` 正是用于这种情况！Legado 会自动获取下一页内容并合并。

**场景3：模糊按钮（也需要设置 nextContentUrl）**

**适用情况**：
- 按钮文字不明确（如"下一"、"下页"等）
- 需要根据按钮文字提取链接

### 总结表格

| 按钮文字 | 功能 | nextContentUrl |
|---------|------|----------------|
| "下一章"、"下章" | 跳转到下一章 | 设置 `text.下一章@href` |
| "下一页" | 同一章分页 | **设置** `text.下一页@href` |
| "下一"、"下页" | 模糊按钮 | **设置** `text.下一@href` |
| 无分页按钮 | 单页正文 | 留空 |

### 记忆口诀

```
分页按钮必须配，
无论下章或下页。
nextContentUrl要设置，
Legado自动合并文。
只有单页才留空，
这是规则要记清。
```

---

## 严禁使用的字段和选择器

### 1. ruleContent 中的 prevContentUrl 字段

- **禁止使用**：`prevContentUrl` 字段在 Legado 阅读中**不存在**
- **正确做法**：Legado 正文中只有 `nextContentUrl` 字段

**错误示例**：
```js
{
  "ruleContent": {
    "content": "#chaptercontent@html",
    "nextContentUrl": "text.下一页@href",
    "prevContentUrl": "text.上一页@href"  // 这个字段不存在！禁止使用！
  }
}
```

**正确示例**：
```js
{
  "ruleContent": {
    "content": "#chaptercontent@html##广告[\\s\\S]*?##",
    "nextContentUrl": "text.下一章@href"  // 只有 nextContentUrl
  }
}
```

### 2. 禁止使用 :contains() 伪类选择器

- **禁止使用**：`a:contains(下一章)@href`、`:a:contains()` 等任何形式的 `:contains()` 伪类选择器在 Legado 阅读中**不可用**
- **正确做法**：使用 Default 语法的 `text.文本@href` 或 `text.文本`

**错误示例**：
```js
{
  "ruleContent": {
    "nextContentUrl": "a:contains(下一章)@href"  // 不可用！禁止使用！
  }
}
```

**正确示例**：
```js
{
  "ruleContent": {
    "nextContentUrl": "text.下一章@href"  // 使用 text.文本 格式
  }
}
```

### 3. 禁止使用 :first-child 和 :last-child 伪类选择器

- **禁止使用**：`:first-child` 和 `:last-child` 伪类选择器在 Legado 阅读中**不可用**
- **正确做法**：使用数字索引，如 `.0`（第一个）、`.1`（第二个）、`.-1`（倒数第一个）、`.-2`（倒数第二个）

**错误示例**：
```js
{
  "ruleSearch": {
    "author": ".author:first-child@text##.*作者：##",     // 不可用！
    "lastChapter": ".author:last-child@text##.*更新：##"  // 不可用！
  }
}
```

**正确示例**：
```js
{
  "ruleSearch": {
    "author": ".author.0@text##.*作者：##",     // 使用数字索引
    "lastChapter": ".author.-1@text##.*更新：##"  // 使用数字索引
  }
}
```

### 记忆口诀

- 正文只有 `nextContentUrl`，没有 `prevContentUrl`
- 不用 `:contains()`，用 `text.文本`
- 不用 `:first-child/:last-child`，用 `.0/.1/.-1/.-2`
