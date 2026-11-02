
"""
作业②：商城商品比价定向爬虫
使用 requests 和 re 提取当当网书包商品的价格和名称。
"""

import csv
import html
import re
from decimal import Decimal
from pathlib import Path

import requests


# 当当网搜索页，关键词为“书包”（GBK URL 编码）
URL = "https://search.dangdang.com/?key=%CA%E9%B0%FC&act=input"

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_FILE = BASE_DIR / "data" / "schoolbag_prices.csv"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    )
}


def fetch_page():
    """请求商品搜索页面，返回 HTML 字符串。"""
    response = requests.get(
        URL,
        headers=HEADERS,
        timeout=20
    )
    response.raise_for_status()

    # 当当网页面通常采用 GBK 系列中文编码
    response.encoding = "gb18030"
    return response.text


def parse_products(page_html):
    """使用正则表达式提取同一商品块内的名称和价格。"""

    # 每个商品对应一个带有商品标识的 li 元素
    item_pattern = re.compile(
        r'<li\b[^>]*\bddt-pit="[^"]*"[^>]*>.*?</li>',
        re.S | re.I
    )

    # 商品售价
    price_pattern = re.compile(
        r'class=["\'][^"\']*\bprice_n\b[^"\']*["\']'
        r'[^>]*>\s*(?:&yen;|&#165;|¥)?\s*'
        r'(\d+(?:\.\d{1,2})?)',
        re.S | re.I
    )

    # 商品链接的 title 属性
    name_pattern = re.compile(
        r'<a\b(?=[^>]*\btitle=["\']([^"\']+)["\'])'
        r'(?=[^>]*\bname=["\']itemlist-title["\'])'
        r'[^>]*>',
        re.S | re.I
    )

    products = []
    seen = set()

    for item in item_pattern.findall(page_html):
        price_match = price_pattern.search(item)
        name_match = name_pattern.search(item)

        if not price_match or not name_match:
            continue

        price = Decimal(price_match.group(1))
        name = html.unescape(name_match.group(1)).strip()

        if not name or (name, price) in seen:
            continue

        seen.add((name, price))
        products.append((price, name))

    return sorted(products, key=lambda product: product[0])


def print_products(products):
    """输出商品价格比较表。"""
    print(f"{'序号':<6}{'价格':<12}商品名称")
    print("-" * 85)

    for index, (price, name) in enumerate(products, start=1):
        print(f"{index:<6}{str(price):<12}{name}")

    print("-" * 85)
    print(f"成功提取 {len(products)} 件商品。")


def save_csv(products):
    """将商品名称及价格保存为 CSV 文件。"""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow(["序号", "价格", "商品名称"])

        for index, (price, name) in enumerate(products, start=1):
            writer.writerow([index, f"{price:.2f}", name])

    print(f"CSV 保存位置：{OUTPUT_FILE}")


def main():
    try:
        page_html = fetch_page()

        # 保存原始网页，便于检查和调试正则表达式
        raw_file = BASE_DIR / "data" / "dangdang_schoolbag.html"
        raw_file.write_text(page_html, encoding="utf-8")

        products = parse_products(page_html)

        if not products:
            print("未提取到商品。请检查网页结构或访问限制。")
            print(f"原始 HTML 已保存：{raw_file}")
            return

        print_products(products)
        save_csv(products)

    except requests.RequestException as error:
        print(f"网络请求失败：{error}")


if __name__ == "__main__":
    main()
