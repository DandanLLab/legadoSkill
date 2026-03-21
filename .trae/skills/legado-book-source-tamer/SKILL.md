---
name: legado-book-source-tamer
description: 用于创建、修复、调试、讲解 Legado 阅读书源。涉及书源规则、站点分析、搜索/详情/目录/正文规则时必须使用。
---

# Legado 书源开发技能

## 技能定位

本技能用于处理所有 Legado 阅读书源相关任务，包括：

- 创建新书源
- 修复已有书源
- 分析站点结构与接口
- 解释书源规则语法

一旦任务涉及以下内容，必须使用本技能：

- 搜索规则
- 详情规则
- 目录规则
- 正文规则
- 发现规则
- API 分析
- 反爬处理

最终目标是输出以下结果之一：

- 可导入 Legado 的书源 JSON
- 修复后的书源 JSON
- 明确的问题分析和待验证项

## 适用范围

适用于以下任务：

- 为小说、漫画、听书、订阅网站创建书源
- 修复搜索失败、正文乱码、目录缺失、章节打不开等问题
- 分析 HTML、JSON API、Ajax、加密参数、验证码、Cloudflare
- 讲解 CSS 选择器、JSONPath、XPath、JavaScript 在书源中的写法
- 使用Python脚本验证书源规则的正确性

常见触发词包括：

- 书源
- Legado
- 阅读 APP
- 搜索规则
- 目录规则
- 正文规则
- 发现规则
- 修复书源
- 调试书源
- 验证书源
- Python验证

## 非适用范围

以下情况不必进入完整书源工作流：

- 单纯小说推荐
- Legado 下载地址
- Legado 安装教程
- 与书源制作无关的普通技术问题

如果只是简单问答，可以直接回答；但一旦涉及书源规则或站点分析，必须切换到本技能。

## 工作模式

### 模式 1：知识问答

适用于：

- 解释规则语法
- 对比不同写法
- 给出示例

要求：

- 解释清楚概念和用法
- 可引用参考文档
- 不创建书源 JSON

### 模式 2：书源修复

适用于：

- 用户提供现成书源 JSON
- 用户描述已有书源的故障现象

要求：

- 先识别问题点
- 再输出修复建议
- 必要时输出修复后的完整 JSON

### 模式 3：新建书源

适用于：

- 用户给出站点 URL，希望从零创建书源

要求：

- 分析站点结构
- 判断请求方式和页面类型
- 生成对应规则
- 输出完整 JSON 或明确的部分可用结果

## 标准主流程

### 第一步：任务分类

先判断任务属于哪一类：

- 知识问答 / 书源修复 / 新建书源
- 只做搜索 / 搜索+详情 / 完整源
- HTML 页面 / JSON API / Ajax 动态加载
- 优先 PC 站 / 优先移动站

### 第二步：信息收集

收集或确认以下信息：

- 站点 URL
- 搜索页或搜索接口
- 详情页 URL
- 目录页 URL
- 正文页 URL
- 请求方式：GET 或 POST
- 页面编码：UTF-8 / GBK / 其他
- 是否存在登录、验证码、Cloudflare、加密参数

如果信息不足，不要直接臆造规则，先补齐关键输入。

### 第三步：规则分析

根据真实页面结构或用户提供内容，分析以下字段：

- `searchUrl`
- `ruleSearch`
- `ruleBookInfo`
- `ruleToc`
- `ruleContent`
- `exploreUrl`
- `ruleExplore`

如果只做搜索源，只需要分析与搜索相关的必需字段。

### 第四步：规则产出

将分析结果整理成完整 JSON。

至少保证：

- 基本字段完整
- 规则结构合法
- 命名清晰
- 风险说明明确

### 第五步：结果校验

输出前必须检查：

- JSON 结构是否正确
- 必填字段是否齐全
- 规则写法是否兼容 Legado
- 是否存在明显的站点依赖风险
- 是否需要用户在 Legado 中进一步实测

### 第六步：Python验证

在输出前，可以使用Python工具进行验证：

1. **规则语法验证**
   - 使用 `scripts/rule_validator.py` 验证选择器和源规则的正确性
   - 检查规则在真实HTML中的匹配效果

2. **网站结构分析**
   - 使用 `scripts/smart_web_analyzer.py` 分析目标网站
   - 确认搜索表单、列表结构、分页信息

