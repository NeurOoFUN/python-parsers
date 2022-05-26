from scrapy.spiders import SitemapSpider
from scrapy.loader import ItemLoader

from priemka_scraper.items import PriemkaScraperItem


class PriemkaSpider(SitemapSpider):
    name = 'priemka'
    allowed_domains = ['priemkaeco.ru']
    sitemap_rules = [
        (r'https://priemkaeco.ru/(\w?-*)\1\1\1', 'parse'),
    ]
    sitemap_urls = [
        'http://priemkaeco.ru/post-sitemap1.xml',
        'http://priemkaeco.ru/post-sitemap2.xml',
        'http://priemkaeco.ru/post-sitemap3.xml',
        'http://priemkaeco.ru/post-sitemap4.xml',
        'http://priemkaeco.ru/post-sitemap5.xml',
    ]

    def parse(self, response):
        i = ItemLoader(item=PriemkaScraperItem(), response=response)
        i.add_xpath('city', '//h1[@class="entry-title"]//text()')
        i.add_xpath('description', '//table[1]//tr')
        yield i.load_item()
