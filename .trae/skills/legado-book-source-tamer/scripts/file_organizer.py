"""
Book Source File Organizer文件整理工具
Automatically organizes generated files into book source specific folders
"""

import os
import shutil
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FileOrganizeResult:
    success: bool
    message: str
    book_source_name: str = ""
    subfolder_path: str = ""
    moved_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class BookSourceFileOrganizer:
    """书源文件整理器"""
    
    def __init__(self, project_root: str = None):
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent.parent
        
        self.temp_folder = self.project_root / "temp"
        self.session_files: Dict[str, List[str]] = {}
        self.current_session_id: Optional[str] = None
    
    def start_session(self, session_id: str = None) -> str:
        """启动新的文件跟踪会话"""
        if not session_id:
            import time
            session_id = f"session_{int(time.time() * 1000)}"
        
        self.current_session_id = session_id
        self.session_files[session_id] = []
        return session_id
    
    def register_file(self, file_path: str, session_id: str = None) -> bool:
        """注册文件到当前会话"""
        if not session_id:
            session_id = self.current_session_id
        
        if not session_id or session_id not in self.session_files:
            return False
        
        abs_path = str(Path(file_path).resolve())
        if abs_path not in self.session_files[session_id]:
            self.session_files[session_id].append(abs_path)
        
        return True
    
    def organize_files(
        self,
        book_source_name: str,
        files_to_move: List[str] = None,
        session_id: str = None,
        copy_mode: bool = False
    ) -> FileOrganizeResult:
        """
        整理文件到书源专属文件夹
        
        参数:
            book_source_name: 书源名称
            files_to_move: 要移动的文件列表（可选，不提供则使用会话文件）
            session_id: 会话ID（可选）
            copy_mode: 是否使用复制模式（默认移动模式）
        
        返回:
            FileOrganizeResult 整理结果
        """
        result = FileOrganizeResult(
            success=False,
            message="",
            book_source_name=book_source_name
        )
        
        try:
            if not self.temp_folder.exists():
                self.temp_folder.mkdir(parents=True, exist_ok=True)
            
            sanitized_name = self._sanitize_folder_name(book_source_name)
            subfolder_path = self.temp_folder / sanitized_name
            
            if not subfolder_path.exists():
                subfolder_path.mkdir(parents=True, exist_ok=True)
            
            result.subfolder_path = str(subfolder_path)
            
            if files_to_move is None:
                if not session_id:
                    session_id = self.current_session_id
                
                if session_id and session_id in self.session_files:
                    files_to_move = self.session_files[session_id]
                else:
                    files_to_move = []
            
            if not files_to_move:
                result.success = True
                result.message = f"已创建/确认书源文件夹: {subfolder_path}"
                return result
            
            import time
            for file_path in files_to_move:
                try:
                    source_path = Path(file_path)
                    if not source_path.exists():
                        result.errors.append(f"文件不存在: {file_path}")
                        continue
                    
                    dest_path = subfolder_path / source_path.name
                    
                    if dest_path.exists():
                        timestamp = int(time.time())
                        stem = source_path.stem
                        suffix = source_path.suffix
                        dest_path = subfolder_path / f"{stem}_{timestamp}{suffix}"
                    
                    if copy_mode:
                        shutil.copy2(source_path, dest_path)
                    else:
                        shutil.move(str(source_path), dest_path)
                    
                    result.moved_files.append(str(dest_path))
                    
                except Exception as e:
                    result.errors.append(f"处理文件失败 {file_path}: {str(e)}")
            
            result.success = True
            moved_count = len(result.moved_files)
            error_count = len(result.errors)
            
            if moved_count > 0 and error_count == 0:
                result.message = f"文件整理成功！书源文件夹: {subfolder_path}，已整理文件数: {moved_count}"
            elif moved_count > 0 and error_count > 0:
                result.message = f"部分文件整理成功。书源文件夹: {subfolder_path}，成功: {moved_count} 个文件，失败: {error_count} 个文件"
            else:
                result.message = f"文件整理失败。书源文件夹: {subfolder_path}，失败: {error_count} 个文件"
            
        except Exception as e:
            result.success = False
            result.message = f"整理过程出错: {str(e)}"
            result.errors.append(str(e))
        
        return result
    
    def _sanitize_folder_name(self, name: str) -> str:
        """清理文件夹名称，移除非法字符"""
        invalid_chars = '<>:"/\\|?*'
        sanitized = ''.join(c for c in name if c not in invalid_chars)
        sanitized = sanitized.strip()
        if not sanitized:
            import time
            sanitized = f"unnamed_{int(time.time())}"
        return sanitized


_global_organizer: Optional[BookSourceFileOrganizer] = None


def organize_book_source_files(
    book_source_name: str,
    files_to_move: List[str] = None,
    session_id: str = None,
    copy_mode: bool = False
) -> FileOrganizeResult:
    """
    整理书源文件的便捷函数
    
    使用示例:
        result = organize_book_source_files(
            book_source_name="笔趣阁hk",
            files_to_move=["笔趣阁hk.json", "search.html"]
        )
    """
    global _global_organizer
    if _global_organizer is None:
        _global_organizer = BookSourceFileOrganizer()
    return _global_organizer.organize_files(book_source_name, files_to_move, session_id, copy_mode)


def start_file_session(session_id: str = None) -> str:
    """启动文件跟踪会话"""
    global _global_organizer
    if _global_organizer is None:
        _global_organizer = BookSourceFileOrganizer()
    return _global_organizer.start_session(session_id)


def register_generated_file(file_path: str, session_id: str = None) -> bool:
    """注册生成的文件到当前会话"""
    global _global_organizer
    if _global_organizer is None:
        _global_organizer = BookSourceFileOrganizer()
    return _global_organizer.register_file(file_path, session_id)
