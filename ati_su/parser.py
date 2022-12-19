import re

from bs4 import BeautifulSoup

from tools import session, SeleniumParser

URL = 'https://ati.su/rating/?skip=0&take=300'


def get_start_links():
    local_selenium_session = SeleniumParser()
    soup = BeautifulSoup(
        local_selenium_session.parse_page(url=URL, sleep=5), 'lxml'
            )

    link_list = soup.find_all('a', class_='glz-link glz-is-primary')
    for i in link_list:
        link = i.get('href')
        parse_rating_tab(link=link)
        parse_main_tab(link=link)


def parse_rating_tab(link: str):
    local_selenium_session = SeleniumParser()
    soup = BeautifulSoup(
            local_selenium_session.parse_page('http:' + link, sleep=2), 'lxml'
            )
    content_block1 = soup.find('div', class_='passport-points-section-container__2X80')
    content_block2 = soup.find('div', class_='_1b0sf-2-0-751 _1Bnca-2-0-751 _18Cys-2-0-751 container__2AIN')
    # print(content_block1)
    # print(content_block2)


def parse_main_tab(link: str):
    correct_link = re.sub('rating', 'info', link)
    local_selenium_session = SeleniumParser()
    soup = BeautifulSoup(
            local_selenium_session.parse_page('http:' + correct_link, sleep=2), 'lxml'
            )
    content_block = soup.find('div', class_='about__2MXw').get_text()
    print(content_block)

