# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FourFragItem(scrapy.Item):
    # define the fields for your item here like:
    category_name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    img_link = scrapy.Field()
    manufacturer = scrapy.Field()
    specifications = scrapy.Field()
