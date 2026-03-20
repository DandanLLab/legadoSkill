"""
Book Source File Organizer
Automatically organizes generated files into book source specific folders

This module provides functionality to:
1. Create or use existing 'temp' folder in project root
2. Create book source specific subfolders
3. Move all related files to the appropriate subfolder
"""

import os
import shutil
import json
import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import re


@dataclass
class FileOrganizeResult:
    success: bool
    message: str
    book_source_name: str = ""
    subfolder_path: str = ""
    moved_files: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class BookSourceFileOrganizer:
    """
    Book Source File Organizer
    
    Manages the organization of generated files into book source specific folders.
    """
    
    def __init__(self, project_root: str = None):
        if project_root:
            self.project_root = Path(project_root)
        else:
            self.project_root = Path(__file__).parent.parent.parent
        
        self.temp_folder = self.project_root / "temp"
        self.session_files: Dict[str, List[str]] = {}
        self.current_session_id: Optional[str] = None
    
    def start_session(self, session_id: str = None) -> str:
        """
        Start a new file tracking session
        
        Args:
            session_id: Optional session identifier. If not provided, generates one based on timestamp.
        
        Returns:
            The session ID
        """
        if not session_id:
            session_id = f"session_{int(time.time() * 1000)}"
        
        self.current_session_id = session_id
        self.session_files[session_id] = []
        
        return session_id
    
    def register_file(self, file_path: str, session_id: str = None) -> bool:
        """
        Register a file for the current session
        
        Args:
            file_path: Path to the file to register
            session_id: Optional session ID. Uses current session if not provided.
        
        Returns:
            True if registration successful, False otherwise
        """
        if not session_id:
            session_id = self.current_session_id
        
        if not session_id or session_id not in self.session_files:
            return False
        
        abs_path = str(Path(file_path).resolve())
        if abs_path not in self.session_files[session_id]:
            self.session_files[session_id].append(abs_path)
        
        return True
    
    def register_book_source_json(self, json_path: str, book_source_name: str, session_id: str = None) -> bool:
        """
        Register a book source JSON file and extract book source name
        
        Args:
            json_path: Path to the JSON file
            book_source_name: Name of the book source
            session_id: Optional session ID
        
        Returns:
            True if registration successful
        """
        result = self.register_file(json_path, session_id)
        if result:
            if not session_id:
                session_id = self.current_session_id
            if session_id and session_id not in self.session_files:
                self.session_files[session_id] = []
            self.session_files[session_id].append(f"__BOOK_SOURCE_NAME__:{book_source_name}")
        
        return result
    
    def get_book_source_name_from_session(self, session_id: str = None) -> Optional[str]:
        """
        Get the book source name from session files
        
        Args:
            session_id: Optional session ID
        
        Returns:
            The book source name if found, None otherwise
        """
        if not session_id:
            session_id = self.current_session_id
        
        if not session_id or session_id not in self.session_files:
            return None
        
        for item in self.session_files[session_id]:
            if isinstance(item, str) and item.startswith("__BOOK_SOURCE_NAME__:"):
                return item.replace("__BOOK_SOURCE_NAME__:", "")
        
        return None
    
    def _sanitize_folder_name(self, name: str) -> str:
        """
        Sanitize folder name to remove invalid characters
        
        Args:
            name: Original folder name
        
        Returns:
            Sanitized folder name
        """
        invalid_chars = '<>:"/\\|?*'
        sanitized = ''.join(c for c in name if c not in invalid_chars)
        sanitized = sanitized.strip()
        if not sanitized:
            sanitized = f"unnamed_{int(time.time())}"
        return sanitized
    
    def _ensure_temp_folder(self) -> Path:
        """
        Ensure the temp folder exists
        
        Returns:
            Path to the temp folder
        """
        if not self.temp_folder.exists():
            self.temp_folder.mkdir(parents=True, exist_ok=True)
        
        return self.temp_folder
    
    def create_book_source_folder(self, book_source_name: str) -> Tuple[Path, bool]:
        """
        Create a book source specific folder in the temp directory
        
        Args:
            book_source_name: Name of the book source
        
        Returns:
            Tuple of (folder path, success boolean)
        """
        self._ensure_temp_folder()
        
        sanitized_name = self._sanitize_folder_name(book_source_name)
        subfolder_path = self.temp_folder / sanitized_name
        
        created_new = False
        if not subfolder_path.exists():
            subfolder_path.mkdir(parents=True, exist_ok=True)
            created_new = True
        
        return subfolder_path, created_new
    
    def organize_files(
        self,
        book_source_name: str,
        files_to_move: List[str] = None,
        session_id: str = None,
        copy_mode: bool = False
    ) -> FileOrganizeResult:
        """
        Organize files into book source specific folder
        
        Args:
            book_source_name: Name of the book source
            files_to_move: List of file paths to move. If None, uses session files.
            session_id: Optional session ID to get files from
            copy_mode: If True, copy files instead of moving them
        
        Returns:
            FileOrganizeResult with operation details
        """
        result = FileOrganizeResult(
            success=False,
            message="",
            book_source_name=book_source_name
        )
        
        try:
            subfolder_path, created_new = self.create_book_source_folder(book_source_name)
            result.subfolder_path = str(subfolder_path)
            
            if files_to_move is None:
                if not session_id:
                    session_id = self.current_session_id
                
                if session_id and session_id in self.session_files:
                    files_to_move = [
                        f for f in self.session_files[session_id]
                        if isinstance(f, str) and not f.startswith("__BOOK_SOURCE_NAME__:")
                    ]
                else:
                    files_to_move = []
            
            if not files_to_move:
                result.success = True
                result.message = f"已创建/确认书源文件夹: {subfolder_path}"
                return result
            
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
                result.message = f"✅ 文件整理成功！\n\n📁 书源文件夹: {subfolder_path}\n📄 已整理文件数: {moved_count}"
            elif moved_count > 0 and error_count > 0:
                result.message = f"⚠️ 部分文件整理成功\n\n📁 书源文件夹: {subfolder_path}\n✅ 成功: {moved_count} 个文件\n❌ 失败: {error_count} 个文件"
            else:
                result.message = f"❌ 文件整理失败\n\n📁 书源文件夹: {subfolder_path}\n❌ 失败: {error_count} 个文件"
            
        except Exception as e:
            result.success = False
            result.message = f"❌ 整理过程出错: {str(e)}"
            result.errors.append(str(e))
        
        return result
    
    def scan_project_for_book_source_files(self, book_source_name: str) -> List[str]:
        """
        Scan the project for files related to a specific book source
        
        Args:
            book_source_name: Name of the book source to scan for
        
        Returns:
            List of file paths that appear to be related to the book source
        """
        related_files = []
        sanitized_name = self._sanitize_folder_name(book_source_name).lower()
        
        scan_patterns = [
            "*.json",
            "*.html",
            "*.py",
        ]
        
        for pattern in scan_patterns:
            for file_path in self.project_root.glob(pattern):
                file_name_lower = file_path.name.lower()
                if sanitized_name in file_name_lower or book_source_name.lower() in file_name_lower:
                    if file_path.name != "file_organizer.py":
                        related_files.append(str(file_path))
        
        for pattern in scan_patterns:
            for file_path in self.temp_folder.glob(pattern):
                file_name_lower = file_path.name.lower()
                if sanitized_name in file_name_lower or book_source_name.lower() in file_name_lower:
                    if str(file_path) not in related_files:
                        related_files.append(str(file_path))
        
        return related_files
    
    def list_book_source_folders(self) -> List[Dict[str, any]]:
        """
        List all book source folders in the temp directory
        
        Returns:
            List of dictionaries containing folder info
        """
        folders = []
        
        if not self.temp_folder.exists():
            return folders
        
        for item in self.temp_folder.iterdir():
            if item.is_dir():
                files = list(item.glob("*"))
                folders.append({
                    "name": item.name,
                    "path": str(item),
                    "file_count": len([f for f in files if f.is_file()]),
                    "files": [f.name for f in files if f.is_file()]
                })
        
        return folders
    
    def get_folder_info(self, book_source_name: str) -> Optional[Dict[str, any]]:
        """
        Get information about a specific book source folder
        
        Args:
            book_source_name: Name of the book source
        
        Returns:
            Dictionary with folder info or None if not found
        """
        sanitized_name = self._sanitize_folder_name(book_source_name)
        folder_path = self.temp_folder / sanitized_name
        
        if not folder_path.exists():
            return None
        
        files = list(folder_path.glob("*"))
        file_list = []
        
        for f in files:
            if f.is_file():
                stat = f.stat()
                file_list.append({
                    "name": f.name,
                    "size": stat.st_size,
                    "modified": stat.st_mtime,
                    "type": f.suffix.lower()
                })
        
        return {
            "name": folder_path.name,
            "path": str(folder_path),
            "file_count": len(file_list),
            "files": file_list
        }
    
    def cleanup_session(self, session_id: str = None):
        """
        Clean up session data
        
        Args:
            session_id: Optional session ID. Uses current session if not provided.
        """
        if not session_id:
            session_id = self.current_session_id
        
        if session_id and session_id in self.session_files:
            del self.session_files[session_id]
        
        if self.current_session_id == session_id:
            self.current_session_id = None


