import scrapy


class WindowsParserItem(scrapy.Item):
    url = scrapy.Field()
    wind_name = scrapy.Field()
