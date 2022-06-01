from fake_useragent import UserAgent


BOT_NAME = 'promled_scrapy_parser'

SPIDER_MODULES = ['promled_scrapy_parser.spiders']

NEWSPIDER_MODULE = 'promled_scrapy_parser.spiders'

USER_AGENT = {'user-agent': f'{UserAgent().random}'}

ROBOTSTXT_OBEY = True

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0.5

COOKIES_ENABLED = True

DEFAULT_REQUEST_HEADERS = {
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
 'Accept-Language': 'en',
}

ITEM_PIPELINES = {
   'promled_scrapy_parser.pipelines.Save_to_csv': 300,
}
