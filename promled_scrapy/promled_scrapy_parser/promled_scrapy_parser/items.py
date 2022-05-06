# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PromledScrapyParserItem(scrapy.Item):
    category_name = scrapy.Field()
    product_name = scrapy.Field()
    modification = scrapy.Field()
