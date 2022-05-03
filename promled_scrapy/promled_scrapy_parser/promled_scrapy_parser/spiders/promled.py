import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader

from promled_scrapy_parser.items import PromledScrapyParserItem


class PromledSpider(SitemapSpider):
    name = 'promled'
    allowed_domains = ['promled.com']
    sitemap_urls = [
        'https://promled.com/sitemap1.xml',
        'https://promled.com/sitemap2.xml'
    ]
    sitemap_rules = [('/kategorii/', 'parse'), ]

    def parse(self, response):
        i = ItemLoader(item=PromledScrapyParserItem(), response=response)
        i.add_value('url', response.url)
        yield i.load_item()
