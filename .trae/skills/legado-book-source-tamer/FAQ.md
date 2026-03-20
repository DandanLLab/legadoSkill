# 常见问题解答（FAQ）

## 书源导入问题

### Q: 书源导入后搜索不到内容？

**检查步骤**：

1. **验证 searchUrl 是否正确**
   ```json
   // 错误示例 - 缺少 POST 配置
   "searchUrl": "/api/search"

   // 正确示例 - 包含完整配置
   "searchUrl": "/api/search,{\"method\":\"POST\",\"body\":\"q={{key}}\"}"
   ```
2. **检查 ruleSearch.bookList 选择器**
   - 使用浏览器开发者工具查看 API 返回的 JSON 结构
   - 确认 JSONPath 表达式正确（如 `$.data.search[*]`）
3. **查看 Legado 日志**
   - 打开 Legado → 我的 → 书源管理
   - 长按书源 → 调试
   - 输入测试关键词，查看错误信息
4. **网站是否有反爬机制**
   - 检查是否需要 Cookie
   - 检查是否有频率限制
   - 检查是否需要加密参数

### Q: 书源导入后显示"格式错误"？

**原因**：

- JSON 格式不正确（缺少逗号、引号等）
- 必填字段缺失（bookSourceUrl、bookSourceName、searchUrl）
- 使用了不支持的字段

**解决方法**：

```json
// 最小可用书源
{
  "bookSourceUrl": "https://www.example.com",
  "bookSourceName": "示例书源",
  "searchUrl": "/search?q={{key}}",
  "ruleSearch": {
    "bookList": ".book-item",
    "name": ".title@text",
    "bookUrl": "a@href"
  }
}
```

## 搜索规则问题

### Q: 搜索规则怎么写？

**基本结构**：

```json
{
  "searchUrl": "/search?q={{key}}",
  "ruleSearch": {
    "bookList": "书籍列表选择器（必填）",
    "name": "书名提取规则（必填）",
    "author": "作者提取规则",
    "bookUrl": "书籍 URL 提取规则（必填）",
    "coverUrl": "封面图片 URL",
    "intro": "简介",
    "kind": "分类",
    "lastChapter": "最新章节",
    "wordCount": "字数"
  }
}
```

**常用语法**：

- CSS 选择器：`.class@text`、`#id@href`
- JSONPath：`$.data[*]`、`$.title`
- XPath：`//div[@class='book']`

### Q: 搜索返回空数据怎么办？

**可能原因**：

1. **searchUrl 错误** - API 地址不正确
2. **请求方法错误** - 应该用 POST 却用了 GET
3. **参数缺失** - 缺少必要的请求参数
4. **编码问题** - 关键字编码错误
5. **IP 被封禁** - 请求太频繁

**调试方法**：

```
1. 在浏览器中直接访问 searchUrl，确认 API 工作
2. 使用 Postman 等工具测试 API
3. 在 Legado 中调试书源，查看请求和响应
4. 检查网站是否有反爬机制
```

## 正文规则问题

### Q: 正文内容显示乱码？

**原因**：

- 网站编码检测错误（UTF-8 vs GBK）
- 内容提取规则错误
- 网站返回的数据包含特殊字符

**解决方法**：

```json
{
  "ruleContent": {
    "content": "#content@html##广告 [\\s\\S]*?##",
    "nextContentUrl": "text.下一章@href"
  }
}
```

使用 `##正则##` 过滤广告和无关内容。

### Q: 正文无法分页（下一章不工作）？

**检查 nextContentUrl**：

```json
// 错误 - 使用了不支持的选择器
"nextContentUrl": "a:contains(下一章)@href"

// 正确 - 使用 text.文本 格式
"nextContentUrl": "text.下一章@href"
```

**常见下一页按钮文字**：

- "下一章"、"下章"、"下一节"
- "下一页"、"下页"、"翻页"
- "继续阅读"、"下一页阅读"

## 目录规则问题

### Q: 目录章节列表获取不到？

**检查步骤**：

1. 确认书籍详情页 URL 正确
2. 使用浏览器查看章节列表的 HTML 结构
3. 验证 chapterList 选择器

**示例**：

```json
{
  "ruleToc": {
    "chapterList": "#chapter-list li",
    "chapterName": "a@text",
    "chapterUrl": "a@href"
  }
}
```

