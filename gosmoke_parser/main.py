import requests
from bs4 import BeautifulSoup

from setings import headers


def pagen():
    response = requests.get(
        url='https://gosmoke.ru/aromatizatory', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    next_page = soup.find('ul', class_='pagination').find_all(
        'li')[-1].find('a').get('href').split('=')[-1]
    get_lot_links(next_page)


def get_lot_links(next_page):
    """ Get links for lots. """
    for i in range(1, int(next_page)):
        page = requests.get(
            url=f'https://gosmoke.ru/aromatizatory?page={i}', headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        global lot_link
        lot_link = soup.find_all('div', class_='caption-title')
        for i in lot_link:
            link = i.find('a').get('href')
            print(link)
            get_datas(link)


def get_datas(link):
    response = requests.get(url=link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        lot_name = soup.find('div', id='content').find('h1').get_text()
    except Exception:
        lot_name = 'not found'
    try:
        flavor = soup.find(
            'div', class_='product-description').find('p').get_text().strip()
    except Exception:
        flavor = 'not found'
    try:
        volume = soup.find('div', class_='form-group required').find_all(
            'label')[1].get_text().strip()
    except Exception:
        volume = 'not found'
    try:
        price = soup.find('meta', itemprop='price').get('content')
    except Exception:
        price = 'not found'
    try:
        img_link = soup.find('a', class_='thumbnail').get('href')
    except Exception:
        img_link = 'not found'
    if soup.find('button', id='button-cart').get_text() == ' Купить':
        presence = 'in stock'
    else:
        presence = 'not available'
    print(presence)


def run():
    pagen()


if __name__ == '__main__':
    run()
