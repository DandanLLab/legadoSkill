"""
Debug Engine - Real Book Source Testing
Provides comprehensive debugging capabilities for book sources
"""

import json
import re
import time
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from urllib.parse import urljoin, urlparse, urlencode
import requests
from bs4 import BeautifulSoup

from .analyze_rule import AnalyzeRule
from .book_source import BookSource, SearchRule, BookInfoRule, TocRule, ContentRule


@dataclass
class DebugResult:
    success: bool
    message: str
    data: Any = None
    error: Optional[str] = None
    duration_ms: float = 0
    steps: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class SearchResult:
    name: str = ""
    author: str = ""
    bookUrl: str = ""
    coverUrl: str = ""
    intro: str = ""
    kind: str = ""
    lastChapter: str = ""
    updateTime: str = ""
    wordCount: str = ""
    raw_data: Any = None  # 保存原始数据用于模板变量替换


@dataclass
class BookInfo:
    name: str = ""
    author: str = ""
    coverUrl: str = ""
    intro: str = ""
    kind: str = ""
    lastChapter: str = ""
    tocUrl: str = ""
    bookUrl: str = ""  # 添加bookUrl字段
    wordCount: str = ""
    updateTime: str = ""


@dataclass
class Chapter:
    title: str = ""
    url: str = ""
    isVip: bool = False
    isPay: bool = False


@dataclass
class Content:
    text: str = ""
    nextUrl: str = ""


