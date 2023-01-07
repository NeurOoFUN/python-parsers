import time
from dataclasses import dataclass

from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By


# fake user-agent
agent = UserAgent()


@dataclass
class DataClass:
    rating: str = ''
    registration_data: str = ''
    number_of_participants: str = ''
    number_of_mentions: str = ''
    number_of_recommendations:str = ''
    name: str = ''
    code: str = ''
    inn: str = ''
    profile: str = ''
    country: str = ''
    city: str = ''
    address:str = ''


# selenium driver settings.
class SeleniumParser:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument(f'user-agent={agent}')
        self.options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.options.add_argument('--headless')
        self.options.add_argument('--disable-blink-features=AutomationControlled')
        self.current_session = webdriver.Chrome(
                executable_path='/home/neuroo/projects/python-parsers/ati_su/chromedriver',
                options=self.options
                )

    def parse_page(self, url: str, sleep: int) -> str:
        self.current_session.get(url)
        self.current_session.find_element(By.TAG_NAME, 'html')

        time.sleep(sleep)
        page = self.current_session.page_source
        
        self.current_session.close()
        
        return page


