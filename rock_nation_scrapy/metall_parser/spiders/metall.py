from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

from metall_parser.items import MetallParserItem


class MetallSpider(CrawlSpider):
    name = 'metall'
    allowed_domains = ['rocknation.su']
    start_urls = [
        'http://rocknation.su/mp3/',
    ]
    rules = (
        Rule(LinkExtractor(
            allow=('/band-', '/album-', )), callback='parse', follow=True
        ),
    )

    def parse(self, response):
        i = ItemLoader(item=MetallParserItem(), response=response)
        i.add_value('url', response.url)
        i.add_xpath('group_name', '//div[@class="brad"]//span/text()')
        i.add_xpath('album_name',
                    '//div[@id="clips"]/ol[@class="list"]/li//text()'
                    )
        i.add_xpath('download_ref', '//script[@type="text/javascript"][3]')
        yield i.load_item()
