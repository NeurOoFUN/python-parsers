import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from metall_parser.items import MetallParserItem


class MetallSpider(CrawlSpider):
    name = 'metall'
    allowed_domains = ['rocknation.su']
    start_urls = ['https://rocknation.su/mp3/', ]
    rules = (
        Rule(LinkExtractor(allow=('/band-',)), callback='parse'),
    )

    def parse(self, response):
        i = ItemLoader(item=MetallParserItem(), response=response)
        i.add_value('url', response.url)
        yield i.load_item()
