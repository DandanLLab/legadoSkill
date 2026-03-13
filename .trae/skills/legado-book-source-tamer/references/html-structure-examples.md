# HTML结构示例

本文档包含常见HTML结构及对应的书源规则示例。

## 目录

1. [标准列表结构（有封面）](#示例1标准列表结构有封面)
2. [搜索页结构（无封面，信息合并）](#示例2搜索页结构无封面信息合并)
3. [懒加载图片](#示例3懒加载图片)

---

## 示例1：标准列表结构（有封面）

**HTML**：
```html
<div class="book-list">
  <div class="item">
    <img src="cover.jpg" class="cover"/>
    <a href="/book/1" class="title">书名</a>
    <p class="author">作者：张三</p>
  </div>
</div>
```

**规则**：
```js
{
  "ruleSearch": {
    "bookList": ".book-list .item",
    "name": ".title@text",
    "author": ".author@text##^作者：##",
    "bookUrl": "a@href",
    "coverUrl": "img@src"
  }
}
```

---

## 示例2：搜索页结构（无封面，信息合并）

**HTML**：
```html
<div class="hot_sale">
  <a href="/biquge_317279/">
    <p class="title">末日成神：我的我的我的都是我的异能</p>
    <p class="author">科幻灵异 | 作者：钱真人</p>
    <p class="author">连载 | 更新：第69章 魔师</p>
  </a>
</div>
```

**规则**：
```js
{
  "ruleSearch": {
    "bookList": ".hot_sale",
    "name": ".title@text",
    // 方法1：删除前缀法（推荐）
    "author": ".author p.0@text##.*\\| |作者：##",
    "kind": ".author p.0@text##\\|.*##",
    "lastChapter": ".author p.1@text##.*更新：##",
    // 方法2：使用捕获组提取法（更灵活）
    // "author": ".author p.0@text##.*作者：(.*)##$1",
    // "kind": ".author p.0@text##^([^|]*)\\|.*##$1",
    // "lastChapter": ".author p.1@text##.*更新：(.*)##$1",
    "bookUrl": "a@href",
    "coverUrl": ""
  }
}
```

**注意**：
- 使用数字索引 `.0` 表示第一个元素（替代 `:first-child`）
- 使用数字索引 `.-1` 表示倒数第一个元素（替代 `:last-child`）
- 使用数字索引 `p.0` 和 `p.1` 选择不同的段落标签
- 正则表达式可以使用两种方式：删除前缀或使用捕获组提取
  - 删除前缀：`##.*作者：##` - 删除"作者："及前面的内容
  - 捕获组提取：`##.*作者：(.*)##$1` - 提取"作者："后面的内容
  - 两种方法都可以，选择哪种取决于具体需求

---

## 示例3：懒加载图片

**HTML**：
```html
<img class="lazy" data-original="cover.jpg" src="placeholder.jpg"/>
```

**规则**：
```js
{
  "coverUrl": "img.lazy@data-original||img@src"
}
```

---

## 分析重点

在分析真实HTML时，**必须**检查以下字段是否存在：

### 搜索页（ruleSearch）检查清单
- [ ] 书籍列表容器（.bookList）
- [ ] 书名- **必填**
- [ ] 书籍URL（.bookUrl）- **必填**
- [ ] 封面图片- 如果有
- [ ] 作者- 如果有
- [ ] 分类- 如果有
- [ ] 最新章节- 如果有
- [ ] 简介- 如果有

### 书籍详情页（ruleBookInfo）检查清单
- [ ] 书名- **必填**
- [ ] 作者- **必填**
- [ ] 封面图片- 如果有
- [ ] 分类- 如果有
- [ ] 简介- 如果有
- [ ] 最新章节- 如果有
- [ ] 字数- 如果有
- [ ] 状态- 如果有

### 目录页（ruleToc）检查清单
- [ ] 章节列表容器（.chapterList）- **必填**
- [ ] 章节名- **必填**
- [ ] 章节URL（.chapterUrl）- **必填**
- [ ] 下一页链接- **如果有分页**

### 正文页（ruleContent）检查清单
- [ ] 正文内容- **必填**
- [ ] 下一页链接- 根据页面结构判断
- [ ] 需要清理的广告/提示文本
- [ ] 禁止使用 `prevContentUrl` 字段 - Legado中没有这个字段
- [ ] 禁止使用 `:contains()` 伪类选择器 - 应使用 `text.文本` 格式