_global_organizer: Optional[BookSourceFileOrganizer] = None


def get_global_organizer(project_root: str = None) -> BookSourceFileOrganizer:
    """
    Get the global file organizer instance
    
    Args:
        project_root: Optional project root path
    
    Returns:
        BookSourceFileOrganizer instance
    """
    global _global_organizer
    
    if _global_organizer is None:
        _global_organizer = BookSourceFileOrganizer(project_root)
    
    return _global_organizer


def organize_book_source_files(
    book_source_name: str,
    files_to_move: List[str] = None,
    session_id: str = None,
    copy_mode: bool = False
) -> FileOrganizeResult:
    """
    Convenience function to organize book source files
    
    Args:
        book_source_name: Name of the book source
        files_to_move: Optional list of files to move
        session_id: Optional session ID
        copy_mode: If True, copy files instead of moving
    
    Returns:
        FileOrganizeResult
    """
    organizer = get_global_organizer()
    return organizer.organize_files(book_source_name, files_to_move, session_id, copy_mode)


def start_file_session(session_id: str = None) -> str:
    """
    Start a new file tracking session
    
    Args:
        session_id: Optional session identifier
    
    Returns:
        The session ID
    """
    organizer = get_global_organizer()
    return organizer.start_session(session_id)


def register_generated_file(file_path: str, session_id: str = None) -> bool:
    """
    Register a generated file for the current session
    
    Args:
        file_path: Path to the generated file
        session_id: Optional session ID
    
    Returns:
        True if registration successful
    """
    organizer = get_global_organizer()
    return organizer.register_file(file_path, session_id)
