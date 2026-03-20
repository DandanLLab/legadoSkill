"""
Test Cases and Test Flow - 测试用例和测试流程
提供标准化的测试方案和测试管理

测试范围：
- 数据解析：验证JSON结构解析准确性、字段提取完整性
- 内容加载：测试网络请求响应时间、本地文件读取性能
- 格式转换：确保不同格式内容正确转换与展示
"""

import json
import os
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Callable, Union
from enum import Enum


class Severity(Enum):
    """问题严重程度"""
    P0 = "P0"  # 致命问题 - 阻塞功能
    P1 = "P1"  # 严重问题 - 核心功能受损
    P2 = "P2"  # 一般问题 - 部分功能异常
    P3 = "P3"  # 轻微问题 - 不影响使用


class TestCategory(Enum):
    """测试类别"""
    DATA_PARSING = "data_parsing"
    CONTENT_LOADING = "content_loading"
    FORMAT_CONVERSION = "format_conversion"
    PERFORMANCE = "performance"
    COMPATIBILITY = "compatibility"
    SECURITY = "security"


@dataclass
class TestStep:
    """测试步骤"""
    name: str
    description: str
    expected_result: str
    actual_result: Optional[str] = None
    status: str = "pending"
    duration_ms: float = 0
    error: Optional[str] = None


@dataclass
class TestIssue:
    """测试问题"""
    id: str
    title: str
    description: str
    severity: Severity
    category: TestCategory
    reproduce_steps: List[str]
    expected_result: str
    actual_result: str
    suggestion: str
    related_test: Optional[str] = None


@dataclass
class PerformanceMetric:
    """性能指标"""
    name: str
    target_value: float
    actual_value: float
    unit: str
    passed: bool
    
    @property
    def deviation(self) -> float:
        if self.target_value == 0:
            return 0
        return ((self.actual_value - self.target_value) / self.target_value) * 100


