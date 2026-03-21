# Python验证工具

本技能提供了一套Python脚本工具，用于验证书源规则的正确性。

## 工具模块

### 1. 规则验证器 (`scripts/rule_validator.py`)

验证CSS选择器、XPath、正则表达式的语法正确性，测试规则在真实HTML中的匹配效果。

**主要功能：**
- 验证CSS选择器语法和匹配效果
- 验证XPath表达式语法和匹配效果
- 验证正则表达式语法和匹配效果
- 验证书源JSON的必填字段

**使用示例：**

```python
from scripts.rule_validator import validate_rule, RuleValidator

# 验证CSS选择器
html = """
<html>
    <div class="book-list">
        <div class="book-item">书籍1</div>
        <div class="book-item">书籍2</div>
    </div>
</html>
"""

result = validate_rule(html, 'css', '.book-list .book-item')
print(result)
# 输出: {'rule_type': 'css', 'rule_value': '.book-list .book-item', 'valid': True, ...}

# 验证书源JSON
from scripts.rule_validator import validate_book_source

book_source = {
    'bookSourceName': '测试书源',
    'bookSourceUrl': 'https://example.com',
    'searchUrl': 'https://example.com/search?q={{key}}',
    'ruleSearch': {
        'bookList': '.book-list .book-item',
        'name': '.book-title',
        'bookUrl': 'a@href'
    }
}

result = validate_book_source(html, book_source)
print(result)
```

### 2. 智能网站分析器 (`scripts/smart_web_analyzer.py`)

自动分析网站结构，检测搜索表单、分页信息、列表结构，识别AJAX请求和安全机制。

**主要功能：**
- 检测页面编码（UTF-8/GBK等）
- 分析搜索表单结构
- 分析分页信息
- 分析列表结构
- 识别AJAX请求
- 检测安全机制（Cloudflare、登录、验证码）

**使用示例：**

```python
from scripts.smart_web_analyzer import smart_analyze_website, SmartWebAnalyzer

# 快速分析
analysis = smart_analyze_website("https://example.com")

print("编码:", analysis['charset'])
print("搜索表单:", analysis['search_info'])
print("分页信息:", analysis['pagination_info'])
print("列表结构:", analysis['list_structure'])
print("AJAX信息:", analysis['ajax_info'])
print("安全信息:", analysis['security_info'])

# 使用类实例
analyzer = SmartWebAnalyzer(timeout=30)
result = analyzer.analyze("https://example.com")

if 'error' in result:
    print(f"分析失败: {result['error']}")
else:
    print(f"找到搜索表单: {result['search_info']['found']}")
    print(f"推荐列表选择器: {result['list_structure']['recommended']}")
```

### 3. 多模式提取引擎 (`scripts/multi_mode_extractor.py`)

支持CSS选择器、XPath、正则表达式、JSONPath等多种提取方式，自动检测提取方法，提供提取结果的置信度评估。

**主要功能：**
- CSS选择器提取
- XPath提取
- 正则表达式提取
- JSONPath提取
- 自动检测提取方法
- 置信度评估
- 提取属性值

**使用示例：**

```python
from scripts.multi_mode_extractor import extract_content, MultiModeExtractor

html = """
<html>
    <div class="book-item">
        <h3 class="book-title">斗破苍穹</h3>
        <a href="/book/123" class="book-link">详情</a>
    </div>
</html>
"""

# 自动检测方法
result = extract_content(html, '.book-title')
print(f"内容: {result.content}")
print(f"方法: {result.method}")
print(f"置信度: {result.confidence}")
print(f"提取数量: {result.extracted_count}")

# 指定方法
result = extract_content(html, '.book-title', method='css')

# 提取属性
result = extract_content(html, '.book-link', extract_attr='href')
print(f"链接: {result.content}")

# 使用类实例
extractor = MultiModeExtractor(html)
result = extractor.extract('.book-title', method='css', extract_all=False)
```

### 4. 智能请求工具 (`scripts/smart_request.py`)

支持GET/POST等多种HTTP方法，智能检测页面编码，自动处理重定向和错误重试。

**主要功能：**
- 支持GET/POST/PUT/DELETE等HTTP方法
- 智能检测页面编码（UTF-8/GBK等）
- 自动处理重定向
- 错误重试机制
- 自定义请求头和Cookie
- 支持SSL验证配置

