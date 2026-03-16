#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直链上传工具 - Legado Book Source Developer

功能：
1. 验证书源内容是否合规
2. 修正不合规的书源格式
3. 将书源内容上传到图床/云存储
4. 返回可访问的直链
5. 支持多种上传方式配置
6. 美化返回结果
"""

import json
import requests
import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, Tuple, List
from datetime import datetime

# 设置Windows控制台输出编码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class BookSourceValidator:
    """书源JSON验证器"""

    # Legado书源必需字段定义
    REQUIRED_FIELDS = {
        'bookSourceUrl': str,
        'bookSourceName': str,
        'bookSourceType': int,
        'searchUrl': str,
        'ruleSearch': dict,
        'ruleToc': dict,
        'ruleContent': dict
    }

    # 可选字段及其默认值
    OPTIONAL_FIELDS_DEFAULTS = {
        'bookSourceGroup': '',
        'enabled': True,
        'enabledExplore': True,
        'enabledCookieJar': False,
        'loginUrl': '',
        'loginUi': '',
        'loginCheckJs': '',
        'concurrentRate': '',
        'header': '',
        'exploreUrl': '',
        'ruleBookInfo': {},
        'ruleExplore': {},
        'ruleReview': {},
        'bookSourceComment': '',
        'variableComment': ''
    }

    def __init__(self):
        self.errors = []
        self.warnings = []

    def validate_and_fix(self, book_source: Dict[str, Any]) -> Tuple[bool, Dict[str, Any], List[str], List[str]]:
        """
        验证并修正书源JSON

        Args:
            book_source: 书源字典

        Returns:
            (is_valid, fixed_source, errors, warnings): 验证结果、修正后的书源、错误列表、警告列表
        """
        self.errors = []
        self.warnings = []

        fixed_source = book_source.copy()

        # 1. 检查是否是单个书源对象
        if not isinstance(fixed_source, dict):
            self.errors.append(f"书源必须是对象类型，当前类型: {type(fixed_source).__name__}")
            return False, fixed_source, self.errors, self.warnings

        # 2. 检查并添加必需字段
        for field, expected_type in self.REQUIRED_FIELDS.items():
            if field not in fixed_source:
                if field == 'bookSourceType':
                    fixed_source[field] = 0
                    self.warnings.append(f"添加缺失的必需字段: {field} = 0")
                elif field in ['ruleSearch', 'ruleToc', 'ruleContent']:
                    fixed_source[field] = {}
                    self.warnings.append(f"添加缺失的必需字段: {field} = {{}}")
                elif field == 'searchUrl':
                    fixed_source[field] = ''
                    self.warnings.append(f"添加缺失的必需字段: {field} = ''")
                else:
                    self.errors.append(f"缺少必需字段: {field}")
            else:
                # 检查类型是否正确
                actual_value = fixed_source[field]
                if not isinstance(actual_value, expected_type):
                    if expected_type == int and isinstance(actual_value, str):
                        # 尝试转换字符串到整数
                        try:
                            fixed_source[field] = int(actual_value)
                            self.warnings.append(f"修正字段类型: {field} 从字符串转换为整数")
                        except ValueError:
                            self.errors.append(
                                f"字段类型错误: {field} "
                                f"(期望: {expected_type.__name__}, 实际: {type(actual_value).__name__})"
                            )
                    elif expected_type == str and isinstance(actual_value, int):
                        # 整数到字符串可以接受
                        fixed_source[field] = str(actual_value)
                        self.warnings.append(f"修正字段类型: {field} 从整数转换为字符串")
                    elif actual_value is None:
                        # None值使用默认值
                        if field in self.OPTIONAL_FIELDS_DEFAULTS:
                            fixed_source[field] = self.OPTIONAL_FIELDS_DEFAULTS[field]
                            self.warnings.append(f"将None字段 {field} 设置为默认值")
                        else:
                            self.errors.append(f"字段 {field} 不能为None")
                    else:
                        self.errors.append(
                            f"字段类型错误: {field} "
                            f"(期望: {expected_type.__name__}, 实际: {type(actual_value).__name__})"
                        )

        # 3. 检查并添加可选字段
        for field, default_value in self.OPTIONAL_FIELDS_DEFAULTS.items():
            if field not in fixed_source:
                fixed_source[field] = default_value
                self.warnings.append(f"添加缺失的可选字段: {field} = {repr(default_value)}")

        # 4. 验证书源名称和URL
        if not fixed_source.get('bookSourceName'):
            self.errors.append("bookSourceName 不能为空")
        elif not isinstance(fixed_source['bookSourceName'], str):
            self.errors.append(f"bookSourceName 必须是字符串类型")

        if not fixed_source.get('bookSourceUrl'):
            self.errors.append("bookSourceUrl 不能为空")
        elif not isinstance(fixed_source['bookSourceUrl'], str):
            self.errors.append(f"bookSourceUrl 必须是字符串类型")

        # 5. 验证规则对象
        self._validate_rule_search(fixed_source.get('ruleSearch', {}))
        self._validate_rule_toc(fixed_source.get('ruleToc', {}))
        self._validate_rule_content(fixed_source.get('ruleContent', {}))

        return len(self.errors) == 0, fixed_source, self.errors, self.warnings

    def _validate_rule_search(self, rule_search: Dict[str, Any]):
        """验证搜索规则"""
        if not isinstance(rule_search, dict):
            self.errors.append("ruleSearch 必须是对象类型")
            return

        # bookList 和 bookUrl 是必需的
        if not rule_search.get('bookList'):
            self.errors.append("ruleSearch.bookList 不能为空")

        if not rule_search.get('bookUrl'):
            self.errors.append("ruleSearch.bookUrl 不能为空")

        # name 是强烈推荐的
        if not rule_search.get('name'):
            self.warnings.append("建议添加 ruleSearch.name 字段")

    def _validate_rule_toc(self, rule_toc: Dict[str, Any]):
        """验证目录规则"""
        if not isinstance(rule_toc, dict):
            self.errors.append("ruleToc 必须是对象类型")
            return

        # chapterList, chapterName, chapterUrl 是必需的
        if not rule_toc.get('chapterList'):
            self.errors.append("ruleToc.chapterList 不能为空")

        if not rule_toc.get('chapterName'):
            self.errors.append("ruleToc.chapterName 不能为空")

        if not rule_toc.get('chapterUrl'):
            self.errors.append("ruleToc.chapterUrl 不能为空")

    def _validate_rule_content(self, rule_content: Dict[str, Any]):
        """验证正文规则"""
        if not isinstance(rule_content, dict):
            self.errors.append("ruleContent 必须是对象类型")
            return

        # content 是必需的
        if not rule_content.get('content'):
            self.errors.append("ruleContent.content 不能为空")


class BookSourceUploader:
    """书源直链上传器"""

    def __init__(self):
        self.references_dir = Path(__file__).parent.parent / 'references'
        self.validator = BookSourceValidator()

    def upload_book_source(
        self,
        book_source_json: Dict[str, Any],
        upload_config: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """
        上传书源内容到图床

        Args:
            book_source_json: 书源JSON对象
            upload_config: 上传配置（如果为None则使用默认配置）

        Returns:
            (success, result): 成功标志和结果字典
        """
        # 步骤1: 验证书源内容并尝试修正
        is_valid, fixed_source, errors, warnings = self.validator.validate_and_fix(book_source_json)

        # 显示验证结果
        self._print_validation_result(is_valid, errors, warnings)

        # 如果验证失败,不执行上传
        if not is_valid:
            return False, {
                'error': '书源验证失败',
                'details': '书源内容不符合Legado标准格式',
                'errors': errors,
                'warnings': warnings
            }

        # 使用修正后的书源进行上传
        book_source_json = fixed_source

        # 保存验证信息,用于后续显示
        validation_info = {
            'is_valid': is_valid,
            'warnings_count': len(warnings),
            'warnings': warnings
        }

        # 步骤2: 默认上传配置
        if upload_config is None:
            upload_config = {
                "compress": False,
                "downloadUrlRule": "$.data.links.url",
                "summary": "鲸落图床",
                "uploadUrl": "https://tu.406np.xyz/api/v1/upload",
                "method": "POST",
                "headers": {"Accept": "application/json"},
                "body": {"file": "fileRequest", "show": "1"},
                "type": "multipart/form-data"
            }

        try:
            # 步骤3: 提取上传配置
            upload_url = upload_config.get('uploadUrl', '')
            method = upload_config.get('method', 'POST').upper()
            headers = upload_config.get('headers', {})
            body_config = upload_config.get('body', {})
            content_type = upload_config.get('type', 'multipart/form-data')
            download_rule = upload_config.get('downloadUrlRule', '$..url')

            if not upload_url:
                return False, {'error': '上传URL为空', 'details': 'uploadUrl配置缺失'}

            # 准备上传内容 - 必须是数组格式
            # Legado要求书源必须是JSON数组格式 [{...}]，而不是单个对象 {...}
            book_source_array = [book_source_json]
            book_source_content = json.dumps(book_source_array, ensure_ascii=False, indent=2)
            book_source_name = book_source_json.get('bookSourceName', 'unknown') + '.json'

            # 验证JSON格式
            is_valid_format, format_message = self._validate_json_array_format(book_source_content)
            print(f"\n📋 JSON格式检查:")
            print(f"  {format_message}")

            # 构建请求参数
            files = {}
            data = {}

            for key, value in body_config.items():
                if value == 'fileRequest':
                    # 文件字段 - 上传原始JSON内容
                    files[key] = (book_source_name, book_source_content, 'application/json')
                else:
                    # 普通表单字段
                    data[key] = value

            # 发送请求
            if method == 'POST':
                if content_type == 'multipart/form-data':
                    response = requests.post(upload_url, headers=headers, files=files, data=data, timeout=30)
                else:
                    # JSON格式
                    headers['Content-Type'] = 'application/json'
                    json_body = {}
                    for key, value in body_config.items():
                        if value == 'fileRequest':
                            json_body[key] = book_source_content
                        else:
                            json_body[key] = value
                    response = requests.post(upload_url, headers=headers, json=json_body, timeout=30)
            else:
                return False, {'error': f'不支持的请求方法: {method}', 'details': '当前仅支持POST'}

            # 检查响应
            if response.status_code == 200:
                result_data = response.json()

                # 提取下载链接
                download_url = self._extract_download_url(result_data, download_rule)

                if download_url:
                    # 美化返回结果
                    formatted_result = self._format_success_result(
                        book_source_json,
                        upload_config,
                        result_data,
                        download_url,
                        validation_info
                    )
                    return True, formatted_result
                else:
                    return False, {
                        'error': '无法提取下载链接',
                        'details': f'规则: {download_rule}',
                        'response': result_data
                    }
            else:
                return False, {
                    'error': f'上传失败: HTTP {response.status_code}',
                    'details': response.text
                }

        except requests.exceptions.Timeout:
            return False, {'error': '请求超时', 'details': '上传服务响应超过30秒'}
        except requests.exceptions.ConnectionError:
            return False, {'error': '连接失败', 'details': '无法连接到上传服务器'}
        except json.JSONDecodeError:
            return False, {'error': '响应解析失败', 'details': '服务器返回的不是有效的JSON'}
        except Exception as e:
            return False, {'error': f'上传异常: {str(e)}', 'details': str(type(e).__name__)}

    def _print_validation_result(self, is_valid: bool, errors: List[str], warnings: List[str]):
        """
        打印验证结果

        Args:
            is_valid: 是否验证通过
            errors: 错误列表
            warnings: 警告列表
        """
        print("\n" + "=" * 70)
        print("📋 书源验证结果")
        print("=" * 70)

        if is_valid:
            print("\n✅ 验证通过! 书源格式符合要求")
        else:
            print("\n❌ 验证失败! 书源格式存在问题")

        if warnings:
            print(f"\n⚠️  发现 {len(warnings)} 个警告:")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")

        if errors:
            print(f"\n🚫 发现 {len(errors)} 个错误:")
            for i, error in enumerate(errors, 1):
                print(f"  {i}. {error}")

        print("\n" + "=" * 70)

    def _validate_json_array_format(self, json_string: str) -> Tuple[bool, str]:
        """
        验证JSON字符串是否为数组格式

        Args:
            json_string: JSON字符串

        Returns:
            (is_valid, message): 是否有效和消息
        """
        try:
            data = json.loads(json_string)
            if isinstance(data, list):
                if len(data) == 0:
                    return False, "JSON数组为空"
                elif len(data) == 1 and isinstance(data[0], dict):
                    return True, "✅ 正确的JSON数组格式 [{...}]"
                else:
                    return True, f"✅ JSON数组格式 [{len(data)}个元素]"
            elif isinstance(data, dict):
                return False, "❌ 错误格式: JSON对象而非数组 (应为 [...], 实际为 {...})"
            else:
                return False, f"❌ 未知格式: {type(data).__name__}"
        except json.JSONDecodeError as e:
            return False, f"❌ JSON解析失败: {e}"

    def _extract_download_url(self, data: Any, rule: str) -> Optional[str]:
        """
        根据规则提取下载链接

        Args:
            data: 响应数据
            rule: 提取规则（简化版JSONPath）

        Returns:
            提取的URL，如果失败返回None
        """
        try:
            if rule == '$':
                return data
            elif rule.startswith('$..'):
                # JSONPath简化支持 - 深度查找
                key = rule[3:]
                if isinstance(data, dict):
                    return data.get(key)
                elif isinstance(data, list) and len(data) > 0:
                    if isinstance(data[0], dict):
                        return data[0].get(key)
            elif rule.startswith('$.'):
                # JSONPath点路径支持 - 如 $.data.links.url
                path = rule[2:].split('.')
                current = data
                for key in path:
                    if isinstance(current, dict):
                        current = current.get(key)
                        if current is None:
                            return None
                    else:
                        return None
                return current
            else:
                # 直接访问
                return data.get(rule if isinstance(rule, str) else rule)
        except:
            return None
        return None

    def _format_success_result(
        self,
        book_source: Dict[str, Any],
        config: Dict[str, Any],
        response: Dict[str, Any],
        download_url: str,
        validation_info: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        格式化成功结果（美化输出）

        Args:
            book_source: 书源对象
            config: 上传配置
            response: 服务器响应
            download_url: 下载链接
            validation_info: 验证信息（可选）

        Returns:
            格式化的结果字典
        """
        result = {
            'success': True,
            'message': '✅ 书源上传成功！',
            'book_source': {
                'name': book_source.get('bookSourceName', '未命名'),
                'url': book_source.get('bookSourceUrl', ''),
                'group': book_source.get('bookSourceGroup', '')
            },
            'upload_info': {
                'service': config.get('summary', '未知服务'),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'compress': config.get('compress', False)
            },
            'result': {
                'download_url': download_url,
                'raw_response': response
            },
            'usage': {
                'import_method': '方法1: 复制链接后，在阅读APP中点击"导入书源"，粘贴链接',
                'import_method_2': '方法2: 直接打开链接，长按分享到阅读APP',
                'qr_tip': '💡 提示：可以将链接生成二维码，扫描即可导入'
            }
        }

        # 添加验证信息
        if validation_info:
            result['validation'] = validation_info

        return result


