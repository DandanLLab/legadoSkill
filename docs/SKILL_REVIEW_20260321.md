# 书源 Skill 信息缺口与优化建议

生成时间：2026-03-21

## 结论概览

当前这套“做书源”的 skill，问题不在于资料数量不够，而在于以下几类问题同时存在：

1. 主入口元数据和链接不够稳定，可能影响 skill 加载和文档跳转。
2. 默认工作流写得过重，把一些可选能力写成了必走主流程。
3. 案例索引里仍有占位内容和失效链接，会降低整体可信度。
4. 根目录历史文档和实际交付结构已经分叉，容易误导维护者。
5. 缺少统一的输入契约、输出契约、失败降级规则和环境边界说明。

## 主要问题

### 1. 当前主 skill 的入口元数据和链接不够稳

`SKILL.md` 同时出现了两段 `name/description` 头，存在重复定义风险。

另外，“新手必读”里的链接路径不正确：

- `../QUICKSTART.md`
- `../FAQ.md`

但这两个文件实际就在同目录，不在上一级目录。

相关文件：

- `.trae/skills/legado-book-source-tamer/SKILL.md`
- `.trae/skills/legado-book-source-tamer/QUICKSTART.md`
- `.trae/skills/legado-book-source-tamer/FAQ.md`

### 2. skill 把“多智能体并行分析 + 上传直链”写成了默认工作流

当前 `SKILL.md` 把以下动作写成了推荐甚至接近默认主流程：

- 使用 `batch_fetcher.py` 并行抓取
- 启动多智能体并行分析
- 使用 `Task(...)` 调起多个智能体
- 调用 `upload_book_source.py` 上传书源并给用户直链

这会带来两个问题：

1. 这些能力并不是所有环境都具备。
2. “上传到外部服务”不应该成为默认必走路径。

`upload_book_source.py` 里还写死了上传地址：

- `https://tu.406np.xyz/api/v1/upload`

这类能力更适合定义为“可选增强能力”，而不是主流程强约束。

相关文件：

- `.trae/skills/legado-book-source-tamer/SKILL.md`
- `.trae/skills/legado-book-source-tamer/scripts/upload_book_source.py`
- `.trae/skills/legado-book-source-tamer/scripts/batch_fetcher.py`

### 3. 案例索引里仍有明确的占位内容和失效链接

`examples/README.md` 中直接写了：

> 这个是假的，后面我会加真的案例

并且引用了当前不存在的文档：

- `references/api-search-examples.md`
- `references/encrypted-api-guide.md`
- `references/anti-crawling.md`

这会直接影响 skill 的专业感和可维护性。

相关文件：

- `.trae/skills/legado-book-source-tamer/examples/README.md`

### 4. 根目录文档和实际交付物已经分叉

仓库根目录下的一些文档仍然在描述一套更大的工程结构，例如：

- 根目录存在 `scripts/`
- 根目录存在 `src/`
- 根目录存在 `tests/`
- “所有检查项目全部通过”
- “部署就绪”

但当前仓库根目录下并没有这套实际结构；真正可用且结构完整的是：

- `.trae/skills/legado-book-source-tamer/`

这说明历史文档和当前交付内容已经分叉，后续继续沿着这些旧文档维护，容易把人带偏。

相关文件：

- `docs/FINAL_CHECKLIST.md`
- `docs/PROJECT_ARCHITECTURE.md`

## 还差什么信息

### 1. 缺少统一的“最小输入契约”

现在虽然有示例，但没有明确规定：用户至少要提供哪些信息，skill 才能高质量工作。

建议最少明确以下输入项：

- 网站 URL
- 目标功能范围
- 只做搜索 / 搜索+详情 / 完整源
- PC 端还是移动端优先
- 是否已有样例页 URL
- 是否已有现成书源需要修复
- 是否遇到反爬、验证码、登录、加密参数

### 2. 缺少统一的“输出验收契约”

现在有“输出 JSON”“保存到 temp”这类描述，但没有形成一个统一的验收模板。

建议固定输出包含：

- 最终 JSON
- 保存路径
- 本次已验证的页面类型
- 尚未验证的页面类型
- 可能存在的风险
- 需要用户在 Legado APP 中实测的项目

