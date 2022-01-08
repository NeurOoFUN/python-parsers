import scrapy

from prom_scrapy_parser.items import PromScrapyParserItem
from scrapy.loader import ItemLoader


class PromSpider(scrapy.Spider):
    name = 'prom'

    def start_requests(self):
        start_url = ['https://prom.ua/consumer-goods']
        for urls in start_url:
            yield scrapy.Request(url=urls, callback=self.get_category_links)

    def get_category_links(self, response):
        links = response.xpath('//a[@class="_6zoki sYTuN"]/@href').getall()
        for i in links:
            yield response.follow(url=i, callback=self.get_category_links)

    def get_sub_category_links(self, response):
        sub_links = response.xpath()

    def parse(self, response):
        i = ItemLoader(item=PromScrapyParserItem(), response=response)
        i.add_value('url', response.url)
        yield i.load_item()
