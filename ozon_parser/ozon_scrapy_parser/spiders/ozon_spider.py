import scrapy

from ozon_scrapy_parser.items import OzonScrapyParserItem
from scrapy.loader import ItemLoader


class OzonSpiderSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['ozon.ru']

    def start_requests(self):
        start_urls = [
            'https://www.ozon.ru/category/elektronika-15500/',
        ]
        for urls in start_urls:
            yield scrapy.Request(url=urls, callback=self.get_category_links)

    def get_category_links(self, response):
        category_links = response.xpath('//div[@class="a0p6"]//@href').getall()
        for links in category_links[0:3]:   # НЕ ЗАБЫТЬ!!!
            yield response.follow(url=links, callback=self.get_product_links)

    def get_product_links(self, response):
        product_links = response.xpath('//div[@class="bi6"]/a/@href').getall()
        for links in product_links:
            yield response.follow(url=links, callback=self.parse)

    def parse(self, response):
        i = ItemLoader(item=OzonScrapyParserItem(), response=response)
        i.add_value('url', response.url)
        i.add_xpath('category_name', '//ol[@class="bd7"]/li[3]//text()')
        i.add_xpath('product_name', '//h1[@class="e8j2"]/text()')
        i.add_xpath('price', '//span[@class="c2h5 c2h6"]//text()')
        i.add_xpath('price', '//span[@class="c2h5"]//text()')
        yield i.load_item()
