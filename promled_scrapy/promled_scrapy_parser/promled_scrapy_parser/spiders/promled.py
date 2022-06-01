import scrapy
from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader

from promled_scrapy_parser.items import PromledScrapyParserItem


class PromledSpider(SitemapSpider):
    name = 'promled'
    login_page = ['https://promled.com/login/']
    allowed_domains = ['promled.com']
    sitemap_rules = [
        (r'http[s]*://promled.com/(\w+-*(\w*-*)\2\2\d+\S+)', 'parse'),
    ]
    sitemap_urls = [
        'https://promled.com/robots.txt',
    ]

    def start_requests(self):
        for i in self.login_page:
            yield scrapy.Request(url=i, callback=self.login)

    def login(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'email': 'knu@sib-p.ru', 'password': 'Svet2021'},
            callback=self._parse_sitemap
        )
        if Exception(ValueError):
            for i in self.sitemap_urls:
                yield scrapy.Request(url=i, callback=self._parse_sitemap)

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
        i.add_xpath('your_price', '//span[@class="urprice"]/text()')
        i.add_xpath('rrc_and_mrc', '//span[@class="prodprice"]/text()')
        yield i.load_item()
