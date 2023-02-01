import re
from dataclasses import astuple

from bs4 import BeautifulSoup

from settings import SeleniumParser, DataClass
from writer import Saver


data_container = DataClass()

save = Saver(csv_headers=data_container.__match_args__)


def main() -> None:
    '''
    Start and pagenation.
    '''
    for page in range(0, 100000, 300):
        url = f'https://ati.su/rating/?skip={str(page)}&take=300'
        get_start_links(url=url)


def get_start_links(url: str) -> None:
    local_selenium_session = SeleniumParser()
    soup = BeautifulSoup(
        local_selenium_session.parse_page(url=url, sleep=5), 'lxml'
            )

    link_list = soup.find_all('a', class_='glz-link glz-is-primary')
    for i in link_list:
        link = i.get('href')

        parse_rating_tab(link=link)
        parse_main_tab(link=link)
        save.save_in_csv(astuple(data_container))
        print(data_container)


def parse_rating_tab(link: str) -> None:
    local_selenium_session = SeleniumParser()

    soup = BeautifulSoup(
            local_selenium_session.parse_page('http:' + link, sleep=3), 'lxml'
            )
    content_block1 = soup.find_all(
            'div', class_='passport-points-section-container__2X80'
            )
    content_block2 = soup.find_all(
            'div', class_='_1b0sf-2-0-751 _1Bnca-2-0-751 _18Cys-2-0-751 container__2AIN'
            )

    # "zip" to iter for 2 lists.
    for iter_block1, iter_block2 in zip(content_block1, content_block2):
        data_container.rating = iter_block1.find(
                'div', class_='pointsSum__1WnA positive__1JU5'
                ).get_text()
        data_container.registration_data = iter_block1.find(
                'span', class_='green__35x0'
                ).get_text()

        tags_a = iter_block2.find_all(
                'a', class_='counter__aY8_'
                )
        data_container.number_of_participants = tags_a[0].get_text()
        data_container.number_of_mentions = tags_a[1].get_text()
        data_container.number_of_recommendations = tags_a[2].get_text()


def parse_main_tab(link: str) -> None:
    correct_link = re.sub('rating', 'info', link)

    local_selenium_session = SeleniumParser()
    soup = BeautifulSoup(
            local_selenium_session.parse_page('http:' + correct_link, sleep=3), 'lxml'
            )
    content_block = soup.find_all('div', class_='value__u5eB')
    
    data_container.name = content_block[0].get_text()
    data_container.code = content_block[1].get_text()
    data_container.inn = content_block[2].get_text()
    data_container.profile = content_block[4].get_text()
    data_container.country = content_block[5].get_text()
    data_container.city = content_block[6].get_text()

    if content_block[7].get_text() == 'доступно бесплатно после регистрации на ATI.SU':
        data_container.address = 'address is absent'
    else:
        data_container.address = content_block[7].get_text()

