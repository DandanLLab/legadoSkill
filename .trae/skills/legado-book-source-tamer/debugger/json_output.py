"""
JSON Output Utility - 书源JSON输出工具
负责将书源JSON输出到项目根目录

职责说明：
- 输出路径定位准确无误，严格指向项目根目录
- 文件格式完全符合JSON规范
- UTF-8字符编码和4空格标准缩进
- 跨操作系统兼容性（Windows/macOS/Linux）
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class JsonOutputError(Exception):
    """JSON输出错误"""
    pass


class JsonOutputUtility:
    """JSON输出工具类"""
    
    def __init__(self, project_root: Optional[str] = None):
        """
        初始化JSON输出工具
        
        Args:
            project_root: 项目根目录路径，如果为None则自动检测
        """
        self.project_root = self._detect_project_root(project_root)
        self._validate_project_root()
    
    def _detect_project_root(self, project_root: Optional[str]) -> Path:
        """
        检测项目根目录
        
        优先级：
        1. 用户指定的路径
        2. 当前工作目录
        3. 脚本所在目录的上级目录
        """
        if project_root:
            return Path(project_root).resolve()
        
        cwd = Path.cwd()
        if self._is_project_root(cwd):
            return cwd
        
        script_dir = Path(__file__).parent
        parent_dir = script_dir.parent
        if self._is_project_root(parent_dir):
            return parent_dir
        
        return cwd
    
    def _is_project_root(self, path: Path) -> bool:
        """检查路径是否为项目根目录"""
        indicators = [
            '.trae',
            'assets',
            'debugger',
            'legado_source',
        ]
        
        for indicator in indicators:
            if (path / indicator).exists():
                return True
        return False
    
    def _validate_project_root(self):
        """验证项目根目录是否有效"""
        if not self.project_root.exists():
            raise JsonOutputError(f"项目根目录不存在: {self.project_root}")
        
        if not self.project_root.is_dir():
            raise JsonOutputError(f"项目根目录不是目录: {self.project_root}")
    
    def _sanitize_filename(self, name: str) -> str:
        """
        清理文件名中的非法字符
        
        Args:
            name: 原始名称
        
        Returns:
            清理后的安全文件名
        """
        illegal_chars = r'[<>:"/\\|?*\x00-\x1f]'
        safe_name = re.sub(illegal_chars, '_', name)
        safe_name = safe_name.strip(' .')
        return safe_name or 'unknown'
    
    def _generate_filename(self, source_name: str, date: Optional[str] = None) -> str:
        """
        生成符合规范的文件名
        
        格式：book_source_{书源名称}_{日期}.json
        
        Args:
            source_name: 书源名称
            date: 日期字符串，如果为None则使用当前日期
        
        Returns:
            符合规范的文件名
        """
        safe_name = self._sanitize_filename(source_name)
        
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        
        return f"book_source_{safe_name}_{date}.json"
    
    def _validate_json_content(self, content: Any) -> List[Dict[str, Any]]:
        """
        验证JSON内容是否符合Legado书源规范
        
        Args:
            content: 要验证的内容
        
        Returns:
            验证后的书源列表
        
        Raises:
            JsonOutputError: 如果内容不符合规范
        """
        if isinstance(content, str):
            try:
                content = json.loads(content)
            except json.JSONDecodeError as e:
                raise JsonOutputError(f"JSON解析失败: {e}")
        
        if isinstance(content, dict):
            content = [content]
        
        if not isinstance(content, list):
            raise JsonOutputError("内容必须是字典或列表")
        
        if len(content) == 0:
            raise JsonOutputError("书源列表不能为空")
        
        for i, source in enumerate(content):
            if not isinstance(source, dict):
                raise JsonOutputError(f"书源 {i} 不是字典类型")
            
            required_fields = ['bookSourceUrl', 'bookSourceName']
            for field in required_fields:
                if field not in source:
                    raise JsonOutputError(f"书源 {i} 缺少必填字段: {field}")
        
        return content
    
    def _format_json(self, content: Any) -> str:
        """
        格式化JSON内容
        
        - UTF-8字符编码
        - 4空格标准缩进
        - 确保中文不被转义
        
        Args:
            content: 要格式化的内容
        
        Returns:
            格式化后的JSON字符串
        """
        return json.dumps(
            content,
            ensure_ascii=False,
            indent=4,
            sort_keys=False
        )
    
    def get_output_path(self, source_name: str, date: Optional[str] = None) -> Path:
        """
        获取输出文件的完整路径
        
        Args:
            source_name: 书源名称
            date: 日期字符串
        
        Returns:
            输出文件的完整路径
        """
        filename = self._generate_filename(source_name, date)
        return self.project_root / filename
    
    def save_book_source(
        self,
        content: Union[str, Dict, List],
        source_name: Optional[str] = None,
        date: Optional[str] = None,
        overwrite: bool = False
    ) -> Dict[str, Any]:
        """
        保存书源JSON到项目根目录
        
        Args:
            content: 书源内容（字符串、字典或列表）
            source_name: 书源名称（如果为None则从内容中提取）
            date: 日期字符串
            overwrite: 是否覆盖已存在的文件
        
        Returns:
            保存结果字典，包含：
            - success: 是否成功
            - path: 文件路径
            - message: 结果消息
            - size: 文件大小（字节）
        
        Raises:
            JsonOutputError: 如果保存失败
        """
        validated_content = self._validate_json_content(content)
        
        if source_name is None:
            source_name = validated_content[0].get('bookSourceName', 'unknown')
        
        output_path = self.get_output_path(source_name, date)
        
        if output_path.exists() and not overwrite:
            timestamp = datetime.now().strftime('%H%M%S')
            if date:
                output_path = self.get_output_path(source_name, f"{date}_{timestamp}")
            else:
                date_str = datetime.now().strftime('%Y%m%d')
                output_path = self.get_output_path(source_name, f"{date_str}_{timestamp}")
        
        formatted_json = self._format_json(validated_content)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
        except IOError as e:
            raise JsonOutputError(f"文件写入失败: {e}")
        
        file_size = output_path.stat().st_size
        
        return {
            'success': True,
            'path': str(output_path),
            'absolute_path': str(output_path.absolute()),
            'relative_path': str(output_path.relative_to(self.project_root)),
            'message': f'书源JSON已保存到: {output_path}',
            'size': file_size,
            'source_name': source_name,
            'sources_count': len(validated_content),
        }
    
    def save_debug_result(
        self,
        debug_result: Dict[str, Any],
        source_name: Optional[str] = None,
        date: Optional[str] = None,
        include_debug_log: bool = False
    ) -> Dict[str, Any]:
        """
        保存调试结果到项目根目录
        
        Args:
            debug_result: 调试结果字典
            source_name: 书源名称
            date: 日期字符串
            include_debug_log: 是否包含调试日志
        
        Returns:
            保存结果字典
        """
        if source_name is None:
            source_name = debug_result.get('book_source', 'debug_result')
        
        if not include_debug_log and 'debug_log' in debug_result:
            debug_result = {k: v for k, v in debug_result.items() if k != 'debug_log'}
        
        safe_name = self._sanitize_filename(source_name)
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        
        filename = f"debug_result_{safe_name}_{date}.json"
        output_path = self.project_root / filename
        
        formatted_json = self._format_json(debug_result)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
        except IOError as e:
            raise JsonOutputError(f"文件写入失败: {e}")
        
        file_size = output_path.stat().st_size
        
        return {
            'success': True,
            'path': str(output_path),
            'absolute_path': str(output_path.absolute()),
            'message': f'调试结果已保存到: {output_path}',
            'size': file_size,
        }
    
    def save_test_report(
        self,
        test_report: Dict[str, Any],
        report_name: str,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        保存测试报告到项目根目录
        
        Args:
            test_report: 测试报告字典
            report_name: 报告名称
            date: 日期字符串
        
        Returns:
            保存结果字典
        """
        safe_name = self._sanitize_filename(report_name)
        if date is None:
            date = datetime.now().strftime('%Y%m%d')
        
        filename = f"test_report_{safe_name}_{date}.json"
        output_path = self.project_root / filename
        
        formatted_json = self._format_json(test_report)
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(formatted_json)
        except IOError as e:
            raise JsonOutputError(f"文件写入失败: {e}")
        
        file_size = output_path.stat().st_size
        
        return {
            'success': True,
            'path': str(output_path),
            'absolute_path': str(output_path.absolute()),
            'message': f'测试报告已保存到: {output_path}',
            'size': file_size,
        }
    
    def list_saved_files(self, pattern: str = "book_source_*.json") -> List[Dict[str, Any]]:
        """
        列出已保存的书源文件
        
        Args:
            pattern: 文件匹配模式
        
        Returns:
            文件信息列表
        """
        files = []
        for file_path in self.project_root.glob(pattern):
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    'name': file_path.name,
                    'path': str(file_path),
                    'size': stat.st_size,
                    'modified_time': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                })
        
        return sorted(files, key=lambda x: x['modified_time'], reverse=True)


