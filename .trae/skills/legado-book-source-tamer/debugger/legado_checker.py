"""
Legado Repository Checker - 实时检查和更新Legado源码

功能：
1. 检查legado仓库是否存在
2. 获取最新源码参考
3. 对比Python实现与Kotlin源码
4. 提供源码参考路径

使用方法：
    from debugger.legado_checker import LegadoChecker
    checker = LegadoChecker()
    checker.check_analyze_rule()
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class LegadoChecker:
    """
    Legado源码检查器
    用于实时检查和参考Legado Kotlin源码
    """
    
    LEGADO_REPO_URL = "https://github.com/gedoor/legado"
    
    CORE_FILES = {
        "AnalyzeRule": "app/src/main/java/io/legado/app/model/analyzeRule/AnalyzeRule.kt",
        "AnalyzeByJSoup": "app/src/main/java/io/legado/app/model/analyzeRule/AnalyzeByJSoup.kt",
        "AnalyzeByXPath": "app/src/main/java/io/legado/app/model/analyzeRule/AnalyzeByXPath.kt",
        "AnalyzeUrl": "app/src/main/java/io/legado/app/model/analyzeRule/AnalyzeUrl.kt",
        "WebBook": "app/src/main/java/io/legado/app/model/webBook/WebBook.kt",
        "BookList": "app/src/main/java/io/legado/app/model/webBook/BookList.kt",
        "BookInfo": "app/src/main/java/io/legado/app/model/webBook/BookInfo.kt",
        "BookChapterList": "app/src/main/java/io/legado/app/model/webBook/BookChapterList.kt",
        "BookContent": "app/src/main/java/io/legado/app/model/webBook/BookContent.kt",
        "BookSource": "app/src/main/java/io/legado/app/data/entities/BookSource.kt",
    }
    
    def __init__(self, legado_path: str = None):
        if legado_path:
            self.legado_path = Path(legado_path)
        else:
            project_root = Path(__file__).parent.parent.parent
            self.legado_path = project_root / "legado"
    
    def check_repository(self) -> Dict:
        """
        检查legado仓库状态
        
        Returns:
            {
                "exists": bool,
                "path": str,
                "has_core_files": bool,
                "missing_files": List[str],
                "message": str
            }
        """
        result = {
            "exists": self.legado_path.exists(),
            "path": str(self.legado_path),
            "has_core_files": False,
            "missing_files": [],
            "message": ""
        }
        
        if not result["exists"]:
            result["message"] = f"Legado仓库不存在: {self.legado_path}"
            result["message"] += f"\n请克隆仓库: git clone {self.LEGADO_REPO_URL}.git legado"
            return result
        
        missing = []
        for name, rel_path in self.CORE_FILES.items():
            full_path = self.legado_path / rel_path
            if not full_path.exists():
                missing.append(name)
        
        result["missing_files"] = missing
        result["has_core_files"] = len(missing) == 0
        
        if result["has_core_files"]:
            result["message"] = "Legado仓库完整，所有核心文件存在"
        else:
            result["message"] = f"缺少核心文件: {', '.join(missing)}"
        
        return result
    
    def get_source_path(self, file_name: str) -> Optional[Path]:
        """
        获取指定源码文件的路径
        
        Args:
            file_name: 文件名（如 AnalyzeRule）
            
        Returns:
            文件路径，不存在则返回None
        """
        if file_name in self.CORE_FILES:
            path = self.legado_path / self.CORE_FILES[file_name]
            return path if path.exists() else None
        return None
    
    def read_source(self, file_name: str, start_line: int = 0, end_line: int = None) -> Optional[str]:
        """
        读取源码文件内容
        
        Args:
            file_name: 文件名
            start_line: 起始行
            end_line: 结束行
            
        Returns:
            源码内容
        """
        path = self.get_source_path(file_name)
        if not path:
            return None
        
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        if end_line:
            return ''.join(lines[start_line:end_line])
        return ''.join(lines[start_line:])
    
    def find_function(self, file_name: str, function_name: str) -> Optional[Tuple[int, str]]:
        """
        查找函数定义
        
        Args:
            file_name: 文件名
            function_name: 函数名
            
        Returns:
            (行号, 函数代码)
        """
        content = self.read_source(file_name)
        if not content:
            return None
        
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if f"fun {function_name}" in line or f"fun {function_name}(" in line:
                start = i
                brace_count = 0
                code_lines = []
                
                for j in range(i, len(lines)):
                    code_lines.append(lines[j])
                    brace_count += lines[j].count('{') - lines[j].count('}')
                    if brace_count == 0 and j > i:
                        break
                
                return (start, '\n'.join(code_lines))
        
        return None
    
    def check_analyze_rule(self) -> Dict:
        """
        检查AnalyzeRule实现
        
        Returns:
            检查结果
        """
        result = {
            "kotlin_exists": False,
            "python_exists": False,
            "key_functions": {},
            "message": ""
        }
        
        kotlin_path = self.get_source_path("AnalyzeRule")
        if kotlin_path:
            result["kotlin_exists"] = True
            
            key_functions = [
                "getString",
                "getStringList", 
                "getElements",
                "splitSourceRule",
                "applyRule",
                "makeUpRule",
            ]
            
            for func in key_functions:
                found = self.find_function("AnalyzeRule", func)
                result["key_functions"][func] = {
                    "exists": found is not None,
                    "line": found[0] if found else None
                }
        
        project_root = Path(__file__).parent.parent.parent
        python_path = project_root / "debugger" / "engine" / "analyze_rule.py"
        result["python_exists"] = python_path.exists()
        
        if result["kotlin_exists"] and result["python_exists"]:
            result["message"] = "AnalyzeRule实现完整"
        else:
            missing = []
            if not result["kotlin_exists"]:
                missing.append("Kotlin源码")
            if not result["python_exists"]:
                missing.append("Python实现")
            result["message"] = f"缺少: {', '.join(missing)}"
        
        return result
    
    def get_reference_code(self, context: str) -> str:
        """
        根据上下文获取参考代码
        
        Args:
            context: 上下文描述（如 "xpath解析", "css选择器"）
            
        Returns:
            参考代码片段
        """
        context_map = {
            "xpath": ("AnalyzeByXPath", "AnalyzeRule"),
            "css": ("AnalyzeByJSoup", "AnalyzeRule"),
            "json": ("AnalyzeRule",),
            "regex": ("AnalyzeRule",),
            "js": ("AnalyzeRule",),
            "url": ("AnalyzeUrl",),
            "search": ("BookList",),
            "info": ("BookInfo",),
            "toc": ("BookChapterList",),
            "content": ("BookContent",),
        }
        
        for key, files in context_map.items():
            if key in context.lower():
                for file_name in files:
                    content = self.read_source(file_name, 0, 50)
                    if content:
                        return f"// {file_name}.kt\n{content[:1000]}..."
        
        return ""
    
    def suggest_update(self) -> str:
        """
        建议更新操作
        
        Returns:
            更新建议
        """
        check_result = self.check_repository()
        
        if not check_result["exists"]:
            return f"""
