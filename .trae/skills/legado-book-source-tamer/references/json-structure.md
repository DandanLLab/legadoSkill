# 书源JSON结构

本文档定义书源JSON的完整结构。

## 目录

1. [必填字段](#必填字段)
2. [详情页与目录页规则](#详情页与目录页规则)
3. [输出格式要求](#输出格式要求)

---

## 必填字段

```json
{
  "bookSourceUrl": "必填",
  "bookSourceName": "必填",
  "searchUrl": "必填",
  "ruleSearch": {
    "bookList": "必填",
    "name": "必填",
    "bookUrl": "必填"
  },
  "ruleToc": {
    "chapterList": "必填",
    "chapterName": "必填",
    "chapterUrl": "必填"
  },
  "ruleContent": {
    "content": "必填"
  }
}
```

---

## 详情页与目录页规则

**重要规则**：
- **如果详情页和目录页在同一个页面**（即bookUrl指向的页面就是目录页），则 `tocUrl` 字段**不需要填写**
- **只有当详情页和目录页是分开的两个页面时**，才需要填写 `tocUrl` 字段指向目录页地址

### 示例1：详情页和目录页是同一页（不需要tocUrl）

```json
{
  "ruleSearch": {
    "bookUrl": "/book/123.html"  // 这个页面既是详情页也是目录页
  },
  "ruleBookInfo": {
    "name": "h1@text",
    "author": ".author@text"
    // 不需要 tocUrl
  },
  "ruleToc": {
    "chapterList": "#list dd a"  // 直接在当前页面提取目录
  }
}
```

### 示例2：详情页和目录页是分开的（需要tocUrl）

```json
{
  "ruleSearch": {
    "bookUrl": "/book/123.html"  // 详情页
  },
  "ruleBookInfo": {
    "name": "h1@text",
    "author": ".author@text",
    "tocUrl": "a.read@href"      // 需要跳转到另一个页面获取目录
  },
  "ruleToc": {
    "chapterList": "#list dd a"  // 在tocUrl指向的页面提取目录
  }
}
```

### 判断方法

1. 点击搜索结果进入书籍页面
2. 查看页面是否已经显示章节列表
3. 如果有章节列表 → 详情页和目录页是同一页，不需要 `tocUrl`
4. 如果没有章节列表，需要点击"开始阅读"等按钮 → 需要填写 `tocUrl`

---

## 输出格式要求

**必须输出JSON数组格式**：
```json
[
  {
    "bookSourceName": "书源名称",
    "bookSourceUrl": "https://example.com",
    ...
  }
]
```
