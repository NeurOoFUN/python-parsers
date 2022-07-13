import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class OzonSpider(CrawlSpider):
    name = 'ozon'
    allowed_domains = ['ozon.ru']
    start_urls = ['https://www.ozon.ru/category/']

    reles = (
        Rule(LinkExtractor(allow=('smartfony-15502/')), callback='parse'),
    )

    def parse(self, response):
        item = scrapy.Item()
        item['url'] = response.url
        yield item