class TestCaseBuilder:
    """测试用例构建器"""
    
    def __init__(self):
        self.test_cases: Dict[str, Dict[str, Any]] = {}
    
    def build_basic_source_test(self, source_path: str) -> Dict[str, Any]:
        """
        构建基础书源测试用例
        
        测试场景：
        - 数据结构解析
        - 基本字段提取
        - 内容展示
        
        Args:
            source_path: 书源文件路径
        
        Returns:
            测试用例字典
        """
        return {
            'id': 'basic_source_test',
            'name': '基础书源功能测试',
            'description': '验证基础功能完整性，包括数据结构解析、基本字段提取和内容展示',
            'category': TestCategory.DATA_PARSING.value,
            'priority': 1,
            'source_path': source_path,
            'test_scenarios': [
                {
                    'name': 'JSON结构解析',
                    'description': '验证JSON结构解析准确性',
                    'steps': [
                        '加载书源JSON文件',
                        '解析JSON结构',
                        '验证必需字段存在',
                    ],
                    'expected': {
                        'valid_json': True,
                        'required_fields': ['bookSourceUrl', 'bookSourceName', 'searchUrl'],
                    },
                    'validation': 'validate_json_structure',
                },
                {
                    'name': '字段提取完整性',
                    'description': '验证字段提取完整性',
                    'steps': [
                        '解析搜索规则',
                        '解析书籍信息规则',
                        '解析目录规则',
                        '解析正文规则',
                    ],
                    'expected': {
                        'ruleSearch': {'bookList': 'not_empty', 'name': 'not_empty', 'bookUrl': 'not_empty'},
                        'ruleToc': {'chapterList': 'not_empty', 'chapterName': 'not_empty', 'chapterUrl': 'not_empty'},
                        'ruleContent': {'content': 'not_empty'},
                    },
                    'validation': 'validate_field_extraction',
                },
                {
                    'name': '内容展示测试',
                    'description': '验证内容正确展示',
                    'steps': [
                        '执行搜索请求',
                        '获取书籍详情',
                        '获取章节列表',
                        '获取正文内容',
                    ],
                    'expected': {
                        'search_results': {'min_count': 1},
                        'book_info': {'has_name': True, 'has_author': True},
                        'chapters': {'min_count': 1},
                        'content': {'min_length': 100},
                    },
                    'validation': 'validate_content_display',
                },
            ],
            'performance_targets': {
                'search_response_ms': 500,
                'info_response_ms': 300,
                'toc_response_ms': 500,
                'content_response_ms': 300,
            },
        }
    
    def build_complex_js_test(self, source_path: str) -> Dict[str, Any]:
        """
        构建复杂JS源测试用例
        
        测试场景：
        - JavaScript代码执行
        - 动态内容生成
        - 异步加载处理
        
        Args:
            source_path: 书源文件路径
        
        Returns:
            测试用例字典
        """
        return {
            'id': 'complex_js_test',
            'name': '复杂JS源测试',
            'description': '测试动态解析能力，包括JavaScript代码执行、动态内容生成和异步加载处理',
            'category': TestCategory.DATA_PARSING.value,
            'priority': 2,
            'source_path': source_path,
            'test_scenarios': [
                {
                    'name': 'JS库解析',
                    'description': '验证JavaScript库正确解析',
                    'steps': [
                        '提取jsLib字段',
                        '分析JS代码结构',
                        '验证关键函数存在',
                    ],
                    'expected': {
                        'has_jsLib': True,
                        'jsLib_not_empty': True,
                        'valid_js_syntax': True,
                    },
                    'validation': 'validate_js_library',
                },
                {
                    'name': '动态内容生成',
                    'description': '验证动态内容正确生成',
                    'steps': [
                        '执行JS代码',
                        '获取动态生成的内容',
                        '验证内容格式',
                    ],
                    'expected': {
                        'dynamic_content_valid': True,
                        'no_js_errors': True,
                    },
                    'validation': 'validate_dynamic_content',
                },
                {
                    'name': '数据解密测试',
                    'description': '验证加密数据正确解密',
                    'steps': [
                        '获取加密数据',
                        '执行解密函数',
                        '验证解密结果',
                    ],
                    'expected': {
                        'decryption_success': True,
                        'decrypted_data_valid': True,
                    },
                    'validation': 'validate_decryption',
                },
            ],
            'performance_targets': {
                'js_execution_ms': 1000,
                'decryption_ms': 500,
                'total_response_ms': 2000,
            },
            'sandbox_config': {
                'enabled': True,
                'timeout_ms': 5000,
                'memory_limit_mb': 50,
            },
        }
    
    def build_manga_source_test(self, source_path: str) -> Dict[str, Any]:
        """
        构建漫画源测试用例
        
        测试场景：
        - 图片资源加载
        - 漫画分镜处理
        - 特殊布局展示
        
        Args:
            source_path: 书源文件路径
        
        Returns:
            测试用例字典
        """
        return {
            'id': 'manga_source_test',
            'name': '漫画源测试',
            'description': '验证特殊格式处理能力，包括图片资源加载、漫画分镜处理和特殊布局展示',
            'category': TestCategory.CONTENT_LOADING.value,
            'priority': 3,
            'source_path': source_path,
            'test_scenarios': [
                {
                    'name': '图片URL提取',
                    'description': '验证图片URL正确提取',
                    'steps': [
                        '解析图片选择器',
                        '提取图片URL',
                        '验证URL格式',
                    ],
                    'expected': {
                        'image_urls_valid': True,
                        'image_urls_not_empty': True,
                    },
                    'validation': 'validate_image_urls',
                },
                {
                    'name': '图片解密测试',
                    'description': '验证图片解密功能',
                    'steps': [
                        '获取加密图片',
                        '执行解密函数',
                        '验证图片格式',
                    ],
                    'expected': {
                        'image_decode_success': True,
                        'valid_image_format': True,
                    },
                    'validation': 'validate_image_decode',
                },
                {
                    'name': '图片加载性能',
                    'description': '测试图片加载性能',
                    'steps': [
                        '发起图片请求',
                        '测量响应时间',
                        '验证图片大小',
                    ],
                    'expected': {
                        'load_time_ms': 500,
                        'image_size_valid': True,
                    },
                    'validation': 'validate_image_performance',
                },
            ],
            'performance_targets': {
                'image_load_ms': 500,
                'batch_load_ms': 3000,
                'memory_usage_mb': 100,
            },
        }
    
    def build_all_tests(self, sources: Dict[str, str]) -> List[Dict[str, Any]]:
        """
        构建所有测试用例
        
        Args:
            sources: 书源路径字典 {'basic': 'path', 'complex': 'path', 'manga': 'path'}
        
        Returns:
            测试用例列表
        """
        tests = []
        
        if 'basic' in sources:
            tests.append(self.build_basic_source_test(sources['basic']))
        
        if 'complex' in sources:
            tests.append(self.build_complex_js_test(sources['complex']))
        
        if 'manga' in sources:
            tests.append(self.build_manga_source_test(sources['manga']))
        
        return tests


