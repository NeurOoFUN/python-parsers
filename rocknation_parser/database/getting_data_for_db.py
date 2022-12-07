from bs4 import BeautifulSoup

from tools import session
from database.sql_base import create_db, write_all_data_to_db


def pagenation_count() -> int:
    response = session.get(url='https://rocknation.su/mp3/').text
    soup = BeautifulSoup(response, 'lxml')
    pagen_link = soup.find('ul', class_='pagination') \
        .find_all('li')[-1].find_all('a')[-1].get('href').split('/')[-1]
    return int(pagen_link) + 1


def find_all_groups() -> None:
    create_db()
    for i in range(1, pagenation_count()):
        response = session.get(url='https://rocknation.su/mp3/' + str(i)).text
        soup = BeautifulSoup(response, 'lxml')
        group_link = soup.find('table', class_='table-bands').find('tbody')

        for i in group_link:
            try:
                link = 'https://rocknation.su' + \
                    i.find('td').find('a').get('href')
                name = i.find('td').find('a').get_text()
                genre = i.find_all('td')[1].get_text()
                write_all_data_to_db(
                    group_name=name, group_link=link, genre=genre
                        )

            except AttributeError:
                continue
