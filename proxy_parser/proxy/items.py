import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def correct_protocol(text: str):
    return text.lower()


class ProxyItem(scrapy.Item):
    # url = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    protocol = scrapy.Field(output_processor=MapCompose(correct_protocol))
