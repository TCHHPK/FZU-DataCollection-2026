import scrapy


class PageItem(scrapy.Item):
    url = scrapy.Field()
    status = scrapy.Field()
    content = scrapy.Field()