3. **提取测试**
   - 使用 `scripts/multi_mode_extractor.py` 测试提取规则
   - 评估提取结果的置信度



**重要提示**：
- Python验证只是模拟，不能替代Legado APP实测
- 验证通过不代表在Legado中一定能正常工作
- 最终必须在Legado APP中进行完整测试

## 输入契约

### 最少输入

用户至少应提供以下信息之一：

1. 目标站点 URL
2. 任务类型：新建或修复
3. 目标范围：只搜索 / 搜索+详情 / 完整源

### 推荐输入

若用户能补充以下内容，成功率会更高：

- 搜索关键词样例
- 搜索结果页 URL
- 书籍详情页 URL
- 目录页 URL
- 正文页 URL
- 现成书源 JSON
- 报错信息或现象描述
- 是否优先手机站或 PC 站

### 信息不足时的处理原则

如果缺少核心输入：

- 先索要最小补充信息
- 不凭经验臆造完整规则
- 不把猜测写成确定规则

## 输出契约

输出必须尽量包含以下内容：

1. 完整书源 JSON 或修复后的 JSON
2. 保存路径，例如 `temp/站点名/站点名.json`
3. 本次已完成功能说明
4. 本次未完成或未验证项
5. 风险和限制说明
6. 建议用户在 Legado 中实测的步骤

如果当前只能交付部分结果，也必须明确说明：

- 哪些部分可用
- 哪些部分未确认
- 后续还需要什么信息

## 强约束

以下规则必须遵守：

1. 不允许编造站点规则，必须基于真实页面结构或用户提供内容分析。
2. 模拟调试不等于真实行为，Legado 官方源码优先于模拟结果。
3. 只要发现有分页按钮或下一页逻辑，就必须考虑 `nextContentUrl`。
4. 禁止使用 `prevContentUrl`。
5. 禁止使用 `:contains()` 作为 Legado 规则写法。
6. 禁止使用 `:first-child`、`:last-child` 这类不兼容写法，应改用索引方式。
7. 不要把可选增强能力当作默认必走流程。
8. 复杂 JavaScript 必须附用途说明。
9. 最终结果必须提醒用户在 Legado APP 中实测。

## 可选增强能力

以下能力属于可选增强，不是默认主流程：

- 批量抓取多个页面
- 使用调试器进一步验证
- 对特殊反爬站点做专项处理
- 上传书源并生成直链
- 使用Python脚本验证书源规则

使用原则：

- 仅当环境支持时使用
- 仅当任务复杂且确有必要时使用
- 不要因为存在增强能力，就强行改变主流程

## Python验证工具

本技能提供了一套Python脚本工具，用于验证书源规则的正确性。

详细的工具说明、使用方法、验证原则和最佳实践，请参考：
- [Python验证工具完整文档](references/python-validation-tools.md)

### 工具模块概览

1. **规则验证器** (`scripts/rule_validator.py`) - 验证CSS选择器、XPath、正则表达式
2. **智能网站分析器** (`scripts/smart_web_analyzer.py`) - 自动分析网站结构
3. **多模式提取引擎** (`scripts/multi_mode_extractor.py`) - 支持多种提取方式
4. **智能请求工具** (`scripts/smart_request.py`) - 智能HTTP请求和编码检测
5. **知识库工具** (`scripts/knowledge_tools.py`) - 搜索参考文档
6. **文件整理工具** (`scripts/file_organizer.py`) - 自动整理生成的文件
7. **调试器CLI** (`debugger/debugger_cli.py`) - 命令行调试工具
8. **Legado源码检查器** (`debugger/legado_checker.py`) - 参考官方源码

### 快速开始

```bash
# 使用调试器CLI测试书源
python debugger/debugger_cli.py test book_source.json --keyword "斗破苍穹"

# 测试单个功能
python debugger/debugger_cli.py search book_source.json --keyword "斗破苍穹"
python debugger/debugger_cli.py info book_source.json --url "https://example.com/book/1"
```

```python
# Python脚本验证
from scripts.rule_validator import validate_rule
from scripts.multi_mode_extractor import extract_content

# 验证规则
result = validate_rule(html, 'css', '.book-list .book-item')

# 测试提取
result = extract_content(html, '.book-title')
```

### 验证原则

