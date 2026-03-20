"""
AnalyzeUrl - Python Implementation
Translated from Kotlin: io.legado.app.model.analyzeRule.AnalyzeUrl

Handles URL construction, HTTP requests, and response processing.
Based on real Legado Kotlin source code.
"""

import re
import json
import time
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse, urlencode, quote, unquote
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


@dataclass
class StrResponse:
    url: str
    body: str
    status_code: int
    headers: Dict[str, str]
    raw: Any = None


class AnalyzeUrl:
    """
    Python implementation of Legado's AnalyzeUrl class.
    Handles URL construction and HTTP requests.
    
    Based on: io.legado.app.model.analyzeRule.AnalyzeUrl
    """
    
    PARAM_PATTERN = re.compile(r'\{\{([^}]+)\}\}')
    DEFAULT_TIMEOUT = 30
    DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    def __init__(
        self,
        m_url: str,
        key: str = None,
        page: int = None,
        base_url: str = "",
        source: Any = None,
        rule_data: Any = None,
        header_map: Dict[str, str] = None,
    ):
        self.m_url = m_url
        self.key = key or ""
        self.page = page or 1
        self.base_url = base_url
        self.source = source
        self.rule_data = rule_data
        
        self.url = ""
        self.rule_url = ""
        self.header_map = header_map or {}
        self.body: Optional[str] = None
        self.method = "GET"
        self.charset = "utf-8"
        self.type: Optional[str] = None
        self.url_no_query = ""
        self.proxy: Optional[str] = None
        self.retry = 0
        self.use_web_view = False
        self.web_js: Optional[str] = None
        
        self._session = self._create_session()
        self._init_url()
    
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        default_headers = {
            'User-Agent': self.DEFAULT_USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        }
        
        session.headers.update(default_headers)
        
        if self.header_map:
            session.headers.update(self.header_map)
        
        return session
    
    def _init_url(self):
        self.rule_url = self.m_url
        
        url = self.m_url
        url = self._replace_params(url)
        
        if ',' in url:
            parts = url.split(',', 1)
            url_path = parts[0]
            
            if len(parts) > 1:
                try:
                    options = json.loads(parts[1])
                    self._parse_options(options)
                except:
                    pass
            
            url = url_path
        
        if self.base_url and not url.startswith('http'):
            url = urljoin(self.base_url, url)
        
        self.url = url
        self.url_no_query = self._get_url_no_query(url)
    
    def _replace_params(self, url: str) -> str:
        url = url.replace('{{key}}', quote(self.key) if self.key else "")
        url = url.replace('{{page}}', str(self.page))
        url = url.replace('{{keyNoEncode}}', self.key)
        
        def replace_match(match):
            param = match.group(1)
            if param == 'key':
                return quote(self.key) if self.key else ""
            elif param == 'page':
                return str(self.page)
            return match.group(0)
        
        url = self.PARAM_PATTERN.sub(replace_match, url)
        
        return url
    
    def _parse_options(self, options: Dict[str, Any]):
        self.method = options.get('method', 'GET').upper()
        self.body = options.get('body')
        self.charset = options.get('charset', 'utf-8')
        
        if 'headers' in options:
            headers = options['headers']
            if isinstance(headers, str):
                try:
                    headers = json.loads(headers)
                except:
                    headers = {}
            if isinstance(headers, dict):
                self.header_map.update(headers)
        
        self.type = options.get('type')
        self.proxy = options.get('proxy')
        self.web_js = options.get('webJs')
    
    def _get_url_no_query(self, url: str) -> str:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    def get_str_response(self, timeout: int = None) -> StrResponse:
        timeout = timeout or self.DEFAULT_TIMEOUT
        
        try:
            if self.method == 'POST':
                if self.body:
                    if self.charset.lower() in ('gbk', 'gb2312'):
                        body_bytes = self.body.encode('gbk')
                    else:
                        body_bytes = self.body.encode('utf-8')
                    
                    response = self._session.post(
                        self.url,
                        data=body_bytes,
                        headers=self.header_map,
                        timeout=timeout,
                        allow_redirects=True,
                    )
                else:
                    response = self._session.post(
                        self.url,
                        headers=self.header_map,
                        timeout=timeout,
                        allow_redirects=True,
                    )
            else:
                response = self._session.get(
                    self.url,
                    headers=self.header_map,
                    timeout=timeout,
                    allow_redirects=True,
                )
            
            if self.charset.lower() in ('gbk', 'gb2312'):
                body = response.content.decode('gbk', errors='replace')
            else:
                body = response.text
            
            return StrResponse(
                url=response.url,
                body=body,
                status_code=response.status_code,
                headers=dict(response.headers),
                raw=response,
            )
            
        except requests.exceptions.Timeout:
            return StrResponse(
                url=self.url,
                body="",
                status_code=0,
                headers={},
                raw=None,
            )
        except requests.exceptions.ConnectionError:
            return StrResponse(
                url=self.url,
                body="",
                status_code=0,
                headers={},
                raw=None,
            )
        except Exception as e:
            return StrResponse(
                url=self.url,
                body="",
                status_code=0,
                headers={},
                raw=None,
            )
    
    def get_str_response_await(self, timeout: int = None) -> StrResponse:
        return self.get_str_response(timeout)
    
    def get_err_str_response(self, throwable: Exception) -> StrResponse:
        return StrResponse(
            url=self.url,
            body=str(throwable),
            status_code=500,
            headers={},
            raw=None,
        )
    
    def eval_js(self, js_code: str, response: StrResponse) -> Any:
        return f"[JS执行: {js_code[:50]}...]"
    
    def get_url(self) -> str:
        return self.url
    
    def get_header_map(self) -> Dict[str, str]:
        return self.header_map
    
    def get_body(self) -> Optional[str]:
        return self.body
    
    def get_method(self) -> str:
        return self.method
    
    def get_charset(self) -> str:
        return self.charset


def build_analyze_url(
    url: str,
    key: str = None,
    page: int = None,
    base_url: str = "",
    source: Any = None,
    headers: Dict[str, str] = None,
) -> AnalyzeUrl:
    """
    Build an AnalyzeUrl instance with common parameters.
    
    Args:
        url: URL string (may contain options after comma)
        key: Search keyword
        page: Page number
        base_url: Base URL for relative URLs
        source: Book source object
        headers: Additional headers
    
    Returns:
        AnalyzeUrl instance
    """
    return AnalyzeUrl(
        m_url=url,
        key=key,
        page=page,
        base_url=base_url,
        source=source,
        header_map=headers,
    )


def fetch_url(
    url: str,
    method: str = "GET",
    body: str = None,
    headers: Dict[str, str] = None,
    charset: str = "utf-8",
    timeout: int = 30,
) -> StrResponse:
    """
    Fetch URL and return response.
    
    Args:
        url: URL to fetch
        method: HTTP method
        body: Request body (for POST)
        headers: Request headers
        charset: Character encoding
        timeout: Request timeout
    
    Returns:
        StrResponse object
    """
    analyze_url = AnalyzeUrl(
        m_url=f"{url},{json.dumps({'method': method, 'body': body, 'charset': charset, 'headers': headers or {}})}",
    )
    return analyze_url.get_str_response(timeout)
