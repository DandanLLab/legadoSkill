"""
规则验证和优化引擎
验证选择器和规则的正确性，优化性能，提供改进建议
"""

import re
import json
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from bs4 import BeautifulSoup
from lxml import etree, html as lxml_html


@dataclass
class ValidationIssue:
    """验证问题"""
    severity: str
    type: str
    message: str
    location: str
    suggestion: str


class RuleValidator:
    """规则验证器"""
    
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')
        self.lxml_doc = lxml_html.fromstring(html)
        self.issues = []
        self.suggestions = []
    
    def validate_rule(
        self,
        rule_type: str,
        rule_value: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """验证规则"""
        context = context or {}
        
        validation_result = {
            'rule_type': rule_type,
            'rule_value': rule_value,
            'valid': True,
            'issues': [],
            'suggestions': [],
            'test_results': {}
        }
        
        if rule_type == 'css':
            validation_result.update(self._validate_css(rule_value, context))
        elif rule_type == 'xpath':
            validation_result.update(self._validate_xpath(rule_value, context))
        elif rule_type == 'regex':
            validation_result.update(self._validate_regex(rule_value, context))
        
        return validation_result
    
    def _validate_css(self, selector: str, context: Dict) -> Dict:
        """验证CSS选择器"""
        result = {'valid': True, 'issues': []}
        
        if not selector or not selector.strip():
            result['valid'] = False
            result['issues'].append({
                'severity': 'error',
                'type': 'empty_selector',
                'message': 'CSS选择器不能为空',
                'suggestion': '请提供有效的CSS选择器'
            })
            return result
        
        try:
            elements = self.soup.select(selector)
        except Exception as e:
            result['valid'] = False
            result['issues'].append({
                'severity': 'error',
                'type': 'syntax_error',
                'message': f'CSS选择器语法错误: {str(e)}',
                'suggestion': '请检查选择器语法'
            })
            return result
        
        if not elements:
            result['issues'].append({
                'severity': 'warning',
                'type': 'no_match',
                'message': '选择器未匹配到任何元素',
                'suggestion': '请检查选择器是否正确'
            })
        
        return result
    
    def _validate_xpath(self, xpath: str, context: Dict) -> Dict:
        """验证XPath"""
        result = {'valid': True, 'issues': []}
        
        if not xpath or not xpath.strip():
            result['valid'] = False
            result['issues'].append({
                'severity': 'error',
                'type': 'empty_xpath',
                'message': 'XPath不能为空',
                'suggestion': '请提供有效的XPath表达式'
            })
            return result
        
        try:
            elements = self.lxml_doc.xpath(xpath)
        except Exception as e:
            result['valid'] = False
            result['issues'].append({
                'severity': 'error',
                'type': 'syntax_error',
                'message': f'XPath语法错误: {str(e)}',
                'suggestion': '请检查XPath语法'
            })
            return result
        
        if not elements:
            result['issues'].append({
                'severity': 'warning',
                'type': 'no_match',
                'message': 'XPath未匹配到任何元素',
                'suggestion': '请检查XPath是否正确'
            })
        
        return result
    
    def _validate_regex(self, pattern: str, context: Dict) -> Dict:
        """验证正则表达式"""
        result = {'valid': True, 'issues': []}
        
        if not pattern or not pattern.strip():
            result['valid'] = False
            result['issues'].append({
                'severity': 'error',
                'type': 'empty_pattern',
                'message': '正则表达式不能为空',
                'suggestion': '请提供有效的正则表达式'
            })
            return result
        
        try:
            re.compile(pattern)
        except Exception as e:
            result['valid'] = False
            result['issues'].append({
                'severity': 'error',
                'type': 'syntax_error',
                'message': f'正则表达式语法错误: {str(e)}',
                'suggestion': '请检查正则表达式语法'
            })
            return result
        
        matches = re.findall(pattern, self.html)
        if not matches:
            result['issues'].append({
                'severity': 'warning',
                'type': 'no_match',
                'message': '正则表达式未匹配到任何内容',
                'suggestion': '请检查正则表达式是否正确'
            })
        
        return result
    
    def validate_book_source(self, book_source: Dict) -> Dict[str, Any]:
        """验证整个书源配置"""
        results = {
            'valid': True,
            'issues': [],
            'rule_results': {}
        }
        
        required_fields = ['bookSourceName', 'bookSourceUrl', 'searchUrl']
        for field in required_fields:
            if field not in book_source or not book_source[field]:
                results['valid'] = False
                results['issues'].append({
                    'severity': 'error',
                    'type': 'missing_field',
                    'message': f'缺少必填字段: {field}',
                    'location': f'bookSource.{field}'
                })
        
        if 'ruleSearch' in book_source:
            search_rules = book_source['ruleSearch']
            for rule_name in ['bookList', 'name', 'bookUrl']:
                if rule_name not in search_rules or not search_rules[rule_name]:
                    results['valid'] = False
                    results['issues'].append({
                        'severity': 'error',
                        'type': 'missing_rule',
                        'message': f'搜索规则缺少必填字段: {rule_name}',
                        'location': f'ruleSearch.{rule_name}'
                    })
        
        return results


def validate_rule(html: str, rule_type: str, rule_value: str) -> Dict[str, Any]:
    """验证规则的便捷函数"""
    validator = RuleValidator(html)
    return validator.validate_rule(rule_type, rule_value)


def validate_book_source(html: str, book_source: Dict) -> Dict[str, Any]:
    """验证书源的便捷函数"""
    validator = RuleValidator(html)
    return validator.validate_book_source(book_source)
