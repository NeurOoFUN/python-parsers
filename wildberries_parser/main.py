import requests
from bs4 import BeautifulSoup

from settings import headers


def get_start_urls():
    """
Pass
    """
    for i in range(1, 1001):
        url = 'https://www.wildberries.ru/catalog/avtotovary/zapchasti-na-'\
            f'gruzovye-avtomobili?sort=popular&page={i}&xsubject=6728'
        response = requests.get(url=url, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        links = soup.find_all('a', class_='product-card__main')
        for link in links:
            fool_link = 'https://www.wildberries.ru' + link.get('href')
            get_product_datas(fool_link)


def get_product_datas(fool_link):
    """
Pass
    """
    response = requests.get(url=fool_link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    # Name.
    try:
        product_name = soup.find(
            'h1', class_='same-part-kt__header').get_text().strip()
    except Exception:
        product_name = 'product has no name.'
    # Price.
    try:
        price = soup.find(
            'span', class_='price-block__final-price').get_text().strip()
    except Exception:
        price = 'product has no price.'
    # img link.
    try:
        img_link = 'https:' + soup.find(
            'img', class_='photo-zoom__preview j-zoom-preview').get('src')
    except Exception:
        img_link = 'product has no img link'
    # description.
    try:
        description = soup.find(
            'p', class_='collapsable__text')
    except Exception:
        description = 'product has no description'
    print(description)


def run():
    pass


if __name__ == '__main__':
    get_start_urls()
