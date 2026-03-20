"""
Legado Book Source Debugger - Pure Debug Engine
纯调试引擎 - 只负责调试模拟模型

职责说明：
- 只负责调试模拟模型
- 基于真实Legado Kotlin代码翻译
- 返回Python对象/字典
- 不负责JSON输出（由技能包处理）
- 不负责修复优化（由技能包处理）
"""

__version__ = "2.3.0"

from .engine.analyze_rule import AnalyzeRule
from .engine.book_source import BookSource, BookInfoRule, ContentRule, SearchRule, TocRule
from .engine.debug_engine import DebugEngine
from .engine.web_book import WebBook
from .json_output import (
    JsonOutputUtility,
    JsonOutputError,
    save_book_source_to_root,
    validate_json_syntax,
    format_book_source_json,
)
from .environment_simulator import (
    ReadingEnvironmentSimulator,
    BookSourceType,
    TestStatus,
    TestCase,
    TestSuite,
    EnvironmentConfig,
    create_environment,
    run_quick_test,
)
from .test_cases import (
    TestCaseBuilder,
    TestExecutor,
    TestReportGenerator,
    TestIssue,
    TestStep,
    PerformanceMetric,
    Severity,
    TestCategory,
    run_standard_tests,
    generate_and_save_report,
)
from .js_engine import (
    LegadoJsEngine,
    JsExtensions,
    JsExecutionResult,
    execute_js,
    execute_js_rule,
    get_js_engine,
)

__all__ = [
    "AnalyzeRule",
    "BookSource",
    "BookInfoRule",
    "ContentRule",
    "SearchRule",
    "TocRule",
    "DebugEngine",
    "WebBook",
    "debug_book_source",
    "JsonOutputUtility",
    "JsonOutputError",
    "save_book_source_to_root",
    "validate_json_syntax",
    "format_book_source_json",
    "ReadingEnvironmentSimulator",
    "BookSourceType",
    "TestStatus",
    "TestCase",
    "TestSuite",
    "EnvironmentConfig",
    "create_environment",
    "run_quick_test",
    "TestCaseBuilder",
    "TestExecutor",
    "TestReportGenerator",
    "TestIssue",
    "TestStep",
    "PerformanceMetric",
    "Severity",
    "TestCategory",
    "run_standard_tests",
    "generate_and_save_report",
    "LegadoJsEngine",
    "JsExtensions",
    "JsExecutionResult",
    "execute_js",
    "execute_js_rule",
    "get_js_engine",
]


def debug_book_source(book_source, keyword="斗破苍穹"):
    """
    调试书源 - 返回Python字典，不输出JSON
    
    Args:
        book_source: BookSource对象或字典
        keyword: 搜索关键词
    
    Returns:
        dict: 调试结果字典（Python对象，不是JSON字符串）
    """
    if isinstance(book_source, dict):
        source = BookSource.from_dict(book_source)
    else:
        source = book_source
    
    engine = DebugEngine(source)
    return engine.run_full_test(keyword)


def save_book_source(content, source_name=None, project_root=None, **kwargs):
    """
    保存书源JSON到项目根目录
    
    Args:
        content: 书源内容
        source_name: 书源名称
        project_root: 项目根目录
        **kwargs: 其他参数
    
    Returns:
        dict: 保存结果
    """
    utility = JsonOutputUtility(project_root)
    return utility.save_book_source(content, source_name, **kwargs)


def run_full_test_suite(project_root=None, save_report=True):
    """
    运行完整测试套件
    
    Args:
        project_root: 项目根目录
        save_report: 是否保存报告
    
    Returns:
        dict: 测试结果
    """
    results = run_standard_tests(project_root)
    
    if save_report:
        from pathlib import Path
        root = Path(project_root) if project_root else Path.cwd()
        
        json_path = root / f"test_report_{__version__}.json"
        generate_and_save_report(results, str(json_path), 'json')
        
        md_path = root / f"test_report_{__version__}.md"
        generate_and_save_report(results, str(md_path), 'markdown')
        
        results['saved_reports'] = {
            'json': str(json_path),
            'markdown': str(md_path),
        }
    
    return results