def print_upload_result(result: Dict[str, Any]):
    """
    打美化的上传结果

    Args:
        result: 上传结果字典
    """
    if result.get('success'):
        # 成功输出
        print("\n" + "=" * 60)
        print(f"  {result['message']}")
        print("=" * 60)

        # 书源信息
        print("\n📚 书源信息:")
        print(f"  名称: {result['book_source']['name']}")
        print(f"  地址: {result['book_source']['url']}")
        print(f"  分组: {result['book_source']['group']}")

        # 上传信息
        print("\n📤 上传信息:")
        print(f"  服务: {result['upload_info']['service']}")
        print(f"  时间: {result['upload_info']['timestamp']}")
        print(f"  压缩: {'是' if result['upload_info']['compress'] else '否'}")

        # 验证信息
        if 'validation' in result:
            validation = result['validation']
            print("\n📋 验证信息:")
            print(f"  状态: {'✅ 通过' if validation.get('is_valid') else '❌ 失败'}")
            if validation.get('warnings_count', 0) > 0:
                print(f"  警告数: {validation['warnings_count']}")
                print("  警告内容:")
                for warning in validation.get('warnings', [])[:5]:  # 最多显示5个警告
                    print(f"    - {warning}")
                if validation['warnings_count'] > 5:
                    print(f"    ... 还有 {validation['warnings_count'] - 5} 个警告")

        # 下载链接
        print("\n🔗 下载链接:")
        print(f"  {result['result']['download_url']}")

        # 使用方法
        print("\n💡 使用方法:")
        print(f"  {result['usage']['import_method']}")
        print(f"  {result['usage']['import_method_2']}")
        print(f"  {result['usage']['qr_tip']}")

        print("\n" + "=" * 60)

    else:
        # 失败输出
        print("\n" + "=" * 60)
        print("  ❌ 上传失败")
        print("=" * 60)

        print(f"\n错误: {result.get('error', '未知错误')}")
        if 'details' in result:
            print(f"详情: {result['details']}")

        # 显示验证错误
        if 'errors' in result and result['errors']:
            print("\n🚫 验证错误:")
            for i, error in enumerate(result['errors'], 1):
                print(f"  {i}. {error}")

        if 'warnings' in result and result['warnings']:
            print("\n⚠️  警告:")
            for i, warning in enumerate(result['warnings'], 1):
                print(f"  {i}. {warning}")

        print("\n" + "=" * 60)


