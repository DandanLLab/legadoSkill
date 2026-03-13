"""
智能请求工具
支持各种HTTP请求方法，确保用正确的方式获取真实内容
"""

import requests
import json
import re
import chardet
from typing import Dict, List, Any, Optional, Union
from urllib.parse import urlencode


class SmartRequest:
    """智能请求工具"""
    
    def __init__(self, timeout: int = 30, max_retries: int = 3):
        self.timeout = timeout
        self.max_retries = max_retries
        
        self.default_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
    
    def _detect_encoding(self, response: requests.Response, charset: Optional[str] = None) -> str:
        """
        智能检测响应编码
        
        优先级：
        1. 用户指定的 charset 参数
        2. HTTP Content-Type header 中的 charset
        3. HTML meta 标签中的 charset
        4. chardet 库检测
        5. 默认 utf-8
        """
        if charset:
            charset_lower = charset.lower()
            if charset_lower in ['gbk', 'gb2312', 'gb18030']:
                return 'gbk'
            elif charset_lower in ['utf-8', 'utf8']:
                return 'utf-8'
            else:
                return charset_lower
        
        content_type = response.headers.get('Content-Type', '')
        if 'charset=' in content_type:
            match = re.search(r'charset=([^\s;]+)', content_type, re.IGNORECASE)
            if match:
                detected = match.group(1).strip('"\'').lower()
                if detected in ['gbk', 'gb2312', 'gb18030']:
                    return 'gbk'
                elif detected in ['utf-8', 'utf8']:
                    return 'utf-8'
                return detected
        
        try:
            content_preview = response.content[:2048].decode('latin-1', errors='ignore')
            meta_patterns = [
                r'<meta\s+charset=["\']?([^"\'>\s]+)',
                r'<meta\s+http-equiv=["\']?content-type["\']?\s+content=["\']?[^"\']*charset=([^"\'>\s;]+)',
            ]
            for pattern in meta_patterns:
                match = re.search(pattern, content_preview, re.IGNORECASE)
                if match:
                    detected = match.group(1).lower()
                    if detected in ['gbk', 'gb2312', 'gb18030']:
                        return 'gbk'
                    elif detected in ['utf-8', 'utf8']:
                        return 'utf-8'
                    return detected
        except Exception:
            pass
        
        try:
            detected = chardet.detect(response.content)
            if detected and detected.get('encoding'):
                encoding = detected['encoding'].lower()
                confidence = detected.get('confidence', 0)
                if confidence > 0.7:
                    if encoding in ['gbk', 'gb2312', 'gb18030']:
                        return 'gbk'
                    elif encoding in ['utf-8', 'utf8']:
                        return 'utf-8'
                    return encoding
        except Exception:
            pass
        
        return 'utf-8'
    
    def fetch(
        self,
        url: str,
        method: str = 'GET',
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict, str, bytes]] = None,
        json_data: Optional[Dict] = None,
        headers: Optional[Dict[str, str]] = None,
        cookies: Optional[Dict[str, str]] = None,
        allow_redirects: bool = True,
        verify_ssl: bool = True,
        charset: Optional[str] = None,
        url_charset: Optional[str] = None,
        encoded_data: Optional[str] = None,
        encoded_params: Optional[str] = None
    ) -> Dict[str, Any]:
        """发送HTTP请求（支持所有方法）"""
        final_headers = self.default_headers.copy()
        if headers:
            final_headers.update(headers)
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = requests.request(
                    method=method.upper(),
                    url=url,
                    params=params,
                    data=data,
                    json=json_data,
                    headers=final_headers,
                    cookies=cookies,
                    allow_redirects=allow_redirects,
                    verify=verify_ssl,
                    timeout=self.timeout
                )
                
                detected_encoding = self._detect_encoding(response, charset)
                
                try:
                    html_text = response.content.decode(detected_encoding, errors='replace')
                except (UnicodeDecodeError, LookupError):
                    html_text = response.content.decode('utf-8', errors='replace')
                    detected_encoding = 'utf-8'
                
                return {
                    'success': True,
                    'status_code': response.status_code,
                    'url': response.url,
                    'method': method.upper(),
                    'headers': dict(response.headers),
                    'cookies': dict(response.cookies),
                    'encoding': detected_encoding,
                    'html': html_text,
                    'content': response.content,
                    'size': len(response.content),
                    'redirect_count': len(response.history),
                    'final_url': response.url,
                    'is_real': True
                }
                
            except requests.exceptions.Timeout:
                last_error = f"请求超时（{self.timeout}秒）"
            except requests.exceptions.ConnectionError:
                last_error = "连接错误"
            except requests.exceptions.SSLError as e:
                last_error = f"SSL错误: {str(e)}"
            except Exception as e:
                last_error = str(e)
        
        return {
            'success': False,
            'error': last_error,
            'url': url,
            'method': method.upper()
        }


def smart_fetch_html(
    url: str,
    method: str = 'GET',
    body: str = None,
    headers: Dict[str, str] = None,
    charset: str = None,
    timeout: int = 30
) -> Dict[str, Any]:
    """
    智能获取HTML内容的便捷函数
    
    参数:
        url: 目标URL
        method: HTTP方法 (GET/POST)
        body: POST请求体
        headers: 自定义请求头
        charset: 指定编码
        timeout: 超时时间
    
    返回:
        包含HTML内容和元数据的字典
    """
    requester = SmartRequest(timeout=timeout)
    
    data = None
    if method.upper() == 'POST' and body:
        data = body
    
    return requester.fetch(
        url=url,
        method=method,
        data=data,
        headers=headers,
        charset=charset
    )
