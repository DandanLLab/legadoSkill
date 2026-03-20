import sys
sys.path.insert(0, r'g:\Project\阅读SKills\legadoSkill-main\.trae\skills\legado-book-source-tamer\scripts')
from batch_fetcher import BatchFetcher
import json

base_url = "https://www.43kanshu.com"

urls = {
    "homepage": base_url,
    "search_test": f"{base_url}/search.html?searchkey=斗罗",
    "search_alt1": f"{base_url}/search.php?searchkey=斗罗",
    "search_alt2": f"{base_url}/modules/article/search.php?searchkey=斗罗",
    "category_xuanhuan": f"{base_url}/xuanhuan/",
    "category_wuxia": f"{base_url}/wuxia/",
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

fetcher = BatchFetcher(max_concurrent=6, timeout=30)
results, errors = fetcher.fetch_with_headers(urls, headers)

print("\n=== 抓取结果 ===")
for task_id, content in results.items():
    print(f"\n[{task_id}] 长度: {len(content)} bytes")
    print(f"前500字符: {content[:500]}")
    print("-" * 50)

print("\n=== 错误信息 ===")
for task_id, error in errors.items():
    print(f"[{task_id}] {error}")

with open(r'g:\Project\阅读SKills\legadoSkill-main\temp\43kanshu_fetch_results.json', 'w', encoding='utf-8') as f:
    json.dump({"results": {k: v[:2000] for k, v in results.items()}, "errors": errors}, f, ensure_ascii=False, indent=2)
print("\n结果已保存到 temp/43kanshu_fetch_results.json")
