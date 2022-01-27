import scrapy


class AvtoSpider(scrapy.Spider):
    name = 'avto'
    allowed_domains = ['avito.ru']
    start_urls = ['http://avito.ru/']

    def parse(self, response):
        pass
