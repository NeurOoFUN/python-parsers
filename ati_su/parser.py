import re
from dataclasses import dataclass

from bs4 import BeautifulSoup

from settings import SeleniumParser


URL = 'https://ati.su/rating/?skip=0&take=300'

@dataclass
class ParsedData:
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

data = ParsedData()


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
        print(data)


def parse_rating_tab(link: str) -> None:
    local_selenium_session = SeleniumParser()

    soup = BeautifulSoup(
            local_selenium_session.parse_page('http:' + link, sleep=2), 'lxml'
            )
    content_block1 = soup.find_all(
            'div', class_='passport-points-section-container__2X80'
            )
    content_block2 = soup.find_all(
            'div', class_='_1b0sf-2-0-751 _1Bnca-2-0-751 _18Cys-2-0-751 container__2AIN'
            )

    # "zip" to iter for 2 lists.
    for iter_block1, iter_block2 in zip(content_block1, content_block2):
        data.rating = iter_block1.find(
                'div', class_='pointsSum__1WnA positive__1JU5'
                ).get_text()
        data.registration_data = iter_block1.find(
                'span', class_='green__35x0'
                ).get_text()

        tags_a = iter_block2.find_all(
                'a', class_='counter__aY8_ green__PNB4'
                )
        data.number_of_participants = tags_a[0].get_text()
        data.number_of_mentions = tags_a[1].get_text()
        data.number_of_recommendations = tags_a[2].get_text()


def parse_main_tab(link: str) -> None:
    correct_link = re.sub('rating', 'info', link)

    local_selenium_session = SeleniumParser()
    soup = BeautifulSoup(
            local_selenium_session.parse_page('http:' + correct_link, sleep=3), 'lxml'
            )
    content_block = soup.find_all('div', class_='value__u5eB')
    
    data.name = content_block[0].get_text()
    data.code = content_block[1].get_text()
    data.inn = content_block[2].get_text()
    data.profile = content_block[5].get_text()
    data.country = content_block[6].get_text()
    data.city = content_block[7].get_text()
    data.address = content_block[8].get_text()

