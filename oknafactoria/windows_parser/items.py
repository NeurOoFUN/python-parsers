import scrapy


class WindowsParserItem(scrapy.Item):
    window_name = scrapy.Field()