Legado仓库不存在，请先克隆：

cd {Path(__file__).parent.parent.parent}
git clone {self.LEGADO_REPO_URL}.git legado

或者手动下载源码到 legado/ 目录。
"""
        
        if check_result["missing_files"]:
            return f"""
Legado仓库不完整，缺少文件：{', '.join(check_result['missing_files'])}

建议更新仓库：
cd {self.legado_path}
git pull origin master
"""
        
        return "Legado仓库完整，可以正常参考源码。"


def check_legado_update():
    """
    检查Legado更新
    
    Returns:
        检查结果
    """
    checker = LegadoChecker()
    return checker.check_repository()


def get_legado_reference(context: str) -> str:
    """
    获取Legado源码参考
    
    Args:
        context: 上下文描述
        
    Returns:
        参考代码
    """
    checker = LegadoChecker()
    return checker.get_reference_code(context)


if __name__ == "__main__":
    checker = LegadoChecker()
    
    print("=" * 60)
    print("Legado Repository Checker")
    print("=" * 60)
    
    result = checker.check_repository()
    print(f"\n仓库状态: {result['message']}")
    
    if result["exists"]:
        print(f"\n仓库路径: {result['path']}")
        
        analyze_result = checker.check_analyze_rule()
        print(f"\nAnalyzeRule状态: {analyze_result['message']}")
        
        if analyze_result["key_functions"]:
            print("\n关键函数:")
            for func, info in analyze_result["key_functions"].items():
                status = "✓" if info["exists"] else "✗"
                line = f" (行 {info['line']})" if info['line'] is not None else ""
                print(f"  {status} {func}{line}")
    
    print("\n" + checker.suggest_update())