1. **模拟不等于真实**：Python验证只是模拟，最终必须在Legado APP中实测
2. **优先参考官方源码**：使用`debugger/legado_checker.py`参考Legado Kotlin源码
3. **逐步验证**：先验证搜索，再验证详情，最后验证正文
4. **记录问题**：将验证中发现的问题记录到输出中

更多详细内容请查看[Python验证工具完整文档](references/python-validation-tools.md)。

## 失败与降级策略

### 可降级交付的情况

- 搜索规则可确认，但详情规则未确认：允许只交付搜索源
- 搜索、详情、目录可确认，但正文规则不稳定：允许交付部分可用源，并标注风险
- 发现规则无法稳定确认：允许暂不提供 `exploreUrl`

### 必须中止完整交付的情况

- 站点需要登录且当前无法验证
- 存在验证码或 Cloudflare，但当前条件不足以完成验证
- 页面结构未获取到，核心规则只能靠猜测

这时应改为输出：

- 已分析出的结论
- 当前阻塞点
- 需要用户补充的最小信息

### 信息不足时的默认策略

如果用户只给出模糊需求，例如“做个书源”：

- 先补齐站点 URL 和目标范围
- 不直接生成完整书源

## 参考文档导航

### 入门

- [QUICKSTART.md](QUICKSTART.md)
- [FAQ.md](FAQ.md)

### 主流程
- [references/workflow-guide.md](references/workflow-guide.md)
- [references/skill-tips-guide.md](references/skill-tips-guide.md)
- [references/书源规则易错点.md](references/书源规则易错点.md)

### Python验证工具
- [Python验证工具完整文档](references/python-validation-tools.md) - Python验证工具详细说明
- [scripts/rule_validator.py](scripts/rule_validator.py) - 规则验证器
- [scripts/smart_web_analyzer.py](scripts/smart_web_analyzer.py) - 智能网站分析器
- [scripts/multi_mode_extractor.py](scripts/multi_mode_extractor.py) - 多模式提取引擎
- [scripts/smart_request.py](scripts/smart_request.py) - 智能请求工具
- [scripts/knowledge_tools.py](scripts/knowledge_tools.py) - 知识库工具
- [scripts/file_organizer.py](scripts/file_organizer.py) - 文件整理工具
- [debugger/debugger_cli.py](debugger/debugger_cli.py) - 调试器CLI
- [debugger/legado_checker.py](debugger/legado_checker.py) - Legado源码检查器

### 规则语法
- [references/css-selector-reference.md](references/css-selector-reference.md)
- [references/css选择器规则.md](references/css选择器规则.md)
- [references/regex-guide.md](references/regex-guide.md)
- [references/json-structure.md](references/json-structure.md)
- [references/javascript-guide.md](references/javascript-guide.md)
- [references/书源规则易错点.md](references/书源规则易错点.md)

### 特殊场景

- [references/api-discovery-guide.md](references/api-discovery-guide.md)
- [references/post-request-guide.md](references/post-request-guide.md)
- [references/encoding-guide.md](references/encoding-guide.md)
- [references/动态加载.md](references/动态加载.md)
- [references/captcha-detection-guide.md](references/captcha-detection-guide.md)
- [references/webview-limitations.md](references/webview-limitations.md)
- [references/方法-登录检查JS.md](references/方法-登录检查JS.md)
- [references/方法-JS扩展类.md](references/方法-JS扩展类.md)
- [references/方法-加密解密.md](references/方法-加密解密.md)

### 参考资料

- [references/book-source-templates.md](references/book-source-templates.md)
- [references/html-structure-examples.md](references/html-structure-examples.md)
- [references/output-template.md](references/output-template.md)
- [references/书源规则：从入门到入土.md](references/书源规则：从入门到入土.md)
- [references/订阅源规则：从入门到再入门.md](references/订阅源规则：从入门到再入门.md)
- [references/订阅源规则帮助.md](references/订阅源规则帮助.md)
- [references/快速写源订阅源原理分析.md](references/快速写源订阅源原理分析.md)
- [references/阅读lyc版js变量和函数.md](references/阅读lyc版js变量和函数.md)

### 案例

- [examples/README.md](examples/README.md)

## 执行原则总结

核心原则如下：

- 先分类，再分析
- 先收集信息，再写规则
- 先保证可用，再考虑增强
- 有风险就明确标注
- 不确定就降级，不臆造

本技能的重点不是“尽量多写内容”，而是“尽量稳定地产出可验证结果”。
