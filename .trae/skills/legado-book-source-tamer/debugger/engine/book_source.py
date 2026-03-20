"""
BookSource Data Models - Python Implementation
Translated from Kotlin: io.legado.app.data.entities

This module defines the data structures for book sources,
including all rule types and configurations.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
from enum import Enum
import json


class BookSourceType(Enum):
    TEXT = 0
    AUDIO = 1
    IMAGE = 2
    FILE = 3
    VIDEO = 4


@dataclass
class BookInfoRule:
    init: Optional[str] = None
    name: Optional[str] = None
    author: Optional[str] = None
    intro: Optional[str] = None
    kind: Optional[str] = None
    lastChapter: Optional[str] = None
    updateTime: Optional[str] = None
    coverUrl: Optional[str] = None
    tocUrl: Optional[str] = None
    wordCount: Optional[str] = None
    canReName: Optional[str] = None
    downloadUrls: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BookInfoRule':
        return cls(
            init=data.get('init'),
            name=data.get('name'),
            author=data.get('author'),
            intro=data.get('intro'),
            kind=data.get('kind'),
            lastChapter=data.get('lastChapter'),
            updateTime=data.get('updateTime'),
            coverUrl=data.get('coverUrl'),
            tocUrl=data.get('tocUrl'),
            wordCount=data.get('wordCount'),
            canReName=data.get('canReName'),
            downloadUrls=data.get('downloadUrls'),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.init: result['init'] = self.init
        if self.name: result['name'] = self.name
        if self.author: result['author'] = self.author
        if self.intro: result['intro'] = self.intro
        if self.kind: result['kind'] = self.kind
        if self.lastChapter: result['lastChapter'] = self.lastChapter
        if self.updateTime: result['updateTime'] = self.updateTime
        if self.coverUrl: result['coverUrl'] = self.coverUrl
        if self.tocUrl: result['tocUrl'] = self.tocUrl
        if self.wordCount: result['wordCount'] = self.wordCount
        if self.canReName: result['canReName'] = self.canReName
        if self.downloadUrls: result['downloadUrls'] = self.downloadUrls
        return result


@dataclass
class ContentRule:
    content: Optional[str] = None
    subContent: Optional[str] = None
    title: Optional[str] = None
    nextContentUrl: Optional[str] = None
    webJs: Optional[str] = None
    sourceRegex: Optional[str] = None
    replaceRegex: Optional[str] = None
    imageStyle: Optional[str] = None
    imageDecode: Optional[str] = None
    payAction: Optional[str] = None
    callBackJs: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentRule':
        return cls(
            content=data.get('content'),
            subContent=data.get('subContent'),
            title=data.get('title'),
            nextContentUrl=data.get('nextContentUrl'),
            webJs=data.get('webJs'),
            sourceRegex=data.get('sourceRegex'),
            replaceRegex=data.get('replaceRegex'),
            imageStyle=data.get('imageStyle'),
            imageDecode=data.get('imageDecode'),
            payAction=data.get('payAction'),
            callBackJs=data.get('callBackJs'),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.content: result['content'] = self.content
        if self.subContent: result['subContent'] = self.subContent
        if self.title: result['title'] = self.title
        if self.nextContentUrl: result['nextContentUrl'] = self.nextContentUrl
        if self.webJs: result['webJs'] = self.webJs
        if self.sourceRegex: result['sourceRegex'] = self.sourceRegex
        if self.replaceRegex: result['replaceRegex'] = self.replaceRegex
        if self.imageStyle: result['imageStyle'] = self.imageStyle
        if self.imageDecode: result['imageDecode'] = self.imageDecode
        if self.payAction: result['payAction'] = self.payAction
        if self.callBackJs: result['callBackJs'] = self.callBackJs
        return result


@dataclass
class SearchRule:
    checkKeyWord: Optional[str] = None
    bookList: Optional[str] = None
    name: Optional[str] = None
    author: Optional[str] = None
    intro: Optional[str] = None
    kind: Optional[str] = None
    lastChapter: Optional[str] = None
    updateTime: Optional[str] = None
    bookUrl: Optional[str] = None
    coverUrl: Optional[str] = None
    wordCount: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SearchRule':
        return cls(
            checkKeyWord=data.get('checkKeyWord'),
            bookList=data.get('bookList'),
            name=data.get('name'),
            author=data.get('author'),
            intro=data.get('intro'),
            kind=data.get('kind'),
            lastChapter=data.get('lastChapter'),
            updateTime=data.get('updateTime'),
            bookUrl=data.get('bookUrl'),
            coverUrl=data.get('coverUrl'),
            wordCount=data.get('wordCount'),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.checkKeyWord: result['checkKeyWord'] = self.checkKeyWord
        if self.bookList: result['bookList'] = self.bookList
        if self.name: result['name'] = self.name
        if self.author: result['author'] = self.author
        if self.intro: result['intro'] = self.intro
        if self.kind: result['kind'] = self.kind
        if self.lastChapter: result['lastChapter'] = self.lastChapter
        if self.updateTime: result['updateTime'] = self.updateTime
        if self.bookUrl: result['bookUrl'] = self.bookUrl
        if self.coverUrl: result['coverUrl'] = self.coverUrl
        if self.wordCount: result['wordCount'] = self.wordCount
        return result


@dataclass
class TocRule:
    preUpdateJs: Optional[str] = None
    chapterList: Optional[str] = None
    chapterName: Optional[str] = None
    chapterUrl: Optional[str] = None
    formatJs: Optional[str] = None
    isVolume: Optional[str] = None
    isVip: Optional[str] = None
    isPay: Optional[str] = None
    updateTime: Optional[str] = None
    nextTocUrl: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TocRule':
        return cls(
            preUpdateJs=data.get('preUpdateJs'),
            chapterList=data.get('chapterList'),
            chapterName=data.get('chapterName'),
            chapterUrl=data.get('chapterUrl'),
            formatJs=data.get('formatJs'),
            isVolume=data.get('isVolume'),
            isVip=data.get('isVip'),
            isPay=data.get('isPay'),
            updateTime=data.get('updateTime'),
            nextTocUrl=data.get('nextTocUrl'),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.preUpdateJs: result['preUpdateJs'] = self.preUpdateJs
        if self.chapterList: result['chapterList'] = self.chapterList
        if self.chapterName: result['chapterName'] = self.chapterName
        if self.chapterUrl: result['chapterUrl'] = self.chapterUrl
        if self.formatJs: result['formatJs'] = self.formatJs
        if self.isVolume: result['isVolume'] = self.isVolume
        if self.isVip: result['isVip'] = self.isVip
        if self.isPay: result['isPay'] = self.isPay
        if self.updateTime: result['updateTime'] = self.updateTime
        if self.nextTocUrl: result['nextTocUrl'] = self.nextTocUrl
        return result


@dataclass
class ExploreRule:
    bookList: Optional[str] = None
    name: Optional[str] = None
    author: Optional[str] = None
    intro: Optional[str] = None
    kind: Optional[str] = None
    lastChapter: Optional[str] = None
    updateTime: Optional[str] = None
    bookUrl: Optional[str] = None
    coverUrl: Optional[str] = None
    wordCount: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ExploreRule':
        return cls(
            bookList=data.get('bookList'),
            name=data.get('name'),
            author=data.get('author'),
            intro=data.get('intro'),
            kind=data.get('kind'),
            lastChapter=data.get('lastChapter'),
            updateTime=data.get('updateTime'),
            bookUrl=data.get('bookUrl'),
            coverUrl=data.get('coverUrl'),
            wordCount=data.get('wordCount'),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        result = {}
        if self.bookList: result['bookList'] = self.bookList
        if self.name: result['name'] = self.name
        if self.author: result['author'] = self.author
        if self.intro: result['intro'] = self.intro
        if self.kind: result['kind'] = self.kind
        if self.lastChapter: result['lastChapter'] = self.lastChapter
        if self.updateTime: result['updateTime'] = self.updateTime
        if self.bookUrl: result['bookUrl'] = self.bookUrl
        if self.coverUrl: result['coverUrl'] = self.coverUrl
        if self.wordCount: result['wordCount'] = self.wordCount
        return result


@dataclass
class BookSource:
    bookSourceUrl: str = ""
    bookSourceName: str = ""
    bookSourceGroup: Optional[str] = None
    bookSourceType: int = 0
    bookUrlPattern: Optional[str] = None
    customOrder: int = 0
    enabled: bool = True
    enabledExplore: bool = True
    jsLib: Optional[str] = None
    enabledCookieJar: Optional[bool] = True
    concurrentRate: Optional[str] = None
    header: Optional[str] = None
    loginUrl: Optional[str] = None
    loginUi: Optional[str] = None
    loginCheckJs: Optional[str] = None
    coverDecodeJs: Optional[str] = None
    bookSourceComment: Optional[str] = None
    variableComment: Optional[str] = None
    lastUpdateTime: int = 0
    respondTime: int = 180000
    weight: int = 0
    exploreUrl: Optional[str] = None
    exploreScreen: Optional[str] = None
    ruleExplore: Optional[ExploreRule] = None
    searchUrl: Optional[str] = None
    ruleSearch: Optional[SearchRule] = None
    ruleBookInfo: Optional[BookInfoRule] = None
    ruleToc: Optional[TocRule] = None
    ruleContent: Optional[ContentRule] = None
    
    def __post_init__(self):
        if isinstance(self.ruleSearch, dict):
            self.ruleSearch = SearchRule.from_dict(self.ruleSearch)
        if isinstance(self.ruleBookInfo, dict):
            self.ruleBookInfo = BookInfoRule.from_dict(self.ruleBookInfo)
        if isinstance(self.ruleToc, dict):
            self.ruleToc = TocRule.from_dict(self.ruleToc)
        if isinstance(self.ruleContent, dict):
            self.ruleContent = ContentRule.from_dict(self.ruleContent)
        if isinstance(self.ruleExplore, dict):
            self.ruleExplore = ExploreRule.from_dict(self.ruleExplore)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BookSource':
        return cls(
            bookSourceUrl=data.get('bookSourceUrl', ''),
            bookSourceName=data.get('bookSourceName', ''),
            bookSourceGroup=data.get('bookSourceGroup'),
            bookSourceType=data.get('bookSourceType', 0),
            bookUrlPattern=data.get('bookUrlPattern'),
            customOrder=data.get('customOrder', 0),
            enabled=data.get('enabled', True),
            enabledExplore=data.get('enabledExplore', True),
            jsLib=data.get('jsLib'),
            enabledCookieJar=data.get('enabledCookieJar'),
            concurrentRate=data.get('concurrentRate'),
            header=data.get('header'),
            loginUrl=data.get('loginUrl'),
            loginUi=data.get('loginUi'),
            loginCheckJs=data.get('loginCheckJs'),
            coverDecodeJs=data.get('coverDecodeJs'),
            bookSourceComment=data.get('bookSourceComment'),
            variableComment=data.get('variableComment'),
            lastUpdateTime=data.get('lastUpdateTime', 0),
            respondTime=data.get('respondTime', 180000),
            weight=data.get('weight', 0),
            exploreUrl=data.get('exploreUrl'),
            exploreScreen=data.get('exploreScreen'),
            ruleExplore=ExploreRule.from_dict(data['ruleExplore']) if data.get('ruleExplore') else None,
            searchUrl=data.get('searchUrl'),
            ruleSearch=SearchRule.from_dict(data['ruleSearch']) if data.get('ruleSearch') else None,
            ruleBookInfo=BookInfoRule.from_dict(data['ruleBookInfo']) if data.get('ruleBookInfo') else None,
            ruleToc=TocRule.from_dict(data['ruleToc']) if data.get('ruleToc') else None,
            ruleContent=ContentRule.from_dict(data['ruleContent']) if data.get('ruleContent') else None,
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'BookSource':
        data = json.loads(json_str)
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
        return cls.from_dict(data)
    
    def to_dict(self) -> Dict[str, Any]:
        result = {
            'bookSourceUrl': self.bookSourceUrl,
            'bookSourceName': self.bookSourceName,
            'bookSourceType': self.bookSourceType,
            'enabled': self.enabled,
            'enabledExplore': self.enabledExplore,
        }
        
        if self.bookSourceGroup: result['bookSourceGroup'] = self.bookSourceGroup
        if self.bookUrlPattern: result['bookUrlPattern'] = self.bookUrlPattern
        if self.customOrder: result['customOrder'] = self.customOrder
        if self.jsLib: result['jsLib'] = self.jsLib
        if self.enabledCookieJar is not None: result['enabledCookieJar'] = self.enabledCookieJar
        if self.concurrentRate: result['concurrentRate'] = self.concurrentRate
        if self.header: result['header'] = self.header
        if self.loginUrl: result['loginUrl'] = self.loginUrl
        if self.loginUi: result['loginUi'] = self.loginUi
        if self.loginCheckJs: result['loginCheckJs'] = self.loginCheckJs
        if self.coverDecodeJs: result['coverDecodeJs'] = self.coverDecodeJs
        if self.bookSourceComment: result['bookSourceComment'] = self.bookSourceComment
        if self.variableComment: result['variableComment'] = self.variableComment
        if self.lastUpdateTime: result['lastUpdateTime'] = self.lastUpdateTime
        if self.respondTime: result['respondTime'] = self.respondTime
        if self.weight: result['weight'] = self.weight
        if self.exploreUrl: result['exploreUrl'] = self.exploreUrl
        if self.exploreScreen: result['exploreScreen'] = self.exploreScreen
        if self.searchUrl: result['searchUrl'] = self.searchUrl
        
        if self.ruleExplore:
            result['ruleExplore'] = self.ruleExplore.to_dict()
        if self.ruleSearch:
            result['ruleSearch'] = self.ruleSearch.to_dict()
        if self.ruleBookInfo:
            result['ruleBookInfo'] = self.ruleBookInfo.to_dict()
        if self.ruleToc:
            result['ruleToc'] = self.ruleToc.to_dict()
        if self.ruleContent:
            result['ruleContent'] = self.ruleContent.to_dict()
        
        return result
    
    def to_json(self, indent: int = 2) -> str:
        return json.dumps([self.to_dict()], ensure_ascii=False, indent=indent)
    
    def get_tag(self) -> str:
        return self.bookSourceName
    
    def get_key(self) -> str:
        return self.bookSourceUrl
