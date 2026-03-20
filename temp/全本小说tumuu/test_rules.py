# -*- coding: utf-8 -*-
import sys
sys.path.insert(0, r'g:\Project\阅读SKills\legadoSkill-main\.trae\skills\legado-book-source-tamer\scripts')
from batch_fetcher import BatchFetcher
from bs4 import BeautifulSoup
import json

base_url = 'https://www.tumuu.com/'

# 获取分类页面
urls = {
    'category': f'{base_url}fenlei1/',
    'detail': f'{base_url}xiaoshuo/21/21941/',
    'content': f'{base_url}xiaoshuo/21/21941/12436727.html',
}

fetcher = BatchFetcher(max_concurrent=4, timeout=20)
results, errors = fetcher.fetch_with_headers(urls)

# 测试发现规则
print('=== 测试发现规则 ===')
content = results.get('category', '')
soup = BeautifulSoup(content, 'html.parser')
books = soup.select('tr[bgcolor="#FFFFFF"]')
print(f'找到 {len(books)} 本书')

for book in books[:3]:
    tds = book.select('td')
    if len(tds) >= 6:
        name_elem = tds[0].select_one('a')
        if name_elem:
            name = name_elem.get_text(strip=True)
            url = name_elem.get('href', '')
            print(f'  书名: {name}, URL: {url}')
        author = tds[2].get_text(strip=True)
        print(f'  作者: {author}')
    print('---')

# 测试详情规则
print('\n=== 测试详情规则 ===')
content = results.get('detail', '')
soup = BeautifulSoup(content, 'html.parser')
author = soup.select_one('meta[property="og:novel:author"]')
if author:
    print(f'作者: {author.get("content", "")}')
name = soup.select_one('meta[property="og:title"]')
if name:
    print(f'书名: {name.get("content", "")}')
intro = soup.select_one('meta[property="og:description"]')
if intro:
    print(f'简介: {intro.get("content", "")[:100]}...')

# 测试目录规则
print('\n=== 测试目录规则 ===')
chapters = soup.select('#at td.L a')
print(f'找到 {len(chapters)} 个章节')
for ch in chapters[:3]:
    print(f'  章节: {ch.get_text(strip=True)}, URL: {ch.get("href", "")}')

# 测试正文规则
print('\n=== 测试正文规则 ===')
content = results.get('content', '')
soup = BeautifulSoup(content, 'html.parser')
content_elem = soup.select_one('#htmlContent')
if content_elem:
    text = content_elem.get_text(strip=True)
    print(f'正文长度: {len(text)} 字符')
    print(f'正文前200字: {text[:200]}...')
