import scrapy


class AvtoSpider(scrapy.Spider):
    name = 'avto'
    allowed_domains = ['avito.ru']

    def start_requests(self, response):
        pass

    def parse(self, response):
        pass
