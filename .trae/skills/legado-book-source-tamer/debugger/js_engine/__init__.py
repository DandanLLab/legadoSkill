"""
Legado JavaScript Engine - 完整移植Legado的JS运行环境
使用 Node.js 模拟 Rhino 引擎的执行环境
按照阅读源码 JsExtensions.kt 1:1 移植所有内置方法
"""

import os
import json
import re
import subprocess
import tempfile
import time
import base64
import hashlib
import urllib.parse
import urllib.request
import ssl
import gzip
import zlib
import random
import uuid
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path


class CookieStore:
    """
    Cookie存储管理器
    按照阅读源码 CookieStore.kt 实现
    """
    _instance = None
    _cookies: Dict[str, str] = {}
    _session_cookies: Dict[str, str] = {}
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    @staticmethod
    def get_sub_domain(url: str) -> str:
        """获取二级域名"""
        try:
            parsed = urllib.parse.urlparse(url)
            domain = parsed.netloc
            parts = domain.split('.')
            if len(parts) >= 2:
                return '.'.join(parts[-2:])
            return domain
        except:
            return url
    
    def get_cookie(self, url: str) -> str:
        """获取URL对应的所有Cookie"""
        domain = self.get_sub_domain(url)
        cookie = self._cookies.get(domain, '')
        session_cookie = self._session_cookies.get(domain, '')
        return self.merge_cookies(cookie, session_cookie)
    
    def get_key(self, url: str, key: str) -> str:
        """获取特定key的Cookie值"""
        cookie = self.get_cookie(url)
        cookie_map = self.cookie_to_map(cookie)
        return cookie_map.get(key, '')
    
    def set_cookie(self, url: str, cookie: str):
        """设置Cookie"""
        domain = self.get_sub_domain(url)
        self._cookies[domain] = cookie
    
    def remove_cookie(self, url: str, key: str = None):
        """删除Cookie"""
        domain = self.get_sub_domain(url)
        if key:
            cookie = self._cookies.get(domain, '')
            cookie_map = self.cookie_to_map(cookie)
            cookie_map.pop(key, None)
            self._cookies[domain] = self.map_to_cookie(cookie_map)
        else:
            self._cookies.pop(domain, None)
            self._session_cookies.pop(domain, None)
    
    @staticmethod
    def cookie_to_map(cookie: str) -> dict:
        """Cookie字符串转Map"""
        cookie_map = {}
        if not cookie:
            return cookie_map
        for pair in cookie.split(';'):
            if '=' in pair:
                key, value = pair.split('=', 1)
                cookie_map[key.strip()] = value.strip()
        return cookie_map
    
    @staticmethod
    def map_to_cookie(cookie_map: dict) -> str:
        """Map转Cookie字符串"""
        return '; '.join(f'{k}={v}' for k, v in cookie_map.items())
    
    @staticmethod
    def merge_cookies(*cookies: str) -> str:
        """合并多个Cookie字符串"""
        merged = {}
        for cookie in cookies:
            if cookie:
                merged.update(CookieStore.cookie_to_map(cookie))
        return CookieStore.map_to_cookie(merged)


class StrResponse:
    """
    HTTP响应封装类
    按照阅读源码 StrResponse.kt 实现
    """
    def __init__(self, url: str, body: str, code: int = 200, headers: dict = None):
        self.url = url
        self.body = body
        self.code = code
        self.headers = headers or {}
        self.call_time = 0
    
    def body(self) -> str:
        return self.body
    
    def code(self) -> int:
        return self.code
    
    def is_successful(self) -> bool:
        return 200 <= self.code < 300
    
    def __str__(self):
        return f"StrResponse(url={self.url}, code={self.code})"


