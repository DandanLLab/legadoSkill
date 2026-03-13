"""
Legado Book Source Tamer - Scripts Package
"""

from .file_organizer import (
    organize_book_source_files,
    start_file_session,
    register_generated_file,
    BookSourceFileOrganizer,
    FileOrganizeResult
)

from .smart_request import (
    SmartRequest,
    smart_fetch_html
)

from .rule_validator import (
    RuleValidator,
    validate_rule,
    validate_book_source
)

from .multi_mode_extractor import (
    MultiModeExtractor,
    extract_content,
    ExtractionResult
)

from .knowledge_tools import (
    KnowledgeBase,
    get_knowledge_base,
    search_knowledge,
    get_css_selector_rules,
    get_book_source_templates
)

from .smart_web_analyzer import (
    SmartWebAnalyzer,
    smart_analyze_website
)

__all__ = [
    'organize_book_source_files',
    'start_file_session',
    'register_generated_file',
    'BookSourceFileOrganizer',
    'FileOrganizeResult',
    'SmartRequest',
    'smart_fetch_html',
    'RuleValidator',
    'validate_rule',
    'validate_book_source',
    'MultiModeExtractor',
    'extract_content',
    'ExtractionResult',
    'KnowledgeBase',
    'get_knowledge_base',
    'search_knowledge',
    'get_css_selector_rules',
    'get_book_source_templates',
    'SmartWebAnalyzer',
    'smart_analyze_website',
]
