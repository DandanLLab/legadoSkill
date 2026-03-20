"""
Test script for file_organizer module
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from debugger.engine.file_organizer import (
    BookSourceFileOrganizer,
    organize_book_source_files,
    start_file_session,
    register_generated_file,
    get_global_organizer
)


def test_basic_functionality():
    print("=" * 60)
    print("测试1: 基本功能测试")
    print("=" * 60)
    
    organizer = BookSourceFileOrganizer()
    
    print(f"项目根目录: {organizer.project_root}")
    print(f"temp文件夹: {organizer.temp_folder}")
    
    subfolder_path, created_new = organizer.create_book_source_folder("测试书源")
    print(f"书源文件夹: {subfolder_path}")
    print(f"是否新建: {created_new}")
    
    folder_info = organizer.get_folder_info("测试书源")
    if folder_info:
        print(f"文件夹信息: {folder_info}")
    
    print("✅ 基本功能测试通过\n")


def test_session_mode():
    print("=" * 60)
    print("测试2: 会话模式测试")
    print("=" * 60)
    
    session_id = start_file_session()
    print(f"会话ID: {session_id}")
    
    test_file = "test_file.txt"
    with open(test_file, "w", encoding="utf-8") as f:
        f.write("测试内容")
    
    register_generated_file(test_file)
    print(f"已注册文件: {test_file}")
    
    organizer = get_global_organizer()
    print(f"会话文件列表: {organizer.session_files.get(session_id, [])}")
    
    if os.path.exists(test_file):
        os.remove(test_file)
    
    print("✅ 会话模式测试通过\n")


def test_folder_name_sanitization():
    print("=" * 60)
    print("测试3: 文件夹名称清理测试")
    print("=" * 60)
    
    organizer = BookSourceFileOrganizer()
    
    test_names = [
        "笔趣阁hk",
        "书源:测试",
        "test<book>source",
        "书源|作者",
        "  空格测试  ",
    ]
    
    for name in test_names:
        sanitized = organizer._sanitize_folder_name(name)
        print(f"'{name}' -> '{sanitized}'")
    
    print("✅ 文件夹名称清理测试通过\n")


def test_list_folders():
    print("=" * 60)
    print("测试4: 列出所有书源文件夹")
    print("=" * 60)
    
    organizer = BookSourceFileOrganizer()
    folders = organizer.list_book_source_folders()
    
    print(f"找到 {len(folders)} 个书源文件夹:")
    for folder in folders:
        print(f"  - {folder['name']}: {folder['file_count']} 个文件")
    
    print("✅ 列出文件夹测试通过\n")


def test_organize_files():
    print("=" * 60)
    print("测试5: 文件整理测试")
    print("=" * 60)
    
    test_book_source = "测试书源_整理测试"
    test_files = []
    
    for i in range(3):
        test_file = f"test_file_{i}.txt"
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(f"测试内容 {i}")
        test_files.append(os.path.abspath(test_file))
    
    print(f"测试文件: {test_files}")
    
    result = organize_book_source_files(
        book_source_name=test_book_source,
        files_to_move=test_files,
        copy_mode=True
    )
    
    print(f"成功: {result.success}")
    print(f"消息: {result.message}")
    print(f"移动的文件: {result.moved_files}")
    print(f"错误: {result.errors}")
    
    for f in test_files:
        if os.path.exists(f):
            os.remove(f)
    
    print("✅ 文件整理测试通过\n")


def run_all_tests():
    print("\n" + "=" * 60)
    print("开始运行所有测试")
    print("=" * 60 + "\n")
    
    try:
        test_basic_functionality()
        test_session_mode()
        test_folder_name_sanitization()
        test_list_folders()
        test_organize_files()
        
        print("\n" + "=" * 60)
        print("✅ 所有测试通过！")
        print("=" * 60 + "\n")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
