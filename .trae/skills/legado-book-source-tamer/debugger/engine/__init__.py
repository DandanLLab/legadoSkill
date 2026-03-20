"""
Engine Module - Core debugging engine components
Based on Legado Kotlin source code, translated to Python
"""

from .analyze_rule import AnalyzeRule, Mode, SourceRule
from .analyze_url import AnalyzeUrl, StrResponse, build_analyze_url, fetch_url
from .book_source import (
    BookSource,
    BookInfoRule,
    ContentRule,
    SearchRule,
    TocRule,
    ExploreRule,
    BookSourceType,
)
from .debug_engine import DebugEngine, DebugResult, SearchResult, BookInfo, Chapter, Content
from .web_book import WebBook
from .auto_fixer import AutoFixer, ErrorType, ErrorAnalysis, FixResult, run_auto_fix

__all__ = [
    "AnalyzeRule",
    "Mode",
    "SourceRule",
    "AnalyzeUrl",
    "StrResponse",
    "build_analyze_url",
    "fetch_url",
    "BookSource",
    "BookInfoRule",
    "ContentRule",
    "SearchRule",
    "TocRule",
    "ExploreRule",
    "BookSourceType",
    "DebugEngine",
    "DebugResult",
    "SearchResult",
    "BookInfo",
    "Chapter",
    "Content",
    "WebBook",
    "AutoFixer",
    "ErrorType",
    "ErrorAnalysis",
    "FixResult",
    "run_auto_fix",
]
