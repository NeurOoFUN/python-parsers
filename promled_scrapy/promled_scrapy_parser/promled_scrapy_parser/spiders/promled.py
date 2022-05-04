import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader

from promled_scrapy_parser.items import PromledScrapyParserItem


class PromledSpider(SitemapSpider):
    name = 'promled'
    allowed_domains = ['promled.com']
    sitemap_urls = [
        'https://promled.com/robots.txt',
    ]
    sitemap_rules = [
        (r'/kategorii/\b\w{9}\b', 'parse_category_name'),
        # ('/kategorii/', 'parse_sub_category_name')
    ]

    def parse_category_name(self, response):
        i = ItemLoader(item=PromledScrapyParserItem(), response=response)
        i.add_xpath(
            'category_name', '//div[@class="relatedproduct-thumb transition"]//h4//text()')
        yield i.load_item()

    # def parse_sub_category_name(self, response):
    #     pass
