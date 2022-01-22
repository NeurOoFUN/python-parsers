import scrapy

from ozon_scrapy_parser.items import OzonScrapyParserItem
from scrapy.loader import ItemLoader


class OzonSpiderSpider(scrapy.Spider):
    """
    Основной класс паука.
    """
    name = 'ozon_spider'
    allowed_domains = ['ozon.ru']

    def start_requests(self):
        start_urls = [
            'https://www.ozon.ru/category/smartfony-15502/',
        ]
        for urls in start_urls:
            yield scrapy.Request(url=urls, callback=self.get_product_links)

    def get_product_links(self, response):
        """
        Получает ссылки на товары, + пагенация.
        """
        product_links = response.xpath('//a[@class="tile-hover-target hh1"]/@href').getall()
        for links in product_links:
            yield response.follow(url=links, callback=self.parse)
        next_page = response.xpath('//a[@class="ui-b2"]/@href').getall()
        for pagen_links in next_page:
            yield response.follow(url=pagen_links, callback=self.get_product_links)
            if response.xpath('//div[@class="p1w"]'):
                return

    def parse(self, response):
        """
        Основной сборщик данных.
        """
        i = ItemLoader(item=OzonScrapyParserItem(), response=response)
        i.add_value('url', response.url)
        i.add_xpath('product_name', '//h1[@class="j2p"]/text()')
        i.add_xpath('price', '//span[@class="jo0 j0o"]//text()')
        i.add_xpath('price', '//span[@class="jo0"]//text()')
        i.add_xpath('specifications', '//dl[@class="i0n"]//text()')
        i.add_xpath('img_link', '//div[@class="sh1"]/img/@src')
        i.add_xpath('id', '//span[@class="i2w w2i"]//text()[2]')
        yield i.load_item()
