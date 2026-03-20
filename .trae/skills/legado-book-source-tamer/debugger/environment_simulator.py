"""
Reading Environment Simulator - 阅读环境模拟模型
精确复制真实阅读环境的目录结构、文件类型和数据关系

功能说明：
- 模拟Legado阅读APP的运行环境
- 提供书源测试的沙箱环境
- 支持多种书源类型的测试
"""

import json
import os
import re
import time
import hashlib
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from enum import Enum


class BookSourceType(Enum):
    """书源类型枚举"""
    TEXT = 0
    AUDIO = 1
    IMAGE = 2
    FILE = 3
    VIDEO = 4


class TestStatus(Enum):
    """测试状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class TestCase:
    """测试用例"""
    id: str
    name: str
    description: str
    source_type: BookSourceType
    source_path: str
    priority: int = 1
    tags: List[str] = field(default_factory=list)
    expected_results: Dict[str, Any] = field(default_factory=dict)
    actual_results: Dict[str, Any] = field(default_factory=dict)
    status: TestStatus = TestStatus.PENDING
    error_message: Optional[str] = None
    duration_ms: float = 0


@dataclass
class TestSuite:
    """测试套件"""
    name: str
    description: str
    test_cases: List[TestCase] = field(default_factory=list)
    setup_time: float = 0
    teardown_time: float = 0
    total_duration: float = 0


@dataclass
class EnvironmentConfig:
    """环境配置"""
    project_root: Path
    legado_source_path: Path
    debugger_path: Path
    assets_path: Path
    test_sources_path: Path
    output_path: Path
    cache_enabled: bool = True
    timeout_seconds: int = 30
    max_retries: int = 3
    debug_mode: bool = False


class ReadingEnvironmentSimulator:
    """
    阅读环境模拟器
    
    模拟Legado阅读APP的运行环境，提供完整的测试能力
    """
    
    def __init__(self, project_root: Optional[str] = None):
        """
        初始化阅读环境模拟器
        
        Args:
            project_root: 项目根目录路径
        """
        self.project_root = self._detect_project_root(project_root)
        self.config = self._build_config()
        self.test_suites: List[TestSuite] = []
        self.test_results: Dict[str, Any] = {}
        self._cache: Dict[str, Any] = {}
    
    def _detect_project_root(self, project_root: Optional[str]) -> Path:
        """检测项目根目录"""
        if project_root:
            return Path(project_root).resolve()
        
        cwd = Path.cwd()
        if self._is_project_root(cwd):
            return cwd
        
        script_dir = Path(__file__).parent
        for parent in script_dir.parents:
            if self._is_project_root(parent):
                return parent
        
        return cwd
    
    def _is_project_root(self, path: Path) -> bool:
        """检查是否为项目根目录"""
        indicators = ['.trae', 'assets', 'debugger', 'legado_source']
        return any((path / ind).exists() for ind in indicators)
    
    def _build_config(self) -> EnvironmentConfig:
        """构建环境配置"""
        return EnvironmentConfig(
            project_root=self.project_root,
            legado_source_path=self.project_root / 'legado_source',
            debugger_path=self.project_root / 'debugger',
            assets_path=self.project_root / 'assets',
            test_sources_path=self.project_root,
            output_path=self.project_root,
            cache_enabled=True,
            timeout_seconds=30,
            max_retries=3,
            debug_mode=False,
        )
    
    def load_test_source(self, source_path: str) -> Dict[str, Any]:
        """
        加载测试书源
        
        Args:
            source_path: 书源文件路径
        
        Returns:
            书源数据字典
        """
        path = Path(source_path)
        if not path.is_absolute():
            path = self.config.test_sources_path / source_path
        
        if not path.exists():
            raise FileNotFoundError(f"测试书源文件不存在: {path}")
        
        cache_key = f"source_{path}"
        if self.config.cache_enabled and cache_key in self._cache:
            return self._cache[cache_key]
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        data = json.loads(content)
        
        if isinstance(data, list):
            if len(data) == 0:
                raise ValueError(f"书源文件为空: {path}")
            data = data[0]
        
        if self.config.cache_enabled:
            self._cache[cache_key] = data
        
        return data
    
    def analyze_source_type(self, source: Dict[str, Any]) -> BookSourceType:
        """
        分析书源类型
        
        Args:
            source: 书源数据
        
        Returns:
            书源类型枚举值
        """
        source_type = source.get('bookSourceType', 0)
        
        if isinstance(source_type, int):
            return BookSourceType(source_type)
        
        return BookSourceType.TEXT
    
    def analyze_source_complexity(self, source: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析书源复杂度
        
        Args:
            source: 书源数据
        
        Returns:
            复杂度分析结果
        """
        complexity = {
            'level': 'simple',
            'score': 0,
            'features': [],
            'warnings': [],
        }
        
        score = 0
        features = []
        warnings = []
        
        if source.get('jsLib'):
            score += 20
            features.append('jsLib')
            js_lib = source['jsLib']
            if len(js_lib) > 1000:
                score += 10
                complexity['level'] = 'complex'
        
        for rule_name in ['ruleSearch', 'ruleBookInfo', 'ruleToc', 'ruleContent']:
            rule = source.get(rule_name, {})
            if isinstance(rule, dict):
                for field_name, field_value in rule.items():
                    if field_value and '@js' in str(field_value):
                        score += 5
                        features.append(f'{rule_name}.{field_name}:js')
                    if field_value and '##' in str(field_value):
                        score += 2
                        features.append(f'{rule_name}.{field_name}:regex')
        
        if source.get('loginUrl'):
            score += 10
            features.append('login')
        
        if source.get('loginCheckJs'):
            score += 15
            features.append('loginCheck')
        
        if source.get('coverDecodeJs'):
            score += 10
            features.append('coverDecode')
        
        if source.get('header'):
            score += 3
            features.append('customHeader')
        
        search_url = source.get('searchUrl', '')
        if 'POST' in search_url or 'method' in search_url:
            score += 5
            features.append('POST')
        
        if 'charset' in search_url and 'gbk' in search_url.lower():
            score += 3
            features.append('GBK')
        
        if score > 50:
            complexity['level'] = 'complex'
        elif score > 20:
            complexity['level'] = 'medium'
        else:
            complexity['level'] = 'simple'
        
        complexity['score'] = score
        complexity['features'] = features
        complexity['warnings'] = warnings
        
        return complexity
    
    def create_test_case(
        self,
        source_path: str,
        test_name: Optional[str] = None,
        priority: int = 1,
        tags: Optional[List[str]] = None
    ) -> TestCase:
        """
        创建测试用例
        
        Args:
            source_path: 书源文件路径
            test_name: 测试名称
            priority: 优先级
            tags: 标签列表
        
        Returns:
            测试用例对象
        """
        source = self.load_test_source(source_path)
        source_type = self.analyze_source_type(source)
        complexity = self.analyze_source_complexity(source)
        
        source_name = source.get('bookSourceName', 'Unknown')
        
        if test_name is None:
            test_name = f"测试_{source_name}"
        
        test_id = hashlib.md5(f"{source_path}_{test_name}".encode()).hexdigest()[:8]
        
        expected_results = {
            'search': {'min_results': 1},
            'book_info': {'required_fields': ['name', 'author']},
            'toc': {'min_chapters': 1},
            'content': {'min_length': 100},
        }
        
        if complexity['level'] == 'complex':
            expected_results['search']['timeout_ms'] = 5000
            expected_results['content']['timeout_ms'] = 3000
        
        return TestCase(
            id=test_id,
            name=test_name,
            description=f"测试书源: {source_name} (复杂度: {complexity['level']})",
            source_type=source_type,
            source_path=source_path,
            priority=priority,
            tags=tags or [],
            expected_results=expected_results,
        )
    
    def create_standard_test_suite(self) -> TestSuite:
        """
        创建标准测试套件
        
        包含三种类型的测试用例：
        1. 基础书源 (1.json)
        2. 复杂JS源 (3a.json)
        3. 漫画源 (喜漫漫画.json)
        
        Returns:
            测试套件对象
        """
        test_cases = []
        
        test_configs = [
            {
                'path': '1.json',
                'name': '基础书源测试',
                'priority': 1,
                'tags': ['basic', 'text', 'biquge'],
            },
            {
                'path': '3a.json',
                'name': '复杂JS源测试',
                'priority': 2,
                'tags': ['complex', 'js', 'api'],
            },
            {
                'path': '喜漫漫画.json',
                'name': '漫画源测试',
                'priority': 3,
                'tags': ['manga', 'image', 'decode'],
            },
        ]
        
        for config in test_configs:
            try:
                test_case = self.create_test_case(
                    source_path=config['path'],
                    test_name=config['name'],
                    priority=config['priority'],
                    tags=config['tags'],
                )
                test_cases.append(test_case)
            except FileNotFoundError:
                continue
        
        return TestSuite(
            name="标准书源测试套件",
            description="包含基础书源、复杂JS源和漫画源的标准测试套件",
            test_cases=test_cases,
        )
    
    def run_test_case(self, test_case: TestCase) -> Dict[str, Any]:
        """
        运行单个测试用例
        
        Args:
            test_case: 测试用例对象
        
        Returns:
            测试结果字典
        """
        start_time = time.time()
        result = {
            'test_id': test_case.id,
            'test_name': test_case.name,
            'status': TestStatus.RUNNING.value,
            'start_time': datetime.now().isoformat(),
            'steps': [],
        }
        
        try:
            source = self.load_test_source(test_case.source_path)
            
            from .engine import DebugEngine, BookSource
            
            book_source = BookSource.from_dict(source)
            engine = DebugEngine(book_source)
            
            debug_result = engine.run_full_test("斗破苍穹")
            
            result['debug_result'] = debug_result
            result['status'] = TestStatus.PASSED.value if debug_result.get('overall_success') else TestStatus.FAILED.value
            
            for test_name, test_data in debug_result.get('tests', {}).items():
                result['steps'].append({
                    'name': test_name,
                    'success': test_data.get('success', False),
                    'message': test_data.get('message', ''),
                    'duration_ms': test_data.get('duration_ms', 0),
                })
        
        except Exception as e:
            result['status'] = TestStatus.ERROR.value
            result['error'] = str(e)
        
        result['duration_ms'] = (time.time() - start_time) * 1000
        result['end_time'] = datetime.now().isoformat()
        
        test_case.status = TestStatus(result['status'])
        test_case.actual_results = result
        test_case.duration_ms = result['duration_ms']
        
        return result
    
    def run_test_suite(self, test_suite: TestSuite) -> Dict[str, Any]:
        """
        运行测试套件
        
        Args:
            test_suite: 测试套件对象
        
        Returns:
            测试结果字典
        """
        suite_start = time.time()
        
        results = {
            'suite_name': test_suite.name,
            'suite_description': test_suite.description,
            'start_time': datetime.now().isoformat(),
            'test_cases': [],
            'summary': {
                'total': len(test_suite.test_cases),
                'passed': 0,
                'failed': 0,
                'error': 0,
                'skipped': 0,
            },
        }
        
        for test_case in test_suite.test_cases:
            case_result = self.run_test_case(test_case)
            results['test_cases'].append(case_result)
            
            status = case_result['status']
            if status == TestStatus.PASSED.value:
                results['summary']['passed'] += 1
            elif status == TestStatus.FAILED.value:
                results['summary']['failed'] += 1
            elif status == TestStatus.ERROR.value:
                results['summary']['error'] += 1
            else:
                results['summary']['skipped'] += 1
        
        results['total_duration_ms'] = (time.time() - suite_start) * 1000
        results['end_time'] = datetime.now().isoformat()
        
        return results
    
    def run_standard_tests(self) -> Dict[str, Any]:
        """
        运行标准测试套件
        
        Returns:
            测试结果字典
        """
        test_suite = self.create_standard_test_suite()
        return self.run_test_suite(test_suite)
    
    def generate_test_report(
        self,
        test_results: Dict[str, Any],
        output_format: str = 'json'
    ) -> Union[str, Dict[str, Any]]:
        """
        生成测试报告
        
        Args:
            test_results: 测试结果
            output_format: 输出格式 ('json' 或 'dict')
        
        Returns:
            测试报告
        """
        report = {
            'report_type': 'Legado书源测试报告',
            'generated_at': datetime.now().isoformat(),
            'environment': {
                'project_root': str(self.config.project_root),
                'debugger_version': '2.1.0',
            },
            'results': test_results,
            'analysis': self._analyze_test_results(test_results),
        }
        
        if output_format == 'json':
            return json.dumps(report, ensure_ascii=False, indent=4)
        
        return report
    
    def _analyze_test_results(self, test_results: Dict[str, Any]) -> Dict[str, Any]:
        """分析测试结果"""
        analysis = {
            'overall_status': 'unknown',
            'issues': [],
            'recommendations': [],
            'statistics': {},
        }
        
        summary = test_results.get('summary', {})
        total = summary.get('total', 0)
        passed = summary.get('passed', 0)
        
        if total > 0:
            pass_rate = passed / total
            if pass_rate >= 0.8:
                analysis['overall_status'] = 'good'
            elif pass_rate >= 0.5:
                analysis['overall_status'] = 'acceptable'
            else:
                analysis['overall_status'] = 'poor'
            
            analysis['statistics']['pass_rate'] = f"{pass_rate * 100:.1f}%"
        
        for case in test_results.get('test_cases', []):
            if case['status'] != TestStatus.PASSED.value:
                issue = {
                    'test_name': case['test_name'],
                    'status': case['status'],
                    'error': case.get('error', 'Unknown error'),
                }
                analysis['issues'].append(issue)
        
        if analysis['issues']:
            analysis['recommendations'].append('建议检查失败的书源规则配置')
        
        return analysis


def create_environment(project_root: Optional[str] = None) -> ReadingEnvironmentSimulator:
    """
    创建阅读环境模拟器
    
    Args:
        project_root: 项目根目录
    
    Returns:
        阅读环境模拟器实例
    """
    return ReadingEnvironmentSimulator(project_root)


def run_quick_test(source_path: str, keyword: str = "斗破苍穹") -> Dict[str, Any]:
    """
    快速测试书源
    
    Args:
        source_path: 书源文件路径
        keyword: 搜索关键词
    
    Returns:
        测试结果
    """
    simulator = ReadingEnvironmentSimulator()
    source = simulator.load_test_source(source_path)
    
    from .engine import DebugEngine, BookSource
    
    book_source = BookSource.from_dict(source)
    engine = DebugEngine(book_source)
    
    return engine.run_full_test(keyword)
