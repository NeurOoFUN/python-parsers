import scrapy
from scrapy.loader import ItemLoader

from proxy.items import ProxyItem


class ProxySpider(scrapy.Spider):
    name = 'proxy_spider'

    def start_requests(self):
        start_urls = [
            'https://hidemy.name/ru/proxy-list/',
        ]
        for urls in start_urls:
            yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        i = ItemLoader(item=ProxyItem(), response=response)
        # i.add_value('url', response.url)
        i.add_xpath(
            'ip', '//div[@class="table_block"]//tbody/tr/td[1]//text()')
        i.add_xpath(
            'port', '//div[@class="table_block"]//tbody/tr/td[2]//text()')
        i.add_xpath(
            'protocol', '//div[@class="table_block"]//tbody/tr/td[5]//text()')
        yield i.load_item()
        next_page = response.xpath('//li[@class="next_array"]/a/@href').get()
        if next_page is not None:
            yield response.follow(
                url='https://hidemy.name' + next_page, callback=self.parse)
