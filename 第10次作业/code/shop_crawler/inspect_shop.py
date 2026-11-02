import requests
from scrapy.selector import Selector

url = "https://scrapeme.live/shop/page/6/"

response = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=20
)
response.raise_for_status()

selector = Selector(text=response.text)

print("========== 网站检查 ==========")
print("HTTP 状态码:", response.status_code)
print("最终 URL:", response.url)

products = selector.xpath(
    '//li[contains(concat(" ", normalize-space(@class), " "), " product ")]'
)

print("\n========== 商品列表 ==========")
print("当前页面商品数量:", len(products))

for index, product in enumerate(products[:5], 1):
    name = product.xpath(
        './/h2[contains(@class,"woocommerce-loop-product__title")]/text()'
    ).get()

    price = product.xpath(
        './/span[contains(@class,"price")]//bdi//text()'
    ).getall()

    link = product.xpath(
        './/a[contains(@class,"woocommerce-LoopProduct-link")]/@href'
    ).get()

    print(f"\n商品 {index}")
    print("名称:", name)
    print("价格:", "".join(price).strip())
    print("链接:", link)

print("\n========== 分页分析 ==========")

next_page = selector.xpath(
    '//a[contains(@class,"next")]/@href'
).get()

print("下一页:", next_page)

print("\n========== 搜索表单 ==========")

for form in selector.xpath("//form"):
    print("action:", form.xpath("./@action").get())
    print("method:", form.xpath("./@method").get())
    print("inputs:", form.xpath(".//input/@name").getall())

print("\n网页分析完成")
