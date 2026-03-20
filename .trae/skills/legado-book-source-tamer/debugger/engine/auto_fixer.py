"""
AutoFixer - 自动修复迭代模块
实现调试失败自动分析原因、生成修复方案、循环测试直到成功

核心功能：
1. 分析失败原因
2. 智能生成修复方案
3. 应用修复并重新测试
4. 支持多种失败类型的修复策略
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ErrorType(Enum):
    SEARCH_NO_RESULT = "search_no_result"
    SEARCH_EMPTY_LIST = "search_empty_list"
    BOOK_INFO_FAILED = "book_info_failed"
    TOC_EMPTY = "toc_empty"
    CONTENT_EMPTY = "content_empty"
    ENCODING_ERROR = "encoding_error"
    URL_BUILD_ERROR = "url_build_error"
    RULE_PARSE_ERROR = "rule_parse_error"
    NETWORK_ERROR = "network_error"
    JS_ERROR = "js_error"
    UNKNOWN = "unknown"


@dataclass
class ErrorAnalysis:
    error_type: ErrorType
    error_message: str
    error_detail: str = ""
    suggestions: List[str] = field(default_factory=list)
    html_preview: str = ""


@dataclass
class FixResult:
    success: bool
    fixed_source: Dict
    message: str
    changes: List[str] = field(default_factory=list)


class AutoFixer:
    """
    自动修复器 - 实现调试失败自动优化迭代
    
    使用方法：
    fixer = AutoFixer(book_source, debug_engine)
    result = fixer.auto_fix_and_test(keyword, max_attempts=5)
    """
    
    COMMON_SELECTORS = {
        "book_list": [
            ".book-item",
            ".result-item", 
            "#list li",
            "ul.list li",
            ".search-list li",
            ".grid .item",
            ".book-list .item",
            ".novel-list li",
            ".result-list li",
            "table.grid tr",
            ".item",
            "li",
            "dl",
        ],
        "book_name": [
            "a@title",
            "a@text",
            ".name@text",
            ".title@text",
            "h3@text",
            "h4@text",
            "a.1@text",
            "td.1@text",
        ],
        "book_url": [
            "a@href",
            "a.0@href",
            ".title a@href",
            "a.1@href",
        ],
        "author": [
            ".author@text",
            ".author a@text",
            "span.2@text",
            "td.2@text",
            "p@text##作者：##",
        ],
        "chapter_list": [
            "#list dd",
            "#list dl dd",
            ".chapter-list li",
            ".list li",
            "#chapters li",
            "ul.list li",
            "dd",
            "li",
        ],
        "chapter_name": [
            "a@text",
            "a@title",
            "@text",
        ],
        "chapter_url": [
            "a@href",
            "@href",
        ],
        "content": [
            "#content",
            ".content",
            "#chaptercontent",
            ".txt",
            "#Text",
            ".chapter-content",
            ".article-content",
            "#article",
            ".novel-content",
            ".read-content",
            "#read-content",
        ],
    }
    
    def __init__(self, book_source: Dict, debug_engine=None, log_callback=None):
        self.book_source = book_source
        self.debug_engine = debug_engine
        self.log_callback = log_callback
        self.attempt_count = 0
        self.max_attempts = 5
        self.fix_history: List[Dict] = []
    
    def log(self, category: str, message: str):
        if self.log_callback:
            self.log_callback(category, message)
        print(f"[{category}] {message}")
    
    def analyze_error(self, test_result: Dict) -> ErrorAnalysis:
        """
        分析测试结果，诊断失败原因
        
        Args:
            test_result: 测试结果字典，包含success, message, steps等
            
        Returns:
            ErrorAnalysis对象
        """
        if test_result.get("success"):
            return ErrorAnalysis(ErrorType.UNKNOWN, "测试成功，无需修复")
        
        steps = test_result.get("steps", [])
        message = test_result.get("message", "")
        
        for step in steps:
            step_name = step.get("step", "")
            step_message = step.get("message", "")
            step_data = step.get("data", {})
            
            if step_name == "搜索":
                if "无结果" in step_message or "空" in step_message:
                    return ErrorAnalysis(
                        ErrorType.SEARCH_NO_RESULT,
                        step_message,
                        html_preview=step_data.get("html_preview", ""),
                        suggestions=[
                            "检查bookList选择器是否正确",
                            "检查网站是否需要特殊headers",
                            "检查搜索URL是否正确",
                        ]
                    )
                elif "列表大小:0" in step_message:
                    return ErrorAnalysis(
                        ErrorType.SEARCH_EMPTY_LIST,
                        step_message,
                        html_preview=step_data.get("html_preview", ""),
                        suggestions=[
                            "bookList选择器可能不匹配",
                            "尝试更通用的选择器",
                        ]
                    )
            
            elif step_name == "详情":
                if "失败" in step_message or "错误" in step_message:
                    return ErrorAnalysis(
                        ErrorType.BOOK_INFO_FAILED,
                        step_message,
                        suggestions=[
                            "检查bookUrl规则是否正确",
                            "检查URL拼接逻辑",
                        ]
                    )
            
            elif step_name == "目录":
                if "空" in step_message or "列表大小:0" in step_message:
                    return ErrorAnalysis(
                        ErrorType.TOC_EMPTY,
                        step_message,
                        html_preview=step_data.get("html_preview", ""),
                        suggestions=[
                            "检查chapterList选择器",
                            "检查是否需要登录",
                        ]
                    )
            
            elif step_name == "正文":
                if "空" in step_message or "失败" in step_message:
                    return ErrorAnalysis(
                        ErrorType.CONTENT_EMPTY,
                        step_message,
                        html_preview=step_data.get("html_preview", ""),
                        suggestions=[
                            "检查content选择器",
                            "检查是否需要登录",
                            "检查是否有反爬虫",
                        ]
                    )
        
        if "编码" in message or "乱码" in message:
            return ErrorAnalysis(
                ErrorType.ENCODING_ERROR,
                message,
                suggestions=[
                    "添加charset参数",
                    "检查网站编码",
                ]
            )
        
        if "JS" in message or "JavaScript" in message:
            return ErrorAnalysis(
                ErrorType.JS_ERROR,
                message,
                suggestions=[
                    "检查JS语法",
                    "检查JS变量引用",
                ]
            )
        
        return ErrorAnalysis(
            ErrorType.UNKNOWN,
            message,
            suggestions=["请检查书源规则"]
        )
    
    def generate_fix(self, error_analysis: ErrorAnalysis, html_preview: str = "") -> FixResult:
        """
        根据错误分析生成修复方案
        
        Args:
            error_analysis: 错误分析结果
            html_preview: HTML预览（用于分析结构）
            
        Returns:
            FixResult对象
        """
        fixed_source = self.book_source.copy()
        changes = []
        
        if error_analysis.error_type == ErrorType.SEARCH_NO_RESULT:
            fix_result = self._fix_search_no_result(fixed_source, html_preview)
            changes.extend(fix_result.get("changes", []))
            
        elif error_analysis.error_type == ErrorType.SEARCH_EMPTY_LIST:
            fix_result = self._fix_search_empty_list(fixed_source, html_preview)
            changes.extend(fix_result.get("changes", []))
            
        elif error_analysis.error_type == ErrorType.TOC_EMPTY:
            fix_result = self._fix_toc_empty(fixed_source, html_preview)
            changes.extend(fix_result.get("changes", []))
            
        elif error_analysis.error_type == ErrorType.CONTENT_EMPTY:
            fix_result = self._fix_content_empty(fixed_source, html_preview)
            changes.extend(fix_result.get("changes", []))
            
        elif error_analysis.error_type == ErrorType.ENCODING_ERROR:
            fix_result = self._fix_encoding_error(fixed_source)
            changes.extend(fix_result.get("changes", []))
        
        if not changes:
            return FixResult(
                success=False,
                fixed_source=fixed_source,
                message="无法自动修复此错误",
                changes=[]
            )
        
        return FixResult(
            success=True,
            fixed_source=fixed_source,
            message=f"已应用{len(changes)}个修复",
            changes=changes
        )
    
    def _fix_search_no_result(self, source: Dict, html_preview: str) -> Dict:
        changes = []
        
        if not html_preview:
            html_preview = ""
        
        rule_search = source.get("ruleSearch", {})
        
        for selector in self.COMMON_SELECTORS["book_list"]:
            if selector in html_preview or self._test_selector_in_html(selector, html_preview):
                if rule_search.get("bookList") != selector:
                    rule_search["bookList"] = selector
                    changes.append(f"bookList: {selector}")
                    self.log("修复", f"尝试bookList选择器: {selector}")
                    break
        
        if not changes:
            for selector in self.COMMON_SELECTORS["book_list"][:5]:
                rule_search["bookList"] = selector
                changes.append(f"bookList: {selector} (尝试)")
                break
        
        source["ruleSearch"] = rule_search
        return {"changes": changes}
    
    def _fix_search_empty_list(self, source: Dict, html_preview: str) -> Dict:
        changes = []
        
        rule_search = source.get("ruleSearch", {})
        current_selector = rule_search.get("bookList", "")
        
        for selector in self.COMMON_SELECTORS["book_list"]:
            if selector != current_selector:
                rule_search["bookList"] = selector
                changes.append(f"bookList: {current_selector} -> {selector}")
                self.log("修复", f"更换bookList选择器: {selector}")
                break
        
        source["ruleSearch"] = rule_search
        return {"changes": changes}
    
    def _fix_toc_empty(self, source: Dict, html_preview: str) -> Dict:
        changes = []
        
        rule_toc = source.get("ruleToc", {})
        
        for selector in self.COMMON_SELECTORS["chapter_list"]:
            rule_toc["chapterList"] = selector
            changes.append(f"chapterList: {selector}")
            self.log("修复", f"尝试chapterList选择器: {selector}")
            break
        
        if not rule_toc.get("chapterName"):
            rule_toc["chapterName"] = "a@text"
            changes.append("chapterName: a@text")
        
        if not rule_toc.get("chapterUrl"):
            rule_toc["chapterUrl"] = "a@href"
            changes.append("chapterUrl: a@href")
        
        source["ruleToc"] = rule_toc
        return {"changes": changes}
    
    def _fix_content_empty(self, source: Dict, html_preview: str) -> Dict:
        changes = []
        
        rule_content = source.get("ruleContent", {})
        
        for selector in self.COMMON_SELECTORS["content"]:
            rule_content["content"] = f"{selector}@html"
            changes.append(f"content: {selector}@html")
            self.log("修复", f"尝试content选择器: {selector}@html")
            break
        
        source["ruleContent"] = rule_content
        return {"changes": changes}
    
    def _fix_encoding_error(self, source: Dict) -> Dict:
        changes = []
        
        search_url = source.get("searchUrl", "")
        if "charset" not in search_url:
            if "," in search_url:
                parts = search_url.split(",", 1)
                try:
                    options = json.loads(parts[1])
                    options["charset"] = "gbk"
                    source["searchUrl"] = parts[0] + "," + json.dumps(options, ensure_ascii=False)
                except:
                    source["searchUrl"] = search_url + ',{"charset":"gbk"}'
            else:
                source["searchUrl"] = search_url + ',{"charset":"gbk"}'
            changes.append("添加charset: gbk")
            self.log("修复", "添加GBK编码支持")
        
        return {"changes": changes}
    
    def _test_selector_in_html(self, selector: str, html: str) -> bool:
        if not html:
            return False
        
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            elements = soup.select(selector)
            return len(elements) > 0
        except:
            return False
    
    def auto_fix_and_test(self, keyword: str, max_attempts: int = 5) -> Dict:
        """
        自动修复并测试的完整流程
        
        Args:
            keyword: 搜索关键词
            max_attempts: 最大尝试次数
            
        Returns:
            最终测试结果
        """
        self.max_attempts = max_attempts
        self.attempt_count = 0
        self.fix_history = []
        
        self.log("自动修复", f"开始自动修复流程，关键词: {keyword}")
        
        while self.attempt_count < self.max_attempts:
            self.attempt_count += 1
            self.log("自动修复", f"第 {self.attempt_count}/{self.max_attempts} 次尝试")
            
            test_result = self._run_test(keyword)
            
            if test_result.get("success"):
                self.log("自动修复", "✓ 测试成功！")
                return {
                    "success": True,
                    "book_source": self.book_source,
                    "attempts": self.attempt_count,
                    "fix_history": self.fix_history,
                    "test_result": test_result,
                }
            
            error_analysis = self.analyze_error(test_result)
            self.log("自动修复", f"错误类型: {error_analysis.error_type.value}")
            self.log("自动修复", f"错误信息: {error_analysis.error_message}")
            
            html_preview = ""
            for step in test_result.get("steps", []):
                if step.get("data", {}).get("html_preview"):
                    html_preview = step["data"]["html_preview"]
                    break
            
            fix_result = self.generate_fix(error_analysis, html_preview)
            
            if not fix_result.success:
                self.log("自动修复", "✗ 无法自动修复此错误")
                return {
                    "success": False,
                    "book_source": self.book_source,
                    "attempts": self.attempt_count,
                    "fix_history": self.fix_history,
                    "error_analysis": error_analysis,
                    "test_result": test_result,
                }
            
            self.book_source = fix_result.fixed_source
            self.fix_history.append({
                "attempt": self.attempt_count,
                "error_type": error_analysis.error_type.value,
                "changes": fix_result.changes,
            })
            
            self.log("自动修复", f"应用修复: {', '.join(fix_result.changes)}")
        
        self.log("自动修复", f"达到最大尝试次数 {self.max_attempts}")
        return {
            "success": False,
            "book_source": self.book_source,
            "attempts": self.attempt_count,
            "fix_history": self.fix_history,
            "message": f"达到最大尝试次数，未能完全修复",
        }
    
    def _run_test(self, keyword: str) -> Dict:
        if self.debug_engine:
            from debugger.engine.book_source import BookSource
            source = BookSource.from_dict(self.book_source)
            self.debug_engine.book_source = source
            return self.debug_engine.test_content(keyword)
        
        return {
            "success": False,
            "message": "调试引擎未初始化",
            "steps": [],
        }


def run_auto_fix(book_source: Dict, keyword: str, debug_engine=None, max_attempts: int = 5) -> Dict:
    """
    便捷函数：运行自动修复流程
    
    Args:
        book_source: 书源字典
        keyword: 搜索关键词
        debug_engine: 调试引擎实例
        max_attempts: 最大尝试次数
        
    Returns:
        修复结果
    """
    fixer = AutoFixer(book_source, debug_engine)
    return fixer.auto_fix_and_test(keyword, max_attempts)
