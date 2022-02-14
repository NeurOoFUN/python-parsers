from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from proxy.items import ProxyItem


class ProxySpider(CrawlSpider):
    name = 'proxy_spider'
    allowed_domains = ['hidemy.name']
    start_urls = [
        'https://hidemy.name/ru/proxy-list/'
    ]
    rules = (
        Rule(
            LinkExtractor(allow=('hidemy.name/ru/proxy-list/',),),
            callback='parse',
        ),
    )

    def parse(self, response):
        i = ItemLoader(item=ProxyItem(), response=response)
        i.add_value('url', response.url)
        i.add_xpath(
            'ip', '//div[@class="table_block"]//tbody/tr/td[1]//text()')
        i.add_xpath(
            'port', '//div[@class="table_block"]//tbody/tr/td[2]//text()')
        yield i.load_item()
