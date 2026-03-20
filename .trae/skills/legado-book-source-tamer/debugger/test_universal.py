#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Legado书源调试器 - 通用测试脚本
支持自动修复迭代、完整流程测试、详细日志输出

使用方法:
    python debugger/test_universal.py 书源文件.json -k "搜索关键词"
    python debugger/test_universal.py 书源文件.json -k "斗破苍穹" --auto-fix
"""
import sys
import os
import json
import argparse
from datetime import datetime

if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
sys.path.insert(0, parent_dir)
os.chdir(parent_dir)


def format_log_time() -> str:
    now = datetime.now()
    return f"[{now.minute:02d}:{now.second:02d}.{now.microsecond // 1000:03d}]"


def print_header(book_source, keyword, auto_fix=False, max_attempts=5):
    print(f"============================================================")
    print(f" Legado Book Source Debugger - 通用版")
    print(f"============================================================")
    print(f"Book Source: {book_source.bookSourceName}")
    print(f"URL: {book_source.bookSourceUrl}")
    print(f"Keyword: {keyword}")
    print(f"Auto Fix: {'Enabled (max {} attempts)'.format(max_attempts) if auto_fix else 'Disabled'}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"============================================================")
    print()


def run_test(source_file: str, keyword: str, auto_fix: bool = False, max_attempts: int = 5):
    with open(source_file, 'r', encoding='utf-8') as f:
        source_data = json.loads(f.read())

    if isinstance(source_data, list):
        source_data = source_data[0]

    from debugger.engine import BookSource, DebugEngine

    book_source = BookSource.from_dict(source_data)
    engine = DebugEngine(book_source)

    print_header(book_source, keyword, auto_fix, max_attempts)

    log_lines = []
    
    def log_callback(category: str, message: str):
        log_lines.append(f"[{category}] {message}")
        print(f"  [{format_log_time()}] [{category}] {message}")

    if auto_fix:
        print(f"[自动修复] 启动自动修复迭代模式...")
        print()
        
        from debugger.engine.auto_fixer import AutoFixer
        
        fixer = AutoFixer(source_data, engine, log_callback)
        result = fixer.auto_fix_and_test(keyword, max_attempts)
        
        print()
        print(f"============================================================")
        print(f" 自动修复结果")
        print(f"============================================================")
        
        if result["success"]:
            print(f"[{format_log_time()}] 状态: 成功")
            print(f"[{format_log_time()}] 尝试次数: {result['attempts']}")
            
            if result.get("fix_history"):
                print(f"\n修复历史:")
                for fix in result["fix_history"]:
                    print(f"  尝试 {fix['attempt']}: {fix['error_type']}")
                    print(f"    修复: {', '.join(fix['changes'])}")
            
            test_result = result.get("test_result", {})
            if test_result.get("data"):
                content_text = test_result["data"].get("text", "")
                print(f"\n正文长度: {len(content_text)}")
                print(f"\n--- 正文预览 ---")
                print(content_text[:500] + "..." if len(content_text) > 500 else content_text)
            
            final_source = result["book_source"]
            output_file = f"book_source_{book_source.bookSourceName}_{datetime.now().strftime('%Y%m%d')}_fixed.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final_source, f, ensure_ascii=False, indent=2)
            print(f"\n修复后的书源已保存到: {output_file}")
            
        else:
            print(f"[{format_log_time()}] 状态: 失败")
            print(f"[{format_log_time()}] 尝试次数: {result['attempts']}")
            print(f"[{format_log_time()}] 消息: {result.get('message', '未知错误')}")
            
            if result.get("fix_history"):
                print(f"\n修复历史:")
                for fix in result["fix_history"]:
                    print(f"  尝试 {fix['attempt']}: {fix['error_type']}")
                    print(f"    修复: {', '.join(fix['changes'])}")
            
            if result.get("error_analysis"):
                ea = result["error_analysis"]
                print(f"\n错误分析:")
                print(f"  类型: {ea.error_type.value}")
                print(f"  消息: {ea.error_message}")
                if ea.suggestions:
                    print(f"  建议:")
                    for s in ea.suggestions:
                        print(f"    - {s}")
            
            final_source = result["book_source"]
            output_file = f"book_source_{book_source.bookSourceName}_{datetime.now().strftime('%Y%m%d')}_partial.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(final_source, f, ensure_ascii=False, indent=2)
            print(f"\n部分修复的书源已保存到: {output_file}")
        
        save_result(result, book_source, keyword, auto_fix=True)
        return result["success"]
    
    else:
        print(f"[测试] 开始完整流程测试...")
        print()
        
        content_result = engine.test_content(search_keyword=keyword)
        
        current_step = ""
        if hasattr(content_result, 'steps') and content_result.steps:
            for step_info in content_result.steps:
                if isinstance(step_info, dict):
                    step_name = step_info.get('step', '正文')
                    msg = step_info.get('message', '')
                    state = step_info.get('state')
                    
                    if step_name != current_step:
                        current_step = step_name
                        step_names = {
                            "搜索": "Searching...",
                            "详情": "Getting book info...",
                            "目录": "Getting chapter list...",
                            "正文": "Getting content..."
                        }
                        print(f"  → {step_names.get(step_name, step_name)}")
                    
                    if state in [10, 20, 30, 40]:
                        if msg:
                            log_lines.append(f"[{step_name}] HTML长度: {len(msg)}")
                    elif msg:
                        log_lines.append(f"[{step_name}] {msg}")

        print()
        print(f"============================================================")
        print(f" 测试结果")
        print(f"============================================================")

        if content_result.success:
            print(f"[{format_log_time()}] Content: PASS")
            print(f"[{format_log_time()}] Overall: ALL PASS")
            
            if content_result.data:
                content_text = content_result.data.text
                print(f"\n正文长度: {len(content_text)}")
                print(f"\n--- 正文预览 ---")
                print(content_text[:500] + "..." if len(content_text) > 500 else content_text)
        else:
            print(f"[{format_log_time()}] Content: FAIL")
            print(f"[{format_log_time()}] Overall: FAILED")
            print(f"\n错误: {content_result.message}")
            
            if log_lines:
                print(f"\n--- 详细日志 ---")
                for line in log_lines[-20:]:
                    print(f"  {line}")
                
                print(f"\n提示: 使用 --auto-fix 参数启用自动修复功能")

        save_result(content_result, book_source, keyword, auto_fix=False, log_lines=log_lines)
        return content_result.success


def save_result(result, book_source, keyword, auto_fix=False, log_lines=None):
    with open('test_result.txt', 'w', encoding='utf-8') as f:
        f.write(f"============================================================\n")
        f.write(f" Legado Book Source Debugger - 通用版\n")
        f.write(f"============================================================\n")
        f.write(f"Book Source: {book_source.bookSourceName}\n")
        f.write(f"URL: {book_source.bookSourceUrl}\n")
        f.write(f"Keyword: {keyword}\n")
        f.write(f"Auto Fix: {'Enabled' if auto_fix else 'Disabled'}\n")
        f.write(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"============================================================\n\n")
        
        if auto_fix:
            f.write(f"============================================================\n")
            f.write(f" 自动修复结果\n")
            f.write(f"============================================================\n")
            f.write(f"成功: {result.get('success', False)}\n")
            f.write(f"尝试次数: {result.get('attempts', 0)}\n")
            
            if result.get("fix_history"):
                f.write(f"\n修复历史:\n")
                for fix in result["fix_history"]:
                    f.write(f"  尝试 {fix['attempt']}: {fix['error_type']}\n")
                    f.write(f"    修复: {', '.join(fix['changes'])}\n")
            
            test_result = result.get("test_result", {})
            if test_result.get("data"):
                content_text = test_result["data"].get("text", "")
                f.write(f"\n正文长度: {len(content_text)}\n")
                f.write(f"\n--- 正文内容 ---\n")
                f.write(content_text)
        else:
            f.write(f"============================================================\n")
            f.write(f" 测试结果\n")
            f.write(f"============================================================\n")
            success = getattr(result, 'success', False)
            f.write(f"Content: {'PASS' if success else 'FAIL'}\n")
            f.write(f"Overall: {'ALL PASS' if success else 'FAILED'}\n")
            f.write(f"Message: {getattr(result, 'message', '')}\n")
            
            if hasattr(result, 'data') and result.data:
                f.write(f"\n正文长度: {len(result.data.text)}\n")
                f.write(f"\n--- 正文内容 ---\n")
                f.write(result.data.text)
            
            if log_lines:
                f.write(f"\n\n--- 详细日志 ---\n")
                for line in log_lines:
                    f.write(f"{line}\n")

    print(f"\n日志已保存到 test_result.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Legado Book Source Debugger - 通用版")
    parser.add_argument("source", help="书源JSON文件路径")
    parser.add_argument("-k", "--keyword", default="斗破苍穹", help="搜索关键词")
    parser.add_argument("--auto-fix", action="store_true", help="启用自动修复迭代模式")
    parser.add_argument("--max-attempts", type=int, default=5, help="自动修复最大尝试次数")

    args = parser.parse_args()

    run_test(args.source, args.keyword, args.auto_fix, args.max_attempts)
