import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class ProxyItem(scrapy.Item):
    ip = scrapy.Field()
    port = scrapy.Field()
    protocol = scrapy.Field()
