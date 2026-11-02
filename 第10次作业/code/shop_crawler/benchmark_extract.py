import csv
import re
import time
import requests
from pathlib import Path
from bs4 import BeautifulSoup
from scrapy.selector import Selector

DATA_DIR = Path("../../data")
CSV_PATH = DATA_DIR / "books_116.csv"
RESULT_PATH = DATA_DIR / "extract_benchmark.csv"

REPEAT = 1000

with CSV_PATH.open(encoding="utf-8-sig", newline="") as f:
    first = next(csv.DictReader(f))

url = first["product_url"]

session = requests.Session()
session.trust_env = False

response = session.get(url, timeout=20)
response.raise_for_status()
html = response.text

def extract_regex():
    title = re.search(r'<h1[^>]*>(.*?)</h1>', html, re.S)
    price = re.search(
        r'<p[^>]*class="price_color"[^>]*>(.*?)</p>',
        html,
        re.S
    )
    return (
        title.group(1).strip() if title else "",
        price.group(1).strip() if price else ""
    )

def extract_bs4():
    soup = BeautifulSoup(html, "html.parser")
    title = soup.select_one(".product_main h1")
    price = soup.select_one(".product_main .price_color")
    return (
        title.get_text(strip=True) if title else "",
        price.get_text(strip=True) if price else ""
    )

def extract_css():
    selector = Selector(text=html)
    title = selector.css(".product_main h1::text").get()
    price = selector.css(".product_main .price_color::text").get()
    return (title or "", price or "")

def extract_xpath():
    selector = Selector(text=html)
    title = selector.xpath(
        '//div[contains(@class,"product_main")]/h1/text()'
    ).get()
    price = selector.xpath(
        '//div[contains(@class,"product_main")]'
        '//p[contains(@class,"price_color")]/text()'
    ).get()
    return (title or "", price or "")

methods = {
    "Regex": extract_regex,
    "BeautifulSoup": extract_bs4,
    "CSS": extract_css,
    "XPath": extract_xpath,
}

print("========== 提取正确性检查 ==========")

results = {}

for name, func in methods.items():
    result = func()
    results[name] = result
    print(name, result)

if len(set(results.values())) != 1:
    raise SystemExit("四种方法结果不一致，请检查提取规则")

print("\n========== 性能测试 ==========")

benchmark = []

for name, func in methods.items():
    start = time.perf_counter()

    for _ in range(REPEAT):
        func()

    elapsed = time.perf_counter() - start
    average_ms = elapsed / REPEAT * 1000

    benchmark.append({
        "method": name,
        "repeat": REPEAT,
        "total_seconds": round(elapsed, 6),
        "average_ms": round(average_ms, 6),
    })

    print(
        f"{name:<15} "
        f"总耗时: {elapsed:.6f}s "
        f"平均: {average_ms:.6f}ms"
    )

with RESULT_PATH.open("w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["method", "repeat", "total_seconds", "average_ms"]
    )
    writer.writeheader()
    writer.writerows(benchmark)

print("\n性能结果已保存:", RESULT_PATH)
