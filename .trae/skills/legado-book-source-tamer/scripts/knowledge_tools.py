"""
知识库工具
提供知识库查询和学习功能
"""

import os
import json
from typing import Dict, List, Any, Optional


class KnowledgeBase:
    """知识库管理器"""
    
    def __init__(self, knowledge_dir: str = None):
        if knowledge_dir:
            self.knowledge_dir = knowledge_dir
        else:
            self.knowledge_dir = os.path.join(os.path.dirname(__file__), '..', 'references')
        
        self.knowledge_cache: Dict[str, Any] = {}
        self.is_loaded = False
    
    def load_knowledge(self, force: bool = False) -> Dict[str, Any]:
        """加载知识库"""
        if self.is_loaded and not force:
            return self.knowledge_cache
        
        if not os.path.exists(self.knowledge_dir):
            os.makedirs(self.knowledge_dir, exist_ok=True)
            self.is_loaded = True
            return self.knowledge_cache
        
        for filename in os.listdir(self.knowledge_dir):
            if filename.endswith(('.md', '.txt', '.json')):
                filepath = os.path.join(self.knowledge_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                        self.knowledge_cache[filename] = content
                except Exception as e:
                    print(f"加载知识文件失败 {filename}: {e}")
        
        self.is_loaded = True
        return self.knowledge_cache
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """搜索知识库"""
        if not self.is_loaded:
            self.load_knowledge()
        
        results = []
        query_lower = query.lower()
        
        for filename, content in self.knowledge_cache.items():
            if query_lower in content.lower():
                lines = content.split('\n')
                relevant_lines = []
                
                for i, line in enumerate(lines):
                    if query_lower in line.lower():
                        start = max(0, i - 2)
                        end = min(len(lines), i + 3)
                        context = '\n'.join(lines[start:end])
                        relevant_lines.append(context)
                
                if relevant_lines:
                    results.append({
                        'filename': filename,
                        'matches': relevant_lines[:limit],
                        'relevance': len(relevant_lines)
                    })
        
        results.sort(key=lambda x: x['relevance'], reverse=True)
        return results[:limit]
    
    def get_css_selector_rules(self) -> str:
        """获取CSS选择器规则"""
        css_file = os.path.join(self.knowledge_dir, 'css-selector-rules.md')
        if os.path.exists(css_file):
            with open(css_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def get_book_source_templates(self) -> str:
        """获取书源模板"""
        template_file = os.path.join(self.knowledge_dir, 'book-source-templates.md')
        if os.path.exists(template_file):
            with open(template_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    
    def get_javascript_api(self) -> str:
        """获取JavaScript API文档"""
        js_file = os.path.join(self.knowledge_dir, 'javascript-api.md')
        if os.path.exists(js_file):
            with open(js_file, 'r', encoding='utf-8') as f:
                return f.read()
        return ""


_global_knowledge_base: Optional[KnowledgeBase] = None


def get_knowledge_base() -> KnowledgeBase:
    """获取全局知识库实例"""
    global _global_knowledge_base
    if _global_knowledge_base is None:
        _global_knowledge_base = KnowledgeBase()
    return _global_knowledge_base


def search_knowledge(query: str, limit: int = 5) -> List[Dict[str, Any]]:
    """搜索知识库的便捷函数"""
    kb = get_knowledge_base()
    return kb.search(query, limit)


def get_css_selector_rules() -> str:
    """获取CSS选择器规则的便捷函数"""
    kb = get_knowledge_base()
    return kb.get_css_selector_rules()


def get_book_source_templates() -> str:
    """获取书源模板的便捷函数"""
    kb = get_knowledge_base()
    return kb.get_book_source_templates()