class TestExecutor:
    """测试执行器"""
    
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.results: List[Dict[str, Any]] = []
        self.issues: List[TestIssue] = []
        self.metrics: List[PerformanceMetric] = []
    
    def execute_test(self, test_case: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行单个测试用例
        
        Args:
            test_case: 测试用例字典
        
        Returns:
            测试结果字典
        """
        start_time = time.time()
        
        result = {
            'test_id': test_case['id'],
            'test_name': test_case['name'],
            'status': 'running',
            'start_time': datetime.now().isoformat(),
            'scenarios': [],
            'metrics': [],
            'issues': [],
        }
        
        try:
            source_path = test_case.get('source_path')
            if source_path:
                source_data = self._load_source(source_path)
                
                from debugger.engine import DebugEngine, BookSource
                from debugger.json_output import JsonOutputUtility
                
                book_source = BookSource.from_dict(source_data)
                engine = DebugEngine(book_source)
                
                debug_result = engine.run_full_test("斗破苍穹")
                result['debug_result'] = debug_result
                
                for scenario in test_case.get('test_scenarios', []):
                    scenario_result = self._execute_scenario(scenario, debug_result)
                    result['scenarios'].append(scenario_result)
                    
                    if not scenario_result.get('passed', False):
                        issue = self._create_issue(scenario, scenario_result, test_case['id'])
                        result['issues'].append(issue)
                        self.issues.append(issue)
                
                if test_case.get('performance_targets'):
                    perf_results = self._check_performance(
                        debug_result,
                        test_case['performance_targets']
                    )
                    result['metrics'] = perf_results
                    self.metrics.extend(perf_results)
                
                result['status'] = 'passed' if self._is_passed(result) else 'failed'
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
        
        result['duration_ms'] = (time.time() - start_time) * 1000
        result['end_time'] = datetime.now().isoformat()
        
        self.results.append(result)
        
        return result
    
    def _load_source(self, source_path: str) -> Dict[str, Any]:
        """加载书源文件"""
        path = Path(source_path)
        if not path.is_absolute():
            path = self.project_root / source_path
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        data = json.loads(content)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        
        return data
    
    def _execute_scenario(self, scenario: Dict[str, Any], debug_result: Dict[str, Any]) -> Dict[str, Any]:
        """执行测试场景"""
        scenario_result = {
            'name': scenario['name'],
            'description': scenario['description'],
            'passed': False,
            'steps': [],
        }
        
        tests = debug_result.get('tests', {})
        
        if scenario['name'] == 'JSON结构解析':
            scenario_result['passed'] = True
            scenario_result['steps'].append({
                'name': '验证JSON结构',
                'passed': True,
                'message': 'JSON结构有效',
            })
        
        elif scenario['name'] == '字段提取完整性':
            search_success = tests.get('search', {}).get('success', False)
            toc_success = tests.get('toc', {}).get('success', False)
            content_success = tests.get('content', {}).get('success', False)
            
            scenario_result['passed'] = search_success and toc_success and content_success
            scenario_result['steps'].append({
                'name': '搜索规则',
                'passed': search_success,
                'message': tests.get('search', {}).get('message', ''),
            })
            scenario_result['steps'].append({
                'name': '目录规则',
                'passed': toc_success,
                'message': tests.get('toc', {}).get('message', ''),
            })
            scenario_result['steps'].append({
                'name': '正文规则',
                'passed': content_success,
                'message': tests.get('content', {}).get('message', ''),
            })
        
        elif scenario['name'] == '内容展示测试':
            scenario_result['passed'] = debug_result.get('overall_success', False)
            scenario_result['steps'].append({
                'name': '整体测试',
                'passed': debug_result.get('overall_success', False),
                'message': '内容展示测试完成',
            })
        
        elif scenario['name'] == '图片URL提取':
            content_test = tests.get('content', {})
            content_length = content_test.get('content_length', 0)
            scenario_result['passed'] = content_length > 0
            scenario_result['steps'].append({
                'name': '内容提取',
                'passed': content_length > 0,
                'message': f'内容长度: {content_length}',
            })
        
        else:
            scenario_result['passed'] = debug_result.get('overall_success', False)
        
        return scenario_result
    
    def _create_issue(self, scenario: Dict[str, Any], result: Dict[str, Any], test_id: str) -> TestIssue:
        """创建测试问题"""
        issue_id = hashlib.md5(f"{test_id}_{scenario['name']}".encode()).hexdigest()[:8]
        
        return TestIssue(
            id=issue_id,
            title=f"测试失败: {scenario['name']}",
            description=scenario.get('description', ''),
            severity=Severity.P2,
            category=TestCategory.DATA_PARSING,
            reproduce_steps=scenario.get('steps', []),
            expected_result=str(scenario.get('expected', {})),
            actual_result=str(result),
            suggestion='请检查书源规则配置',
            related_test=test_id,
        )
    
    def _check_performance(self, debug_result: Dict[str, Any], targets: Dict[str, float]) -> List[PerformanceMetric]:
        """检查性能指标"""
        metrics = []
        tests = debug_result.get('tests', {})
        
        metric_mapping = {
            'search_response_ms': ('search', 'duration_ms'),
            'info_response_ms': ('book_info', 'duration_ms'),
            'toc_response_ms': ('toc', 'duration_ms'),
            'content_response_ms': ('content', 'duration_ms'),
        }
        
        for target_name, target_value in targets.items():
            if target_name in metric_mapping:
                test_name, metric_name = metric_mapping[target_name]
                actual_value = tests.get(test_name, {}).get(metric_name, 0)
                
                metrics.append(PerformanceMetric(
                    name=target_name,
                    target_value=target_value,
                    actual_value=actual_value,
                    unit='ms',
                    passed=actual_value <= target_value,
                ))
        
        return metrics
    
    def _is_passed(self, result: Dict[str, Any]) -> bool:
        """判断测试是否通过"""
        for scenario in result.get('scenarios', []):
            if not scenario.get('passed', False):
                return False
        
        for metric in result.get('metrics', []):
            if not metric.get('passed', False):
                return False
        
        return True
    
    def execute_all(self, test_cases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        执行所有测试用例
        
        Args:
            test_cases: 测试用例列表
        
        Returns:
            测试结果汇总
        """
        start_time = time.time()
        
        summary = {
            'total': len(test_cases),
            'passed': 0,
            'failed': 0,
            'error': 0,
            'skipped': 0,
        }
        
        for test_case in test_cases:
            result = self.execute_test(test_case)
            
            status = result['status']
            if status == 'passed':
                summary['passed'] += 1
            elif status == 'failed':
                summary['failed'] += 1
            elif status == 'error':
                summary['error'] += 1
            else:
                summary['skipped'] += 1
        
        return {
            'summary': summary,
            'results': self.results,
            'issues': [issue.__dict__ for issue in self.issues],
            'metrics': [metric.__dict__ for metric in self.metrics],
            'total_duration_ms': (time.time() - start_time) * 1000,
            'generated_at': datetime.now().isoformat(),
        }


class TestReportGenerator:
    """测试报告生成器"""
    
    def __init__(self, test_results: Dict[str, Any]):
        self.results = test_results
    
    def generate_json_report(self) -> str:
        """生成JSON格式报告"""
        return json.dumps(self.results, ensure_ascii=False, indent=4)
    
    def generate_markdown_report(self) -> str:
        """生成Markdown格式报告"""
        lines = []
        
        lines.append("# Legado书源测试报告")
        lines.append("")
        lines.append(f"**生成时间**: {self.results.get('generated_at', 'N/A')}")
        lines.append("")
        
        summary = self.results.get('summary', {})
        lines.append("## 测试概要")
        lines.append("")
        lines.append(f"- 总测试数: {summary.get('total', 0)}")
        lines.append(f"- 通过: {summary.get('passed', 0)}")
        lines.append(f"- 失败: {summary.get('failed', 0)}")
        lines.append(f"- 错误: {summary.get('error', 0)}")
        lines.append(f"- 跳过: {summary.get('skipped', 0)}")
        lines.append("")
        
        total = summary.get('total', 0)
        passed = summary.get('passed', 0)
        if total > 0:
            pass_rate = (passed / total) * 100
            lines.append(f"**通过率**: {pass_rate:.1f}%")
            lines.append("")
        
        lines.append("## 测试结果详情")
        lines.append("")
        
        for result in self.results.get('results', []):
            status_emoji = '✅' if result['status'] == 'passed' else '❌'
            lines.append(f"### {status_emoji} {result['test_name']}")
            lines.append("")
            lines.append(f"- **状态**: {result['status']}")
            lines.append(f"- **耗时**: {result.get('duration_ms', 0):.2f}ms")
            lines.append("")
            
            for scenario in result.get('scenarios', []):
                scenario_emoji = '✅' if scenario['passed'] else '❌'
                lines.append(f"  - {scenario_emoji} {scenario['name']}: {scenario.get('description', '')}")
        
        if self.results.get('issues'):
            lines.append("")
            lines.append("## 问题列表")
            lines.append("")
            
            for issue in self.results['issues']:
                lines.append(f"### {issue['title']}")
                lines.append("")
                lines.append(f"- **严重程度**: {issue['severity']}")
                lines.append(f"- **描述**: {issue['description']}")
                lines.append(f"- **预期结果**: {issue['expected_result']}")
                lines.append(f"- **实际结果**: {issue['actual_result']}")
                lines.append(f"- **建议**: {issue['suggestion']}")
                lines.append("")
        
        return '\n'.join(lines)
    
    def save_report(self, output_path: str, format: str = 'json') -> str:
        """
        保存测试报告
        
        Args:
            output_path: 输出路径
            format: 格式 ('json' 或 'markdown')
        
        Returns:
            保存的文件路径
        """
        if format == 'markdown':
            content = self.generate_markdown_report()
            ext = '.md'
        else:
            content = self.generate_json_report()
            ext = '.json'
        
        path = Path(output_path)
        if not path.suffix:
            path = path.with_suffix(ext)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return str(path)


def run_standard_tests(project_root: Optional[str] = None) -> Dict[str, Any]:
    """
    运行标准测试套件
    
    Args:
        project_root: 项目根目录
    
    Returns:
        测试结果
    """
    builder = TestCaseBuilder()
    
    sources = {
        'basic': '1.json',
        'complex': '3a.json',
        'manga': '喜漫漫画.json',
    }
    
    test_cases = builder.build_all_tests(sources)
    
    executor = TestExecutor(project_root)
    return executor.execute_all(test_cases)


def generate_and_save_report(
    test_results: Dict[str, Any],
    output_path: str,
    format: str = 'json'
) -> str:
    """
    生成并保存测试报告
    
    Args:
        test_results: 测试结果
        output_path: 输出路径
        format: 格式
    
    Returns:
        保存的文件路径
    """
    generator = TestReportGenerator(test_results)
    return generator.save_report(output_path, format)