**使用示例：**

```python
from scripts.smart_request import smart_fetch_html, SmartRequest

# 快速获取HTML
result = smart_fetch_html(
    url="https://example.com",
    method="GET",
    timeout=30
)

if result['success']:
    html = result['html']
    encoding = result['encoding']
    print(f"编码: {encoding}")
    print(f"大小: {result['size']} bytes")
else:
    print(f"请求失败: {result['error']}")

# 使用类实例
requester = SmartRequest(timeout=30, max_retries=3)

result = requester.fetch(
    url="https://example.com/search",
    method="POST",
    data={'keyword': '斗破苍穹'},
    headers={'Referer': 'https://example.com'},
    charset='utf-8'
)

# 指定编码
result = smart_fetch_html(
    url="https://gbk-site.com",
    charset='gbk'
)
```

### 5. 知识库工具 (`scripts/knowledge_tools.py`)

搜索参考文档，获取CSS选择器规则、书源模板等。

**主要功能：**
- 加载知识库文档
- 搜索关键词
- 获取CSS选择器规则
- 获取书源模板
- 获取JavaScript API文档

**使用示例：**

```python
from scripts.knowledge_tools import search_knowledge, get_css_selector_rules, get_book_source_templates

# 搜索知识库
results = search_knowledge("CSS选择器", limit=5)
for result in results:
    print(f"文件: {result['filename']}")
    print(f"匹配数: {result['relevance']}")
    for match in result['matches']:
        print(f"  {match}")

# 获取CSS选择器规则
css_rules = get_css_selector_rules()
print(css_rules)

# 获取书源模板
templates = get_book_source_templates()
print(templates)
```

### 6. 文件整理工具 (`scripts/file_organizer.py`)

自动整理生成的文件到书源专属文件夹，支持会话管理和文件跟踪。

**主要功能：**
- 创建书源专属文件夹
- 移动/复制文件到指定文件夹
- 会话管理
- 文件跟踪
- 文件名清理

**使用示例：**

```python
from scripts.file_organizer import organize_book_source_files, start_file_session, register_generated_file

# 整理文件
result = organize_book_source_files(
    book_source_name="笔趣阁hk",
    files_to_move=["笔趣阁hk.json", "search.html", "detail.html"]
)

print(f"成功: {result.success}")
print(f"消息: {result.message}")
print(f"文件夹: {result.subfolder_path}")
print(f"移动的文件: {result.moved_files}")

# 使用会话管理
session_id = start_file_session("session_001")
register_generated_file("book1.json", session_id)
register_generated_file("book2.json", session_id)

# 整理会话文件
result = organize_book_source_files(
    book_source_name="测试书源",
    session_id=session_id
)
```

### 7. 调试器CLI (`debugger/debugger_cli.py`)

命令行调试工具，支持搜索、详情、目录、正文等功能的独立测试。

**主要功能：**
- 完整测试（搜索→详情→目录→正文）
- 搜索功能测试
- 详情页测试
- 目录页测试
- 正文页测试
- 支持文本和JSON输出格式

**使用示例：**

```bash
# 完整测试
python debugger/debugger_cli.py test book_source.json --keyword "斗破苍穹"

# 测试搜索功能
python debugger/debugger_cli.py search book_source.json --keyword "斗破苍穹"

# 测试详情页
python debugger/debugger_cli.py info book_source.json --url "https://example.com/book/1"

# 测试目录页
python debugger/debugger_cli.py toc book_source.json --url "https://example.com/book/1/toc"

# 测试正文页
python debugger/debugger_cli.py content book_source.json --url "https://example.com/chapter/1"

# 使用JSON输出
python debugger/debugger_cli.py search book_source.json --keyword "斗破苍穹" --output json
```

### 8. Legado源码检查器 (`debugger/legado_checker.py`)

实时检查和更新Legado源码，对比Python实现与Kotlin源码，提供源码参考路径。

**主要功能：**
- 检查legado仓库是否存在
- 获取最新源码参考
- 对比Python实现与Kotlin源码
- 查找函数定义
- 提供源码参考路径

**使用示例：**

