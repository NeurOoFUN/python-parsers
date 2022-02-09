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
    response = requests.get(url=fool_link, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    product_name = soup.find('h1', class_='same-part-kt__header').get_text()
    print(product_name)


def run():
    pass


if __name__ == '__main__':
    get_start_urls()
