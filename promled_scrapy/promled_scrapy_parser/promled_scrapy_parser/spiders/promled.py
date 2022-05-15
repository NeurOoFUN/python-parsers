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
        (r'http[s]*://promled.com/(\w+-*(\w*-*)\2\2\d+\S+)', 'parse'),
    ]

    def parse(self, response):
        i = ItemLoader(item=PromledScrapyParserItem(), response=response)
        i.add_value('url', response.url)
        i.add_xpath(
            'category_name', '//ul[@class="breadcrumb"]/li//text()',
        )
        i.add_xpath(
            'sub_category_name', '//ul[@class="breadcrumb"]/li//text()',
        )
        i.add_xpath(
            'product_name', '//ul[@class="breadcrumb"]/li//text()',
        )
        i.add_xpath('modification',
                    '//div[@class="col-sm-12"]/h1[@itemprop="name"]/text()'
                    )
        i.add_xpath(
            'id', '//div[@class="prodmodeL"]/text()'
        )
        i.add_xpath('description', '//div[@class="content_block"]//text()')
        i.add_xpath(
            'characteristics',
            '//table[@class="table table-striped"]//text()')
        yield i.load_item()
