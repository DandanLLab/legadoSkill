"""
Kotlin to Python Translation Reference
Kotlin到Python翻译参考

This module provides reference mapping between Kotlin source code and Python implementation.
本模块提供Kotlin源码和Python实现之间的参考映射。

Directory Structure:
目录结构:

kotlin_reference/          # Kotlin原始代码（仅供参考，不能运行）
├── AnalyzeRule.kt         # 核心规则分析器
├── AnalyzeUrl.kt          # URL分析器
├── WebBook.kt             # 网页获取器
├── AnalyzeByJSoup.kt      # JSoup解析器
├── AnalyzeByXPath.kt      # XPath解析器
└── AnalyzeByJSonPath.kt   # JSONPath解析器

Python Implementation:     # Python实现（可运行）
├── analyze_rule.py        # 对应 AnalyzeRule.kt
├── analyze_url.py         # 对应 AnalyzeUrl.kt
├── web_book.py            # 对应 WebBook.kt
└── book_source.py         # 书源数据模型
"""

# ============================================================
# Kotlin -> Python 翻译映射表
# ============================================================

TRANSLATION_MAPPING = {
    # 类映射
    "classes": {
        "AnalyzeRule": {
            "kotlin": "kotlin_reference/AnalyzeRule.kt",
            "python": "analyze_rule.py",
            "description": "核心规则分析引擎，处理CSS/XPath/JSONPath/正则/JS规则"
        },
        "AnalyzeUrl": {
            "kotlin": "kotlin_reference/AnalyzeUrl.kt", 
            "python": "analyze_url.py",
            "description": "URL构建和HTTP请求处理"
        },
        "WebBook": {
            "kotlin": "kotlin_reference/WebBook.kt",
            "python": "web_book.py",
            "description": "书源网页获取和解析"
        },
        "AnalyzeByJSoup": {
            "kotlin": "kotlin_reference/AnalyzeByJSoup.kt",
            "python": "analyze_rule.py (内置)",
            "description": "JSoup CSS选择器解析"
        },
        "AnalyzeByXPath": {
            "kotlin": "kotlin_reference/AnalyzeByXPath.kt",
            "python": "analyze_rule.py (内置)",
            "description": "XPath表达式解析"
        },
        "AnalyzeByJSonPath": {
            "kotlin": "kotlin_reference/AnalyzeByJSonPath.kt",
            "python": "analyze_rule.py (内置)",
            "description": "JSONPath表达式解析"
        },
    },
    
    # 方法映射
    "methods": {
        # AnalyzeRule
        "setContent": "set_content",
        "getString": "get_string",
        "getStringList": "get_string_list",
        "getElements": "get_elements",
        "splitSourceRule": "_split_source_rule",
        "applyRule": "_apply_rules",
        
        # AnalyzeUrl
        "getStrResponse": "get_str_response",
        "getStrResponseAwait": "get_str_response_await",
        "initUrl": "_init_url",
        
        # WebBook
        "searchBookAwait": "search_book",
        "getBookInfoAwait": "get_book_info",
        "getChapterListAwait": "get_chapter_list",
        "getContentAwait": "get_content",
    },
    
    # 类型映射
    "types": {
        "String": "str",
        "List<String>": "List[str]",
        "Map<String, String>": "Dict[str, str]",
        "Boolean": "bool",
        "Int": "int",
        "Long": "int",
        "Any": "Any",
        "Unit": "None",
        "suspend fun": "async def",
        "fun": "def",
        "val": "变量",
        "var": "变量",
    },
    
    # 语法映射
    "syntax": {
        "?.": "?. (安全调用) -> if x is not None",
        "?:": "?: (Elvis操作符) -> or",
        "!!": "!! (非空断言) -> 直接访问",
        "isNullOrEmpty()": "not x or len(x) == 0",
        "isNotBlank()": "x and x.strip()",
        "substringBefore()": "x.split(delimiter)[0]",
        "substringAfter()": "x.split(delimiter)[-1]",
        "split()": "split()",
        "firstOrNull()": "[0] if list else None",
        "lastOrNull()": "[-1] if list else None",
        "forEach { }": "for x in list:",
        "map { }": "[f(x) for x in list]",
        "filter { }": "[x for x in list if condition]",
        "let { }": "if x is not None: ...",
        "also { }": "x; ...; return x",
        "apply { }": "x.attr = value; return x",
        "run { }": "代码块执行",
        "with(x) { }": "with x:",
        "when(x) { }": "if/elif/else 或 match/case",
        "object { }": "lambda 或 dict",
        "data class": "@dataclass",
        "companion object": "类方法/静态方法",
    },
}

