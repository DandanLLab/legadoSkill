"""
WebBook - Web Content Fetcher
Translated from Kotlin: io.legado.app.model.webBook.WebBook

Handles HTTP requests and content fetching for book sources.
"""

import re
import json
import time
from typing import Any, Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse, urlencode, quote
from dataclasses import dataclass
import requests
from bs4 import BeautifulSoup

from .book_source import BookSource
from .analyze_rule import AnalyzeRule


@dataclass
class AnalyzeUrl:
    url: str
    method: str = "GET"
    body: Optional[str] = None
    headers: Dict[str, str] = None
    charset: str = "utf-8"
    
    def __post_init__(self):
        if self.headers is None:
            self.headers = {}


@dataclass
class StrResponse:
    body: str
    url: str
    status_code: int
    headers: Dict[str, str]
    

class WebBook:
    """
    WebBook class for fetching and parsing web content.
    Implements the same functionality as Legado's WebBook class.
    """
    
    DEFAULT_HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    def __init__(self, book_source: BookSource):
        self.book_source = book_source
        self.session = requests.Session()
        self._init_session()
    
    def _init_session(self):
        self.session.headers.update(self.DEFAULT_HEADERS)
        
        if self.book_source.header:
            try:
                headers = json.loads(self.book_source.header)
                self.session.headers.update(headers)
            except:
                pass
    
    def build_search_url(self, keyword: str) -> AnalyzeUrl:
        search_url = self.book_source.searchUrl
        if not search_url:
            raise ValueError("未配置searchUrl")
        
        base_url = self.book_source.bookSourceUrl
        
        if ',' in search_url:
            parts = search_url.split(',', 1)
            url_path = parts[0]
            options = {}
            
            if len(parts) > 1:
                try:
                    options = json.loads(parts[1])
                except:
                    pass
            
            charset = options.get('charset', 'utf-8')
            
            # 根据charset编码关键词
            if charset.lower() in ('gbk', 'gb2312', 'gb18030'):
                encoded_keyword = quote(keyword, safe='', encoding='gbk')
            else:
                encoded_keyword = quote(keyword, safe='', encoding='utf-8')
            
            url = urljoin(base_url, url_path)
            url = url.replace('{{key}}', encoded_keyword)
            
            method = options.get('method', 'GET')
            body = options.get('body', '')
            if body:
                body = body.replace('{{key}}', encoded_keyword)
            
            headers = options.get('headers', {})
            
            return AnalyzeUrl(
                url=url,
                method=method,
                body=body,
                headers=headers,
                charset=charset
            )
        else:
            url = urljoin(base_url, search_url.replace('{{key}}', quote(keyword, safe='', encoding='utf-8')))
            return AnalyzeUrl(url=url)
    
    def get_str_response(self, analyze_url: AnalyzeUrl) -> StrResponse:
        headers = dict(self.session.headers)
        headers.update(analyze_url.headers)
        
        try:
            if analyze_url.method.upper() == 'POST':
                body = analyze_url.body
                if body and analyze_url.charset.lower() in ('gbk', 'gb2312'):
                    body = body.encode('gbk')
                response = self.session.post(
                    analyze_url.url, 
                    data=body, 
                    headers=headers, 
                    timeout=30,
                    allow_redirects=True
                )
            else:
                response = self.session.get(
                    analyze_url.url, 
                    headers=headers, 
                    timeout=30,
                    allow_redirects=True
                )
            
            content = response.content
            
            charset = analyze_url.charset.lower()
            if charset in ('gbk', 'gb2312', 'gb18030'):
                try:
                    body = content.decode('gbk', errors='replace')
                except:
                    body = content.decode('utf-8', errors='replace')
            else:
                try:
                    content_type = response.headers.get('Content-Type', '')
                    if 'charset=gb' in content_type.lower():
                        body = content.decode('gbk', errors='replace')
                    else:
                        body = content.decode('utf-8', errors='replace')
                except:
                    body = response.text
            
            return StrResponse(
                body=body,
                url=response.url,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
        except Exception as e:
            return StrResponse(
                body="",
                url=analyze_url.url,
                status_code=0,
                headers={}
            )
    
    def search_book(self, keyword: str) -> List[Dict[str, Any]]:
        analyze_url = self.build_search_url(keyword)
        response = self.get_str_response(analyze_url)
        
        if not response.body:
            return []
        
        rule = self.book_source.ruleSearch
        if not rule or not rule.bookList:
            return []
        
        analyzer = AnalyzeRule(response.body, response.url)
        book_elements = analyzer.get_elements(rule.bookList)
        
        results = []
        for elem in book_elements:
            item = {}
            item_analyzer = AnalyzeRule(elem, response.url)
            
            if rule.name:
                item['name'] = item_analyzer.get_string(rule.name)
            if rule.author:
                item['author'] = item_analyzer.get_string(rule.author)
            if rule.bookUrl:
                item['bookUrl'] = item_analyzer.get_string(rule.bookUrl, is_url=True)
            if rule.coverUrl:
                item['coverUrl'] = item_analyzer.get_string(rule.coverUrl, is_url=True)
            if rule.intro:
                item['intro'] = item_analyzer.get_string(rule.intro)
            if rule.kind:
                item['kind'] = item_analyzer.get_string(rule.kind)
            if rule.lastChapter:
                item['lastChapter'] = item_analyzer.get_string(rule.lastChapter)
            
            if item.get('name') and item.get('bookUrl'):
                results.append(item)
        
        return results
    
    def get_book_info(self, book_url: str) -> Dict[str, Any]:
        analyze_url = AnalyzeUrl(url=book_url)
        response = self.get_str_response(analyze_url)
        
        if not response.body:
            return {}
        
        rule = self.book_source.ruleBookInfo
        if not rule:
            return {}
        
        analyzer = AnalyzeRule(response.body, response.url)
        info = {}
        
        if rule.name:
            info['name'] = analyzer.get_string(rule.name)
        if rule.author:
            info['author'] = analyzer.get_string(rule.author)
        if rule.coverUrl:
            info['coverUrl'] = analyzer.get_string(rule.coverUrl, is_url=True)
        if rule.intro:
            info['intro'] = analyzer.get_string(rule.intro)
        if rule.kind:
            info['kind'] = analyzer.get_string(rule.kind)
        if rule.lastChapter:
            info['lastChapter'] = analyzer.get_string(rule.lastChapter)
        if rule.tocUrl:
            info['tocUrl'] = analyzer.get_string(rule.tocUrl, is_url=True)
        if rule.wordCount:
            info['wordCount'] = analyzer.get_string(rule.wordCount)
        
        return info
    
    def get_chapter_list(self, toc_url: str) -> List[Dict[str, Any]]:
        analyze_url = AnalyzeUrl(url=toc_url)
        response = self.get_str_response(analyze_url)
        
        if not response.body:
            return []
        
        rule = self.book_source.ruleToc
        if not rule or not rule.chapterList:
            return []
        
        analyzer = AnalyzeRule(response.body, response.url)
        chapter_elements = analyzer.get_elements(rule.chapterList)
        
        chapters = []
        for elem in chapter_elements:
            chapter = {}
            item_analyzer = AnalyzeRule(elem, response.url)
            
            if rule.chapterName:
                chapter['title'] = item_analyzer.get_string(rule.chapterName)
            if rule.chapterUrl:
                chapter['url'] = item_analyzer.get_string(rule.chapterUrl, is_url=True)
            
            if chapter.get('title') and chapter.get('url'):
                chapters.append(chapter)
        
        return chapters
    
    def get_content(self, chapter_url: str) -> Dict[str, Any]:
        analyze_url = AnalyzeUrl(url=chapter_url)
        response = self.get_str_response(analyze_url)
        
        if not response.body:
            return {}
        
        rule = self.book_source.ruleContent
        if not rule or not rule.content:
            return {}
        
        analyzer = AnalyzeRule(response.body, response.url)
        content = {}
        
        text = analyzer.get_string(rule.content)
        
        if rule.replaceRegex:
            try:
                text = re.sub(rule.replaceRegex, '', text)
            except:
                pass
        
        content['text'] = text
        
        if rule.nextContentUrl:
            content['nextUrl'] = analyzer.get_string(rule.nextContentUrl, is_url=True)
        
        return content