class DebugEngine:
    """
    Real debugging engine for Legado book sources.
    Tests each rule step by step and provides detailed feedback.
    """
    
    def __init__(self, book_source: BookSource):
        self.book_source = book_source
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        })
        
        if book_source.header:
            try:
                headers = json.loads(book_source.header)
                self.session.headers.update(headers)
            except:
                pass
        
        self.debug_log: List[Dict[str, Any]] = []
        self.variables: Dict[str, str] = {}
        
        # 按照Legado源码处理bookSourceUrl中的#注释
        # 参考: AnalyzeUrl.kt 第131-132行
        # val urlMatcher = paramPattern.matcher(baseUrl)
        # if (urlMatcher.find()) baseUrl = baseUrl.substring(0, urlMatcher.start())
        # 但这里需要处理#注释
        self._clean_book_source_url()
    
    def _clean_book_source_url(self):
        """清理bookSourceUrl中的#注释"""
        url = self.book_source.bookSourceUrl
        if '#' in url:
            # 移除#及其后面的内容
            clean_url = url.split('#')[0].strip()
            self.log("初始化", f"清理bookSourceUrl: {url} -> {clean_url}")
            # 创建一个新的book_source对象，更新URL
            from dataclasses import replace
            self.book_source.bookSourceUrl = clean_url
    
    def log(self, step: str, message: str, data: Any = None, error: str = None, state: int = None):
        """
        记录调试日志
        
        参数:
            step: 步骤名称（如"搜索"、"详情"、"目录"、"正文"）
            message: 日志消息
            data: 附加数据
            error: 错误信息
            state: 日志状态（Legado中state=40表示HTML内容）
        """
        entry = {
            'step': step,
            'message': message,
            'timestamp': time.time(),
        }
        if data is not None:
            entry['data'] = data
        if error:
            entry['error'] = error
        if state is not None:
            entry['state'] = state
        self.debug_log.append(entry)
    
    def _build_search_url(self, keyword: str) -> Tuple[str, Dict[str, Any]]:
        from urllib.parse import quote
        import re
        
        search_url = self.book_source.searchUrl
        if not search_url:
            return "", {}
        
        base_url = self.book_source.bookSourceUrl
        
        # 使用Legado真实的paramPattern: 只在{前面切分
        # Pattern.compile("\\s*,\\s*(?=\\{)")
        param_pattern = re.compile(r'\s*,\s*(?=\{)')
        match = param_pattern.search(search_url)
        
        if match:
            url_path = search_url[:match.start()]
            option_str = search_url[match.end():]
            options = {}
            
            try:
                options = json.loads(option_str)
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
                body = body.replace('{{page}}', '1')
            
            return url, {
                'method': method,
                'body': body,
                'charset': charset,
                'headers': options.get('headers', {}),
            }
        else:
            encoded_keyword = quote(keyword, safe='', encoding='utf-8')
            url = urljoin(base_url, search_url.replace('{{key}}', encoded_keyword))
            return url, {'method': 'GET'}
    
    def _fetch_url(self, url: str, options: Dict[str, Any] = None) -> Tuple[str, int]:
        """
        发送HTTP请求获取内容
        
        按照阅读源码的实现：
        - HttpHelper.kt: OkHttpClient配置
        - DecompressInterceptor.kt: gzip/deflate解压
        - OkHttpUtils.kt: 响应解码
        - EncodingDetect.kt: 编码自动检测
        """
        import urllib.request
        import urllib.error
        import ssl
        import gzip
        import io
        
        options = options or {}
        method = options.get('method', 'GET')
        body = options.get('body')
        charset = options.get('charset', '')  # 书源指定的编码
        extra_headers = options.get('headers', {})
        
        # 创建SSL上下文 - 忽略证书验证
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # 构建请求
        body_data = body.encode(charset or 'utf-8') if body else None
        req = urllib.request.Request(url, data=body_data, method=method)
        
        # 设置请求头 - 按照阅读的HttpHelper.kt
        for key, value in self.session.headers.items():
            req.add_header(key, value)
        for key, value in extra_headers.items():
            req.add_header(key, value)
        
        # 按照阅读添加默认头
        if 'Accept-Encoding' not in extra_headers:
            req.add_header('Accept-Encoding', 'gzip, deflate')
        
        # POST请求需要设置Content-Type
        if method.upper() == 'POST' and body and 'Content-Type' not in extra_headers:
            req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        
        try:
            with urllib.request.urlopen(req, timeout=30, context=ssl_context) as response:
                content = response.read()
                status_code = response.status
                
                # 1. 解压处理 - 按照阅读的DecompressInterceptor.kt
                content_encoding = response.headers.get('Content-Encoding', '').lower()
                if 'gzip' in content_encoding or (len(content) > 2 and content[:2] == b'\x1f\x8b'):
                    try:
                        content = gzip.decompress(content)
                    except Exception:
                        pass
                elif 'deflate' in content_encoding:
                    import zlib
                    try:
                        content = zlib.decompress(content, -zlib.MAX_WBITS)
                    except Exception:
                        pass
                
                # 2. 移除UTF-8 BOM - 按照阅读的Utf8BomUtils.kt
                if len(content) >= 3 and content[0:3] == b'\xef\xbb\xbf':
                    content = content[3:]
                
                # 3. 编码检测和解码 - 按照阅读的OkHttpUtils.kt text()方法
                # 优先级：指定编码 > HTTP头 > HTML内容检测
                
                # 3.1 检查书源指定的编码
                if charset:
                    try:
                        return content.decode(charset), status_code
                    except:
                        pass
                
                # 3.2 检查HTTP头的Content-Type charset
                content_type = response.headers.get('Content-Type', '')
                if 'charset=' in content_type.lower():
                    try:
                        http_charset = content_type.lower().split('charset=')[-1].split(';')[0].strip()
                        if http_charset:
                            return content.decode(http_charset), status_code
                    except:
                        pass
                
                # 3.3 从HTML内容检测编码 - 按照阅读的EncodingDetect.getHtmlEncode()
                try:
                    # 尝试解析HTML的meta标签获取charset
                    html_head = content[:4096]  # 只读取前4KB
                    
                    # 检查 <meta charset="xxx">
                    import re
                    charset_match = re.search(rb'<meta[^>]+charset=["\']?([^"\'\s>]+)', html_head, re.I)
                    if charset_match:
                        detected_charset = charset_match.group(1).decode('ascii', errors='ignore')
                        try:
                            return content.decode(detected_charset), status_code
                        except:
                            pass
                    
                    # 检查 <meta http-equiv="content-type" content="text/html; charset=xxx">
                    content_type_match = re.search(
                        rb'<meta[^>]+http-equiv=["\']?content-type["\']?[^>]+content=["\']?[^"\']*charset=([^"\'\s;>]+)',
                        html_head, re.I
                    )
                    if content_type_match:
                        detected_charset = content_type_match.group(1).decode('ascii', errors='ignore')
                        try:
                            return content.decode(detected_charset), status_code
                        except:
                            pass
                except:
                    pass
                
                # 3.4 尝试UTF-8解码
                try:
                    return content.decode('utf-8'), status_code
                except:
                    pass
                
                # 3.5 尝试GBK解码（中文网站常见）
                try:
                    return content.decode('gbk'), status_code
                except:
                    pass
                
                # 3.6 最后使用utf-8忽略错误
                return content.decode('utf-8', errors='ignore'), status_code
                
        except urllib.error.HTTPError as e:
            return "", e.code
        except urllib.error.URLError as e:
            return "", 0
        except Exception as e:
            return "", 0
    
    def test_search(self, keyword: str = "斗破苍穹") -> DebugResult:
        result = DebugResult(success=False, message="搜索测试")
        start_time = time.time()
        
        try:
            url, options = self._build_search_url(keyword)
            if not url:
                result.error = "未配置搜索URL"
                result.message = "搜索测试失败：未配置searchUrl"
                return result
            
            self.log("搜索", f"请求URL: {url}")
            self.log("搜索", f"请求方式: {options.get('method', 'GET')}")
            
            html, status_code = self._fetch_url(url, options)
            
            if not html:
                result.error = "获取网页内容失败"
                result.message = f"搜索测试失败：HTTP状态码 {status_code}"
                self.log("搜索", f"◇HTTP请求失败，状态码: {status_code}")
                self.log("搜索", "◇可能原因: 网站无法访问、被防火墙拦截、或网站已关闭")
                return result
            
            self.log("搜索", f"获取到HTML内容，长度: {len(html)}")
            
            # 输出HTML预览，帮助调试
            html_preview = html[:500] if len(html) > 500 else html
            self.log("搜索", f"≡HTML预览: {html_preview}")
            
            rule = self.book_source.ruleSearch
            if not rule or not rule.bookList:
                result.error = "未配置搜索规则"
                result.message = "搜索测试失败：未配置ruleSearch或bookList"
                return result
            
            analyzer = AnalyzeRule(html, url, self.book_source.jsLib, log_callback=self.log)
            book_elements = analyzer.get_elements(rule.bookList)
            
            self.log("搜索", f"找到 {len(book_elements)} 个搜索结果")
            
            # 如果没有找到结果，输出调试信息
            if len(book_elements) == 0:
                self.log("搜索", "◇未找到搜索结果，可能原因:")
                self.log("搜索", "  1. 网站结构已变化，规则需要更新")
                self.log("搜索", "  2. 搜索关键词没有匹配结果")
                self.log("搜索", "  3. 网站返回了错误页面或验证码")
                self.log("搜索", f"  4. 规则 '{rule.bookList}' 可能不匹配当前页面结构")
                
                # 尝试分析页面结构
                self._analyze_page_structure(html, "搜索")
            
            search_results = []
            # 移除限制，遍历所有搜索结果（Legado没有硬编码限制）
            for i, elem in enumerate(book_elements):
                item_result = SearchResult()
                
                # 保存原始元素数据用于模板变量替换
                if hasattr(elem, 'name') or hasattr(elem, 'get'):
                    # BeautifulSoup元素
                    item_result.raw_data = elem
                else:
                    # 可能是JSON数据
                    try:
                        if isinstance(elem, str):
                            import json
                            item_result.raw_data = json.loads(elem)
                        else:
                            item_result.raw_data = elem
                    except:
                        item_result.raw_data = str(elem)
                
                if rule.name:
                    analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                    item_result.name = analyzer_item.get_string(rule.name)
                
                if rule.author:
                    analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                    item_result.author = analyzer_item.get_string(rule.author)
                
                if rule.bookUrl:
                    analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                    book_url_raw = analyzer_item.get_string(rule.bookUrl, is_url=True)
                    
                    # 处理模板变量 {{$.field}}
                    if book_url_raw and '{{' in book_url_raw and '}}' in book_url_raw:
                        # 从元素中提取需要的变量
                        import re
                        def replace_template(match):
                            field_path = match.group(1)
                            # 支持 $.field 格式
                            if field_path.startswith('$.'):
                                field_name = field_path[2:]
                                # 尝试从元素中获取字段值
                                if isinstance(item_result.raw_data, dict):
                                    return str(item_result.raw_data.get(field_name, ''))
                                else:
                                    # 使用JSONPath提取
                                    try:
                                        from jsonpath_ng import parse
                                        jsonpath_expr = parse(field_path)
                                        matches = jsonpath_expr.find(item_result.raw_data)
                                        if matches:
                                            return str(matches[0].value)
                                    except:
                                        pass
                            return match.group(0)
                        
                        book_url_raw = re.sub(r'\{\{([^}]+)\}\}', replace_template, book_url_raw)
                    
                    # 如果是相对URL，拼接基础URL
                    if book_url_raw and not book_url_raw.startswith('http'):
                        book_url_raw = urljoin(self.book_source.bookSourceUrl, book_url_raw)
                    
                    item_result.bookUrl = book_url_raw
                
                if rule.coverUrl:
                    analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                    item_result.coverUrl = analyzer_item.get_string(rule.coverUrl, is_url=True)
                
                if rule.intro:
                    analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                    item_result.intro = analyzer_item.get_string(rule.intro)
                
                if rule.kind:
                    analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                    item_result.kind = analyzer_item.get_string(rule.kind)
                
                if rule.lastChapter:
                    analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                    item_result.lastChapter = analyzer_item.get_string(rule.lastChapter)
                
                search_results.append(item_result)
                self.log("搜索", f"结果 {i+1}: {item_result.name} - {item_result.author}")
            
            result.success = True
            result.data = search_results
            result.message = f"搜索测试成功，找到 {len(book_elements)} 个结果"
            
        except Exception as e:
            result.error = str(e)
            result.message = f"搜索测试失败：{str(e)}"
        
        result.duration_ms = (time.time() - start_time) * 1000
        result.steps = self.debug_log.copy()
        return result
    
    def _analyze_page_structure(self, html: str, step: str):
        """分析页面结构，帮助调试"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 输出页面标题
            title = soup.find('title')
            if title:
                self.log(step, f"≡页面标题: {title.get_text(strip=True)}")
            
            # 输出主要结构
            self.log(step, "≡页面主要结构:")
            
            # 查找常见的列表容器
            common_containers = [
                ('class', 'list'), ('class', 'item'), ('class', 'result'),
                ('class', 'book'), ('class', 'chapter'), ('class', 'content'),
                ('id', 'list'), ('id', 'content'), ('id', 'main'),
            ]
            
            found_containers = []
            for attr_type, attr_val in common_containers:
                if attr_type == 'class':
                    elements = soup.find_all(class_=re.compile(attr_val, re.I))
                else:
                    elements = soup.find_all(id=re.compile(attr_val, re.I))
                
                for elem in elements[:3]:  # 只显示前3个
                    tag = elem.name
                    classes = elem.get('class', [])
                    elem_id = elem.get('id', '')
                    found_containers.append(f"<{tag} class=\"{' '.join(classes)}\" id=\"{elem_id}\">")
            
            if found_containers:
                for container in found_containers[:10]:
                    self.log(step, f"  {container}")
            else:
                self.log(step, "  未找到常见的列表容器")
            
            # 检查是否是错误页面
            error_indicators = ['验证码', 'captcha', 'error', '404', '403', '禁止', '不存在', '已关闭']
            html_lower = html.lower()
            for indicator in error_indicators:
                if indicator in html_lower:
                    self.log(step, f"◇检测到可能的错误页面: 包含 '{indicator}'")
            
            # 检查是否需要登录
            login_indicators = ['登录', 'login', '注册', 'register', 'sign in']
            for indicator in login_indicators:
                if indicator in html_lower:
                    self.log(step, f"◇页面可能需要登录: 包含 '{indicator}'")
                    
        except Exception as e:
            self.log(step, f"◇页面结构分析失败: {str(e)}")
    
    def test_book_info(self, book_url: str = None, search_keyword: str = "斗破苍穹") -> DebugResult:
        result = DebugResult(success=False, message="书籍详情测试")
        start_time = time.time()
        
        try:
            if not book_url:
                search_result = self.test_search(search_keyword)
                if not search_result.success or not search_result.data:
                    result.error = "搜索失败，无法获取书籍URL"
                    result.message = "书籍详情测试失败：搜索无结果"
                    return result
                
                book_url = search_result.data[0].bookUrl
            
            self.log("详情", f"≡获取成功:{book_url}")
            # 按照Legado源码: BookInfo.kt 第39-40行
            # Debug.log(bookSource.bookSourceUrl, "≡获取成功:${baseUrl}")
            # Debug.log(bookSource.bookSourceUrl, body, state = 20)
            
            html, status_code = self._fetch_url(book_url)
            
            if not html:
                result.error = "获取网页内容失败"
                result.message = f"书籍详情测试失败：HTTP状态码 {status_code}"
                return result
            
            # 输出HTML内容（state=20表示详情页HTML）
            self.log("详情", html, state=20)
            
            rule = self.book_source.ruleBookInfo
            if not rule:
                result.error = "未配置书籍详情规则"
                result.message = "书籍详情测试失败：未配置ruleBookInfo"
                return result
            
            # 输出规则信息
            self.log("详情", f"≡规则: name={rule.name}, author={rule.author}")
            
            # 执行init规则
            json_data = None  # 用于存储解压后的JSON数据
            if rule.init and rule.init.strip():
                self.log("详情", "≡执行详情页初始化规则")
                init_analyzer = AnalyzeRule(html, book_url, self.book_source.jsLib)
                init_result = init_analyzer.get_string(rule.init, is_url=False)
                if init_result:
                    html = init_result
                    self.log("详情", f"初始化结果长度: {len(html)}")
                    # 如果init返回的是JSON字符串，需要解析它
                    try:
                        json_data = json.loads(html)
                        self.log("详情", f"初始化结果解析为JSON成功")
                    except:
                        pass
            
            analyzer = AnalyzeRule(html, book_url, self.book_source.jsLib)
            book_info = BookInfo()
            book_info.bookUrl = book_url  # 保存bookUrl
            
            # 按照Legado格式输出调试信息
            if rule.name:
                self.log("详情", "┌获取书名")
                book_info.name = analyzer.get_string(rule.name)
                self.log("详情", f"└{book_info.name}")
            
            if rule.author:
                self.log("详情", "┌获取作者")
                book_info.author = analyzer.get_string(rule.author)
                self.log("详情", f"└{book_info.author}")
            
            if rule.kind:
                self.log("详情", "┌获取分类")
                try:
                    book_info.kind = analyzer.get_string(rule.kind)
                    self.log("详情", f"└{book_info.kind}")
                except Exception as e:
                    self.log("详情", f"└{str(e)}")
            
            if rule.wordCount:
                self.log("详情", "┌获取字数")
                try:
                    book_info.wordCount = analyzer.get_string(rule.wordCount)
                    self.log("详情", f"└{book_info.wordCount}")
                except Exception as e:
                    self.log("详情", f"└{str(e)}")
            
            if rule.lastChapter:
                self.log("详情", "┌获取最新章节")
                try:
                    book_info.lastChapter = analyzer.get_string(rule.lastChapter)
                    self.log("详情", f"└{book_info.lastChapter}")
                except Exception as e:
                    self.log("详情", f"└{str(e)}")
            
            if rule.intro:
                self.log("详情", "┌获取简介")
                try:
                    book_info.intro = analyzer.get_string(rule.intro)
                    intro_display = book_info.intro[:100] + "..." if len(book_info.intro) > 100 else book_info.intro
                    self.log("详情", f"└{intro_display}")
                except Exception as e:
                    self.log("详情", f"└{str(e)}")
            
            if rule.coverUrl:
                self.log("详情", "┌获取封面链接")
                try:
                    book_info.coverUrl = analyzer.get_string(rule.coverUrl, is_url=True)
                    self.log("详情", f"└{book_info.coverUrl}")
                except Exception as e:
                    self.log("详情", f"└{str(e)}")
            
            if rule.tocUrl:
                self.log("详情", "┌获取目录链接")
                toc_url_raw = rule.tocUrl
                
                # 处理模板变量 {{$.field}}
                if '{{' in toc_url_raw and '}}' in toc_url_raw and json_data:
                    # 从解压后的JSON数据中获取变量
                    import re
                    # 使用闭包捕获json_data
                    def make_replacer(data):
                        def replace_template(match):
                            field_path = match.group(1)
                            if field_path.startswith('$.'):
                                field_name = field_path[2:]
                                # 直接从字典获取
                                if isinstance(data, dict) and field_name in data:
                                    return str(data[field_name])
                                # 尝试使用JSONPath
                                try:
                                    from jsonpath_ng import parse
                                    jsonpath_expr = parse(field_path)
                                    matches = jsonpath_expr.find(data)
                                    if matches:
                                        return str(matches[0].value)
                                except:
                                    pass
                            return match.group(0)
                        return replace_template
                    
                    toc_url_raw = re.sub(r'\{\{([^}]+)\}\}', make_replacer(json_data), toc_url_raw)
                
                # 如果是相对URL，拼接基础URL
                if toc_url_raw and not toc_url_raw.startswith('http'):
                    toc_url_raw = urljoin(self.book_source.bookSourceUrl, toc_url_raw)
                
                book_info.tocUrl = toc_url_raw
                if not book_info.tocUrl:
                    book_info.tocUrl = book_url
                self.log("详情", f"└{book_info.tocUrl}")
            
            result.success = True
            result.data = book_info
            result.message = f"书籍详情测试成功：{book_info.name}"
            
        except Exception as e:
            result.error = str(e)
            result.message = f"书籍详情测试失败：{str(e)}"
        
        result.duration_ms = (time.time() - start_time) * 1000
        result.steps = self.debug_log.copy()
        return result
    
    def test_toc(self, book_url: str = None, search_keyword: str = "斗破苍穹") -> DebugResult:
        result = DebugResult(success=False, message="目录测试")
        start_time = time.time()
        
        try:
            if not book_url:
                info_result = self.test_book_info(search_keyword=search_keyword)
                if not info_result.success:
                    result.error = "获取书籍信息失败"
                    result.message = "目录测试失败：无法获取书籍信息"
                    return result
                
                book_info = info_result.data
                # 优先使用tocUrl，如果没有则使用bookUrl
                toc_url = book_info.tocUrl if book_info.tocUrl else book_info.bookUrl if hasattr(book_info, 'bookUrl') else None
                
                # 如果还是没有，从搜索结果中获取
                if not toc_url:
                    # 重新搜索获取bookUrl
                    search_result = self.test_search(search_keyword)
                    if search_result.success and search_result.data:
                        toc_url = search_result.data[0].bookUrl
            
            if not toc_url:
                result.error = "无法获取目录URL"
                result.message = "目录测试失败：无法获取目录URL"
                return result
            self.log("目录", f"≡获取成功:{toc_url}")
            # 按照Legado源码: BookChapterList.kt 第48-49行
            # Debug.log(bookSource.bookSourceUrl, "≡获取成功:${baseUrl}")
            # Debug.log(bookSource.bookSourceUrl, body, state = 30)
            
            html, status_code = self._fetch_url(toc_url)
            
            if not html:
                result.error = "获取网页内容失败"
                result.message = f"目录测试失败：HTTP状态码 {status_code}"
                return result
            
            # 输出HTML内容（state=30表示目录页HTML）
            self.log("目录", html, state=30)
            
            rule = self.book_source.ruleToc
            if not rule or not rule.chapterList:
                result.error = "未配置目录规则"
                result.message = "目录测试失败：未配置ruleToc或chapterList"
                return result
            
            # 处理目录列表规则的前缀（-表示倒序）
            list_rule = rule.chapterList
            reverse = False
            if list_rule.startswith("-"):
                reverse = True
                list_rule = list_rule[1:]
            if list_rule.startswith("+"):
                list_rule = list_rule[1:]
            
            analyzer = AnalyzeRule(html, toc_url, self.book_source.jsLib)
            
            # 按照Legado源码: BookChapterList.kt 第202-204行
            # Debug.log(bookSource.bookSourceUrl, "┌获取目录列表", log)
            # val elements = analyzeRule.getElements(listRule)
            # Debug.log(bookSource.bookSourceUrl, "└列表大小:${elements.size}", log)
            self.log("目录", "┌获取目录列表")
            chapter_elements = analyzer.get_elements(list_rule)
            self.log("目录", f"└列表大小:{len(chapter_elements)}")
            
            # 获取下一页链接
            # 按照Legado源码: BookChapterList.kt 第206-222行
            # Debug.log(bookSource.bookSourceUrl, "┌获取目录下一页列表", log)
            # Debug.log(bookSource.bookSourceUrl, "└" + nextUrlList.joinToString("，"), log)
            next_toc_urls = []
            if rule.nextTocUrl:
                self.log("目录", "┌获取目录下一页列表")
                raw_next_urls = analyzer.get_string_list(rule.nextTocUrl, is_url=True)
                # 按照Legado源码: 过滤掉当前URL（重定向后的URL）
                # for (item in it) { if (item != redirectUrl) { nextUrlList.add(item) } }
                # 将相对URL转换为完整URL，并过滤掉当前URL
                next_toc_urls = []
                for url in raw_next_urls:
                    if not url.startswith('http'):
                        url = urljoin(toc_url, url)
                    # 过滤掉当前URL（注意：toc_url已经是重定向后的URL）
                    if url != toc_url and url not in next_toc_urls:
                        next_toc_urls.append(url)
                
                # 按照Legado源码: 使用中文逗号分隔
                if next_toc_urls:
                    # 显示简短的URL列表（去掉基础URL）
                    display_urls = [url.replace(self.book_source.bookSourceUrl, '') for url in next_toc_urls[:10]]
                    if len(next_toc_urls) > 10:
                        display_urls.append(f'...共{len(next_toc_urls)}个')
                    self.log("目录", f"└{'，'.join(display_urls)}")
                else:
                    self.log("目录", "└")
            
            # 按照Legado源码: BookChapterList.kt 第225行
            # Debug.log(bookSource.bookSourceUrl, "┌解析目录列表", log)
            self.log("目录", "┌解析目录列表")
            
            chapters = []
            # 移除限制，遍历所有章节（Legado没有硬编码限制）
            for i, elem in enumerate(chapter_elements):
                chapter = Chapter()
                
                # 保存原始数据用于模板变量替换
                raw_data = elem
                if isinstance(elem, str):
                    try:
                        raw_data = json.loads(elem)
                    except:
                        raw_data = {"text": elem}
                
                if rule.chapterName:
                    analyzer_item = AnalyzeRule(elem, toc_url, self.book_source.jsLib)
                    chapter.title = analyzer_item.get_string(rule.chapterName)
                
                if rule.chapterUrl:
                    # 使用AnalyzeRule解析chapterUrl规则
                    analyzer_item = AnalyzeRule(elem, toc_url, self.book_source.jsLib)
                    chapter_url_raw = analyzer_item.get_string(rule.chapterUrl, is_url=True)
                    
                    # 处理模板变量 {{...}}
                    if chapter_url_raw and '{{' in chapter_url_raw and '}}' in chapter_url_raw:
                        def replace_template(match):
                            expr = match.group(1)
                            
                            # 处理baseUrl.replace()
                            if 'baseUrl.replace' in expr:
                                old_val = expr.split("'")[1]
                                new_val = expr.split("'")[3]
                                url = toc_url.replace(old_val, new_val)
                                return url
                            
                            # 处理$.field格式
                            if expr.startswith('$.'):
                                field_name = expr[2:]
                                if isinstance(raw_data, dict):
                                    return str(raw_data.get(field_name, ''))
                            
                            return match.group(0)
                        
                        chapter_url_raw = re.sub(r'\{\{([^}]+)\}\}', replace_template, chapter_url_raw)
                    
                    # 如果是相对URL，拼接基础URL
                    if chapter_url_raw and not chapter_url_raw.startswith('http'):
                        chapter_url_raw = urljoin(self.book_source.bookSourceUrl, chapter_url_raw)
                    
                    chapter.url = chapter_url_raw
                
                chapters.append(chapter)
            
            # 按照Legado源码: BookChapterList.kt 第285-300行
            # Debug.log(bookSource.bookSourceUrl, "└目录列表解析完成", log)
            self.log("目录", "└目录列表解析完成")
            
            if not chapters:
                # 按照Legado源码: BookChapterList.kt 第287行
                self.log("目录", "◇章节列表为空")
            else:
                # 按照Legado源码: BookChapterList.kt 第289-300行
                # Debug.log(bookSource.bookSourceUrl, "≡首章信息", log)
                # Debug.log(bookSource.bookSourceUrl, "◇章节名称:${chapterList[0].title}", log)
                # Debug.log(bookSource.bookSourceUrl, "◇章节链接:${chapterList[0].url}", log)
                self.log("目录", "≡首章信息")
                self.log("目录", f"◇章节名称:{chapters[0].title}")
                self.log("目录", f"◇章节链接:{chapters[0].url}")
            
            # 处理目录分页
            # 按照Legado源码: BookChapterList.kt 第68-120行
            if len(next_toc_urls) == 1:
                # 单页循环模式
                # 按照Legado源码: BookChapterList.kt 第70-91行
                next_url = next_toc_urls[0]
                page_count = 1
                visited_urls = [toc_url]
                
                while next_url and next_url not in visited_urls:
                    visited_urls.append(next_url)
                    
                    # 获取下一页目录
                    next_html, next_status = self._fetch_url(next_url)
                    if not next_html:
                        break
                    
                    next_analyzer = AnalyzeRule(next_html, next_url, self.book_source.jsLib)
                    next_elements = next_analyzer.get_elements(list_rule)
                    
                    # 解析下一页章节
                    for i, elem in enumerate(next_elements):
                        chapter = Chapter()
                        
                        if rule.chapterName:
                            analyzer_item = AnalyzeRule(elem, next_url, self.book_source.jsLib)
                            chapter.title = analyzer_item.get_string(rule.chapterName)
                        
                        if rule.chapterUrl:
                            analyzer_item = AnalyzeRule(elem, next_url, self.book_source.jsLib)
                            chapter_url_raw = analyzer_item.get_string(rule.chapterUrl, is_url=True)
                            if chapter_url_raw and not chapter_url_raw.startswith('http'):
                                chapter_url_raw = urljoin(self.book_source.bookSourceUrl, chapter_url_raw)
                            chapter.url = chapter_url_raw
                        
                        chapters.append(chapter)
                    
                    # 获取下一页的下一页
                    if rule.nextTocUrl:
                        next_url = next_analyzer.get_string(rule.nextTocUrl, is_url=True)
                        if next_url == next_url:  # 避免死循环
                            break
                    else:
                        next_url = ""
                    
                    page_count += 1
                
                # 按照Legado源码: BookChapterList.kt 第91行
                # Debug.log(bookSource.bookSourceUrl, "◇目录总页数:${nextUrlList.size}")
                self.log("目录", f"◇目录总页数:{page_count}")
            
            elif len(next_toc_urls) > 1:
                # 并发模式
                # 按照Legado源码: BookChapterList.kt 第94-98行
                # Debug.log(bookSource.bookSourceUrl, "◇并发解析目录,总页数:${chapterData.second.size}")
                self.log("目录", f"◇并发解析目录,总页数:{len(next_toc_urls)}")
                
                # 按照Legado源码，并发模式下章节是按页码顺序追加的
                # 每页内部的章节顺序是从网站获取的原始顺序
                for i, url in enumerate(next_toc_urls):
                    self.log("目录", f"┌解析第{i+1}页目录")
                    self.log("目录", f"≡请求URL:{url}")
                    next_html, next_status = self._fetch_url(url)
                    if not next_html:
                        self.log("目录", f"└获取失败:HTTP {next_status}")
                        continue
                    
                    self.log("目录", f"≡HTML长度:{len(next_html)}")
                    next_analyzer = AnalyzeRule(next_html, url, self.book_source.jsLib)
                    next_elements = next_analyzer.get_elements(list_rule)
                    self.log("目录", f"└列表大小:{len(next_elements)}")
                    
                    for j, elem in enumerate(next_elements):
                        chapter = Chapter()
                        
                        if rule.chapterName:
                            analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                            chapter.title = analyzer_item.get_string(rule.chapterName)
                        
                        if rule.chapterUrl:
                            analyzer_item = AnalyzeRule(elem, url, self.book_source.jsLib)
                            chapter_url_raw = analyzer_item.get_string(rule.chapterUrl, is_url=True)
                            if chapter_url_raw and not chapter_url_raw.startswith('http'):
                                chapter_url_raw = urljoin(self.book_source.bookSourceUrl, chapter_url_raw)
                            chapter.url = chapter_url_raw
                        
                        chapters.append(chapter)
            
            # 按照Legado源码: BookChapterList.kt 第129-133行
            # 去重和最终反转
            # val lh = LinkedHashSet(chapterList)
            # val list = ArrayList(lh)
            # if (!book.getReverseToc()) { list.reverse() }
            # 
            # Legado的两次反转逻辑：
            # - 第一次反转：把网站的倒序变成正序（上面已完成）
            # - 第二次反转：根据用户设置决定是否反转
            #   - getReverseToc()=false（默认）：用户想要正序，所以再次反转变成倒序
            #   - getReverseToc()=true：用户想要倒序，所以不反转
            # 
            # 但这看起来很奇怪？让我再仔细看看...
            # 实际上，Legado的逻辑是：
            # - 网站返回的是倒序（最新章节在前）
            # - 第一次反转：把倒序变成正序
            # - 第二次反转：如果用户想要正序显示，则不反转；如果用户想要倒序显示，则反转
            # 
            # 但代码是 `if (!book.getReverseToc()) { list.reverse() }`
            # 这意味着：如果用户想要正序（getReverseToc()=false），则反转
            # 
            # 所以最终结果是：
            # - 网站倒序 -> 第一次反转 -> 正序 -> 第二次反转 -> 倒序
            # 
            # 这不对！让我再看看...
            # 
            # 实际上，getReverseToc()的含义是"书籍是否倒序目录"
            # - getReverseToc()=false：书籍不是倒序目录，即正序目录
            # - getReverseToc()=true：书籍是倒序目录
            # 
            # 但代码是 `if (!book.getReverseToc()) { list.reverse() }`
            # 这意味着：如果书籍不是倒序目录（即正序），则反转
            # 
            # 所以：
            # - 网站倒序 -> 第一次反转 -> 正序 -> 第二次反转（因为默认是正序） -> 倒序
            # 
            # 这还是不对！让我再看看...
            # 
            # 实际上，我理解错了。让我重新理解：
            # - reverse变量：规则是否有"-"前缀
            #   - reverse=false：规则没有"-"前缀，表示网站返回的是倒序
            #   - reverse=true：规则有"-"前缀，表示网站返回的是正序
            # 
            # - 第一次反转：`if (!reverse) { chapterList.reverse() }`
            #   - 如果网站返回的是倒序（reverse=false），则反转成正序
            #   - 如果网站返回的是正序（reverse=true），则不反转
            # 
            # - 第二次反转：`if (!book.getReverseToc()) { list.reverse() }`
            #   - 如果用户想要正序显示（getReverseToc()=false），则反转
            #   - 如果用户想要倒序显示（getReverseToc()=true），则不反转
            # 
            # 所以最终结果是：
            # - 网站倒序 -> 第一次反转 -> 正序 -> 第二次反转 -> 倒序
            # 
            # 这意味着Legado默认显示的是倒序目录（最新章节在前）！
            # 
            # 但调试模式下，我们想要正序目录（第1章在前），所以不需要第二次反转
            
            # 第一次反转：按照Legado源码 BookChapterList.kt 第124-126行
            # if (!reverse) { chapterList.reverse() }
            # 注意：reverse=false表示没有-前缀，需要反转；reverse=true表示有-前缀，不需要反转
            self.log("目录", f"≡reverse值:{reverse}")
            self.log("目录", f"≡反转前首章:{chapters[0].title if chapters else '无'}")
            self.log("目录", f"≡反转前末章:{chapters[-1].title if chapters else '无'}")
            self.log("目录", f"≡反转前总数:{len(chapters)}")
            if not reverse:
                self.log("目录", "≡执行反转操作")
                chapters = list(reversed(chapters))
            else:
                self.log("目录", "≡跳过反转操作")
            self.log("目录", f"≡反转后首章:{chapters[0].title if chapters else '无'}")
            self.log("目录", f"≡反转后末章:{chapters[-1].title if chapters else '无'}")
            
            # 去重（保持顺序）
            # 按照Legado源码: BookChapterList.kt 第129-130行
            # val lh = LinkedHashSet(chapterList)
            # val list = ArrayList(lh)
            # LinkedHashSet会保持插入顺序，同时去除重复元素
            # 重复判断基于equals()和hashCode()，对于BookChapter是基于url和bookUrl
            seen = set()
            unique_chapters = []
            duplicates = 0
            for chapter in chapters:
                if chapter.url not in seen:
                    seen.add(chapter.url)
                    unique_chapters.append(chapter)
                else:
                    duplicates += 1
            chapters = unique_chapters
            if duplicates > 0:
                self.log("目录", f"≡去重:移除了{duplicates}个重复章节")
            
            # 第二次反转：按照Legado源码 BookChapterList.kt 第131-133行
            # if (!book.getReverseToc()) { list.reverse() }
            # 调试模式下，默认用户想要正序（第1章在前），所以需要再次反转
            self.log("目录", "≡执行第二次反转（用户设置）")
            chapters = list(reversed(chapters))
            self.log("目录", f"≡最终首章:{chapters[0].title if chapters else '无'}")
            self.log("目录", f"≡最终末章:{chapters[-1].title if chapters else '无'}")
            
            # 按照Legado源码: BookChapterList.kt 第134行
            # Debug.log(book.origin, "◇目录总数:${list.size}")
            self.log("目录", f"◇目录总数:{len(chapters)}")
            
            result.success = True
            result.data = chapters
            result.message = f"目录测试成功，找到 {len(chapters)} 个章节"
            
        except Exception as e:
            result.error = str(e)
            result.message = f"目录测试失败：{str(e)}"
        
        result.duration_ms = (time.time() - start_time) * 1000
        result.steps = self.debug_log.copy()
        return result
    
    def test_content(self, chapter_url: str = None, search_keyword: str = "斗破苍穹") -> DebugResult:
        result = DebugResult(success=False, message="正文测试")
        start_time = time.time()
        
        try:
            if not chapter_url:
                toc_result = self.test_toc(search_keyword=search_keyword)
                if not toc_result.success or not toc_result.data:
                    result.error = "获取目录失败"
                    result.message = "正文测试失败：无法获取章节列表"
                    return result
                
                # 选择第一章进行测试
                chapters = toc_result.data
                chapter_url = chapters[0].url
                self.log("正文", f"≡选择第一章: {chapters[0].title}")
                self.log("正文", f"≡章节链接: {chapter_url}")
            
            self.log("正文", f"≡获取成功:{chapter_url}")
            # 按照Legado源码: BookContent.kt 第51-52行
            # Debug.log(bookSource.bookSourceUrl, "≡获取成功:${baseUrl}")
            # Debug.log(bookSource.bookSourceUrl, body, state = 40)  # state=40表示HTML内容
            
            html, status_code = self._fetch_url(chapter_url)
            
            if not html:
                result.error = "获取网页内容失败"
                result.message = f"正文测试失败：HTTP状态码 {status_code}"
                return result
            
            # 输出HTML内容（按照Legado格式，state=40表示HTML内容）
            self.log("正文", html, state=40)
            
            rule = self.book_source.ruleContent
            if not rule or not rule.content:
                result.error = "未配置正文规则"
                result.message = "正文测试失败：未配置ruleContent或content"
                return result
            
            analyzer = AnalyzeRule(html, chapter_url, self.book_source.jsLib)
            
            # 按照Legado源码: BookContent.kt 第234行
            # var content = analyzeRule.getString(contentRule.content, unescape = false)
            content_text = analyzer.get_string(rule.content)
            
            # 按照Legado源码: BookContent.kt 第235-251行
            # HTML格式化（如果不是音频或视频）
            # content = HtmlFormatter.formatKeepImg(content, rUrl)
            # 如果包含&，进行HTML反转义
            if content_text and '&' in content_text:
                import html as html_module
                content_text = html_module.unescape(content_text)
            
            # 全文替换
            # 按照Legado源码: BookContent.kt 第168-175行
            if rule.replaceRegex:
                try:
                    content_text = re.sub(rule.replaceRegex, '', content_text)
                except:
                    pass
            
            # 按照Legado源码: BookContent.kt 第200-203行输出调试日志
            self.log("正文", "┌获取正文内容")
            content_display = content_text[:500] + "..." if len(content_text) > 500 else content_text
            self.log("正文", f"└\n{content_display}")
            
            # 获取下一页链接
            # 按照Legado源码: BookContent.kt 第253-262行
            # Debug.log(bookSource.bookSourceUrl, "┌获取正文下一页链接", printLog)
            # Debug.log(bookSource.bookSourceUrl, "└" + nextUrlList.joinToString("，"), printLog)
            next_urls = []
            if rule.nextContentUrl:
                self.log("正文", "┌获取正文下一页链接")
                next_urls = analyzer.get_string_list(rule.nextContentUrl, is_url=True)
                # 按照Legado源码: 使用中文逗号分隔
                if next_urls:
                    self.log("正文", f"└{'，'.join(next_urls)}")
                else:
                    self.log("正文", "└")
            
            # 按照Legado源码: BookContent.kt 第73-127行
            # 处理下一页（单页循环模式）
            if len(next_urls) == 1:
                # 单页循环模式
                next_url = next_urls[0]
                page_count = 1
                visited_urls = [chapter_url]
                
                while next_url and next_url not in visited_urls:
                    visited_urls.append(next_url)
                    
                    # 获取下一页内容
                    next_html, next_status = self._fetch_url(next_url)
                    if not next_html:
                        break
                    
                    next_analyzer = AnalyzeRule(next_html, next_url, self.book_source.jsLib)
                    next_content = next_analyzer.get_string(rule.content)
                    
                    if next_content:
                        if '&' in next_content:
                            import html as html_module
                            next_content = html_module.unescape(next_content)
                        content_text += "\n" + next_content
                    
                    # 获取下一页的下一页
                    if rule.nextContentUrl:
                        next_url = next_analyzer.get_string(rule.nextContentUrl, is_url=True)
                    else:
                        next_url = ""
                    
                    page_count += 1
                    self.log("正文", f"第{page_count}页完成")
                
                self.log("正文", f"◇本章总页数:{page_count}")
            
            elif len(next_urls) > 1:
                # 并发模式（简化实现，顺序获取）
                self.log("正文", f"◇并发解析正文,总页数:{len(next_urls)}")
                
                for i, url in enumerate(next_urls):
                    next_html, next_status = self._fetch_url(url)
                    if not next_html:
                        continue
                    
                    next_analyzer = AnalyzeRule(next_html, url, self.book_source.jsLib)
                    next_content = next_analyzer.get_string(rule.content)
                    
                    if next_content:
                        if '&' in next_content:
                            import html as html_module
                            next_content = html_module.unescape(next_content)
                        content_text += "\n" + next_content
            
            content = Content(text=content_text, nextUrl=next_urls[0] if next_urls else "")
            
            result.success = True
            result.data = content
            result.message = f"正文测试成功，内容长度: {len(content_text)}"
            
        except Exception as e:
            result.error = str(e)
            result.message = f"正文测试失败：{str(e)}"
        
        result.duration_ms = (time.time() - start_time) * 1000
        result.steps = self.debug_log.copy()
        return result
    
    def run_full_test(self, keyword: str = "斗破苍穹") -> Dict[str, Any]:
        self.debug_log = []
        
        results = {
            'book_source': self.book_source.bookSourceName,
            'url': self.book_source.bookSourceUrl,
            'keyword': keyword,
            'tests': {},
            'overall_success': False,
            'total_duration_ms': 0,
        }
        
        start_time = time.time()
        
        search_result = self.test_search(keyword)
        results['tests']['search'] = {
            'success': search_result.success,
            'message': search_result.message,
            'duration_ms': search_result.duration_ms,
            'results_count': len(search_result.data) if search_result.data else 0,
            'error': search_result.error,
        }
        
        if search_result.success and search_result.data:
            book_url = search_result.data[0].bookUrl
            
            info_result = self.test_book_info(book_url)
            results['tests']['book_info'] = {
                'success': info_result.success,
                'message': info_result.message,
                'duration_ms': info_result.duration_ms,
                'book_name': info_result.data.name if info_result.data else None,
                'error': info_result.error,
            }
            
            toc_result = self.test_toc(book_url)
            results['tests']['toc'] = {
                'success': toc_result.success,
                'message': toc_result.message,
                'duration_ms': toc_result.duration_ms,
                'chapters_count': len(toc_result.data) if toc_result.data else 0,
                'error': toc_result.error,
            }
            
            if toc_result.success and toc_result.data:
                chapter_url = toc_result.data[0].url
                
                content_result = self.test_content(chapter_url)
                results['tests']['content'] = {
                    'success': content_result.success,
                    'message': content_result.message,
                    'duration_ms': content_result.duration_ms,
                    'content_length': len(content_result.data.text) if content_result.data else 0,
                    'error': content_result.error,
                }
        
        results['total_duration_ms'] = (time.time() - start_time) * 1000
        results['overall_success'] = all(
            t.get('success', False) for t in results['tests'].values()
        )
        results['debug_log'] = self.debug_log
        
        return results
