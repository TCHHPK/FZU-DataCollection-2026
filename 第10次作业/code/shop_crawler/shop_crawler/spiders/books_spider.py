import re
import scrapy


class BooksSpider(scrapy.Spider):
    name = "books"
    allowed_domains = ["books.toscrape.com"]

    keyword = "the"
    start_page = 6

    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "CONCURRENT_REQUESTS": 1,
        "DOWNLOAD_DELAY": 0.3,
        "CLOSESPIDER_ITEMCOUNT": 116,
        "FEED_EXPORT_ENCODING": "utf-8-sig",
        "LOG_LEVEL": "INFO",
        "HTTPPROXY_ENABLED": False,
    }

    async def start(self):
        url = (
            "https://books.toscrape.com/"
            f"catalogue/page-{self.start_page}.html"
        )
        yield scrapy.Request(
            url,
            callback=self.parse,
            cb_kwargs={"page": self.start_page}
        )

    def parse(self, response, page):
        products = response.xpath(
            '//article[contains(@class,"product_pod")]'
        )

        self.logger.info(
            "正在分析第 %d 页，商品数量：%d",
            page,
            len(products)
        )

        for product in products:
            name = product.xpath(".//h3/a/@title").get(default="")

            if self.keyword.lower() not in name.lower():
                continue

            link = product.xpath(".//h3/a/@href").get()

            if link:
                yield response.follow(
                    link,
                    callback=self.parse_detail,
                    cb_kwargs={"page": page}
                )

        next_page = response.xpath(
            '//li[contains(@class,"next")]/a/@href'
        ).get()

        if next_page:
            yield response.follow(
                next_page,
                callback=self.parse,
                cb_kwargs={"page": page + 1}
            )

    def parse_detail(self, response, page):
        title = response.xpath(
            '//div[contains(@class,"product_main")]/h1/text()'
        ).get(default="").strip()

        price = response.xpath(
            '//div[contains(@class,"product_main")]'
            '//p[contains(@class,"price_color")]/text()'
        ).get(default="")

        price_number = re.search(r"\d+(?:\.\d+)?", price)

        category = response.xpath(
            '//ul[contains(@class,"breadcrumb")]/li[3]/a/text()'
        ).get(default="").strip()

        availability = response.xpath(
            '//div[contains(@class,"product_main")]'
            '//p[contains(@class,"availability")]//text()'
        ).getall()

        image = response.xpath(
            '//div[contains(@class,"item")]/img/@src'
        ).get()

        yield {
            "keyword": self.keyword,
            "page": page,
            "title": title,
            "price_gbp": float(price_number.group()) if price_number else None,
            "category": category,
            "availability": " ".join(
                text.strip() for text in availability if text.strip()
            ),
            "product_url": response.url,
            "image_url": response.urljoin(image) if image else "",
        }