def save_book_source_to_root(
    content: Union[str, Dict, List],
    source_name: Optional[str] = None,
    project_root: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    便捷函数：保存书源JSON到项目根目录
    
    Args:
        content: 书源内容
        source_name: 书源名称
        project_root: 项目根目录
        **kwargs: 其他参数传递给save_book_source
    
    Returns:
        保存结果字典
    """
    utility = JsonOutputUtility(project_root)
    return utility.save_book_source(content, source_name, **kwargs)


def validate_json_syntax(content: str) -> Dict[str, Any]:
    """
    验证JSON语法
    
    Args:
        content: JSON字符串
    
    Returns:
        验证结果字典
    """
    try:
        parsed = json.loads(content)
        return {
            'valid': True,
            'message': 'JSON语法正确',
            'type': type(parsed).__name__,
            'size': len(content),
        }
    except json.JSONDecodeError as e:
        return {
            'valid': False,
            'message': f'JSON语法错误: {e}',
            'line': e.lineno,
            'column': e.colno,
        }


def format_book_source_json(content: Union[str, Dict, List]) -> str:
    """
    格式化书源JSON
    
    Args:
        content: 书源内容
    
    Returns:
        格式化后的JSON字符串
    """
    if isinstance(content, str):
        content = json.loads(content)
    
    if isinstance(content, dict):
        content = [content]
    
    return json.dumps(content, ensure_ascii=False, indent=4)
