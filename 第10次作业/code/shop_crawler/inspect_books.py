import requests
from scrapy.selector import Selector

url = "https://books.toscrape.com/catalogue/page-6.html"

for mode in ["direct", "proxy"]:
    print(f"\n========== {mode} ==========")

    session = requests.Session()
    session.trust_env = False

    if mode == "proxy":
        session.proxies = {
            "http": "http://127.0.0.1:7897",
            "https": "http://127.0.0.1:7897"
        }

    try:
        response = session.get(
            url,
            timeout=(8, 15),
            headers={"User-Agent": "Mozilla/5.0"}
        )
        response.raise_for_status()

        selector = Selector(text=response.text)
        products = selector.xpath('//article[contains(@class,"product_pod")]')

        print("HTTP:", response.status_code)
        print("商品数量:", len(products))

        for product in products[:5]:
            name = product.xpath('.//h3/a/@title').get()
            price = product.xpath('.//p[contains(@class,"price_color")]/text()').get()
            link = product.xpath('.//h3/a/@href').get()

            print(name, price, link)

        if products:
            print("\n网站访问和 XPath 提取成功")
            break

        print("没有提取到商品，检查页面结构。")

    except requests.RequestException as e:
        print("请求失败:", type(e).__name__, str(e))
