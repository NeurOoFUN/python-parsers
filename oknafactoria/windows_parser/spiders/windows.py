import scrapy
from scrapy.loader import ItemLoader

from windows_parser.items import WindowsParserItem


class WindowsSpider(scrapy.Spider):
    start_urls = []
    name = 'windows'
    for number_page in range(1, 23):
        start_urls.append(
            f'https://oknafactoria.ru/gotovie-okna/page/{str(number_page)}/'
        )

    def start_requests(self):
        for urls in self.start_urls:
            yield scrapy.Request(
                url=urls,
                callback=self.parse_links_for_each_window
                )

    def parse_links_for_each_window(self, response):
        links = response.xpath(
            '//div[@class="finished-catalog__item-title"]/a/@href'
        ).getall()
        for url in links:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        i = ItemLoader(item=WindowsParserItem(), response=response)
        i.add_value('url', response.url)
        i.add_xpath(
            'product_name',
            '//div[@class="head__title h3"]/h1/text()'
        )
        i.add_xpath(
            'characteristics',
            '//div[@class="data__list"]//text()'
        )
        i.add_xpath(
            'new_and_old_prices',
            '//div[@class="price__count"]/var/text()'
        )
        i.add_xpath(
            'description',
            '//div[@class="finished-catalog__text t4 c-gray-l"]//text()'
        )
        yield i.load_item()
