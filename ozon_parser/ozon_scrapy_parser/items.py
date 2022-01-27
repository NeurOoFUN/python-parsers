# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def filter_id(value):
    return value.split(':')[-1].strip()


class OzonScrapyParserItem(scrapy.Item):
    """
    Собс-но айтемы.
    """
    # define the fields for your item here like:
    url = scrapy.Field()
    product_name = scrapy.Field(output_processor=MapCompose(str.strip))
    price = scrapy.Field(input_processor=TakeFirst())
    specifications = scrapy.Field()
    img_link = scrapy.Field()
    id = scrapy.Field(output_processor=MapCompose(filter_id))
