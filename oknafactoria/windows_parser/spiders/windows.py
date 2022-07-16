import scrapy

from windows_parser.items import WindowsParserItem


class WindowsSpider(scrapy.Spider):
    name = 'windows'
    start_urls = 'https://oknafactoria.ru/gotovie-okna/',

    def start_requests(self):
        for urls in self.start_urls:
            yield scrapy.Request(url=urls, callback=self.parse)

    def parse(self, response):
        item = WindowsParserItem()
        item['url'] = response.url
        item['wind_name'] = response.xpath(
            '//div[@class="finished-catalog__item-title"]/a/text()'
        ).getall()
        yield item
