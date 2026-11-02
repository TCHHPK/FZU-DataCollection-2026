import urllib3
import re
import html as html_lib

http = urllib3.PoolManager()

url = "https://search.dangdang.com/?key=%CA%E9%B0%FC"

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/154.0.0.0 Safari/537.36"
    )
}

response = http.request(
    "GET",
    url,
    headers=headers
)

print("HTTP状态码：", response.status)

html = response.data.decode("gbk", errors="ignore")

# 商品名称：
# <a title="..." ... name="itemlist-title" ...>
name_pattern = re.compile(
    r'<a\s+title="(.*?)"[^>]*name="itemlist-title"',
    re.S
)

# 商品价格：
# <span class="price_n">&yen;146.00</span>
price_pattern = re.compile(
    r'<span\s+class="price_n">\s*&yen;([\d.]+)\s*</span>',
    re.S
)

names = name_pattern.findall(html)
prices = price_pattern.findall(html)

print("商品名称数量：", len(names))
print("商品价格数量：", len(prices))

print("\n书包商品比价结果")
print("=" * 90)

count = min(len(names), len(prices), 60)

for i in range(count):
    name = html_lib.unescape(names[i]).strip()
    price = prices[i].strip()

    print(f"{i + 1:<3} 商品名称：{name}")
    print(f"    价格：￥{price}")
    print("-" * 90)

print(f"\n共爬取 {count} 项商品")