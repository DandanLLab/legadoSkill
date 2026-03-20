"""
AnalyzeRule - Python Implementation
Translated from Kotlin: io.legado.app.model.analyzeRule.AnalyzeRule

This is the core rule analysis engine that handles:
- CSS selectors (JSoup style)
- XPath expressions
- JSONPath expressions
- Regular expressions
- JavaScript evaluation

Based on real Legado Kotlin source code.
"""

import re
import json
from typing import Any, Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, field
from enum import Enum
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, Tag
from lxml import etree, html as lxml_html

try:
    from jsonpath_ng.ext import parse as jsonpath_parse
    HAS_JSONPATH = True
except ImportError:
    HAS_JSONPATH = False


class Mode(Enum):
    XPath = "xpath"
    Json = "json"
    Default = "default"
    Js = "js"
    Regex = "regex"
    WebJs = "webjs"


@dataclass
class SourceRule:
    rule: str
    mode: Mode = Mode.Default
    replace_regex: str = ""
    replacement: str = ""
    replace_first: bool = False
    put_map: Dict[str, str] = field(default_factory=dict)
    rule_param: List[str] = field(default_factory=list)
    rule_type: List[int] = field(default_factory=list)


class AnalyzeRule:
    """
    Python implementation of Legado's AnalyzeRule class.
    Handles rule parsing and content extraction.
    
    Based on: io.legado.app.model.analyzeRule.AnalyzeRule
    """
    
    JS_PATTERN = re.compile(r'@js:|{{.+?}}', re.DOTALL)
    WEB_JS_PATTERN = re.compile(r'@webJs:', re.DOTALL)
    PUT_PATTERN = re.compile(r'@put:\{([^}]+)\}', re.IGNORECASE)
    GET_PATTERN = re.compile(r'@get:\{([^}]+)\}', re.IGNORECASE)
    
    def __init__(self, content: Any = None, base_url: str = None, js_lib: str = None, log_callback=None):
        self.content = content
        self.base_url = base_url or ""
        self.js_lib = js_lib  # 书源JS库（直接使用书源中的真实代码）
        self.is_json = False
        self.is_regex = False
        self.log_callback = log_callback  # 日志回调函数
        self.variables: Dict[str, str] = {}
        
        self._soup: Optional[BeautifulSoup] = None
        self._lxml_doc: Optional[etree._Element] = None
        self._json_data: Any = None
        
        if content is not None:
            self._init_content(content)
    
    def _init_content(self, content: Any):
        if isinstance(content, str):
            stripped = content.strip()
            self.is_json = (stripped.startswith('{') and stripped.endswith('}')) or \
                          (stripped.startswith('[') and stripped.endswith(']'))
            
            if self.is_json:
                try:
                    self._json_data = json.loads(content)
                except:
                    self.is_json = False
            
            if not self.is_json:
                try:
                    self._soup = BeautifulSoup(content, 'html.parser')
                    self._lxml_doc = lxml_html.fromstring(content)
                except Exception:
                    pass
        elif isinstance(content, (dict, list)):
            self.is_json = True
            self._json_data = content
        elif isinstance(content, Tag):
            self._soup = content
            self._lxml_doc = lxml_html.fromstring(str(content))
    
    def set_content(self, content: Any, base_url: str = None) -> 'AnalyzeRule':
        self.content = content
        if base_url:
            self.base_url = base_url
        self._init_content(content)
        return self
    
    def get_string(self, rule: str, is_url: bool = False) -> str:
        if not rule:
            return ""
        
        rules = self._split_source_rule(rule)
        result = self._apply_rules(rules, is_url=is_url)
        
        if result is None:
            return ""
        elif isinstance(result, str):
            return result
        elif isinstance(result, list):
            return result[0] if result else ""
        else:
            return str(result)
    
    def get_string_list(self, rule: str, is_url: bool = False) -> List[str]:
        if not rule:
            return []
        
        rules = self._split_source_rule(rule)
        result = self._apply_rules(rules, is_url=is_url, return_list=True)
        
        if isinstance(result, list):
            return [str(r) for r in result if r]
        elif result:
            return [str(result)]
        return []
    
    def get_elements(self, rule: str) -> List[Any]:
        if not rule:
            return []
        
        rules = self._split_source_rule(rule, all_in_one=True)
        return self._apply_rules_for_elements(rules)
    
    def _split_source_rule(self, rule_str: str, all_in_one: bool = False) -> List[SourceRule]:
        if not rule_str:
            return []
        
        rules = []
        mode = Mode.Default
        
        if all_in_one and rule_str.startswith(":"):
            mode = Mode.Regex
            self.is_regex = True
            rule_str = rule_str[1:]
        elif self.is_regex:
            mode = Mode.Regex
        
        # 关键修复: 按照Legado源码判断XPath模式
        # 参考: AnalyzeRule.kt 第601-612行
        # 只有以 // 或 ./ 或 .. 开头才是XPath
        # 注意: 单独的 / 开头不是XPath，可能是URL模板
        if rule_str.startswith("//") or rule_str.startswith("./") or rule_str.startswith(".."):
            mode = Mode.XPath
        elif rule_str.startswith("$.") or rule_str.startswith("$["):
            mode = Mode.Json
        
        # 处理<js>...</js>标签
        if rule_str.startswith('<js>') and '</js>' in rule_str:
            js_match = re.search(r'<js>(.*?)</js>', rule_str, re.DOTALL)
            if js_match:
                js_code = js_match.group(1).strip()
                rules.append(SourceRule(rule=js_code, mode=Mode.Js))
                # 继续处理剩余部分
                remaining = rule_str[js_match.end():].strip()
                if remaining:
                    remaining_rules = self._split_source_rule(remaining, all_in_one)
                    rules.extend(remaining_rules)
                return rules
        
        if "@js:" in rule_str:
            js_parts = rule_str.split("@js:")
            if js_parts[0].strip():
                rules.append(SourceRule(rule=js_parts[0].strip(), mode=mode))
            if len(js_parts) > 1:
                rules.append(SourceRule(rule=js_parts[1].strip(), mode=Mode.Js))
        elif "@webJs:" in rule_str:
            web_js_parts = rule_str.split("@webJs:")
            if web_js_parts[0].strip():
                rules.append(SourceRule(rule=web_js_parts[0].strip(), mode=mode))
            if len(web_js_parts) > 1:
                rules.append(SourceRule(rule=web_js_parts[1].strip(), mode=Mode.WebJs))
        else:
            rules.append(SourceRule(rule=rule_str, mode=mode))
        
        return rules
    
    def _apply_rules(self, rules: List[SourceRule], is_url: bool = False, 
                     return_list: bool = False) -> Union[str, List[str], None]:
        result = self.content
        
        for source_rule in rules:
            if result is None:
                break
            
            source_rule = self._make_up_rule(source_rule, result)
            rule = source_rule.rule
            
            if not rule and not source_rule.replace_regex:
                continue
            
            mode = source_rule.mode
            
            # 关键修复: 处理字典类型
            # 参考: AnalyzeRule.kt 第233-236行
            if isinstance(result, dict):
                # 字典类型，需要提取值
                if mode == Mode.Json or rule.startswith('$.') or rule.startswith('$['):
                    result = self._apply_json_rule(rule, result, return_list)
                elif '@' in rule:
                    # 包含@分隔符，需要提取
                    key = rule.split('@')[0].strip()
                    if key.startswith('$.'):
                        key = key[2:]
                    result = result.get(key, '')
                else:
                    # 不包含提取操作，直接返回规则字符串（比如URL模板）
                    # 这是关键修复：当规则不包含提取操作时，直接返回规则本身
                    result = rule
            elif isinstance(result, list) and mode != Mode.Json and mode != Mode.XPath:
                # 列表类型，返回第一个元素或使用JSON规则
                if return_list:
                    result = [str(item) for item in result if item]
                elif result:
                    result = str(result[0]) if result[0] else ""
                else:
                    result = ""
            elif mode == Mode.Json:
                result = self._apply_json_rule(rule, result, return_list)
            elif mode == Mode.XPath:
                result = self._apply_xpath_rule(rule, result, return_list)
            elif mode == Mode.Regex:
                result = self._apply_regex_rule(rule, result, return_list)
            elif mode == Mode.Js:
                result = self._eval_js(rule, result)
            elif mode == Mode.WebJs:
                result = self._eval_web_js(rule, result)
            else:
                result = self._apply_default_rule(rule, result, is_url, return_list)
            
            if source_rule.replace_regex and result:
                result = self._apply_replace_regex(result, source_rule)
        
        return result
    
    def _apply_rules_for_elements(self, rules: List[SourceRule]) -> List[Any]:
        result = self.content
        elements = []
        
        for i, source_rule in enumerate(rules):
            if result is None:
                break
            
            rule = source_rule.rule
            mode = source_rule.mode
            
            # 检查下一个规则的模式
            next_mode = None
            if i + 1 < len(rules):
                next_mode = rules[i + 1].mode
            
            if mode == Mode.Js:
                # 执行JS规则
                result = self._apply_js_rule(rule, result)
                # 更新content以便后续规则处理
                if result is not None:
                    self.content = result
                    # 如果结果是JSON字符串，预解析
                    if isinstance(result, str):
                        try:
                            self._json_data = json.loads(result)
                            self.is_json = True
                        except:
                            pass
                    elif isinstance(result, (dict, list)):
                        self._json_data = result
                        self.is_json = True
            elif mode == Mode.Json:
                result = self._apply_json_rule(rule, result, return_elements=True)
            elif mode == Mode.XPath:
                result = self._apply_xpath_rule(rule, result, return_elements=True)
            elif mode == Mode.Regex:
                result = self._apply_regex_rule(rule, result, return_list=True)
            else:
                # 检查是否包含<js>...</js>标签
                if rule.startswith('<js>') and '</js>' in rule:
                    # 提取JS代码并执行
                    js_match = re.search(r'<js>(.*?)</js>', rule, re.DOTALL)
                    if js_match:
                        js_code = js_match.group(1).strip()
                        result = self._apply_js_rule(js_code, result)
                        # 更新content以便后续规则处理
                        if result is not None:
                            self.content = result
                            if isinstance(result, str):
                                try:
                                    self._json_data = json.loads(result)
                                    self.is_json = True
                                except:
                                    pass
                            elif isinstance(result, (dict, list)):
                                self._json_data = result
                                self.is_json = True
                        # 继续处理剩余规则 - 关键修复：需要处理后续的JSON规则
                        remaining_rule = rule[js_match.end():].strip()
                        if remaining_rule:
                            # 检查剩余规则的类型
                            if remaining_rule.startswith('$.') or remaining_rule.startswith('$['):
                                result = self._apply_json_rule(remaining_rule, result, return_elements=True)
                            else:
                                result = self._apply_default_rule(remaining_rule, result, return_elements=True)
                else:
                    result = self._apply_default_rule(rule, result, return_elements=True)
            
            if isinstance(result, list):
                elements = result
        
        return elements
    
    def _apply_js_rule(self, rule: str, content: Any) -> Any:
        """执行JS规则 - 直接使用书源中的真实jsLib代码"""
        try:
            from debugger.js_engine import execute_js
            
            # 准备上下文 - 关键修复：必须传递baseUrl
            context = {
                'result': str(content) if not isinstance(content, str) else content,
                'body': str(content) if not isinstance(content, str) else content,
                'src': str(content) if not isinstance(content, str) else content,
                'baseUrl': self.base_url or '',
            }
            
            # 调试日志
            if self.log_callback:
                self.log_callback("JS规则", f"执行JS规则, baseUrl={self.base_url}")
                self.log_callback("JS规则", f"JS代码长度: {len(rule)}")
            
            # 执行JS - 传递书源的真实jsLib
            js_result = execute_js(rule, context, self.js_lib)
            
            # 调试日志
            if self.log_callback:
                self.log_callback("JS规则", f"JS执行结果: success={js_result.success}, result={str(js_result.result)[:200] if js_result.result else 'None'}")
                if js_result.error:
                    self.log_callback("JS规则", f"JS执行错误: {js_result.error}")
            
            if js_result.success:
                # 更新result变量
                if js_result.result is not None:
                    return js_result.result
            else:
                # JS执行失败，返回原内容
                pass
            
            return content
        except Exception as e:
            if self.log_callback:
                self.log_callback("JS规则", f"JS规则执行异常: {e}")
            return content
    
    def _apply_json_rule(self, rule: str, content: Any, 
                         return_list: bool = False, 
                         return_elements: bool = False) -> Any:
        try:
            # 处理JS返回的字典/列表对象
            if isinstance(content, (dict, list)):
                # 已经是JSON对象，直接使用
                pass
            elif isinstance(content, str):
                # 字符串，尝试解析
                try:
                    content = json.loads(content)
                except:
                    return [] if return_list or return_elements else ""
            else:
                # 其他类型，转换为字符串再解析
                try:
                    content = json.loads(str(content))
                except:
                    return [] if return_list or return_elements else ""
            
            # 处理JSONPath规则
            if rule.startswith("$."):
                rule = rule[2:]
            
            if HAS_JSONPATH:
                jsonpath_expr = jsonpath_parse("$." + rule)
                matches = jsonpath_expr.find(content)
                
                if return_list or return_elements:
                    results = [m.value for m in matches]
                    # 如果结果是单个列表，展开它
                    if len(results) == 1 and isinstance(results[0], list):
                        return results[0]
                    return results
                else:
                    return matches[0].value if matches else ""
            else:
                # 简单的JSONPath实现
                parts = rule.split(".")
                result = content
                for part in parts:
                    if not part:
                        continue
                    if part.startswith("["):
                        idx = int(part[1:-1])
                        if isinstance(result, list) and 0 <= idx < len(result):
                            result = result[idx]
                        else:
                            return [] if return_list or return_elements else ""
                    elif "[" in part:
                        match = re.match(r'(\w+)\[(\d+)\]', part)
                        if match:
                            key, idx = match.groups()
                            if isinstance(result, dict) and key in result:
                                result = result[key]
                                if isinstance(result, list) and 0 <= int(idx) < len(result):
                                    result = result[int(idx)]
                                else:
                                    return [] if return_list or return_elements else ""
                            else:
                                return [] if return_list or return_elements else ""
                    else:
                        if isinstance(result, dict):
                            result = result.get(part, "")
                        elif isinstance(result, list):
                            # 尝试对列表中的每个元素获取属性
                            result = [item.get(part, "") if isinstance(item, dict) else "" for item in result]
                        else:
                            return [] if return_list or return_elements else ""
                
                return result
        except Exception as e:
            return [] if return_list or return_elements else ""
    
    def _apply_xpath_rule(self, rule: str, content: Any,
                          return_list: bool = False,
                          return_elements: bool = False) -> Any:
        try:
            if self._lxml_doc is None:
                if isinstance(content, str):
                    self._lxml_doc = lxml_html.fromstring(content)
                elif isinstance(content, Tag):
                    self._lxml_doc = lxml_html.fromstring(str(content))
                else:
                    return [] if return_list or return_elements else ""
            
            result = self._lxml_doc.xpath(rule)
            
            if return_list or return_elements:
                return result if isinstance(result, list) else [result]
            else:
                if isinstance(result, list):
                    if not result:
                        return ""
                    result = result[0]
                if hasattr(result, 'text'):
                    return result.text or ""
                elif hasattr(result, 'text_content'):
                    return result.text_content()
                return str(result) if result else ""
        except Exception:
            return [] if return_list or return_elements else ""
    
    def _apply_regex_rule(self, rule: str, content: Any,
                          return_list: bool = False) -> Any:
        try:
            content_str = str(content) if not isinstance(content, str) else content
            rules = rule.split("&&")
            results = []
            
            for r in rules:
                r = r.strip()
                if not r:
                    continue
                matches = re.findall(r, content_str, re.DOTALL)
                results.extend(matches)
            
            if return_list:
                return results
            return results[0] if results else ""
        except Exception:
            return [] if return_list else ""
    
    def _apply_default_rule(self, rule: str, content: Any, 
                            is_url: bool = False,
                            return_list: bool = False,
                            return_elements: bool = False) -> Any:
        # 注意: 字典/列表类型已经在_apply_rules中通过_make_up_rule处理
        # 这里只处理字符串和Tag类型
        
        if self._soup is None:
            if isinstance(content, str):
                self._soup = BeautifulSoup(content, 'html.parser')
            elif isinstance(content, Tag):
                self._soup = content
            else:
                # 对于字典/列表类型，直接返回空（不应该到达这里）
                return [] if return_list or return_elements else ""
        
        # 按照Legado源码处理##分隔符（正则替换）
        # 参考: AnalyzeRule.kt 第761-772行
        # ruleStrS = rule.split("##")
        # rule = ruleStrS[0].trim()
        # if (ruleStrS.size > 1) replaceRegex = ruleStrS[1]
        # if (ruleStrS.size > 2) replacement = ruleStrS[2]
        # if (ruleStrS.size > 3) replaceFirst = true
        replace_regex = ""
        replacement = ""
        replace_first = False
        if '##' in rule:
            rule_parts = rule.split('##')
            rule = rule_parts[0].strip()
            if len(rule_parts) > 1:
                replace_regex = rule_parts[1]
            if len(rule_parts) > 2:
                replacement = rule_parts[2]
            if len(rule_parts) > 3:
                replace_first = True
        
        parts = rule.split('@')
        elements = [self._soup]
        
        # 提取类型列表 - 这些是Legado中的提取类型，不是选择器
        extract_types = ['text', 'html', 'ownText', 'textNodes', 'href', 'src', 
                         '@text', '@html', '@ownText', '@textNodes', '@href', '@src',
                         'textNodes']
        
        for i, part in enumerate(parts):
            if not part:
                continue
            
            # 检查是否是提取类型
            if part in extract_types and i > 0:
                # 这是提取类型，对当前所有元素应用提取
                is_last = (i == len(parts) - 1)
                if is_last:
                    results = []
                    for elem in elements:
                        extracted = self._extract_from_element(elem, part, True, is_url)
                        if extracted:
                            if isinstance(extracted, list):
                                results.extend(extracted)
                            else:
                                results.append(extracted)
                    
                    if return_list:
                        final_results = [str(e) for e in results if e]
                    else:
                        final_results = str(results[0]) if results else ""
                    
                    # 应用正则替换
                    if replace_regex and final_results:
                        try:
                            if isinstance(final_results, list):
                                final_results = [self._apply_legado_replace_regex(r, replace_regex, replacement, replace_first) for r in final_results]
                            else:
                                final_results = self._apply_legado_replace_regex(final_results, replace_regex, replacement, replace_first)
                        except:
                            pass
                    
                    return final_results
                continue
            
            is_last = (i == len(parts) - 1)
            new_elements = []
            
            for elem in elements:
                # 当return_elements=True且is_last=True时，不要提取文本，返回元素
                extracted = self._extract_from_element(elem, part, is_last and not return_elements, is_url)
                if extracted:
                    if isinstance(extracted, list):
                        new_elements.extend(extracted)
                    else:
                        new_elements.append(extracted)
            
            elements = new_elements
            
            if is_last and not return_elements:
                if return_list:
                    results = [str(e) for e in elements if e]
                else:
                    results = str(elements[0]) if elements else ""
                
                # 应用正则替换
                # 按照Legado源码: AnalyzeRule.kt 第482-506行
                if replace_regex and results:
                    try:
                        if isinstance(results, list):
                            results = [self._apply_legado_replace_regex(r, replace_regex, replacement, replace_first) for r in results]
                        else:
                            results = self._apply_legado_replace_regex(results, replace_regex, replacement, replace_first)
                    except:
                        pass
                
                return results
        
        if return_elements:
            return elements
        if return_list:
            results = [str(e) for e in elements if e]
        else:
            results = str(elements[0]) if elements else ""
        
        # 应用正则替换
        # 按照Legado源码: AnalyzeRule.kt 第482-506行
        if replace_regex and results:
            try:
                if isinstance(results, list):
                    results = [self._apply_legado_replace_regex(r, replace_regex, replacement, replace_first) for r in results]
                else:
                    results = self._apply_legado_replace_regex(results, replace_regex, replacement, replace_first)
            except:
                pass
        
        return results
    
    def _extract_from_element(self, element: Any, rule: str, 
                               is_last: bool, is_url: bool) -> Any:
        if not rule:
            return element
        
        rule = rule.strip()
        
        # 处理Legado特殊索引格式: .class.0, .class.-1, tag.div.0
        index_match = re.match(r'^(\w+)\.(\w+)([.\-!\d:]+)$', rule)
        if index_match:
            rule_type = index_match.group(1)
            rule_name = index_match.group(2)
            index_part = index_match.group(3)
            
            # 解析索引
            indexes = self._parse_legado_index(index_part)
            
            # 获取元素
            if rule_type == 'class':
                elements = element.find_all(class_=rule_name) if hasattr(element, 'find_all') else []
            elif rule_type == 'tag':
                elements = element.find_all(rule_name) if hasattr(element, 'find_all') else []
            elif rule_type == 'id':
                found = element.find(id=rule_name) if hasattr(element, 'find') else None
                elements = [found] if found else []
            else:
                # 尝试作为CSS选择器
                try:
                    elements = element.select(f"{rule_type}.{rule_name}") if hasattr(element, 'select') else []
                except:
                    elements = []
            
            # 应用索引
            if indexes and elements:
                selected = []
                for idx in indexes:
                    if idx < 0:
                        idx = len(elements) + idx
                    if 0 <= idx < len(elements):
                        selected.append(elements[idx])
                
                if is_last:
                    if len(selected) == 1:
                        return self._extract_value(selected, "text")
                    return self._extract_value(selected, "text")
                return selected if len(selected) > 1 else (selected[0] if selected else None)
        
        # 处理简化格式: .className.0 或 .className.-1
        simple_index_match = re.match(r'^\.([^.]+)\.(-?\d+)$', rule)
        if simple_index_match:
            class_name = simple_index_match.group(1)
            idx = int(simple_index_match.group(2))
            
            elements = element.find_all(class_=class_name) if hasattr(element, 'find_all') else []
            
            if idx < 0:
                idx = len(elements) + idx
            
            if 0 <= idx < len(elements):
                if is_last:
                    return self._extract_value([elements[idx]], "text")
                return elements[idx]
            return None
        
        if rule.startswith("class."):
            class_name = rule[6:]
            dot_idx = class_name.find(".")
            if dot_idx > 0:
                try:
                    idx = int(class_name[dot_idx+1:])
                    class_name = class_name[:dot_idx]
                    elements = element.find_all(class_=class_name)
                    if idx < 0:
                        idx = len(elements) + idx
                    if 0 <= idx < len(elements):
                        return elements[idx]
                    return None
                except:
                    pass
            elements = element.find_all(class_=class_name)
            return elements if not is_last else self._extract_value(elements, "text")
        
        elif rule.startswith("id."):
            id_name = rule[3:]
            found = element.find(id=id_name)
            return found if not is_last else self._extract_value([found], "text") if found else ""
        
        elif rule.startswith("tag."):
            tag_name = rule[4:]
            dot_idx = tag_name.find(".")
            if dot_idx > 0:
                try:
                    idx = int(tag_name[dot_idx+1:])
                    tag_name = tag_name[:dot_idx]
                    elements = element.find_all(tag_name)
                    if idx < 0:
                        idx = len(elements) + idx
                    if 0 <= idx < len(elements):
                        return elements[idx]
                    return None
                except:
                    pass
            elements = element.find_all(tag_name)
            return elements if not is_last else self._extract_value(elements, "text")
        
        elif rule.startswith("@css:"):
            css_selector = rule[5:]
            elements = element.select(css_selector)
            return elements if not is_last else self._extract_value(elements, "text")
        
        elif rule.startswith("@@"):
            css_selector = rule[2:]
            elements = element.select(css_selector)
            return elements if not is_last else self._extract_value(elements, "text")
        
        elif rule.startswith("."):
            # 检查是否是复合CSS选择器（包含空格或其他CSS语法）
            if ' ' in rule or '>' in rule or '+' in rule or '~' in rule or '[' in rule:
                # 复合CSS选择器，直接使用select
                elements = element.select(rule) if hasattr(element, 'select') else []
                return elements if not is_last else self._extract_value(elements, "text")
            
            parts = rule.split(".")
            if len(parts) > 1:
                class_name = parts[1]
                try:
                    idx = int(parts[2]) if len(parts) > 2 else 0
                except:
                    idx = 0
                elements = element.find_all(class_=class_name)
                if idx < 0:
                    idx = len(elements) + idx
                if 0 <= idx < len(elements):
                    return elements[idx]
            elements = element.select(rule) if hasattr(element, 'select') else []
            return elements if not is_last else self._extract_value(elements, "text")
        
        elif rule.startswith("#"):
            id_name = rule[1:]
            found = element.find(id=id_name)
            return found if not is_last else self._extract_value([found], "text") if found else ""
        
        # 按照Legado源码: AnalyzeByJSoup.kt 第319行
        # "text" -> temp.getElementsContainingOwnText(rules[1])
        # text.xxx 表示获取包含xxx文本的元素
        elif rule.startswith("text."):
            text_content = rule[5:]
            if hasattr(element, 'find_all'):
                # 获取包含指定文本的元素
                elements = element.find_all(string=lambda s: s and text_content in s)
                if elements:
                    # 返回父元素
                    result_elements = [e.parent for e in elements]
                    return result_elements if not is_last else self._extract_value(result_elements, "text")
            return [] if not is_last else ""
        
        if is_last:
            if rule in ("text", "@text"):
                if hasattr(element, 'get_text'):
                    return element.get_text(strip=True)
                return str(element) if element else ""
            elif rule in ("html", "@html"):
                return str(element) if element else ""
            elif rule in ("ownText", "@ownText"):
                if hasattr(element, 'get_text'):
                    return element.get_text(strip=True)
                return ""
            elif rule in ("href", "@href"):
                if hasattr(element, 'get'):
                    href = element.get('href', '')
                    if href and self.base_url and not href.startswith('http'):
                        return urljoin(self.base_url, href)
                    return href
                return ""
            elif rule in ("src", "@src"):
                if hasattr(element, 'get'):
                    src = element.get('src', '')
                    if src and self.base_url and not src.startswith('http'):
                        return urljoin(self.base_url, src)
                    return src
                return ""
            elif rule in ("textNodes", "@textNodes"):
                # 按照Legado源码: AnalyzeByJSoup.kt 第239-251行
                # 获取元素的textNodes（文本节点），过滤空文本，用换行符连接
                if hasattr(element, 'find_all'):
                    from bs4 import NavigableString
                    texts = []
                    # 遍历所有文本节点
                    for text_node in element.find_all(string=True):
                        text = text_node.strip()
                        if text:
                            texts.append(text)
                    return '\n'.join(texts)
                return ""
            else:
                if hasattr(element, 'get'):
                    return element.get(rule, "")
        
        try:
            elements = element.select(rule)
            return elements if elements else None
        except:
            pass
        
        return element
    
    def _parse_legado_index(self, index_str: str) -> List[int]:
        """
        解析Legado索引格式 - 完美还原Legado源码
        
        参考: AnalyzeByJSoup.kt 第283-510行
        
        支持格式:
        1. 阅读原有写法：':'分隔索引，'!'或'.'表示筛选方式，索引可为负数
           例如: tag.div.-1:10:2 或 tag.div!0:3
        2. 与jsonPath类似的[]索引写法
           格式形如 [it,it，。。。] 或 [!it,it，。。。] 
           其中[!开头表示筛选方式为排除，it为单个索引或区间。
           区间格式为 start:end 或 start:end:step
           例如: tag.div[-1, 3:-2:-10, 2]
           特殊用法: tag.div[-1:0] 可在任意地方让列表反向
        """
        indexes = []
        
        index_str = index_str.strip()
        if not index_str:
            return indexes
        
        # 检查是否为[]格式
        is_bracket_format = index_str.endswith(']')
        
        if is_bracket_format:
            # []格式索引解析
            # 参考: AnalyzeByJSoup.kt 第418-481行
            content = index_str[:-1]  # 移除结尾的]
            
            # 逆向遍历解析
            i = len(content) - 1
            while i >= 0:
                char = content[i]
                
                if char == ' ':
                    i -= 1
                    continue
                
                if char in '0123456789':
                    # 解析数字
                    num_str = ''
                    is_negative = False
                    while i >= 0 and content[i] in '0123456789-':
                        if content[i] == '-':
                            is_negative = True
                        else:
                            num_str = content[i] + num_str
                        i -= 1
                    
                    if num_str:
                        num = int(num_str)
                        if is_negative:
                            num = -num
                        indexes.append(num)
                
                elif char == ':':
                    # 区间分隔符
                    i -= 1
                    # 继续解析下一个数字
                
                elif char == ',':
                    # 索引分隔符
                    i -= 1
                
                elif char == '!':
                    # 排除模式
                    indexes.append('!')
                    i -= 1
                
                elif char == '[':
                    # 结束
                    break
                else:
                    i -= 1
            
            # 反转索引列表（因为是逆向遍历）
            indexes.reverse()
        
        else:
            # 阅读原有写法解析
            # 参考: AnalyzeByJSoup.kt 第482-506行
            index_str = index_str.lstrip('.')
            is_exclude = index_str.startswith('!')
            if is_exclude:
                index_str = index_str[1:]
            
            # 按冒号分割
            parts = index_str.split(':')
            
            if len(parts) == 1:
                # 单个索引
                try:
                    indexes.append(int(parts[0]))
                except:
                    pass
            elif len(parts) >= 2:
                # 范围
                try:
                    start = int(parts[0]) if parts[0] else 0
                    end = int(parts[1]) if parts[1] else -1
                    step = int(parts[2]) if len(parts) > 2 and parts[2] else 1
                    
                    if end < 0:
                        # 负数结尾表示到末尾
                        indexes = list(range(start, 10000, step))
                    else:
                        indexes = list(range(start, end + 1, step))
                except:
                    pass
            
            if is_exclude:
                indexes.insert(0, '!')
        
        return indexes
    
    def _extract_value(self, elements: List, extract_type: str) -> str:
        if not elements:
            return ""
        
        if extract_type == "text":
            texts = []
            for e in elements:
                if hasattr(e, 'get_text'):
                    texts.append(e.get_text(strip=True))
                elif e:
                    texts.append(str(e))
            return '\n'.join(texts)
        elif extract_type == "html":
            return '\n'.join(str(e) for e in elements if e)
        elif extract_type == "href":
            for e in elements:
                if hasattr(e, 'get'):
                    href = e.get('href', '')
                    if href:
                        if self.base_url and not href.startswith('http'):
                            return urljoin(self.base_url, href)
                        return href
            return ""
        elif extract_type == "src":
            for e in elements:
                if hasattr(e, 'get'):
                    src = e.get('src', '')
                    if src:
                        if self.base_url and not src.startswith('http'):
                            return urljoin(self.base_url, src)
                        return src
            return ""
        
        return ""
    
    def _make_up_rule(self, source_rule: SourceRule, result: Any) -> SourceRule:
        """
        按照Legado源码实现规则变量替换
        参考: AnalyzeRule.kt 第714-760行
        
        处理:
        1. ##分隔符（正则替换）
        2. {{$.field}}模板变量替换
        3. {{js_expression}}JavaScript表达式替换
        """
        rule = source_rule.rule
        
        # 第一步：处理{{...}}模板变量
        # 参考: AnalyzeRule.kt 第732-749行
        if '{{' in rule and '}}' in rule:
            import re
            
            def replace_template(match):
                template_content = match.group(1).strip()
                
                # 检查是否是$.field格式（简单字段访问）
                if template_content.startswith('$.'):
                    # 简单字段访问
                    field_name = template_content[2:]
                    if isinstance(result, dict):
                        value = result.get(field_name, '')
                        return str(value) if value else ""
                    elif isinstance(result, list) and len(result) > 0:
                        return str(result[0]) if result[0] else ""
                    else:
                        return match.group(0)
                
                # 检查是否是JavaScript表达式（包含函数调用或操作符）
                # 例如: baseUrl.replace('list-', '-')
                if any(op in template_content for op in ['.', '(', ')', '+', '-', '*', '/', 'replace', 'substring', 'split']):
                    # JavaScript表达式
                    try:
                        js_result = self._eval_js(template_content, result)
                        return str(js_result) if js_result else ""
                    except:
                        return match.group(0)
                
                # 直接键名访问
                if isinstance(result, dict):
                    value = result.get(template_content, '')
                    return str(value) if value else ""
                elif isinstance(result, list) and len(result) > 0:
                    return str(result[0]) if result[0] else ""
                else:
                    return match.group(0)
            
            rule = re.sub(r'\{\{([^}]+)\}\}', replace_template, rule)
        
        # 第二步：处理##分隔符（正则替换）
        # 参考: AnalyzeRule.kt 第761-772行
        rule_parts = rule.split("##")
        source_rule.rule = rule_parts[0].strip()
        
        if len(rule_parts) > 1:
            source_rule.replace_regex = rule_parts[1]
        if len(rule_parts) > 2:
            source_rule.replacement = rule_parts[2]
        if len(rule_parts) > 3:
            source_rule.replace_first = True
        
        return source_rule
    
    def _apply_legado_replace_regex(self, result: str, replace_regex: str, replacement: str, replace_first: bool) -> str:
        """
        按照Legado源码实现正则替换逻辑
        参考: AnalyzeRule.kt 第482-506行
        
        规则:
        - 如果replaceFirst为True: 获取第一个匹配到的结果并进行替换
          - 如果匹配成功: 返回matcher.group(0).replaceFirst(regex, replacement)
          - 如果匹配失败: 返回空字符串
        - 如果replaceFirst为False: 全局替换
          - 如果regex有效: 返回result.replace(regex, replacement)
          - 如果regex无效: 返回result.replace(replaceRegex, replacement) (字面替换)
        """
        if not replace_regex:
            return result
        
        result_str = str(result) if not isinstance(result, str) else result
        
        try:
            if replace_first:
                # ##match##replace### 获取第一个匹配到的结果并进行替换
                match = re.search(replace_regex, result_str)
                if match:
                    # 获取匹配到的内容，然后进行替换
                    matched_text = match.group(0)
                    return matched_text.replace(replace_regex, replacement, 1) if replacement else matched_text
                else:
                    return ""
            else:
                # ##match##replace 替换
                try:
                    return re.sub(replace_regex, replacement, result_str)
                except:
                    # 如果正则无效，进行字面替换
                    return result_str.replace(replace_regex, replacement)
        except Exception:
            return result_str

    def _apply_replace_regex(self, result: Any, source_rule: SourceRule) -> str:
        result_str = str(result) if not isinstance(result, str) else result
        
        if not source_rule.replace_regex:
            return result_str
        
        try:
            if source_rule.replace_first:
                match = re.search(source_rule.replace_regex, result_str)
                if match:
                    if source_rule.replacement:
                        return re.sub(source_rule.replace_regex, source_rule.replacement, result_str, count=1)
                    return match.group(0)
                return source_rule.replacement
            else:
                return re.sub(source_rule.replace_regex, source_rule.replacement, result_str)
        except Exception:
            return result_str
    
    def _eval_js(self, js_code: str, result: Any) -> Any:
        """执行JS代码 - 使用真实的JS引擎"""
        try:
            from debugger.js_engine import execute_js
            
            result_str = str(result) if not isinstance(result, str) else result
            escaped_result = result_str.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r')
            
            escaped_base_url = self.base_url.replace('\\', '\\\\').replace('"', '\\"') if self.base_url else ""
            
            context = {
                'result': result_str,
                'body': result_str,
                'src': result_str,
                'baseUrl': self.base_url,
            }
            
            # 判断是表达式还是语句块
            js_code_trimmed = js_code.strip()
            
            # 如果是语句块（包含换行、if/for/while、或以分号结尾的多语句）
            is_statement_block = (
                '\n' in js_code_trimmed or
                js_code_trimmed.startswith('if ') or
                js_code_trimmed.startswith('if(') or
                js_code_trimmed.startswith('for ') or
                js_code_trimmed.startswith('for(') or
                js_code_trimmed.startswith('while ') or
                js_code_trimmed.startswith('while(') or
                js_code_trimmed.startswith('try ') or
                js_code_trimmed.startswith('try{') or
                js_code_trimmed.startswith('function ') or
                js_code_trimmed.startswith('function(') or
                js_code_trimmed.startswith('{') or
                js_code_trimmed.startswith('var ') or
                js_code_trimmed.startswith('let ') or
                js_code_trimmed.startswith('const ')
            )
            
            if is_statement_block:
                # 语句块：直接执行，result 变量已在上下文中
                wrapped_js = f'''
result = "{escaped_result}";
src = result;
body = result;
baseUrl = "{escaped_base_url}";

// 执行用户JS代码
{js_code_trimmed}

// 清空body，防止JS引擎用body覆盖result
body = null;
'''
            else:
                # 表达式：包装为 result = expression
                wrapped_js = f'''
result = "{escaped_result}";
src = result;
body = result;
baseUrl = "{escaped_base_url}";

// 执行用户JS表达式
result = {js_code_trimmed};

// 清空body，防止JS引擎用body覆盖result
body = null;
'''
            
            js_result = execute_js(wrapped_js, context, self.js_lib)
            
            if js_result.success:
                return js_result.result
            else:
                return result
        except Exception as e:
            return result
    
    def _eval_web_js(self, js_code: str, result: Any) -> Any:
        """执行WebJS代码"""
        return self._eval_js(js_code, result)
    
    def put(self, key: str, value: str) -> str:
        self.variables[key] = value
        return value
    
    def get(self, key: str) -> str:
        return self.variables.get(key, "")
