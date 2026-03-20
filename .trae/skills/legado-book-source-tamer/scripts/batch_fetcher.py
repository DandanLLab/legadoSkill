"""
批量并行抓取模块
用于同时抓取多个页面，提高书源创建效率
"""
import asyncio
import aiohttp
from typing import Dict, Tuple
import time
class BatchFetcher:
    """
    批量并行抓取器
    支持同时抓取多个 URL，大幅提升网站分析速度
    """
    def __init__(self, max_concurrent: int = 4, timeout: int = 30):
        self.max_concurrent = max_concurrent
        self.timeout = timeout
        self.results = {}
        self.errors = {}
    async def _fetch_url(self, session, url, task_id):
        try:
            async with session.get(url, timeout=self.timeout) as response:
                content = await response.text(encoding='utf-8', errors='replace')
                return (task_id, content, None)
        except Exception as e:
            return (task_id, None, str(e))
    async def _fetch_all(self, urls):
        self.results = {}
        self.errors = {}
        connector = aiohttp.TCPConnector(limit=self.max_concurrent)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = []
            for task_id, url in urls.items():
                task = asyncio.create_task(self._fetch_url(session, url, task_id))
                tasks.append(task)
            for future in asyncio.as_completed(tasks):
                task_id, content, error = await future
                if content:
                    self.results[task_id] = content
                else:
                    self.errors[task_id] = error
        return self.results
    def fetch_multiple(self, urls):
        start_time = time.time()
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        results = loop.run_until_complete(self._fetch_all(urls))
        elapsed = time.time() - start_time
        print(f"批量抓取完成：成功{len(results)}/{len(urls)}个页面，耗时{elapsed:.2f}秒")
        return self.results, self.errors
    def fetch_with_headers(self, urls, headers=None):
        self.results = {}
        self.errors = {}
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            }
        async def fetch_with_headers_inner():
            connector = aiohttp.TCPConnector(limit=self.max_concurrent)
            async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
                tasks = []
                for task_id, url in urls.items():
                    task = asyncio.create_task(self._fetch_url(session, url, task_id))
                    tasks.append(task)
                for future in asyncio.as_completed(tasks):
                    task_id, content, error = await future
                    if content:
                        self.results[task_id] = content
                    else:
                        self.errors[task_id] = error
        start_time = time.time()
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        loop.run_until_complete(fetch_with_headers_inner())
        elapsed = time.time() - start_time
        print(f"批量抓取完成：成功{len(self.results)}/{len(urls)}个页面，耗时{elapsed:.2f}秒")
        return self.results, self.errors
def quick_analyze_site(base_url, max_concurrent=4):
    test_urls = {
        "homepage": base_url,
        "mobile_home": f"{base_url.rstrip('/')}/m/",
        "search_simple": f"{base_url.rstrip('/')}/search.html",
        "search_api": f"{base_url.rstrip('/')}/modules/article/search.php?searchtype=articlename&searchkey=%E6%B5%8B%E8%AF%95",
    }
    categories = ["xuanhuan", "wuxia", "dushi", "lishi", "kehuan", "youxi", "nvsheng", "qita"]
    for cat in categories:
        test_urls[f"category_{cat}"] = f"{base_url.rstrip('/')}/{cat}/"
    fetcher = BatchFetcher(max_concurrent=max_concurrent, timeout=20)
    results, errors = fetcher.fetch_with_headers(test_urls)
    print(f"\n网站结构分析结果：")
    print(f"  成功页面：{len(results)} 个")
    print(f"  失败页面：{len(errors)} 个")
    for task_id, content in results.items():
        if content:
            print(f"  ✓ {task_id}: {len(content)} bytes")
    for task_id, error in errors.items():
        print(f"  ✗ {task_id}: {error}")
    return results, errors
