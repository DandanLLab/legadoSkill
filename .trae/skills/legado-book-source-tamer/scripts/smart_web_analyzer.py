"""
智能网站分析器
自动分析网站结构，智能构建请求，获取正确的列表内容
"""

import re
import json
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode, urljoin as _urljoin
from bs4 import BeautifulSoup
import requests


def urljoin(base: str, url: str) -> str:
    """简单的URL拼接"""
    return _urljoin(base, url)


class SmartWebAnalyzer:
    """智能网站分析器"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def analyze(self, url: str) -> Dict[str, Any]:
        """分析网站结构"""
        try:
            response = requests.get(url, headers=self.default_headers, timeout=self.timeout)
            response.raise_for_status()
            html = response.text
            
            soup = BeautifulSoup(html, 'html.parser')
            
            analysis = {
                'url': url,
                'charset': self._detect_charset(response, html),
                'search_info': self._analyze_search_form(soup, url),
                'pagination_info': self._analyze_pagination(soup, url),
                'list_structure': self._analyze_list_structure(soup),
                'ajax_info': self._analyze_ajax(soup),
                'security_info': self._analyze_security(soup, html)
            }
            
            return analysis
            
        except Exception as e:
            return {
                'url': url,
                'error': str(e)
            }
    
    def _detect_charset(self, response, html: str) -> str:
        """检测编码"""
        content_type = response.headers.get('Content-Type', '')
        if 'charset=' in content_type:
            match = re.search(r'charset=([^\s;]+)', content_type, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        
        match = re.search(r'<meta\s+charset=["\']?([^"\'>\s]+)', html, re.IGNORECASE)
        if match:
            return match.group(1).lower()
        
        return 'utf-8'
    
    def _analyze_search_form(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """分析搜索表单"""
        forms = soup.find_all('form')
        search_forms = []
        
        for form in forms:
            form_info = {
                'action': urljoin(base_url, str(form.get('action', ''))),
                'method': str(form.get('method', 'GET')).upper(),
                'inputs': []
            }
            
            inputs = form.find_all('input')
            for inp in inputs:
                input_info = {
                    'type': inp.get('type', 'text'),
                    'name': inp.get('name', ''),
                    'id': inp.get('id', ''),
                    'placeholder': inp.get('placeholder', ''),
                    'value': inp.get('value', '')
                }
                if input_info['name']:
                    form_info['inputs'].append(input_info)
            
            is_search = False
            search_keywords = ['search', 'query', 'keyword', 'q']
            for keyword in search_keywords:
                if keyword in form_info['action'].lower():
                    is_search = True
                    break
                for inp in form_info['inputs']:
                    if keyword in inp['name'].lower() or keyword in inp.get('placeholder', '').lower():
                        is_search = True
                        break
                if is_search:
                    break
            
            if is_search:
                search_forms.append(form_info)
        
        return {
            'found': len(search_forms) > 0,
            'forms': search_forms
        }
    
    def _analyze_pagination(self, soup: BeautifulSoup, base_url: str) -> Dict:
        """分析分页信息"""
        pagination_info = {
            'found': False,
            'type': None,
            'page_param': None,
            'selectors': [],
            'total_pages': None
        }
        
        pagination_keywords = ['page', 'pagination', 'pager', 'nav', 'next', 'prev', '上一页', '下一页']
        
        for keyword in pagination_keywords:
            by_class = soup.find_all(class_=lambda x: x and keyword in str(x).lower())
            by_id = soup.find_all(id=lambda x: x and keyword in str(x).lower())
            
            if by_class or by_id:
                pagination_info['found'] = True
                for elem in by_class[:3]:
                    class_name = ' '.join(elem.get('class', []))
                    pagination_info['selectors'].append(f".{class_name}")
                for elem in by_id[:3]:
                    elem_id = elem.get('id')
                    pagination_info['selectors'].append(f"#{elem_id}")
                break
        
        links = soup.find_all('a', href=True)
        page_pattern = re.compile(r'[?&](p|page|offset)=(\d+)', re.IGNORECASE)
        
        for link in links:
            href = link.get('href', '')
            match = page_pattern.search(href)
            if match:
                pagination_info['found'] = True
                pagination_info['type'] = 'url_param'
                pagination_info['page_param'] = match.group(1)
                break
        
        return pagination_info
    
    def _analyze_list_structure(self, soup: BeautifulSoup) -> Dict:
        """分析列表结构"""
        list_selectors = []
        list_keywords = ['list', 'item', 'book', 'article', 'post', 'content', 'card']
        
        for keyword in list_keywords:
            by_class = soup.find_all(class_=lambda x: x and keyword in str(x).lower())
            for elem in by_class[:5]:
                class_name = ' '.join(elem.get('class', []))
                children = elem.find_all(recursive=False)
                if len(children) >= 3:
                    list_selectors.append(f".{class_name}")
        
        for tag in ['ul', 'ol']:
            lists = soup.find_all(tag)
            for lst in lists[:3]:
                items = lst.find_all('li', recursive=False)
                if len(items) >= 3:
                    if lst.get('class'):
                        class_name = ' '.join(lst.get('class', []))
                        list_selectors.append(f"{tag}.{class_name}")
                    elif lst.get('id'):
                        list_selectors.append(f"{tag}#{lst.get('id')}")
                    else:
                        list_selectors.append(tag)
        
        return {
            'list_selectors': list_selectors[:10],
            'recommended': list_selectors[0] if list_selectors else None
        }
    
    def _analyze_ajax(self, soup: BeautifulSoup) -> Dict:
        """分析AJAX请求"""
        ajax_info = {
            'found': False,
            'endpoints': []
        }
        
        scripts = soup.find_all('script')
        api_patterns = [
            re.compile(r'url\s*:\s*["\']([^"\']+)["\']', re.IGNORECASE),
            re.compile(r'fetch\s*\(\s*["\']([^"\']+)["\']', re.IGNORECASE),
            re.compile(r'\$\.ajax\s*\(\s*{[^}]*url\s*:\s*["\']([^"\']+)["\']', re.IGNORECASE),
        ]
        
        for script in scripts:
            if script.string:
                for pattern in api_patterns:
                    matches = pattern.findall(script.string)
                    for match in matches:
                        if '/api/' in match or 'ajax' in match.lower():
                            ajax_info['found'] = True
                            ajax_info['endpoints'].append(match)
        
        return ajax_info
    
    def _analyze_security(self, soup: BeautifulSoup, html: str) -> Dict:
        """分析安全机制"""
        security_info = {
            'cloudflare': False,
            'login_required': False,
            'captcha': False
        }
        
        cf_indicators = ['cloudflare', 'cf-', 'ray id', 'checking your browser']
        for indicator in cf_indicators:
            if indicator in html.lower():
                security_info['cloudflare'] = True
                break
        
        login_indicators = ['login', 'sign in', '登录', '登陆']
        forms = soup.find_all('form')
        for form in forms:
            form_text = form.get_text().lower()
            for indicator in login_indicators:
                if indicator in form_text:
                    security_info['login_required'] = True
                    break
        
        captcha_indicators = ['captcha', '验证码', 'recaptcha', 'hcaptcha']
        for indicator in captcha_indicators:
            if indicator in html.lower():
                security_info['captcha'] = True
                break
        
        return security_info


def smart_analyze_website(url: str) -> Dict[str, Any]:
    """分析网站的便捷函数"""
    analyzer = SmartWebAnalyzer()
    return analyzer.analyze(url)
