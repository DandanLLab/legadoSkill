"""
Legado Kotlin Source Code Index
真实Legado Kotlin源码索引和引用

本模块提供对克隆的Legado Kotlin源码的直接访问和引用。
源码位置: legado_source/app/src/main/java/io/legado/app/
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class KotlinSourceFile:
    file_path: str
    package_name: str
    class_name: str
    description: str
    importance: str  # core, important, reference


class LegadoKotlinSourceIndex:
    """
    Legado Kotlin源码索引
    
    提供对真实Legado源码的快速访问和引用。
    源码已克隆到: legado_source/
    """
    
    BASE_PATH = Path(__file__).parent.parent.parent / "legado_source" / "app" / "src" / "main" / "java" / "io" / "legado" / "app"
    
    CORE_FILES: Dict[str, KotlinSourceFile] = {
        "AnalyzeRule": KotlinSourceFile(
            file_path="model/analyzeRule/AnalyzeRule.kt",
            package_name="io.legado.app.model.analyzeRule",
            class_name="AnalyzeRule",
            description="核心规则分析引擎 - 支持CSS、XPath、JSONPath、正则、JS等多种规则",
            importance="core"
        ),
        "AnalyzeByJSoup": KotlinSourceFile(
            file_path="model/analyzeRule/AnalyzeByJSoup.kt",
            package_name="io.legado.app.model.analyzeRule",
            class_name="AnalyzeByJSoup",
            description="JSoup HTML解析器 - CSS选择器和元素提取",
            importance="core"
        ),
        "AnalyzeByXPath": KotlinSourceFile(
            file_path="model/analyzeRule/AnalyzeByXPath.kt",
            package_name="io.legado.app.model.analyzeRule",
            class_name="AnalyzeByXPath",
            description="XPath解析器 - XML路径语言解析",
            importance="core"
        ),
        "AnalyzeByJSonPath": KotlinSourceFile(
            file_path="model/analyzeRule/AnalyzeByJSonPath.kt",
            package_name="io.legado.app.model.analyzeRule",
            class_name="AnalyzeByJSonPath",
            description="JSONPath解析器 - JSON数据提取",
            importance="core"
        ),
        "AnalyzeByRegex": KotlinSourceFile(
            file_path="model/analyzeRule/AnalyzeByRegex.kt",
            package_name="io.legado.app.model.analyzeRule",
            class_name="AnalyzeByRegex",
            description="正则表达式解析器 - 文本匹配和提取",
            importance="core"
        ),
        "AnalyzeUrl": KotlinSourceFile(
            file_path="model/analyzeRule/AnalyzeUrl.kt",
            package_name="io.legado.app.model.analyzeRule",
            class_name="AnalyzeUrl",
            description="URL分析器 - 构建和处理请求URL",
            importance="core"
        ),
        "RuleAnalyzer": KotlinSourceFile(
            file_path="model/analyzeRule/RuleAnalyzer.kt",
            package_name="io.legado.app.model.analyzeRule",
            class_name="RuleAnalyzer",
            description="规则分析器 - 解析和拆分规则字符串",
            importance="core"
        ),
        "BookSource": KotlinSourceFile(
            file_path="data/entities/BookSource.kt",
            package_name="io.legado.app.data.entities",
            class_name="BookSource",
            description="书源实体类 - 书源数据结构定义",
            importance="core"
        ),
        "BookInfoRule": KotlinSourceFile(
            file_path="data/entities/rule/BookInfoRule.kt",
            package_name="io.legado.app.data.entities.rule",
            class_name="BookInfoRule",
            description="书籍详情规则 - 书籍信息提取规则",
            importance="core"
        ),
        "ContentRule": KotlinSourceFile(
            file_path="data/entities/rule/ContentRule.kt",
            package_name="io.legado.app.data.entities.rule",
            class_name="ContentRule",
            description="正文规则 - 正文内容提取规则",
            importance="core"
        ),
        "SearchRule": KotlinSourceFile(
            file_path="data/entities/rule/SearchRule.kt",
            package_name="io.legado.app.data.entities.rule",
            class_name="SearchRule",
            description="搜索规则 - 搜索结果提取规则",
            importance="core"
        ),
        "TocRule": KotlinSourceFile(
            file_path="data/entities/rule/TocRule.kt",
            package_name="io.legado.app.data.entities.rule",
            class_name="TocRule",
            description="目录规则 - 章节列表提取规则",
            importance="core"
        ),
        "WebBook": KotlinSourceFile(
            file_path="model/webBook/WebBook.kt",
            package_name="io.legado.app.model.webBook",
            class_name="WebBook",
            description="网页书籍获取 - HTTP请求和内容获取",
            importance="core"
        ),
        "SourceDebug": KotlinSourceFile(
            file_path="model/Debug.kt",
            package_name="io.legado.app.model",
            class_name="Debug",
            description="书源调试 - 书源测试和调试功能",
            importance="core"
        ),
    }
    
    JS_ENGINE_FILES: Dict[str, KotlinSourceFile] = {
        "RhinoScriptEngine": KotlinSourceFile(
            file_path="help/rhino/RhinoScriptEngine.kt",
            package_name="io.legado.app.help.rhino",
            class_name="RhinoScriptEngine",
            description="Rhino JS引擎 - JavaScript执行引擎",
            importance="core"
        ),
        "JsExtensions": KotlinSourceFile(
            file_path="help/JsExtensions.kt",
            package_name="io.legado.app.help",
            class_name="JsExtensions",
            description="JS扩展 - JavaScript扩展函数",
            importance="important"
        ),
        "JsEncodeUtils": KotlinSourceFile(
            file_path="help/JsEncodeUtils.kt",
            package_name="io.legado.app.help",
            class_name="JsEncodeUtils",
            description="JS编码工具 - 编码解码工具函数",
            importance="important"
        ),
    }
    
    HELPER_FILES: Dict[str, KotlinSourceFile] = {
        "HttpHelper": KotlinSourceFile(
            file_path="help/http/HttpHelper.kt",
            package_name="io.legado.app.help.http",
            class_name="HttpHelper",
            description="HTTP帮助类 - HTTP请求辅助功能",
            importance="important"
        ),
        "CookieManager": KotlinSourceFile(
            file_path="help/http/CookieManager.kt",
            package_name="io.legado.app.help.http",
            class_name="CookieManager",
            description="Cookie管理器 - Cookie存储和管理",
            importance="important"
        ),
        "BackstageWebView": KotlinSourceFile(
            file_path="help/http/BackstageWebView.kt",
            package_name="io.legado.app.help.http",
            class_name="BackstageWebView",
            description="后台WebView - 动态内容加载",
            importance="important"
        ),
    }
    
    @classmethod
    def get_source_path(cls, name: str) -> Optional[Path]:
        """获取源码文件路径"""
        if name in cls.CORE_FILES:
            return cls.BASE_PATH / cls.CORE_FILES[name].file_path
        elif name in cls.JS_ENGINE_FILES:
            return cls.BASE_PATH / cls.JS_ENGINE_FILES[name].file_path
        elif name in cls.HELPER_FILES:
            return cls.BASE_PATH / cls.HELPER_FILES[name].file_path
        return None
    
    @classmethod
    def read_source(cls, name: str) -> Optional[str]:
        """读取源码内容"""
        path = cls.get_source_path(name)
        if path and path.exists():
            return path.read_text(encoding='utf-8')
        return None
    
    @classmethod
    def list_core_files(cls) -> List[KotlinSourceFile]:
        """列出所有核心文件"""
        return list(cls.CORE_FILES.values())
    
    @classmethod
    def list_js_engine_files(cls) -> List[KotlinSourceFile]:
        """列出所有JS引擎相关文件"""
        return list(cls.JS_ENGINE_FILES.values())
    
    @classmethod
    def get_file_info(cls, name: str) -> Optional[KotlinSourceFile]:
        """获取文件信息"""
        if name in cls.CORE_FILES:
            return cls.CORE_FILES[name]
        elif name in cls.JS_ENGINE_FILES:
            return cls.JS_ENGINE_FILES[name]
        elif name in cls.HELPER_FILES:
            return cls.HELPER_FILES[name]
        return None
    
    @classmethod
    def search_files(cls, keyword: str) -> List[KotlinSourceFile]:
        """搜索文件"""
        results = []
        keyword_lower = keyword.lower()
        
        for file_info in cls.CORE_FILES.values():
            if (keyword_lower in file_info.class_name.lower() or 
                keyword_lower in file_info.description.lower()):
                results.append(file_info)
        
        for file_info in cls.JS_ENGINE_FILES.values():
            if (keyword_lower in file_info.class_name.lower() or 
                keyword_lower in file_info.description.lower()):
                results.append(file_info)
        
        for file_info in cls.HELPER_FILES.values():
            if (keyword_lower in file_info.class_name.lower() or 
                keyword_lower in file_info.description.lower()):
                results.append(file_info)
        
        return results


def get_legado_source(name: str) -> Optional[str]:
    """便捷函数：获取Legado源码"""
    return LegadoKotlinSourceIndex.read_source(name)


def list_all_sources() -> Dict[str, List[KotlinSourceFile]]:
    """便捷函数：列出所有源码文件"""
    return {
        "core": LegadoKotlinSourceIndex.list_core_files(),
        "js_engine": LegadoKotlinSourceIndex.list_js_engine_files(),
        "helpers": list(LegadoKotlinSourceIndex.HELPER_FILES.values()),
    }
