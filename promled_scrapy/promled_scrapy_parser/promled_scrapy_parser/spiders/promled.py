import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader

from promled_scrapy_parser.items import PromledScrapyParserItem


class PromledSpider(SitemapSpider):
    name = 'promled'
    allowed_domains = ['promled.com']
    sitemap_urls = [
        'https://promled.com/sitemap1.xml',
    ]
    sitemap_rules = [
        (r'(/+?\w+\S*)', 'parse'),
    ]

    def parse(self, response):
        i = ItemLoader(item=PromledScrapyParserItem(), response=response)
        i.add_xpath(
            'category_name',
            '//ul[@class="breadcrumb"]/li[2]//text()',  # FIXME
        )
        i.add_xpath(
            'sub_category_name', '//ul[@class="breadcrumb"]/li[3]//text()',
        )
        i.add_xpath(
            'product_name', '//ul[@class="breadcrumb"]/li[4]//text()',
        )
        i.add_xpath('modification',
                    '//div[@class="col-sm-12"]/h1[@itemprop="name"]/text()')
        yield i.load_item()
