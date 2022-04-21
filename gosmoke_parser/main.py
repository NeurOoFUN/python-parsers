import requests
from bs4 import BeautifulSoup

from setings import headers


def get_lot_links():
    """ Get links for lots. """
    page = requests.get(
        url='https://gosmoke.ru/aromatizatory', headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    lot_link = soup.find_all('div', class_='caption-title')
    for i in lot_link:
        link = i.find('a').get('href')
        get_datas(link)


def get_datas(link):
    response = requests.get(url=link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    lot_name = soup.find('div', id='content').find('h1').get_text()
    flavor = soup.find(
        'div', class_='product-description').find('p').get_text().strip()
    volume = soup.find('div', class_='form-group required').find_all(
        'label')[1].get_text().strip()
    price = soup.find('meta', itemprop='price').get('content')
    print(price)


def run():
    get_lot_links()


if __name__ == '__main__':
    run()