# ============================================================
# 翻译示例
# ============================================================

TRANSLATION_EXAMPLES = """
# Kotlin 原始代码
fun getString(rule: String?): String {
    if (rule.isNullOrEmpty()) return ""
    val rules = splitSourceRule(rule)
    return applyRules(rules)
}

# Python 翻译代码
def get_string(self, rule: str) -> str:
    if not rule:
        return ""
    rules = self._split_source_rule(rule)
    return self._apply_rules(rules)

---

# Kotlin 原始代码
val url = when {
    mUrl.contains("{{key}}") -> mUrl.replace("{{key}}", key)
    else -> mUrl
}

# Python 翻译代码
if "{{key}}" in m_url:
    url = m_url.replace("{{key}}", key)
else:
    url = m_url

---

# Kotlin 原始代码
suspend fun getStrResponseAwait(): StrResponse {
    return withContext(Dispatchers.IO) {
        // 网络请求
    }
}

# Python 翻译代码
def get_str_response_await(self) -> StrResponse:
    # 直接执行网络请求（Python是同步的）
    return self.get_str_response()
"""

# ============================================================
# 注意事项
# ============================================================

TRANSLATION_NOTES = """
1. Kotlin的协程(coroutine)在Python中用同步代码模拟
   - suspend fun -> def (同步函数)
   - withContext -> 直接执行

2. Kotlin的空安全在Python中用条件判断模拟
   - x?.method() -> if x is not None: x.method()
   - x ?: default -> x or default

3. Kotlin的扩展函数在Python中用普通方法实现
   - String.isBlank() -> str.strip() == ""

4. Kotlin的lambda表达式在Python中用lambda或def实现
   - { x -> x + 1 } -> lambda x: x + 1

5. Kotlin的集合操作在Python中用列表推导式
   - list.map { it.name } -> [x.name for x in list]
   - list.filter { it.active } -> [x for x in list if x.active]

6. Kotlin的when表达式在Python 3.10+可用match/case
   - 早期版本用if/elif/else

7. Kotlin的data class在Python中用@dataclass装饰器

8. Kotlin的companion object在Python中用@classmethod或@staticmethod
"""


def get_kotlin_source(class_name: str) -> str:
    """
    获取Kotlin源码文件路径
    
    Args:
        class_name: 类名
    
    Returns:
        Kotlin源码文件路径
    """
    from pathlib import Path
    
    mapping = TRANSLATION_MAPPING["classes"].get(class_name)
    if mapping:
        kotlin_path = Path(__file__).parent / mapping["kotlin"]
        if kotlin_path.exists():
            return str(kotlin_path)
    return ""


def get_python_source(class_name: str) -> str:
    """
    获取Python源码文件路径
    
    Args:
        class_name: 类名
    
    Returns:
        Python源码文件路径
    """
    from pathlib import Path
    
    mapping = TRANSLATION_MAPPING["classes"].get(class_name)
    if mapping:
        python_path = Path(__file__).parent / mapping["python"]
        if python_path.exists():
            return str(python_path)
    return ""


def list_available_translations() -> Dict[str, Dict[str, str]]:
    """
    列出所有可用的翻译映射
    
    Returns:
        翻译映射字典
    """
    return TRANSLATION_MAPPING["classes"]