```python
from debugger.legado_checker import LegadoChecker, check_legado_update, get_legado_reference

# 检查仓库状态
checker = LegadoChecker()
result = checker.check_repository()
print(f"仓库存在: {result['exists']}")
print(f"核心文件完整: {result['has_core_files']}")

# 检查AnalyzeRule实现
analyze_result = checker.check_analyze_rule()
print(f"Kotlin源码存在: {analyze_result['kotlin_exists']}")
print(f"Python实现存在: {analyze_result['python_exists']}")

# 获取源码参考
reference = checker.get_reference_code("xpath解析")
print(reference)

# 查找函数定义
func_info = checker.find_function("AnalyzeRule", "getString")
if func_info:
    line, code = func_info
    print(f"函数位于第 {line} 行")
    print(code)
```

## 使用流程

### 场景1：验证单个规则

适用于验证某个特定的CSS选择器、XPath或正则表达式是否正确。

```python
from scripts.rule_validator import validate_rule

# 获取HTML内容
html = """
<html>
    <div class="book-list">
        <div class="book-item">
            <h3 class="book-title">斗破苍穹</h3>
            <a href="/book/123">详情</a>
        </div>
    </div>
</html>
"""

# 验证CSS选择器
result = validate_rule(html, 'css', '.book-list .book-item')
if result['valid']:
    print("✓ CSS选择器有效")
    if result['issues']:
        for issue in result['issues']:
            print(f"  {issue['severity']}: {issue['message']}")
else:
    print("✗ CSS选择器无效")
    for issue in result['issues']:
        print(f"  {issue['message']}: {issue['suggestion']}")
```

### 场景2：分析网站结构

适用于刚开始制作书源时，快速了解目标网站的结构。

```python
from scripts.smart_web_analyzer import smart_analyze_website

# 分析网站
analysis = smart_analyze_website("https://example.com")

if 'error' in analysis:
    print(f"分析失败: {analysis['error']}")
else:
    print(f"页面编码: {analysis['charset']}")
    
    # 搜索表单信息
    if analysis['search_info']['found']:
        print("找到搜索表单:")
        for form in analysis['search_info']['forms']:
            print(f"  Action: {form['action']}")
            print(f"  Method: {form['method']}")
            print(f"  Inputs: {[inp['name'] for inp in form['inputs']]}")
    
    # 分页信息
    if analysis['pagination_info']['found']:
        print(f"分页类型: {analysis['pagination_info']['type']}")
        print(f"分页参数: {analysis['pagination_info']['page_param']}")
    
    # 列表结构
    if analysis['list_structure']['recommended']:
        print(f"推荐列表选择器: {analysis['list_structure']['recommended']}")
    
    # 安全信息
    if analysis['security_info']['cloudflare']:
        print("⚠️ 检测到Cloudflare")
    if analysis['security_info']['login_required']:
        print("⚠️ 需要登录")
    if analysis['security_info']['captcha']:
        print("⚠️ 存在验证码")
```

### 场景3：测试提取规则

适用于测试提取规则是否能正确提取内容。

```python
from scripts.multi_mode_extractor import extract_content

html = """
<html>
    <div class="book-list">
        <div class="book-item">
            <h3 class="book-title">斗破苍穹</h3>
            <p class="book-author">天蚕土豆</p>
            <a href="/book/123" class="book-link">详情</a>
        </div>
    </div>
</html>
"""

# 测试书名提取
result = extract_content(html, '.book-title')
print(f"书名: {result.content}")
print(f"置信度: {result.confidence:.2f}")
print(f"提取数量: {result.extracted_count}")

# 测试作者提取
result = extract_content(html, '.book-author')
print(f"作者: {result.content}")

# 测试链接提取
result = extract_content(html, '.book-link', extract_attr='href')
print(f"链接: {result.content}")

# 测试XPath
result = extract_content(html, '//h3[@class="book-title"]', method='xpath')
print(f"XPath提取: {result.content}")
```

### 场景4：完整调试流程

适用于对整个书源进行完整测试。

```bash
# 1. 测试搜索功能
python debugger/debugger_cli.py search book_source.json --keyword "斗破苍穹"

# 2. 测试详情页（使用搜索结果中的URL）
python debugger/debugger_cli.py info book_source.json --url "https://example.com/book/123"

# 3. 测试目录页
python debugger/debugger_cli.py toc book_source.json --url "https://example.com/book/123/toc"

# 4. 测试正文页
python debugger/debugger_cli.py content book_source.json --url "https://example.com/chapter/1"

# 5. 完整测试（自动执行以上所有步骤）
python debugger/debugger_cli.py test book_source.json --keyword "斗破苍穹"
```

