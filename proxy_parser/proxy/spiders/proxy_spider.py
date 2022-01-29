import scrapy


class ProxySpider(scrapy.Spider):
    name = 'proxy_spider'
    allowed_domains = ['proxy.com']

    def start_requests(self):
        pass

    def parse(self, response):
        pass
