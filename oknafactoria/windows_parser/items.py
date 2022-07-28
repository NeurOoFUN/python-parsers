import scrapy
from scrapy.loader.processors import MapCompose


def correct_prices(value):
    return value + '₽ '


class WindowsParserItem(scrapy.Item):
    url = scrapy.Field()
    product_name = scrapy.Field()
    characteristics = scrapy.Field()
    new_and_old_prices = scrapy.Field(
        input_processor=MapCompose(correct_prices)
    )
    description = scrapy.Field()
