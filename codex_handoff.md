# Codex Handoff

生成时间：2026-03-21

## 1. 项目用途

这个项目是一个围绕 Legado 阅读书源制作与调试的知识/技能仓库，目标是帮助 AI 或人工更稳定地完成以下任务：

- 创建 Legado 书源
- 修复已有书源
- 讲解书源规则
- 分析真实网站结构
- 沉淀书源案例、规则参考、调试经验

当前仓库里既有历史性的大型工程文档，也有一套更接近实际交付的 skill 包。现阶段真正需要重点关注的是：

- `.trae/skills/legado-book-source-tamer/`

这套内容比根目录历史文档更贴近当前实际可用形态。

## 2. 已分析过的目录和关键文件

### 仓库根目录

已查看：

- `README.md`
- `docs/`
- `assets/`
- `skills/`
- `.trae/`
- `temp/`
- `legado/`
- `config/`

### 发现的重要结构判断

1. 根目录存在大量历史文档，描述的是一套更大的“完整工程”结构。
2. 但根目录当前并不存在这些历史文档里反复提到的实际目录，例如：
   - `src/`
   - `tests/`
   - 根目录级 `scripts/`
3. 当前真正成型、结构完整、可直接作为 skill 交付参考的是：
   - `.trae/skills/legado-book-source-tamer/`

### 已重点查看的关键文件

#### 根目录文档

- `README.md`
- `docs/PROJECT_ARCHITECTURE.md`
- `docs/FINAL_CHECKLIST.md`

结论：

- 这些文档和当前仓库实际结构存在分叉。
- 文档里提到的大量 `src/`、`scripts/`、`tests/` 结构，在当前根目录并不存在。
- `FINAL_CHECKLIST.md` 仍宣称“全部通过”“部署就绪”，但和现状不一致。

#### 根目录配置与提示词

- `config/system_prompt.md`
- `config/system/prompt.md`
- `config/agent_llm_config.json`

结论：

- 根目录仍保留了一套旧的系统提示和工具约束。
- 其中大量提到 `search_knowledge`、`detect_charset`、`smart_fetch_html`、`edit_book_source` 等能力。
- 这些文件更像历史方案/旧 prompt 体系，而不是当前唯一可信的交付入口。

#### 历史 skills 目录

- `skills/SKILLV0.1.md` 到 `skills/SKILLV1.1.md`
- 重点查看了 `skills/SKILLV1.md`

结论：

- `skills/` 下是多版演进文档。
- `skills/SKILLV1.md` 中存在引用 `references/`、`scripts/`、`search_knowledge`、`edit_book_source` 等内容，但这些引用并不完全对应当前根目录结构。
- 这些版本更适合作为历史演进参考，而不是当前主入口。

#### 当前实际 skill 包

重点查看：

- `.trae/skills/legado-book-source-tamer/SKILL.md`
- `.trae/skills/legado-book-source-tamer/QUICKSTART.md`
- `.trae/skills/legado-book-source-tamer/FAQ.md`
- `.trae/skills/legado-book-source-tamer/examples/README.md`
- `.trae/skills/legado-book-source-tamer/references/`
- `.trae/skills/legado-book-source-tamer/scripts/`

结论：

- 这是当前最值得继续维护的主 skill 包。
- `references/` 和 `scripts/` 在该目录下是真实存在的。
- 但 `SKILL.md` 本身还有结构和边界问题，需要重构。

#### 当前 skill 包中已确认的问题

1. `SKILL.md` 顶部存在重复的 `name/description` 头。
2. `SKILL.md` 中 `QUICKSTART.md`、`FAQ.md` 的相对链接写成了 `../QUICKSTART.md`、`../FAQ.md`，路径不对。
3. `SKILL.md` 把以下能力写成了默认主流程的一部分：
   - 批量并行抓取
   - 上传书源并提供直链
4. `examples/README.md` 中存在明显占位内容：
   - “这个是假的，后面我会加真的案例”
5. `examples/README.md` 中引用了不存在的文档：
   - `references/api-search-examples.md`
   - `references/encrypted-api-guide.md`
   - `references/anti-crawling.md`
6. `scripts/upload_book_source.py` 内包含固定外部上传地址：
   - `https://tu.406np.xyz/api/v1/upload`

## 3. 已做的修改

本次没有修改现有 skill 正文，也没有动 `.trae/skills/legado-book-source-tamer/` 下的现有文件内容。

本次只新增了以下文档：

### 1. 项目与 skill 评估

- `docs/SKILL_REVIEW_20260321.md`

内容包括：

- 当前主要问题
- 还缺哪些信息
- 可执行的优化方向
- 推荐补充的文档清单
- 优先级建议

### 2. `SKILL.md` 重构方案说明

- `docs/SKILL_MD_RESTRUCTURE_PLAN_20260321.md`

内容包括：

- 为什么要重构
- 建议结构
- 每一部分该写什么
- 哪些内容应该从主 `SKILL.md` 下沉
- 建议优先级

### 3. 重构后的 `SKILL.md` 草案

- `docs/SKILL_MD_DRAFT_20260321.md`

内容包括一版未落盘到正式 skill 的草案正文，核心结构为：

- 技能定位
- 适用范围
- 非适用范围
- 工作模式
- 标准主流程
- 输入契约
- 输出契约
- 强约束
- 可选增强能力
- 失败与降级策略
- 参考文档导航

## 4. 尚未完成的任务

以下事项已经明确需要做，但当前尚未执行：

1. 正式重构 `.trae/skills/legado-book-source-tamer/SKILL.md`
2. 清理 `SKILL.md` 里的重复头部和错误链接
3. 把“批量抓取 / 上传直链”从默认主流程降级为可选增强能力
4. 清理 `examples/README.md` 中的占位描述和失效链接
5. 决定如何处理根目录历史文档：
   - 标记 archived
   - 保留但加说明
   - 合并精华后弱化其主入口地位
6. 继续补“输入契约 / 输出契约 / 环境边界 / 降级策略”相关文档
## 5. 接下来建议的下一步

最推荐的顺序如下：

### 第一步

正式对 `.trae/skills/legado-book-source-tamer/SKILL.md` 做收口重构，优先落地已有草案。

### 第二步

清理以下显性问题：

- 顶部重复 YAML 头
- 错误相对链接
- 过重的默认工作流表述

### 第三步

清理案例索引：

- 删掉“这个是假的”之类占位语句
- 删除不存在的链接
- 只保留真实案例和真实导航

### 第四步

补充一组结构化辅助文档：

- 输入输出契约文档
- 失败降级策略文档
- 环境边界说明文档
- 站点类型决策树文档

## 6. 我当前最关心的问题

根据当前会话，用户当前最关心的问题主要是以下几项：

1. 做书源的 skill 现在到底还缺什么信息。
2. 这套 skill 还能怎么优化，尤其是主入口 `SKILL.md` 怎么重构更合理。
3. 在不立刻改正式文件的前提下，先把问题、方案、草案整理清楚。

进一步归纳，当前最核心的关注点其实是：

- 把这套 skill 从“信息很多但边界混乱”整理成“结构清晰、主流程稳定、能力边界真实”的版本。

## 当前阶段的一句话总结

当前项目最重要的工作，不是继续堆资料，而是统一主入口、明确能力边界、压缩默认流程、清理失效内容，并把 `SKILL.md` 真正改造成一个可靠的主控调度文档。