### 3. 缺少“站点类型分流表”

当前知识很多，但分散在多个参考文档中，没有集中成一个前置决策表。

建议把以下类型集中整理：

- HTML 列表页
- JSON API
- Ajax 动态加载
- Cloudflare
- 登录态
- 验证码
- 加密参数
- 纯搜索源
- 完整小说源
- 漫画 / 听书 / 订阅源

并明确每类站点该走哪条流程。

### 4. 缺少“失败降级策略”的统一定义

现在 skill 提到了容错，但对用户可见的交付标准不够清晰。

建议明确：

- 什么时候允许只交付搜索源
- 什么时候可以交付部分可用源
- 什么时候必须中止并索要更多样例
- 什么时候需要用户去 Legado 内手测后再继续修复

### 5. 缺少“环境兼容说明”

当前 skill 混合了文档、脚本、并行架构、上传功能，但没有清楚标注哪些是：

- 当前 agent 一定能执行的
- 需要特定运行环境的
- 只是参考资料，不是必定可执行动作
- 依赖联网或外部服务的

这个边界如果不写清楚，模型很容易误判“应该做什么”和“实际上能做什么”。

## 优化建议

### 1. 先做文档收口

建议把以下路径明确为唯一真源：

- `.trae/skills/legado-book-source-tamer/`

同时对根目录历史文档做处理：

- 标记为 archived
- 或迁移精华内容后删除
- 或在文件开头加“历史方案，非当前主入口”

### 2. 把 `SKILL.md` 收缩成主控文档

当前 `SKILL.md` 信息很多，但主流程和边界不够聚焦。

建议保留四类核心内容：

1. 适用场景
2. 主流程
3. 强约束
4. 输入输出契约

其余深度内容继续放在 `references/` 里，不要把主入口写成大型百科。

### 3. 把“多智能体 / 批量抓取 / 上传直链”改成可选增强

建议将它们从“推荐主流程”改成“可选增强”：

- 当环境支持且任务复杂时才启用多智能体
- 当需要多页验证时再启用批量抓取
- 上传直链仅在用户明确需要，且环境允许时再做

### 4. 增加一个 `INPUT_OUTPUT_SPEC.md`

这是当前最值得优先补的文档。

建议包含：

- 用户最少输入要求
- 推荐补充输入项
- 输出格式标准
- 保存路径规范
- 风险说明模板
- 用户手测清单模板

### 5. 清理案例索引

建议对 `examples/README.md` 做三件事：

1. 删除“这个是假的”这类占位描述
2. 删除不存在的链接
3. 给每个真实案例补上：
   - 适用场景
   - 技术特征
   - 风险点
   - 推荐学习顺序

### 6. 增加一个决策树文档

建议新增：

- `references/decision-tree.md`

或者在 `workflow-guide.md` 最前面增加一页“站点类型决策表”。

目标是让模型在开始工作前，先决定：

- 这是修复还是新建
- 这是搜索源还是完整源
- 这是 HTML 还是 API
- 是否需要 WebView
- 是否需要登录 / 验证码处理

这样能显著降低流程漂移。

## 推荐补充的文档清单

建议后续优先新增或重构以下文档：

- `INPUT_OUTPUT_SPEC.md`
- `references/decision-tree.md`
- `references/fallback-strategy.md`
- `references/environment-boundaries.md`
- `references/source-debug-checklist.md`

## 建议的优先级

### P0

- 修正 `SKILL.md` 头部重复定义
- 修正 `QUICKSTART.md` / `FAQ.md` 链接路径
- 删除 `examples/README.md` 里的假内容和失效链接

### P1

- 增加输入输出契约文档
- 把多智能体和上传功能从默认主流程降级为可选增强
- 标记根目录旧文档为历史文档

### P2

- 补站点类型决策树
- 补失败降级规则
- 补环境边界说明
- 继续补充真实案例库

## 一句话总结

当前这套 skill 的核心知识并不缺，真正缺的是“统一主入口、明确边界、稳定链接、输入输出契约、失败降级规则”。

只要先把这些基础结构补齐，skill 的可靠性会比继续堆资料提升更明显。