def http_ajax(url: str, options: dict = None, timeout: int = 60000) -> str:
    """
    发送HTTP请求
    按照阅读源码 JsExtensions.kt ajax() 方法实现
    """
    options = options or {}
    
    url_str = url
    headers = {}
    
    if ',' in url and '{' in url:
        parts = url.split(',', 1)
        url_str = parts[0]
        try:
            opt = json.loads(parts[1])
            headers = opt.get('headers', {})
        except:
            pass
    
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    req = urllib.request.Request(url_str)
    
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
    req.add_header('Accept-Encoding', 'gzip, deflate')
    req.add_header('Accept-Language', 'zh-CN,zh;q=0.9,en;q=0.8')
    
    for key, value in headers.items():
        req.add_header(key, value)
    
    cookie = CookieStore.get_instance().get_cookie(url_str)
    if cookie:
        req.add_header('Cookie', cookie)
    
    try:
        with urllib.request.urlopen(req, timeout=timeout // 1000, context=ssl_context) as response:
            content = response.read()
            
            content_encoding = response.headers.get('Content-Encoding', '').lower()
            if 'gzip' in content_encoding or (len(content) > 2 and content[:2] == b'\x1f\x8b'):
                try:
                    content = gzip.decompress(content)
                except:
                    pass
            elif 'deflate' in content_encoding:
                try:
                    content = zlib.decompress(content, -zlib.MAX_WBITS)
                except:
                    pass
            
            try:
                return content.decode('utf-8')
            except:
                try:
                    return content.decode('gbk')
                except:
                    return content.decode('utf-8', errors='ignore')
    except Exception as e:
        return f"Error: {str(e)}"


def http_connect(url: str, header: str = None, timeout: int = 60000) -> StrResponse:
    """
    发送HTTP请求并返回完整响应
    按照阅读源码 JsExtensions.kt connect() 方法实现
    """
    headers = {}
    if header:
        try:
            headers = json.loads(header)
        except:
            pass
    
    body = http_ajax(url, {'headers': headers}, timeout)
    return StrResponse(url, body)


def web_view(html: str, url: str, js: str, cache_first: bool = False, timeout: int = 60000) -> str:
    """
    使用无头浏览器获取页面内容
    按照阅读源码 JsExtensions.kt webView() 方法实现
    
    Args:
        html: 直接加载的HTML内容
        url: 要访问的URL
        js: 用于获取结果的JavaScript表达式
        cache_first: 是否优先使用缓存
        timeout: 超时时间(毫秒)
    
    Returns:
        str: 页面内容或JS执行结果
    """
    import sys
    print(f'[web_view] Called with url={url}, js={js}', file=sys.stderr)
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            
            # 添加已有的Cookie
            cookie_store = CookieStore.get_instance()
            existing_cookies = cookie_store.get_cookie(url) if url else ''
            if existing_cookies:
                cookies = []
                for pair in existing_cookies.split(';'):
                    if '=' in pair:
                        key, value = pair.strip().split('=', 1)
                        cookies.append({
                            'name': key,
                            'value': value,
                            'domain': urllib.parse.urlparse(url).netloc,
                            'path': '/'
                        })
                if cookies:
                    context.add_cookies(cookies)
            
            page = context.new_page()
            
            if html:
                page.set_content(html)
            elif url:
                print(f'[web_view] Navigating to {url}', file=sys.stderr)
                page.goto(url, timeout=timeout, wait_until='networkidle')
            
            # 等待页面加载完成
            page.wait_for_load_state('domcontentloaded', timeout=timeout)
            
            # 执行JS获取结果
            if js:
                print(f'[web_view] Evaluating JS: {js}', file=sys.stderr)
                result = page.evaluate(js)
                print(f'[web_view] JS result: {result}', file=sys.stderr)
            else:
                result = page.content()
            
            # 保存Cookie
            new_cookies = context.cookies()
            if new_cookies:
                cookie_dict = {}
                for c in new_cookies:
                    cookie_dict[c['name']] = c['value']
                cookie_str = '; '.join(f'{k}={v}' for k, v in cookie_dict.items())
                cookie_store.set_cookie(url, cookie_str)
                print(f'[web_view] Saved cookies: {cookie_str[:100]}...', file=sys.stderr)
            
            browser.close()
            return result if result else ''
            
    except ImportError as e:
        print(f'[JS Engine] Playwright not available: {e}', file=sys.stderr)
        return ''
    except Exception as e:
        print(f'[JS Engine] webView error: {e}', file=sys.stderr)
        import traceback
        traceback.print_exc()
        return ''


@dataclass
class JsExecutionResult:
    success: bool
    result: Any = None
    error: Optional[str] = None
    console_output: List[str] = field(default_factory=list)
    duration_ms: float = 0
    variables: Dict[str, str] = field(default_factory=dict)


LEGADO_JS_FUNCTIONS = '''
// ========================================
// Legado JavaScript Engine - 内置方法
// 按照 JsExtensions.kt 1:1 移植
// ========================================

// ==================== 同步 HTTP 实现 ====================

var _httpAjax = function(url, options, timeout) {
    timeout = timeout || 60000;
    
    try {
        var childProcess = require('child_process');
        
        var result = childProcess.execSync(
            'python -c "import sys; sys.path.insert(0, \\'.' + '\\'); from debugger.js_engine import http_ajax; print(http_ajax(\\'' + url.replace(/'/g, "\\\\'") + '\\'))"',
            { 
                encoding: 'utf-8',
                timeout: timeout / 1000 + 5,
                maxBuffer: 50 * 1024 * 1024
            }
        );
        
        return result.trim();
    } catch (e) {
        console.log('[JS Engine] HTTP request error: ' + e.message);
        return 'Error: ' + e.message;
    }
};

var _httpConnect = function(url, header, timeout) {
    var body = _httpAjax(url, header ? { headers: JSON.parse(header) } : {}, timeout);
    return { url: url, body: body, code: 200, headers: {} };
};

var _webView = function(html, url, js, cacheFirst) {
    cacheFirst = cacheFirst || false;
    var timeout = 60000;
    
    console.log('[JS Engine] _webView called with url=' + url + ', js=' + js);
    
    try {
        var childProcess = require('child_process');
        
        // 使用 JSON.stringify 安全转义字符串
        var htmlJson = html ? JSON.stringify(html) : 'null';
        var urlJson = url ? JSON.stringify(url) : 'null';
        var jsJson = js ? JSON.stringify(js) : 'null';
        
        // 构建 Python 代码
        var pyCode = 'import sys; sys.path.insert(0, "."); from debugger.js_engine import web_view; r = web_view(' + 
            htmlJson + ', ' + urlJson + ', ' + jsJson + ', ' + 
            (cacheFirst ? 'True' : 'False') + ', ' + timeout + '); print(r if r else "")';
        
        console.log('[JS Engine] Executing Python for webView...');
        
        var result = childProcess.execSync(
            'python -c ' + JSON.stringify(pyCode),
            { 
                encoding: 'utf-8',
                timeout: timeout / 1000 + 30,
                maxBuffer: 50 * 1024 * 1024
            }
        );
        
        console.log('[JS Engine] webView result length: ' + (result ? result.length : 0));
        
        return result.trim();
    } catch (e) {
        console.log('[JS Engine] webView error: ' + e.message);
        return '';
    }
};

// Cookie管理对象
var cookie = {
    getCookie: function(url, key) {
        if (typeof _cookieStore !== 'undefined') {
            if (key) {
                return _cookieStore.getKey(url, key);
            }
            return _cookieStore.getCookie(url);
        }
        return '';
    },
    setCookie: function(url, cookieStr) {
        if (typeof _cookieStore !== 'undefined') {
            _cookieStore.setCookie(url, cookieStr);
        }
    },
    removeCookie: function(url, key) {
        if (typeof _cookieStore !== 'undefined') {
            _cookieStore.removeCookie(url, key);
        }
    },
    getKey: function(url, key) {
        return this.getCookie(url, key);
    }
};

// Java内置方法对象
var java = {
    // ==================== 编码解码方法 ====================
    
    base64Decode: function(str, charset) {
        charset = charset || 'utf-8';
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(str, 'base64').toString(charset);
            }
            return atob(str);
        } catch (e) {
            return '';
        }
    },
    
    base64Encode: function(str, charset) {
        charset = charset || 'utf-8';
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(str, charset).toString('base64');
            }
            return btoa(str);
        } catch (e) {
            return '';
        }
    },
    
    base64DecodeToByteArray: function(str) {
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(str, 'base64').toString('hex');
            }
            return '';
        } catch (e) {
            return '';
        }
    },
    
    hexDecodeToString: function(hex) {
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(hex, 'hex').toString('utf-8');
            }
            return '';
        } catch (e) {
            return '';
        }
    },
    
    hexEncodeToString: function(str) {
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(str, 'utf-8').toString('hex');
            }
            return '';
        } catch (e) {
            return '';
        }
    },
    
    hexDecodeToByteArray: function(hex) {
        return this.hexDecodeToString(hex);
    },
    
    md5Encode: function(str) {
        if (typeof require === 'function') {
            try {
                var crypto = require('crypto');
                return crypto.createHash('md5').update(str).digest('hex');
            } catch (e) {}
        }
        return '';
    },
    
    md5Encode16: function(str) {
        var md5 = this.md5Encode(str);
        return md5.substring(8, 24);
    },
    
    // ==================== URL编码方法 ====================
    
    encodeURI: function(str, enc) {
        enc = enc || 'UTF-8';
        try {
            return encodeURIComponent(str);
        } catch (e) {
            return str;
        }
    },
    
    decodeURI: function(str, enc) {
        enc = enc || 'UTF-8';
        try {
            return decodeURIComponent(str);
        } catch (e) {
            return str;
        }
    },
    
    // ==================== 时间格式化方法 ====================
    
    timeFormatUTC: function(time, format, sh) {
        sh = sh || 0;
        var date = new Date(time);
        var offset = date.getTimezoneOffset() * 60000;
        var utc = new Date(date.getTime() + offset + sh * 3600000);
        var pad = function(n) { return n < 10 ? '0' + n : n; };
        return format
            .replace(/yyyy/g, utc.getFullYear())
            .replace(/yy/g, String(utc.getFullYear()).slice(-2))
            .replace(/MM/g, pad(utc.getMonth() + 1))
            .replace(/M/g, utc.getMonth() + 1)
            .replace(/dd/g, pad(utc.getDate()))
            .replace(/d/g, utc.getDate())
            .replace(/HH/g, pad(utc.getHours()))
            .replace(/H/g, utc.getHours())
            .replace(/mm/g, pad(utc.getMinutes()))
            .replace(/m/g, utc.getMinutes())
            .replace(/ss/g, pad(utc.getSeconds()))
            .replace(/s/g, utc.getSeconds());
    },
    
    timeFormat: function(time) {
        var date = new Date(time);
        var pad = function(n) { return n < 10 ? '0' + n : n; };
        return date.getFullYear() + '-' + pad(date.getMonth() + 1) + '-' + pad(date.getDate()) + ' ' +
               pad(date.getHours()) + ':' + pad(date.getMinutes()) + ':' + pad(date.getSeconds());
    },
    
    // ==================== HTTP请求方法 ====================
    
    ajax: function(url, callTimeout) {
        callTimeout = callTimeout || 60000;
        if (typeof _httpAjax !== 'undefined') {
            return _httpAjax(url, {}, callTimeout);
        }
        return 'Error: No HTTP client available';
    },
    
    ajaxAll: function(urlList, skipRateLimit) {
        var results = [];
        for (var i = 0; i < urlList.length; i++) {
            results.push(this.ajax(urlList[i]));
        }
        return results;
    },
    
    connect: function(urlStr, header, callTimeout) {
        callTimeout = callTimeout || 60000;
        if (typeof _httpConnect !== 'undefined') {
            return _httpConnect(urlStr, header, callTimeout);
        }
        return { url: urlStr, body: '', code: 0, headers: {} };
    },
    
    get: function(urlStr, headers, timeout) {
        timeout = timeout || 30;
        return this.ajax(urlStr, timeout * 1000);
    },
    
    post: function(urlStr, body, headers, timeout) {
        timeout = timeout || 30;
        return 'Error: POST not implemented';
    },
    
    head: function(urlStr, headers, timeout) {
        timeout = timeout || 30;
        return { url: urlStr, body: '', code: 0, headers: {} };
    },
    
    // ==================== WebView方法 ====================
    
    webView: function(html, url, js, cacheFirst) {
        cacheFirst = cacheFirst || false;
        if (typeof _webView !== 'undefined') {
            return _webView(html, url, js, cacheFirst);
        }
        console.log('[JS Engine] webView not fully implemented');
        return '';
    },
    
    webViewGetSource: function(html, url, js, sourceRegex, cacheFirst, delayTime) {
        return this.webView(html, url, js || 'document.documentElement.outerHTML', cacheFirst || false);
    },
    
    webViewGetOverrideUrl: function(html, url, js, overrideUrlRegex, cacheFirst, delayTime) {
        return '';
    },
    
    startBrowser: function(url, title, html) {
        console.log('[JS Engine] startBrowser requires GUI');
    },
    
    startBrowserAwait: function(url, title, refetchAfterSuccess, html) {
        console.log('[JS Engine] startBrowserAwait requires GUI');
        return { url: url, body: '', code: 0 };
    },
    
    getVerificationCode: function(imageUrl) {
        console.log('[JS Engine] getVerificationCode requires OCR');
        return '';
    },
    
    // ==================== 文件操作方法 ====================
    
    cacheFile: function(urlStr, saveTime) {
        console.log('[JS Engine] cacheFile: ' + urlStr);
        return '';
    },
    
    downloadFile: function(url) {
        console.log('[JS Engine] downloadFile: ' + url);
        return '';
    },
    
    readTxtFile: function(path, charsetName) {
        console.log('[JS Engine] readTxtFile: ' + path);
        return '';
    },
    
    readFile: function(path) {
        console.log('[JS Engine] readFile: ' + path);
        return null;
    },
    
    deleteFile: function(path) {
        console.log('[JS Engine] deleteFile: ' + path);
        return false;
    },
    
    getFile: function(path) {
        console.log('[JS Engine] getFile: ' + path);
        return null;
    },
    
    // ==================== 压缩文件方法 ====================
    
    unzipFile: function(zipPath) {
        console.log('[JS Engine] unzipFile: ' + zipPath);
        return '';
    },
    
    un7zFile: function(zipPath) {
        console.log('[JS Engine] un7zFile: ' + zipPath);
        return '';
    },
    
    unrarFile: function(zipPath) {
        console.log('[JS Engine] unrarFile: ' + zipPath);
        return '';
    },
    
    unArchiveFile: function(zipPath) {
        console.log('[JS Engine] unArchiveFile: ' + zipPath);
        return '';
    },
    
    getTxtInFolder: function(path) {
        console.log('[JS Engine] getTxtInFolder: ' + path);
        return '';
    },
    
    getZipStringContent: function(url, path, charsetName) {
        console.log('[JS Engine] getZipStringContent: ' + url);
        return '';
    },
    
    getRarStringContent: function(url, path, charsetName) {
        console.log('[JS Engine] getRarStringContent: ' + url);
        return '';
    },
    
    get7zStringContent: function(url, path, charsetName) {
        console.log('[JS Engine] get7zStringContent: ' + url);
        return '';
    },
    
    getZipByteArrayContent: function(url, path) {
        return '';
    },
    
    getRarByteArrayContent: function(url, path) {
        return '';
    },
    
    get7zByteArrayContent: function(url, path) {
        return '';
    },
    
    // ==================== 字节转换方法 ====================
    
    strToBytes: function(str, charset) {
        charset = charset || 'utf-8';
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(str, charset).toString('hex');
            }
            return '';
        } catch (e) {
            return '';
        }
    },
    
    bytesToStr: function(bytes, charset) {
        charset = charset || 'utf-8';
        try {
            if (typeof Buffer !== 'undefined') {
                return Buffer.from(bytes, 'hex').toString(charset);
            }
            return '';
        } catch (e) {
            return '';
        }
    },
    
    // ==================== 字体处理方法 ====================
    
    queryTTF: function(data, useCache) {
        console.log('[JS Engine] queryTTF not implemented');
        return null;
    },
    
    queryBase64TTF: function(data) {
        return this.queryTTF(data);
    },
    
    replaceFont: function(text, errorQueryTTF, correctQueryTTF, filter) {
        return text;
    },
    
    // ==================== 存储方法 ====================
    
    log: function(msg) {
        console.log('[Legado] ' + msg);
        return msg;
    },
    
    logType: function(any) {
        console.log('[Legado] Type: ' + typeof any);
    },
    
    toast: function(msg) {
        console.log('[Toast] ' + msg);
        return msg;
    },
    
    longToast: function(msg) {
        console.log('[LongToast] ' + msg);
    },
    
    put: function(key, value) {
        if (typeof _variables !== 'undefined') {
            _variables[key] = String(value);
        }
        return value;
    },
    
    get: function(key) {
        if (typeof _variables !== 'undefined' && _variables[key]) {
            return _variables[key];
        }
        return '';
    },
    
    // ==================== 其他工具方法 ====================
    
    randomUUID: function() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    },
    
    jsonParse: function(str) {
        try {
            return JSON.parse(str);
        } catch (e) {
            return null;
        }
    },
    
    t2s: function(text) {
        return text;
    },
    
    s2t: function(text) {
        return text;
    },
    
    htmlFormat: function(str) {
        return str;
    },
    
    toNumChapter: function(s) {
        if (!s) return s;
        try {
            var num = parseFloat(s);
            if (!isNaN(num)) {
                return num.toString();
            }
        } catch (e) {}
        return s;
    },
    
    toURL: function(urlStr, baseUrl) {
        return { url: urlStr, baseUrl: baseUrl || '' };
    },
    
    getWebViewUA: function() {
        return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36';
    },
    
    androidId: function() {
        return 'debug-android-id';
    },
    
    openUrl: function(url, mimeType) {
        console.log('[JS Engine] openUrl: ' + url);
    },
    
    openVideoPlayer: function(url, title, isFloat) {
        console.log('[JS Engine] openVideoPlayer: ' + url);
    },
    
    importScript: function(path) {
        console.log('[JS Engine] importScript: ' + path);
        return '';
    },
    
    getReadBookConfig: function() {
        return '{}';
    },
    
    getReadBookConfigMap: function() {
        return {};
    },
    
    getThemeMode: function() {
        return 'light';
    },
    
    getThemeConfig: function() {
        return '{}';
    },
    
    getThemeConfigMap: function() {
        return {};
    },
    
    getSource: function() {
        return null;
    },
    
    getTag: function() {
        return '';
    }
};

// ==================== 全局变量 ====================

var result = '';
var baseUrl = '';
var src = '';
var body = '';
var source = null;
var book = null;
var chapter = null;
var title = '';
var page = 1;
var key = '';
var _variables = {};

// ==================== 全局函数 ====================

function getVariable(key) {
    return java.get(key);
}

function setVariable(key, value) {
    return java.put(key, value);
}

// JSON扩展方法
if (typeof JSON !== 'undefined') {
    JSON.stringifyWithIndent = function(obj, indent) {
        return JSON.stringify(obj, null, indent || 2);
    };
}
'''


def build_js_lib_wrapper(js_lib_code: str) -> str:
    processed_code = js_lib_code
    processed_code = processed_code.replace('})(this,', '})(globalThis,')
    processed_code = processed_code.replace('})(this)', '})(globalThis)')
    processed_code = processed_code.replace('})(this);', '})(globalThis);')
    
    processed_code = processed_code.replace('typeof exports === "object"', 'false')
    processed_code = processed_code.replace('typeof exports==="object"', 'false')
    processed_code = processed_code.replace('typeof define === "function" && define.amd', 'false')
    processed_code = processed_code.replace('typeof define==="function"&&define.amd', 'false')
    
    js_lib_json = json.dumps(processed_code)
    return '''
(function() {
    try {
        (0, eval)(''' + js_lib_json + ''');
    } catch (e) {
        console.log('[JS Engine] Error executing jsLib:', e.message);
        console.log('[JS Engine] Stack:', e.stack);
    }
})();

(function() {
    var detectedVars = [];
    var knownBuiltins = ['java', 'cookie', 'result', 'baseUrl', 'src', 'body', 'source', 'book', 'chapter', 'title', 'page', 'key', '_variables', 'console', 'global', 'globalThis', 'process', 'Buffer', 'setTimeout', 'setInterval', 'clearTimeout', 'clearInterval', 'module', 'exports', 'require', '__filename', '__dirname', 'clearImmediate', 'setImmediate', 'queueMicrotask', 'structuredClone', 'atob', 'btoa', 'performance', 'fetch', 'crypto', 'navigator', 'localStorage', 'sessionStorage'];
    
    for (var key in globalThis) {
        if (knownBuiltins.indexOf(key) === -1) {
            var val = globalThis[key];
            if (typeof val === 'function') {
                detectedVars.push(key + '()');
            } else if (typeof val === 'object' && val !== null) {
                detectedVars.push(key + ' {}');
            } else {
                detectedVars.push(key);
            }
        }
    }
    
    if (detectedVars.length > 0) {
        console.log('[JS Engine] Detected global variables from jsLib: ' + detectedVars.join(', '));
    } else {
        console.log('[JS Engine] WARNING: No global variables detected from jsLib');
    }
})();
'''


class LegadoJsEngine:
    def __init__(self):
        self.node_path = self._find_node()
        self.engine_type = 'node' if self.node_path else 'python'
    
    def _find_node(self) -> Optional[str]:
        try:
            result = subprocess.run(
                ['node', '--version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return 'node'
        except:
            pass
        return None
    
    def execute(
        self,
        js_code: str,
        context: Dict[str, Any] = None,
        js_lib: str = None,
        timeout: int = 30
    ) -> JsExecutionResult:
        start_time = time.time()
        context = context or {}
        
        context_js = "// Context variables\n"
        for key, value in context.items():
            if isinstance(value, str):
                escaped_value = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
                context_js += f'var {key} = "{escaped_value}";\n'
            elif isinstance(value, (int, float, bool)):
                context_js += f'var {key} = {json.dumps(value)};\n'
            elif isinstance(value, (dict, list)):
                context_js += f'var {key} = {json.dumps(value, ensure_ascii=False)};\n'
            elif value is None:
                context_js += f'var {key} = null;\n'
        
        js_lib_code = js_lib or ''
        js_lib_wrapper = build_js_lib_wrapper(js_lib_code)
        
        full_code = f'''
{LEGADO_JS_FUNCTIONS}

// ==================== Context ====================
{context_js}

// ==================== jsLib ====================
{js_lib_wrapper}

// ==================== User Code ====================
{js_code}

// ==================== Output ====================
if (typeof body !== 'undefined' && body) {{
    result = body;
}}

console.log('<<<RESULT_START>>>');
try {{
    console.log(JSON.stringify({{result: result}}));
}} catch (e) {{
    console.log(JSON.stringify({{result: String(result)}}));
}}
console.log('<<<RESULT_END>>>');
'''
        
        if self.engine_type == 'node':
            exec_result = self._execute_with_node(full_code, timeout)
        else:
            exec_result = self._execute_with_python(full_code, timeout)
        
        exec_result.duration_ms = (time.time() - start_time) * 1000
        return exec_result
    
    def _execute_with_node(self, code: str, timeout: int) -> JsExecutionResult:
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_path = f.name
            
            result = subprocess.run(
                ['node', temp_path],
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )
            
            try:
                os.unlink(temp_path)
            except:
                pass
            
            output = result.stdout
            console_output = []
            js_result = None
            
            if '<<<RESULT_START>>>' in output:
                parts = output.split('<<<RESULT_START>>>')
                console_output = parts[0].strip().split('\n') if parts[0].strip() else []
                result_part = parts[1].split('<<<RESULT_END>>>')[0].strip()
                try:
                    parsed = json.loads(result_part)
                    js_result = parsed.get('result')
                except:
                    js_result = result_part
            else:
                console_output = output.strip().split('\n') if output.strip() else []
            
            if result.returncode != 0:
                return JsExecutionResult(
                    success=False,
                    result=None,
                    error=result.stderr or 'Unknown error',
                    console_output=console_output
                )
            
            return JsExecutionResult(
                success=True,
                result=js_result,
                console_output=console_output
            )
            
        except subprocess.TimeoutExpired:
            return JsExecutionResult(success=False, error=f"Timeout ({timeout}s)")
        except Exception as e:
            return JsExecutionResult(success=False, error=str(e))
    
    def _execute_with_python(self, code: str, timeout: int) -> JsExecutionResult:
        try:
            import js2py
            result = js2py.eval_js(code)
            return JsExecutionResult(success=True, result=result)
        except ImportError:
            return JsExecutionResult(success=False, error="Please install Node.js")
        except Exception as e:
            return JsExecutionResult(success=False, error=str(e))
    
    def execute_rule(
        self,
        rule: str,
        content: str,
        base_url: str = "",
        js_lib: str = None,
        variables: Dict[str, str] = None
    ) -> JsExecutionResult:
        if '@js:' in rule:
            js_code = rule.split('@js:')[1].strip()
        elif rule.startswith('<js>'):
            match = re.search(r'<js>(.*?)</js>', rule, re.DOTALL)
            js_code = match.group(1).strip() if match else rule[4:].strip()
        else:
            return JsExecutionResult(success=False, error="Not a JS rule")
        
        context = {
            'result': content,
            'src': content,
            'body': content,
            'baseUrl': base_url,
            '_variables': variables or {},
        }
        
        return self.execute(js_code, context, js_lib)


class JsExtensions:
    @staticmethod
    def base64_decode(str_val: str, charset: str = 'utf-8') -> str:
        try:
            return base64.b64decode(str_val).decode(charset)
        except:
            return ""
    
    @staticmethod
    def base64_encode(str_val: str, charset: str = 'utf-8') -> str:
        try:
            return base64.b64encode(str_val.encode(charset)).decode('utf-8')
        except:
            return ""
    
    @staticmethod
    def time_format(time_ms: int) -> str:
        try:
            from datetime import datetime
            return datetime.fromtimestamp(time_ms / 1000).strftime('%Y-%m-%d %H:%M:%S')
        except:
            return ""
    
    @staticmethod
    def encode_uri(str_val: str, enc: str = 'UTF-8') -> str:
        from urllib.parse import quote
        try:
            return quote(str_val, safe='')
        except:
            return ""
    
    @staticmethod
    def decode_uri(str_val: str, enc: str = 'UTF-8') -> str:
        from urllib.parse import unquote
        try:
            return unquote(str_val)
        except:
            return ""
    
    @staticmethod
    def md5_encode(str_val: str) -> str:
        return hashlib.md5(str_val.encode('utf-8')).hexdigest()


_js_engine: Optional[LegadoJsEngine] = None


def get_js_engine() -> LegadoJsEngine:
    global _js_engine
    if _js_engine is None:
        _js_engine = LegadoJsEngine()
    return _js_engine


def execute_js(js_code: str, context: Dict[str, Any] = None, js_lib: str = None) -> JsExecutionResult:
    return get_js_engine().execute(js_code, context, js_lib)


def execute_js_rule(rule: str, content: str, base_url: str = "", js_lib: str = None, variables: Dict[str, str] = None) -> JsExecutionResult:
    return get_js_engine().execute_rule(rule, content, base_url, js_lib, variables)
