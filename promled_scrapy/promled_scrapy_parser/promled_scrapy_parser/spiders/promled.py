import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader

from promled_scrapy_parser.items import PromledScrapyParserItem


class PromledSpider(SitemapSpider):
    name = 'promled'
    allowed_domains = ['promled.com']
    sitemap_urls = [
        'https://promled.com/sitemap1.xml',
        'https://promled.com/sitemap2.xml',
    ]
    sitemap_rules = [
        ('/kategorii/', 'parse_category_and_product_name'),
        ('', 'parse_modification'),
    ]

    def parse_category_and_product_name(self, response):
        i = ItemLoader(item=PromledScrapyParserItem(), response=response)
        i.add_xpath(
            'category_name',
            '//div[@class="relatedproduct-thumb transition"]/h4//text()'
        )
        i.add_xpath(
            'product_name', '//h1[@class="prohead"]/text()'
        )
        yield i.load_item()

    def parse_modification(self, response):
        i = ItemLoader(item=PromledScrapyParserItem(), response=response)
        i.add_xpath('modification', '//td[@class="cattdleft"]//text()')
        yield i.load_item()
