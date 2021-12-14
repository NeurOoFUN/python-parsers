# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader.processors import TakeFirst


class OzonScrapyParserItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    category_name = scrapy.Field(input_processor=TakeFirst())
    product_name = scrapy.Field()
    price = scrapy.Field(input_processor=TakeFirst())
    specifications = scrapy.Field()
    presence = scrapy.Field()
    img_link = scrapy.Field()
    id = scrapy.Field()