### 场景5：结合多个工具

适用于复杂场景，需要多个工具配合使用。

```python
from scripts.smart_request import smart_fetch_html
from scripts.multi_mode_extractor import extract_content
from scripts.rule_validator import validate_rule

# 1. 获取页面HTML
result = smart_fetch_html("https://example.com/search?q=斗破苍穹")
if not result['success']:
    print(f"请求失败: {result['error']}")
    exit(1)

html = result['html']

# 2. 验证规则
validation = validate_rule(html, 'css', '.book-list .book-item')
if not validation['valid']:
    print("规则验证失败")
    exit(1)

# 3. 测试提取
extraction = extract_content(html, '.book-list .book-item')
print(f"提取到 {extraction.extracted_count} 个书籍")

# 4. 提取详细信息
for item in extraction.content[:5]:
    title = extract_content(html, '.book-title')
    author = extract_content(html, '.book-author')
    link = extract_content(html, '.book-link', extract_attr='href')
    print(f"书名: {title.content}, 作者: {author.content}, 链接: {link.content}")
```

## 验证原则

### 1. 模拟不等于真实

Python验证只是模拟环境，最终必须在Legado APP中实测。

**原因：**
- Python的HTML解析库（BeautifulSoup、lxml）与Legado使用的JSoup可能有差异
- Python的正则表达式引擎与Java的正则表达式可能有细微差异
- 网站可能对Python请求和Legado请求有不同的反爬策略
- JavaScript渲染的内容在Python中无法获取

**建议：**
- Python验证通过后，必须在Legado APP中进行完整测试
- 如果Python验证失败，优先检查规则本身
- 如果Python验证通过但Legado失败，考虑环境差异

### 2. 优先参考官方源码

使用`debugger/legado_checker.py`参考Legado Kotlin源码。

**原因：**
- 官方源码是最权威的参考
- 可以了解Legado的实际实现逻辑
- 可以发现Python模拟可能遗漏的细节

**建议：**
- 遇到不确定的规则时，查看Legado源码
- 对比Python实现和Kotlin实现
- 确保Python模拟与官方实现一致

### 3. 逐步验证

先验证搜索，再验证详情，最后验证正文。

**验证顺序：**
1. 搜索规则
2. 详情规则
3. 目录规则
4. 正文规则

**原因：**
- 搜索是入口，必须先保证搜索可用
- 详情页依赖搜索结果
- 目录页依赖详情页
- 正文页依赖目录页

**建议：**
- 每个环节验证通过后再进行下一步
- 记录每个环节的验证结果
- 发现问题及时修复

### 4. 记录问题

将验证中发现的问题记录到输出中。

**记录内容：**
- 验证失败的规则
- 验证通过的规则
- 置信度低的规则
- 需要人工确认的规则
- 环境差异导致的潜在问题

**建议：**
- 使用结构化的方式记录问题
- 提供改进建议
- 标注需要在Legado中实测的项

## 验证输出格式

验证结果应包含以下信息：

### 基本格式

```python
{
    'success': True/False,           # 验证是否成功
    'message': '验证结果描述',        # 结果描述
    'duration_ms': 123.45,          # 耗时（毫秒）
    'error': None,                  # 错误信息（如果有）
    'data': {...},                  # 提取的数据
    'confidence': 0.95,              # 置信度（0-1）
    'issues': [...],                # 问题列表
    'suggestions': [...]            # 改进建议
}
```

### 问题列表格式

```python
{
    'severity': 'error/warning/info',  # 严重程度
    'type': '规则类型',                # 问题类型
    'message': '问题描述',              # 问题描述
    'location': '规则位置',             # 规则位置
    'suggestion': '改进建议'            # 改进建议
}
```

### 输出示例

```python
{
    'success': True,
    'message': '搜索规则验证通过',
    'duration_ms': 45.67,
    'error': None,
    'data': {
        'books': [
            {'name': '斗破苍穹', 'author': '天蚕土豆', 'url': '/book/123'},
            {'name': '武动乾坤', 'author': '天蚕土豆', 'url': '/book/456'}
        ]
    },
    'confidence': 0.98,
    'issues': [],
    'suggestions': [
        '建议在Legado APP中实测搜索功能',
        '建议测试不同关键词的搜索结果'
    ]
}
```

## 常见问题

