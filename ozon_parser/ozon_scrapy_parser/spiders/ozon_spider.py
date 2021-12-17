import scrapy

from ozon_scrapy_parser.items import OzonScrapyParserItem
from scrapy.loader import ItemLoader


class OzonSpiderSpider(scrapy.Spider):
    name = 'ozon_spider'
    allowed_domains = ['ozon.ru']

    def start_requests(self):
        start_urls = [
            'https://www.ozon.ru/category/smartfony-15502/',
        ]
        for urls in start_urls:
            yield scrapy.Request(url=urls, callback=self.get_product_links)

    def get_product_links(self, response):
        product_links = response.xpath('//div[@class="bi6"]/a/@href').getall()
        for links in product_links:
            yield response.follow(url=links, callback=self.parse)
        next_page = response.xpath('//a[@class="ui-b4"]/@href').getall()
        for pagen_links in next_page:
            yield response.follow(url=pagen_links, callback=self.get_product_links)
            if response.xpath('//div[@class="f9g7"]'):
                return

    def parse(self, response):
        i = ItemLoader(item=OzonScrapyParserItem(), response=response)
        i.add_value('url', response.url)
        i.add_xpath('product_name', '//h1[@class="e8j2"]/text()')
        i.add_xpath('price', '//span[@class="c2h5 c2h6"]//text()')
        i.add_xpath('price', '//span[@class="c2h5"]//text()')
        i.add_xpath('specifications', '//div[@class="da3"]//text()')
        i.add_xpath('img_link', '//div[@class="e9r7"]/img/@src')
        i.add_xpath('id', '//span[@class="fk fk1"]//text()[2]')
        yield i.load_item()
