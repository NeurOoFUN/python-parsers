import scrapy
from scrapy.loader import ItemLoader

from auto_parser.items import AutoParserItem


class AvtoSpider(scrapy.Spider):
    name = 'avto'
    allowed_domains = ['avito.ru']

    def start_requests(self):
        start_urls = [
            'https://www.avito.ru/uzlovaya/avtomobili?radius=200',
        ]
        for urls in start_urls:
            yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        i = ItemLoader(item=AutoParserItem(), response=response)
        i.add_value('url', response.url)
        yield i