### Q1: Python验证通过，但在Legado中失败？

**可能原因：**
1. 网站对Python和Legado有不同的反爬策略
2. Python解析库与JSoup的实现差异
3. 编码问题（Python检测的编码与实际不符）
4. JavaScript渲染的内容
5. Cookie或Session问题

**解决方法：**
1. 检查Legado的请求头是否与Python一致
2. 在Legado中手动测试，对比结果
3. 检查是否需要登录或验证码
4. 查看Legado源码，对比实现逻辑

### Q2: 如何验证动态加载的内容？

**解决方法：**
1. 使用浏览器开发者工具分析网络请求
2. 找到实际的API接口
3. 使用`scripts/smart_request.py`测试API
4. 如果需要JavaScript渲染，Python无法模拟，直接在Legado中测试

### Q3: 验证时遇到编码问题？

**解决方法：**
1. 使用`scripts/smart_request.py`的智能编码检测
2. 手动指定编码：`smart_fetch_html(url, charset='gbk')`
3. 检查HTML的meta标签和HTTP响应头
4. 使用chardet库检测编码

### Q4: 如何提高验证的准确性？

**建议：**
1. 使用真实的HTML进行验证（而不是模拟的HTML）
2. 测试多个不同的页面，确保规则的通用性
3. 测试边界情况（空列表、单条记录等）
4. 参考Legado官方源码，确保实现一致
5. 在Legado中进行完整测试

## 最佳实践

### 1. 验证前准备

```python
# 准备测试数据
test_cases = {
    'search': {
        'keyword': '斗破苍穹',
        'expected_count': 10
    },
    'detail': {
        'url': 'https://example.com/book/123',
        'expected_fields': ['name', 'author', 'intro']
    },
    'toc': {
        'url': 'https://example.com/book/123/toc',
        'expected_count': 100
    },
    'content': {
        'url': 'https://example.com/chapter/1',
        'expected_min_length': 1000
    }
}
```

### 2. 验证流程

```python
def validate_book_source(book_source, test_cases):
    """验证书源的完整流程"""
    results = {}
    
    # 1. 验证搜索
    results['search'] = validate_search(book_source, test_cases['search'])
    
    if results['search']['success']:
        # 2. 验证详情
        book_url = results['search']['data'][0]['url']
        results['detail'] = validate_detail(book_source, book_url, test_cases['detail'])
        
        if results['detail']['success']:
            # 3. 验证目录
            toc_url = results['detail']['data']['toc_url']
            results['toc'] = validate_toc(book_source, toc_url, test_cases['toc'])
            
            if results['toc']['success']:
                # 4. 验证正文
                chapter_url = results['toc']['data'][0]['url']
                results['content'] = validate_content(book_source, chapter_url, test_cases['content'])
    
    return results
```

### 3. 结果报告

```python
def generate_report(results):
    """生成验证报告"""
    report = []
    
    for stage, result in results.items():
        status = "✓" if result['success'] else "✗"
        report.append(f"{status} {stage}: {result['message']}")
        
        if result['issues']:
            for issue in result['issues']:
                report.append(f"  - {issue['severity']}: {issue['message']}")
        
        if result['suggestions']:
            for suggestion in result['suggestions']:
                report.append(f"  建议: {suggestion}")
    
    return '\n'.join(report)
```

### 4. 持续验证

```python
def continuous_validation(book_source, test_cases, iterations=3):
    """持续验证，检查稳定性"""
    all_results = []
    
    for i in range(iterations):
        print(f"\n第 {i+1} 次验证...")
        results = validate_book_source(book_source, test_cases)
        all_results.append(results)
    
    # 分析稳定性
    stability = analyze_stability(all_results)
    print(f"\n稳定性评分: {stability:.2f}")
    
    return all_results
```

## 总结

Python验证工具是书源制作过程中的重要辅助工具，但需要注意：

1. **验证不等于真实**：Python验证只是模拟，最终必须在Legado APP中实测
2. **逐步验证**：按照搜索→详情→目录→正文的顺序逐步验证
3. **记录问题**：详细记录验证中发现的问题和改进建议
4. **参考官方源码**：使用Legado源码作为权威参考
5. **持续改进**：根据验证结果不断优化规则

通过合理使用这些工具，可以大大提高书源制作的效率和准确性，但最终的验证必须在Legado APP中进行。
