import time

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By


class SeleniumDownloaderMiddleware:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(
            '/home/neuroo/projects/python-parsers/oknafactoria/chromedriver',
            options=options
        )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            self.driver.implicitly_wait(10)
            button = self.driver.find_element(
                By.CLASS_NAME, 'finished-catalog__more-page-btn'
            )
            self.driver.implicitly_wait(10)
            for i in range(1):
                button.click()
                time.sleep(7)
            body = self.driver.page_source
            return HtmlResponse(
                url=request.url, body=body, encoding='utf-8', request=request
            )
        finally:
            self.driver.quit()
            print('Close chrome driver.')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        if request.Exception(ConnectionRefusedError):
            return None

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
