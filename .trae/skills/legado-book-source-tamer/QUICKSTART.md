# 快速入门指南

欢迎使用 Legado 书源驯兽师！本指南帮助你快速上手书源开发。

## 📖 何时使用此 Skill？

### ✅ 适合场景

**创建书源**：
- "为 https://www.example.com 创建一个书源"
- "帮我做笔趣阁的书源，要能搜索和看发现"
- "这个网站怎么做书源？https://www.tumuu.com"

**调试书源**：
- "这个书源搜索失败怎么办？[粘贴书源]"
- "书源正文乱码，帮我看看什么问题"
- "目录规则不工作，章节列表获取不到"

**学习书源开发**：
- "Legado 书源的搜索规则怎么写？"
- "CSS 选择器和 XPath 有什么区别？"
- "如何处理加密的 API 参数？"

**优化书源**：
- "这个书源太慢了，怎么优化？"
- "网站有反爬机制，书源被限制了"
- "帮我把书源的规则精简一下"

### ❌ 不适合场景

**简单问题（可以直接回答）**：
- "推荐几本小说" → 直接推荐小说
- "Legado 在哪里下载" → 提供下载链接
- "书源是什么" → 简单解释概念

**非书源相关问题**：
- "如何安装 Legado APP" → 提供安装教程
- "小说结局是什么" → 直接回答剧情

## 🚀 使用示例

### 示例 1：创建书源

```
用户：为 https://www.tumuu.com 创建一个书源，只做搜索

Skill：收到！我将为全本小说网创建书源。

【第一阶段：收集信息】
1. 查询知识库 - 了解书源开发规范
2. 检测网站编码 - UTF-8
3. 获取真实 HTML - 分析网站结构
4. 发现搜索 API - POST /api/search

【第二阶段：编写规则】
- 搜索规则：JSONPath 提取
- 书名：$.title
- 作者：$.author
- 书籍 URL：$.book_detail_url

【第三阶段：输出书源】
已生成书源 JSON，保存到 temp/全本小说 tumuu/全本小说 tumuu.json

请在 Legado APP 中导入测试！
```

### 示例 2：调试书源

```
用户：这个书源搜索失败，帮我看看
[粘贴书源 JSON]

Skill：让我分析一下你的书源...

问题分析：
1. ❌ searchUrl 格式错误 - 缺少 POST 配置
2. ❌ ruleSearch.bookList 选择器不匹配
3. ✅ ruleSearch.name 正确

修复方案：
1. 修改 searchUrl 为 POST 请求
2. 更新 bookList 为 $.data.search[*]
3. 添加必要的请求头

这是修复后的书源...[输出完整书源]
```

### 示例 3：学习规则写法

```
用户：Legado 的 CSS 选择器怎么写？

Skill：CSS 选择器是 Legado 最常用的规则语法。

基础语法：
- `.class` - 选择 class
- `#id` - 选择 id
- `tag` - 选择标签
- `@text` - 提取文本
- `@href` - 提取链接

示例：
- `.book-title@text` - 获取 class 为 book-title 的文本
- `#chapter-list a@href` - 获取 id 为 chapter-list 下的所有 a 标签链接

详细用法请查看：references/css-selector-reference.md
```

## 📋 工作流程

当你请求创建书源时，Skill 会按以下流程工作：

```
【第一阶段：收集】
├─ 查询知识库（了解规范）
├─ 检测网站编码（UTF-8/GBK）
├─ 获取真实 HTML（分析结构）
└─ 记录信息（不创建书源）

【第二阶段：审查】
├─ 编写规则（基于真实 HTML）
├─ 验证语法（确保正确）
├─ 处理特殊情况（加密/反爬）
└─ 最后审查

【第三阶段：创建】
├─ 准备完整 JSON
├─ 输出给用户
└─ 保存到 temp/书源名称/目录
```

## 💡 提示技巧

**提供完整信息**：
- ✅ "为 https://www.example.com 创建书源，需要搜索和发现功能"
- ❌ "做个书源"（缺少网站地址）

**说明具体需求**：
- ✅ "只做搜索，不需要发现"
- ✅ "要能处理验证码"
- ✅ "网站有手机版和电脑版，用哪个？"

**提供错误信息**：
- ✅ "搜索报错：403 Forbidden"
- ✅ "正文显示乱码"
- ❌ "不工作"（太模糊）

## 📚 下一步

- 查看 [FAQ.md](FAQ.md) 了解常见问题
- 阅读 [references/workflow-guide.md](references/workflow-guide.md) 了解完整工作流程
- 参考 [references/book-source-templates.md](references/book-source-templates.md) 查看书源模板

开始创建你的第一个书源吧！🎉
