import requests
from bs4 import BeautifulSoup

from setings import headers, csv_headers
from saver import Saver

# init Saver class.
instance_saver = Saver()

category = input(
    '''AVAILABLE CATEGORIES: \nosnova-samozamesa\naromatizatory\ntara
zhidkosti\nzhelezo\nnamotka\nelektronika'''
    '\nEnter the category to be parsed in English, then press "ENTER": '
)

print('The scanning process has started, it will take time...')

# Create csv table with headers.
instance_saver.create_csv_table(csv_headers)


def start_func():
    """ Start and pagenation. """
    response = requests.get(
        url=f'https://gosmoke.ru/{category}', headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        next_page = soup.find('ul', class_='pagination').find_all(
            'li')[-1].find('a').get('href').split('=')[-1]
        get_lot_links(next_page)
    # if next_page is None, parse 1 page.
    except AttributeError:
        get_lot_links(1)


def get_lot_links(next_page):
    """ Get links for lots. """
    for i in range(1, int(next_page) + 1):
        page = requests.get(
            url=f'https://gosmoke.ru/{category}?page={i}', headers=headers)
        print(f'page: {i} / {next_page}')
        soup = BeautifulSoup(page.text, 'lxml')
        lot_link = soup.find_all('div', class_='caption-title')
        for i in lot_link:
            link = i.find('a').get('href')
            get_datas(link)


def get_datas(link):
    """ Get all datas, and save to csv table. """
    response = requests.get(url=link, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    try:
        lot_name = soup.find('div', id='content').find('h1').get_text()
    except Exception:
        lot_name = 'not found'
    try:
        description = soup.find(
            'div', class_='product-description').find('p').get_text().strip()
    except Exception:
        description = 'not found'
    try:
        amount = soup.find('div', class_='form-group required').find_all(
            'label')[1].get_text().strip()
    except Exception:
        amount = 'not found'
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
    # Save all datas in csv table.
    instance_saver.save_to_csv((
            link,
            lot_name,
            description,
            amount,
            price,
            img_link,
            presence
    ))


if __name__ == '__main__':
    start_func()
    print('Parsing is completed, the data is in the root of the project.')
