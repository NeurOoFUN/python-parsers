import requests
from bs4 import BeautifulSoup

from settings import headers
from saver import Saver  # Saved class.


CSV_HEADERS = (
    'Product name',
    'Price',
    'Img link',
)
# Create csv file with headers.
Saver().create_csv_table(CSV_HEADERS)


def get_start_urls():
    """
    Connect to the site "www.wildberries.ru", gets links to product
    in the "auto parts" category.
    Pages are also paginated, total pages == 1000.
    Send links func "get_product_datas" for further processing.
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
    Get product links from func "get_start_urls".
    Collected all required datas.
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

    # Saved datas to csv table.
    Saver().save_to_csv(
        (
            product_name,
            price,
            img_link,
        )
    )
    # json datas
    json_dict = {
        'product_name': product_name,
        'price': price,
        'img_link': img_link
    }
    # Saved datas to json file.
    Saver().save_to_json(json_dict)
    # need added link from product.


if __name__ == '__main__':
    get_start_urls()
