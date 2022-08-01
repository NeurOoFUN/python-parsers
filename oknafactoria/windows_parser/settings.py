from faker import Faker

# useragent
f = Faker()
agent = f.firefox()
USER_AGENT = agent

BOT_NAME = 'windows_parser'

SPIDER_MODULES = ['windows_parser.spiders']

NEWSPIDER_MODULE = 'windows_parser.spiders'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
   'windows_parser.pipelines.Save_to_csv': 300,
}

FEED_EXPORTERS = {
    'xlsx': 'scrapy_xlsx.XlsxItemExporter',
}

XLSX_FILE = 'data.xlsx'
