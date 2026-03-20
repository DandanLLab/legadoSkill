#!/usr/bin/env python3
"""
Legado Book Source Debugger CLI
Command-line tool for debugging and testing book sources

Usage:
    python debugger_cli.py test <book_source.json> --keyword "斗破苍穹"
    python debugger_cli.py search <book_source.json> --keyword "斗破苍穹"
    python debugger_cli.py info <book_source.json> --url <book_url>
    python debugger_cli.py toc <book_source.json> --url <toc_url>
    python debugger_cli.py content <book_source.json> --url <chapter_url>
"""

import sys
import os
import json
import argparse
from typing import Dict, Any, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from debugger.engine import BookSource, DebugEngine


def load_book_source(file_path: str) -> BookSource:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if isinstance(data, list) and len(data) > 0:
        data = data[0]
    
    return BookSource.from_dict(data)


def print_result(result: Dict[str, Any], output_format: str = 'text'):
    if output_format == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print("\n" + "=" * 60)
        print(f"测试结果: {'成功' if result.get('success') else '失败'}")
        print(f"消息: {result.get('message', '')}")
        print(f"耗时: {result.get('duration_ms', 0):.2f}ms")
        
        if result.get('error'):
            print(f"错误: {result.get('error')}")
        
        if result.get('data'):
            print("\n数据:")
            data = result['data']
            if isinstance(data, list):
                for i, item in enumerate(data[:5]):
                    if hasattr(item, '__dict__'):
                        print(f"  [{i+1}] {item}")
                    else:
                        print(f"  [{i+1}] {item}")
            elif hasattr(data, '__dict__'):
                for key, value in data.__dict__.items():
                    if value:
                        value_str = str(value)[:100]
                        print(f"  {key}: {value_str}")
            else:
                print(f"  {data}")
        
        if result.get('steps'):
            print("\n调试日志:")
            for step in result['steps'][-10:]:
                print(f"  [{step.get('step')}] {step.get('message')}")


def cmd_test(args):
    book_source = load_book_source(args.source)
    engine = DebugEngine(book_source)
    
    print(f"\n书源: {book_source.bookSourceName}")
    print(f"地址: {book_source.bookSourceUrl}")
    print(f"搜索关键词: {args.keyword}")
    
    result = engine.run_full_test(args.keyword)
    
    if args.output == 'json':
        print(json.dumps(result, ensure_ascii=False, indent=2, default=str))
    else:
        print("\n" + "=" * 60)
        print("完整测试结果")
        print("=" * 60)
        
        for test_name, test_result in result.get('tests', {}).items():
            status = "✓" if test_result.get('success') else "✗"
            print(f"\n[{status}] {test_name}: {test_result.get('message', '')}")
            print(f"    耗时: {test_result.get('duration_ms', 0):.2f}ms")
            if test_result.get('error'):
                print(f"    错误: {test_result.get('error')}")
        
        print("\n" + "=" * 60)
        print(f"总耗时: {result.get('total_duration_ms', 0):.2f}ms")
        print(f"总体结果: {'成功' if result.get('overall_success') else '失败'}")


def cmd_search(args):
    book_source = load_book_source(args.source)
    engine = DebugEngine(book_source)
    
    print(f"\n书源: {book_source.bookSourceName}")
    print(f"搜索关键词: {args.keyword}")
    
    result = engine.test_search(args.keyword)
    
    if args.output == 'json':
        output = {
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'results': [r.__dict__ for r in result.data] if result.data else []
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_result({
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'data': result.data
        })


def cmd_info(args):
    book_source = load_book_source(args.source)
    engine = DebugEngine(book_source)
    
    print(f"\n书源: {book_source.bookSourceName}")
    print(f"书籍URL: {args.url}")
    
    result = engine.test_book_info(args.url)
    
    if args.output == 'json':
        output = {
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'book_info': result.data.__dict__ if result.data else None
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_result({
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'data': result.data
        })


def cmd_toc(args):
    book_source = load_book_source(args.source)
    engine = DebugEngine(book_source)
    
    print(f"\n书源: {book_source.bookSourceName}")
    print(f"目录URL: {args.url}")
    
    result = engine.test_toc(args.url)
    
    if args.output == 'json':
        output = {
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'chapters': [c.__dict__ for c in result.data] if result.data else []
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_result({
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'data': result.data
        })


def cmd_content(args):
    book_source = load_book_source(args.source)
    engine = DebugEngine(book_source)
    
    print(f"\n书源: {book_source.bookSourceName}")
    print(f"章节URL: {args.url}")
    
    result = engine.test_content(args.url)
    
    if args.output == 'json':
        output = {
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'content': result.data.__dict__ if result.data else None
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print_result({
            'success': result.success,
            'message': result.message,
            'duration_ms': result.duration_ms,
            'error': result.error,
            'data': result.data
        })


def main():
    parser = argparse.ArgumentParser(
        description='Legado Book Source Debugger',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python debugger_cli.py test book_source.json --keyword "斗破苍穹"
    python debugger_cli.py search book_source.json --keyword "斗破苍穹" --output json
    python debugger_cli.py info book_source.json --url "https://example.com/book/1"
    python debugger_cli.py toc book_source.json --url "https://example.com/book/1/toc"
    python debugger_cli.py content book_source.json --url "https://example.com/chapter/1"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    parser_test = subparsers.add_parser('test', help='Run full test on book source')
    parser_test.add_argument('source', help='Book source JSON file')
    parser_test.add_argument('--keyword', '-k', default='斗破苍穹', help='Search keyword')
    parser_test.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='Output format')
    parser_test.set_defaults(func=cmd_test)
    
    parser_search = subparsers.add_parser('search', help='Test search functionality')
    parser_search.add_argument('source', help='Book source JSON file')
    parser_search.add_argument('--keyword', '-k', default='斗破苍穹', help='Search keyword')
    parser_search.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='Output format')
    parser_search.set_defaults(func=cmd_search)
    
    parser_info = subparsers.add_parser('info', help='Test book info extraction')
    parser_info.add_argument('source', help='Book source JSON file')
    parser_info.add_argument('--url', '-u', required=True, help='Book info URL')
    parser_info.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='Output format')
    parser_info.set_defaults(func=cmd_info)
    
    parser_toc = subparsers.add_parser('toc', help='Test table of contents extraction')
    parser_toc.add_argument('source', help='Book source JSON file')
    parser_toc.add_argument('--url', '-u', required=True, help='TOC URL')
    parser_toc.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='Output format')
    parser_toc.set_defaults(func=cmd_toc)
    
    parser_content = subparsers.add_parser('content', help='Test content extraction')
    parser_content.add_argument('source', help='Book source JSON file')
    parser_content.add_argument('--url', '-u', required=True, help='Chapter URL')
    parser_content.add_argument('--output', '-o', choices=['text', 'json'], default='text', help='Output format')
    parser_content.set_defaults(func=cmd_content)
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
