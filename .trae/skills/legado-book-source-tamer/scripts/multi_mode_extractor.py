"""
多模式提取引擎
支持CSS选择器、XPath、正则表达式、JSONPath等多种提取方式
"""

import re
import json
from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass
from bs4 import BeautifulSoup
from lxml import etree, html as lxml_html


@dataclass
class ExtractionResult:
    """提取结果"""
    content: Union[str, List[str]]
    method: str
    selector: str
    success: bool
    confidence: float
    error_message: Optional[str] = None
    sample_items: List[str] = None
    extracted_count: int = 0


class MultiModeExtractor:
    """多模式提取器"""
    
    def __init__(self, html: str):
        self.html = html
        self.soup = BeautifulSoup(html, 'html.parser')
        self.lxml_doc = lxml_html.fromstring(html)
        self.results = {}
    
    def extract(
        self,
        selector: str,
        method: str = 'auto',
        extract_attr: str = None,
        extract_all: bool = True
    ) -> ExtractionResult:
        """提取内容"""
        if method == 'auto':
            method = self._detect_method(selector)
        
        if method == 'css':
            return self._extract_css(selector, extract_attr, extract_all)
        elif method == 'xpath':
            return self._extract_xpath(selector, extract_attr, extract_all)
        elif method == 'regex':
            return self._extract_regex(selector, extract_all)
        elif method == 'json':
            return self._extract_json(selector, extract_attr)
        
        return ExtractionResult(
            content='',
            method=method,
            selector=selector,
            success=False,
            confidence=0.0,
            error_message=f'不支持的提取方法: {method}',
            extracted_count=0
        )
    
    def _detect_method(self, selector: str) -> str:
        """自动检测提取方法"""
        if selector.startswith('//') or selector.startswith('/'):
            return 'xpath'
        if selector.startswith('regex:') or selector.startswith('re:'):
            return 'regex'
        if selector.startswith('json:') or selector.startswith('jsonPath:'):
            return 'json'
        return 'css'
    
    def _extract_css(
        self,
        selector: str,
        extract_attr: str = None,
        extract_all: bool = True
    ) -> ExtractionResult:
        """使用CSS选择器提取"""
        try:
            if extract_all:
                elements = self.soup.select(selector)
            else:
                element = self.soup.select_one(selector)
                elements = [element] if element else []
            
            if not elements:
                return ExtractionResult(
                    content=[],
                    method='css',
                    selector=selector,
                    success=True,
                    confidence=0.0,
                    extracted_count=0
                )

            if extract_attr:
                contents = [elem.get(extract_attr, '') for elem in elements if elem.get(extract_attr)]
            else:
                contents = [elem.get_text(strip=True) for elem in elements]

            contents = [c for c in contents if c]
            extracted_count = len(contents)

            return ExtractionResult(
                content=contents if extract_all else (contents[0] if contents else ''),
                method='css',
                selector=selector,
                success=True,
                confidence=min(extracted_count / max(1, len(elements)), 1.0),
                sample_items=contents[:5],
                extracted_count=extracted_count
            )
            
        except Exception as e:
            return ExtractionResult(
                content=[],
                method='css',
                selector=selector,
                success=False,
                confidence=0.0,
                error_message=str(e)
            )
    
    def _extract_xpath(
        self,
        selector: str,
        extract_attr: str = None,
        extract_all: bool = True
    ) -> ExtractionResult:
        """使用XPath提取"""
        try:
            if extract_all:
                elements = self.lxml_doc.xpath(selector)
            else:
                elements = self.lxml_doc.xpath(f'{selector}[1]')
            
            if not elements:
                return ExtractionResult(
                    content=[],
                    method='xpath',
                    selector=selector,
                    success=True,
                    confidence=0.0,
                    extracted_count=0
                )

            if extract_attr:
                contents = [elem.get(extract_attr, '') for elem in elements if hasattr(elem, 'get')]
            else:
                contents = [elem.text_content().strip() for elem in elements if hasattr(elem, 'text_content')]

            contents = [c for c in contents if c]
            extracted_count = len(contents)

            return ExtractionResult(
                content=contents if extract_all else (contents[0] if contents else ''),
                method='xpath',
                selector=selector,
                success=True,
                confidence=min(extracted_count / max(1, len(elements)), 1.0),
                sample_items=contents[:5],
                extracted_count=extracted_count
            )
            
        except Exception as e:
            return ExtractionResult(
                content=[],
                method='xpath',
                selector=selector,
                success=False,
                confidence=0.0,
                error_message=str(e)
            )
    
    def _extract_regex(
        self,
        selector: str,
        extract_all: bool = True
    ) -> ExtractionResult:
        """使用正则表达式提取"""
        try:
            pattern = selector.replace('regex:', '').replace('re:', '')
            matches = re.findall(pattern, self.html)
            
            if not matches:
                return ExtractionResult(
                    content=[],
                    method='regex',
                    selector=pattern,
                    success=True,
                    confidence=0.0,
                    extracted_count=0
                )

            if extract_all:
                contents = matches
                extracted_count = len(matches) if isinstance(matches, list) else 1
            else:
                contents = matches[0]
                extracted_count = 1

            return ExtractionResult(
                content=contents,
                method='regex',
                selector=pattern,
                success=True,
                confidence=1.0,
                sample_items=matches[:5] if isinstance(matches, list) else [str(matches)],
                extracted_count=extracted_count
            )
            
        except Exception as e:
            return ExtractionResult(
                content=[],
                method='regex',
                selector=selector,
                success=False,
                confidence=0.0,
                error_message=str(e)
            )
    
    def _extract_json(
        self,
        selector: str,
        extract_attr: str = None
    ) -> ExtractionResult:
        """使用JSONPath提取"""
        try:
            import jsonpath_ng
            pattern = selector.replace('json:', '').replace('jsonPath:', '')
            
            try:
                data = json.loads(self.html)
            except:
                return ExtractionResult(
                    content='',
                    method='json',
                    selector=selector,
                    success=False,
                    confidence=0.0,
                    error_message='HTML不是有效的JSON'
                )
            
            jsonpath_expr = jsonpath_ng.parse(pattern)
            matches = [match.value for match in jsonpath_expr.find(data)]
            
            if not matches:
                return ExtractionResult(
                    content=[],
                    method='json',
                    selector=pattern,
                    success=True,
                    confidence=0.0,
                    extracted_count=0
                )
            
            contents = [str(m) for m in matches]
            extracted_count = len(contents)
            
            return ExtractionResult(
                content=contents,
                method='json',
                selector=pattern,
                success=True,
                confidence=1.0,
                sample_items=contents[:5],
                extracted_count=extracted_count
            )
            
        except ImportError:
            return ExtractionResult(
                content='',
                method='json',
                selector=selector,
                success=False,
                confidence=0.0,
                error_message='需要安装 jsonpath_ng 库'
            )
        except Exception as e:
            return ExtractionResult(
                content='',
                method='json',
                selector=selector,
                success=False,
                confidence=0.0,
                error_message=str(e)
            )


def extract_content(html: str, selector: str, method: str = 'auto', extract_attr: str = None) -> ExtractionResult:
    """提取内容的便捷函数"""
    extractor = MultiModeExtractor(html)
    return extractor.extract(selector, method, extract_attr)
