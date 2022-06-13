# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MetallParserItem(scrapy.Item):
    url = scrapy.Field()
    group_name = scrapy.Field()
    album_name = scrapy.Field()
    download_ref = scrapy.Field()
