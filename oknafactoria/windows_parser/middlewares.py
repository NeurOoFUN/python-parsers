import time

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

    def process_request(self, request, spider):
        try:
            self.driver.get(request.url)
            self.driver.implicitly_wait(10)
            button = self.driver.find_element(
                By.CLASS_NAME, 'finished-catalog__more-page-btn'
            )
            self.driver.implicitly_wait(10)
            for i in range(10):
                button.click()
                time.sleep(7)
            body = self.driver.page_source
            return HtmlResponse(
                url=request.url, body=body,
                encoding='utf-8', request=request
                )
        except Exception:
            return None
        finally:
            self.driver.quit()
