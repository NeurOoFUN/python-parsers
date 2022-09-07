from bs4 import BeautifulSoup

from tools import session
from database.sql_base import SqliteBase


def pagenation_count():
    response = session.get(url='https://rocknation.su/mp3/').text
    soup = BeautifulSoup(response, 'lxml')
    pagen_link = soup.find('ul', class_='pagination') \
        .find_all('li')[-1].find_all('a')[-1].get('href').split('/')[-1]
    return int(pagen_link) + 1


def find_all_groups():
    db = SqliteBase()
    for i in range(1, pagenation_count()):
        response = session.get(url='https://rocknation.su/mp3/' + str(i)).text
        soup = BeautifulSoup(response, 'lxml')
        group_link = soup.find('table', class_='table-bands').find('tbody')

        for i in group_link:
            try:
                link = 'https://rocknation.su' + \
                    i.find('td').find('a').get('href')
                name = i.find('td').find('a').get_text()
                print(name)

            except AttributeError:
                continue
