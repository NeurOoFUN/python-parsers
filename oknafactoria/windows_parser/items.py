import scrapy


class WindowsParserItem(scrapy.Item):
    url = scrapy.Field()
    wind_refs = scrapy.Field()
