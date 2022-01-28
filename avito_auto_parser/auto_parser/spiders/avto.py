import scrapy
from scrapy.loader import ItemLoader

from auto_parser.items import AutoParserItem


class AvtoSpider(scrapy.Spider):
    """

Main class.

    """
    name = 'avto'
    allowed_domains = ['avito.ru']

    def start_requests(self):
        start_urls = [
            'https://www.avito.ru/moskva/avtomobili?radius=200',
        ]
        for urls in start_urls:
            yield scrapy.Request(url=urls,  # FIXME
                                 meta={'proxy': '188.43.15.89'},
                                 callback=self.get_lot_links)

    def get_lot_links(self, response):
        lot_links = response.xpath(
            '//div[@class="iva-item-titleStep-pdebR"]/a/@href').getall()
        for links in lot_links:
            yield response.follow(url=links, callback=self.parse)

    def parse(self, response):
        i = ItemLoader(item=AutoParserItem(), response=response)
        i.add_value('url', response.url)
        yield i.load_item()
