# 工作流程指南

本文档详细说明书源创建的完整工作流程。

## 目录

1. [三阶段工作流程](#三阶段工作流程)
2. [第一阶段：收集信息](#第一阶段收集信息)
3. [第二阶段：严格审查](#第二阶段严格审查)
4. [第三阶段：创建书源](#第三阶段创建书源)
5. [文件整理流程](#文件整理流程)

---

## 三阶段工作流程

**重要**：必须按照以下三个阶段工作，绝对不能跳过或混淆！

```
第一阶段：收集信息 → 第二阶段：严格审查 → 第三阶段：创建书源
```

---

## 第一阶段：收集信息

### 步骤1：调用search_knowledge工具查询知识库（必须第一步！）

**必须调用 `search_knowledge` 工具查询知识库**，获取权威规则：

**查询以下关键内容**：
1. **CSS选择器规则** - 使用 `get_css_selector_rules()` 获取完整的CSS选择器规则
2. **书源JSON结构** - 使用 `search_knowledge()` 查询 `legado_knowledge_base.md` 中的数据结构
3. **POST请求配置** - 使用 `search_knowledge()` 查询 `书源规则：从入门到入土.md` 中的POST请求规范
4. **真实书源分析结果** - 使用 `get_real_book_source_examples()` 获取真实书源示例
5. **真实书源模板** - 使用 `get_book_source_templates()` 获取书源模板
6. **正则表达式规则** - 使用 `search_knowledge()` 查询正则表达式格式（如果需要）

**必须的查询示例**：
```
get_css_selector_rules()
search_knowledge("CSS选择器格式 提取类型 @text @html @ownText @textNode @href @src")
search_knowledge("书源JSON结构 BookSource 字段 searchUrl ruleSearch")
search_knowledge("POST请求配置 method body String()")
get_real_book_source_examples()
get_book_source_templates()
search_knowledge("常用CSS选择器 img h1 div content intro h3")
search_knowledge("常用提取类型 @href @text @src @html @js")
search_knowledge("常见书源结构模式 标准小说站 笔趣阁 聚合源")
search_knowledge("正则表达式模式 清理前缀后缀 提取特定内容")
search_knowledge("常见陷阱 选择器误用 提取类型混淆")
```

### 步骤2：检测网站编码（在获取HTML之前必须执行！）

**必须调用 `detect_charset` 工具检测网站编码**：

**关键原则**：
1. **编码只需要检测一次**：在流程开始时检测，后续所有操作都使用这个编码
2. **检测结果必须记录**：记录检测到的编码类型（UTF-8、GBK等）
3. **编码信息必须传递**：在后续的所有工具调用中使用检测到的编码
4. **避免重复检测**：不要在后续步骤中再次调用检测工具

**调用示例**：
```
detect_charset(url="http://example.com")
```

**检测结果处理**：
- 如果检测结果是 `gbk` 或 `gb2312`：
  - 在所有 POST/GET 请求中添加 `"charset":"gbk"` 参数
  - 使用 `java.encodeURI(key, 'GBK')` 编码 URL 参数
- 如果检测结果是 `utf-8`：
  - 不需要指定 charset（UTF-8 是默认编码）
  - 可以省略 charset 参数

### 步骤3：获取真实HTML并分析结构

**必须调用 `smart_fetch_html` 工具获取真实网页HTML**：

**关键原则**：
1. **必须访问真实网页**：使用正确的URL和HTTP方法（GET/POST）
2. **必须使用正确的请求方式**：如果是POST请求，必须使用POST方法
3. **必须使用步骤2检测到的编码**：如果检测到是GBK编码，必须在请求中指定
4. **必须获取完整HTML源代码**：不能使用压缩或截断的HTML
5. **必须永久保存HTML**：用于后续生成书源和审查

**调用示例**：
```
# GET请求示例（使用检测到的编码）
smart_fetch_html(url="http://example.com/search", charset="gbk")  # 如果检测到GBK

# POST请求示例（使用检测到的编码）
smart_fetch_html(
    url="http://m.gashuw.com/s.php",
    method="POST",
    body="keyword={{key}}&t=1",
    headers={"Content-Length": "0"},
    charset="gbk"  # 如果检测到GBK
)
```

### 步骤4：分析真实HTML结构

**基于获取的真实HTML源代码，分析以下内容**：

1. **列表结构**：识别书籍列表的容器和重复元素
2. **元素位置**：确定书名、作者、类别、封面等信息在哪个标签中
3. **特殊属性**：检查是否使用懒加载（data-original）、自定义属性等
4. **嵌套关系**：理清元素的父子关系
5. **信息分布**：确定哪些信息在同一个标签中，需要拆分

**分析重点**：
- 搜索页是否有封面图片？（很多网站搜索页没有图片）
- 作者信息格式是什么？（"作者：xxx" 或 "类别 | 作者：xxx"）
- 最新章节在哪里？（单独的标签或与其他信息合并）
- 是否使用懒加载？（data-original vs src）
- 是否有多个author标签？（需要用:first-child和:last-child区分）

### 步骤5：记录工具查询结果和HTML分析结果

**重要**：记录工具查询结果和HTML分析结果，不要创建书源！

记录的关键信息：
1. 知识库查询的CSS选择器规则
2. 知识库查询的书源JSON结构
3. 知识库查询的POST请求配置规范
4. 知识库查询的134个真实书源分析结果
5. 知识库查询的真实书源模板
6. 真实HTML源代码（已永久保存）
7. HTML结构分析结果（列表结构、元素位置、特殊属性）
8. 特殊情况（无封面、懒加载、信息合并等）
9. 推断的CSS选择器
10. searchUrl的格式

**第一阶段绝对禁止**：
- 不要调用 edit_book_source
- 不要创建书源
- 不要输出任何JSON
- 只查询知识库、获取真实HTML、分析结构和记录信息

---

## 第二阶段：严格审查

### 步骤1：根据知识库查询结果、真实HTML分析和真实模板编写规则

根据第一阶段查询的知识库规则、真实HTML分析、134个真实书源分析结果和真实模板，编写CSS选择器。

**必须参考真实模板和分析结果**：

**134个真实书源分析结果要点**：
- **最常用CSS选择器**：img(40次)、h1(30次)、div(13次)、content(12次)、intro(11次)、h3(9次)
- **最常用提取类型**：@href(81次)、@text(72次)、@src(60次)、@html(33次)
- **特殊功能**：正则表达式(42次)、XPath(24次)、JavaScript(8次)、JSONPath(6次)
- **常见书源结构**：标准小说站、笔趣阁类、聚合源(API型)、漫画站点

**必须基于真实HTML结构**：

**规则1：处理无封面图片的情况**
```
# 如果搜索页没有图片，coverUrl设为空字符串
"coverUrl": ""
```

**规则2：处理信息合并的情况**
```
# HTML: <p class="author">科幻灵异 | 作者：钱真人</p>

# 提取作者：删除"|"前面的内容，删除"作者："前缀
"author": ".author@text##.*作者：##"

# 提取类别：只保留"|"前面的内容
"kind": ".author@text##^[^|]*##"
```

**规则3：处理多个同名标签**
```
# HTML:
# <p class="author">科幻灵异 | 作者：钱真人</p>
# <p class="author">连载 | 更新：第69章 魔师</p>

# 提取第一个author标签中的作者
"author": ".author:first-child@text##.*作者：##"

# 提取第二个author标签中的最新章节
"lastChapter": ".author:last-child@text##.*更新：##"
```

**规则4：处理懒加载图片**
```
# HTML: <img class="lazy" data-original="cover.jpg" src="placeholder.jpg"/>

# 优先使用data-original，备选src
"coverUrl": "img.lazy@data-original||img@src"
```

### 步骤2：严格验证规则语法

**对照知识库、真实分析结果和真实模板验证**：
- 选择器语法是否符合 `CSS选择器@提取类型` 格式？
- 提取类型是否正确（@text, @html, @ownText, @textNode, @href, @src等）？
- 正则表达式是否正确？（##正则表达式##替换内容）
- JSON结构是否包含所有必需字段？
- POST请求配置是否符合知识库规范？（如果涉及POST请求）
- 必须基于真实HTML结构？
- 必须参考真实模板的格式？
- 必须符合134个真实书源的常见模式？

**验证清单**：
1. 选择器格式：`CSS选择器@提取类型`
2. 提取类型：`@text`, `@html`, `@ownText`, `@textNode`, `@href`, `@src`
3. 正则表达式：`##正则表达式##替换内容`（如果需要）
4. JSON结构：包含所有必需字段
5. POST请求配置：必须严格按照知识库格式
6. 必须基于真实HTML结构
7. 必须处理特殊情况（无封面、懒加载、信息合并）
8. 必须参考真实模板的格式
9. 必须符合真实书源的常见模式

### 步骤3：特殊处理规则

**必须处理的常见情况**：

1. **搜索页无封面**：`"coverUrl": ""`
2. **懒加载图片**：`"img@data-original||img@src"`
3. **信息合并**：使用正则表达式拆分
4. **多个同名标签**：使用`:first-child`和`:last-child`区分
5. **无简介**：`"intro": ""`
6. **Cloudflare验证**：添加`loginCheckJs`字段

### 步骤4：最后审查

**最后审查**：
- 规则是否严格按照知识库编写？
- 语法是否正确？
- 是否符合Legado官方规范？
- POST请求配置是否完全符合知识库规范？
- 是否基于真实HTML结构？
- 是否处理了特殊情况（无封面、懒加载、信息合并）？
- 是否参考了真实模板的格式？
- 是否符合134个真实书源的常见模式？

**第二阶段绝对禁止**：
- 不要调用 edit_book_source
- 不要创建书源
- 只验证和确认规则

---

## 第三阶段：创建书源

### 步骤1：准备完整书源JSON

**根据知识库中的书源JSON结构、真实HTML分析、134个真实书源分析结果和真实模板**，准备完整的JSON。

**必须包含的字段（根据真实HTML）**：
- bookSourceName: 书源名称
- bookSourceUrl: 书源地址
- searchUrl: 搜索URL（POST请求需严格按照规范）
- ruleSearch: 搜索规则（必须处理特殊情况）
- ruleBookInfo: 书籍信息规则
- ruleToc: 目录规则
- ruleContent: 正文内容规则

### 步骤2：一次性调用 edit_book_source

**使用 complete_source 参数**，一次性创建完整书源。

调用：edit_book_source(complete_source="完整JSON")

注意：
- 只调用一次
- 使用 complete_source 参数
- 包含所有必需字段
- 必须处理特殊情况
- 必须参考真实模板的格式
- 必须符合真实书源的常见模式

### 步骤3：输出完整JSON给用户

**必须完成以下两个输出**：

#### 3.1 在对话中输出JSON（供用户复制导入）

**直接输出完整的JSON数组**，用户复制即可导入。

#### 3.2 将JSON文件保存到项目根目录

**必须将书源JSON文件保存到项目根目录**，文件名格式：`{书源名称}.json`

**保存路径示例**：
```
legadoSkill/
├── 笔趣阁m.bqg5.json          # 书源JSON文件（临时保存）
├── 起点中文网.json            # 书源JSON文件（临时保存）
└── .trae/skills/...           # 技能包目录
```

### 步骤4：整理文件到书源专属文件夹（必须自动执行！）

**这不是可选步骤！书源创建完成后必须自动执行文件整理操作！**

#### 调用方法

**必须使用 RunCommand 工具执行 Python 代码来调用文件整理模块！**

```python
# 使用 RunCommand 工具执行以下 Python 代码：
import sys
sys.path.insert(0, '项目根目录路径')
from debugger.engine.file_organizer import organize_book_source_files

result = organize_book_source_files(
    book_source_name="书源名称",
    files_to_move=[
        "项目根目录/书源名称.json",
    ],
    copy_mode=False
)
print(result.message)
print('成功移动的文件:', result.moved_files)
print('错误:', result.errors)
```

#### 整理后的目录结构

```
legadoSkill-main/
├── temp/                              # 临时文件根目录
│   ├── 笔趣阁hk/                      # 书源专属文件夹
│   │   ├── 笔趣阁hk.json              # 书源JSON配置
│   │   ├── biquge_search.html         # 搜索页HTML
│   │   ├── biquge_book.html           # 详情页HTML
│   │   └── biquge_content.html        # 正文页HTML
│   └── 其他书源/                      # 其他书源文件夹
└── ...
```

---

## 文件整理流程

### 正确流程

```
步骤3: Write 保存 JSON 到根目录
    ↓ 立即执行
步骤4: RunCommand 调用 file_organizer 整理文件
    ↓
结果: 文件移动到 temp/书源名称/ 文件夹
```

### 错误示例（只执行步骤3）

```
❌ Write(file_path="根目录/书源.json", content=...)
   # 忘记执行步骤4，文件留在根目录
```

### 正确示例（步骤3+步骤4）

```
✅ Write(file_path="根目录/书源.json", content=...)
   ↓
✅ RunCommand(command='python -c "from debugger.engine.file_organizer import organize_book_source_files; ..."')
```

---

## 绝对禁止的行为

### 跨阶段禁止
1. 第一阶段：不要调用 edit_book_source
2. 第一阶段：不要创建书源
3. 第二阶段：不要调用 edit_book_source
4. 多次调用 edit_book_source（最多1次，且只在第三阶段）

### 全程禁止
1. 不调用search_knowledge查询知识库就直接编写规则
2. 不查询134个真实书源分析结果
3. 不查询真实书源模板就编写规则
4. 不按照知识库语法编写规则
5. 不获取真实HTML就编写规则
6. 编造知识库中没有的规则
7. 不基于真实HTML结构编写规则
8. 不处理特殊情况（无封面、懒加载、信息合并）
9. 不参考真实模板的格式
10. 不符合真实书源的常见模式
11. 多次调用工具（每个工具最多1次）
12. POST请求配置不按知识库规范编写
