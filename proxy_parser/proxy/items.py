import scrapy
from scrapy.loader.processors import TakeFirst


class ProxyItem(scrapy.Item):
    url = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