def main():
    """命令行入口"""
    import sys

    if len(sys.argv) < 2:
        print("用法:")
        print("  python upload_book_source.py <书源JSON文件路径> [上传配置JSON文件路径]")
        print("\n示例:")
        print("  python upload_book_source.py references/book_source_database/my_source.json")
        print("  python upload_book_source.py my_source.json custom_upload_config.json")
        sys.exit(1)

    # 读取书源文件
    book_source_file = Path(sys.argv[1])
    if not book_source_file.exists():
        print(f"❌ 错误: 书源文件不存在: {book_source_file}")
        sys.exit(1)

    with open(book_source_file, 'r', encoding='utf-8') as f:
        book_source_data = json.load(f)

    # 如果是数组，取第一个元素
    if isinstance(book_source_data, list) and len(book_source_data) > 0:
        book_source = book_source_data[0]
        print(f"✓ 检测到书源数组，使用第一个书源")
    elif isinstance(book_source_data, dict):
        book_source = book_source_data
    else:
        print(f"❌ 错误: 无效的书源格式")
        sys.exit(1)

    # 读取上传配置（可选）
    upload_config = None
    if len(sys.argv) >= 3:
        config_file = Path(sys.argv[2])
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                upload_config = json.load(f)
            print(f"📝 使用自定义上传配置: {config_file}")
        else:
            print(f"⚠️  警告: 配置文件不存在，使用默认配置: {config_file}")

    # 执行上传
    uploader = BookSourceUploader()
    success, result = uploader.upload_book_source(book_source, upload_config)

    # 打印结果
    print_upload_result(result)

    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
