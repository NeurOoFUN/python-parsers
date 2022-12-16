import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from tools import session, SeleniumParser

URL = 'https://ati.su/rating/?skip=0&take=300'


def get_start_links():
    local_selenium_session = SeleniumParser()
    soup = BeautifulSoup(local_selenium_session.parse_page(URL, 5), 'lxml')

    link_list = soup.find_all('a', class_='glz-link glz-is-primary')
    for i in link_list:
        link = i.get('href')
        print(link)
        parse_each_lot(link)


def parse_each_lot(link: str):
    local_selenium_session = SeleniumParser()
    lot_page = local_selenium_session.parse_page('https:' + link, 2)
    soup = BeautifulSoup(lot_page, 'lxml')
    name = soup.find('h1', class_='main__2Tqn')
    print(name)