### Q: 目录章节顺序错乱？

**原因**：

- 网站章节列表本身顺序错误
- 选择器选择了错误的元素

**解决方法**：

- 使用更精确的选择器
- 检查是否有倒序排列的需求

## 发现规则问题

### Q: 发现（分类）规则怎么写？

**基本格式**：

```json
{
  "exploreUrl": "玄幻::/fenlei/xuanhuan_{{page}}.html\n都市::/fenlei/doushi_{{page}}.html",
  "ruleExplore": {
    "bookList": ".book-item",
    "name": ".title@text",
    "author": ".author@text",
    "bookUrl": "a@href"
  }
}
```

**注意事项**：

- 分类名和 URL 用 `::` 分隔
- 多个分类用换行符 `\n` 分隔
- `{{page}}` 表示页码（从 1 开始）

## 反爬措施问题

### Q: 网站有频率限制怎么办？

**解决方法**：

```json
{
  "concurrentRate": "1000",  // 限制为每秒 1 次请求
  "header": {
    "User-Agent": "Mozilla/5.0..."
  }
}
```

**建议**：

- 设置合理的并发率（1000-3000 毫秒）
- 添加真实的 User-Agent
- 使用 Cookie 保持会话

### Q: 网站需要登录怎么办？

**配置登录信息**：

```json
{
  "loginUrl": "https://www.example.com/login",
  "loginUi": "{\"username\":\"文本框\",\"password\":\"密码框\"}",
  "loginCheckJs": "检测登录失败的 JS 代码"
}
```

### Q: 网站有验证码怎么处理？

**验证码类型**：

1. **简单验证码** - 使用 loginCheckJs 检测
2. **Cloudflare 验证** - 使用 WebView
3. **图形验证码** - 需要人工输入

**示例**：

```json
{
  "loginCheckJs": "(function(a){var r=a.body();if(r&&r.includes('验证码')){return false}return true})(result)"
}
```

## 移动端适配问题

### Q: 应该用手机版还是电脑版？

**选择原则**：哪个简单用哪个！

**优先电脑版的情况**：

- 手机版不能搜索
- 手机版目录规则复杂
- 手机版需要大量 JavaScript

**优先手机版的情况**：

- 手机版 API 更简单
- 手机版 HTML 结构清晰
- 手机版无验证码

**判断方法**：

- 电脑版：`www.example.com`
- 手机版：`m.example.com`

## 调试技巧

### Q: 如何调试书源？

**步骤**：

1. 打开 Legado → 我的 → 书源管理
2. 找到书源，长按 → 调试
3. 输入测试关键词（搜索调试）或书籍 URL（正文调试）
4. 查看日志输出，定位问题

**常用调试方法**：

- 查看请求 URL 是否正确
- 查看响应内容是否为空
- 查看规则提取结果

### Q: 书源测试工具在哪里？

**Legado 内置工具**：

- 书源管理 → 右上角菜单 → 书源调试
- 可以选择多个书源批量测试

**在线工具**：

- 无官方在线工具，建议在 Legado APP 中测试

## 其他问题

### Q: 书源注释怎么写？

**使用 bookSourceComment 字段**：

```json
{
  "bookSourceComment": "【技术实现】\n搜索：API 搜索（POST /api/search）\n发现：XPath 发现规则\n\n【局限性】\n- 有 IP 频率限制\n- 需要登录才能阅读"
}
```

### Q: 如何备份书源？

**方法**：

1. Legado → 我的 → 书源管理
2. 右上角菜单 → 导出书源
3. 保存为 JSON 文件

### Q: 书源在哪里下载？

**书源获取途径**：
- 自行制作（推荐学习本 Skill）

***

## 需要帮助？

如果以上 FAQ 没有解决你的问题，可以：

1. **查看参考文档**：
   - [references/workflow-guide.md](references/workflow-guide.md) - 完整工作流程
   - [references/javascript-guide.md](references/javascript-guide.md) - JavaScript 开发指南
   - [references/api-discovery-guide.md](references/api-discovery-guide.md) - API 发现技巧
2. **提供详细信息提问**：
   - 网站地址
   - 书源 JSON
   - 错误信息/截图
   - 已尝试的解决方法
3. **查看 Legado 官方文档**：
   - GitHub: <https://github.com/gedoor/legado>
   - 语雀文档：<https://www.yuque.com/legado>

