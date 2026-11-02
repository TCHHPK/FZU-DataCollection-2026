import scrapy
from demo.items import PageItem


class MySpider(scrapy.Spider):
    name = "mySpider"
    allowed_domains = ["127.0.0.1"]

    # Scrapy 2.19.0 的异步爬虫入口
    async def start(self):
        yield scrapy.Request(
            url="http://127.0.0.1:5000/",
            callback=self.parse
        )

    # 解析 Response
    def parse(self, response):
        item = PageItem()
        item["url"] = response.url
        item["status"] = response.status
        item["content"] = response.text.strip()

        print("========== Scrapy解析结果 ==========")
        print("URL:", item["url"])
        print("HTTP状态码:", item["status"])
        print("网页内容:", item["content"])

        yield item
