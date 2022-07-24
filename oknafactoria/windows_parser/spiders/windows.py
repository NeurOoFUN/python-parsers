import scrapy

from windows_parser.items import WindowsParserItem


class WindowsSpider(scrapy.Spider):
    name = 'windows'
    start_urls = 'https://oknafactoria.ru/gotovie-okna/',

    def start_requests(self):
        for urls in self.start_urls:
            yield scrapy.Request(
                url=urls, callback=self.parse_links_for_each_window
            )

    def parse_links_for_each_window(self, response):
        links = response.xpath(
            '//div[@class="finished-catalog__item-title"]/a/@href'
        ).getall()
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = WindowsParserItem()
        item['window_name'] = response.xpath(
            '//div[@class="head__title h3"]/h1/text()'
        ).get()
        yield item
