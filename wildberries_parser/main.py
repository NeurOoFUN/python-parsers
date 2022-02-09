import requests
from fake_useragent import UserAgent


useragent = UserAgent().random
url = 'https://www.wildberries.ru/catalog/avtotovary/zapchasti-'\
    'na-gruzovye-avtomobili?sort=popular&page=1&xsubject=6728'
headers = {
    'user-agent': f'{useragent}',
    'accept': '*/*'
}


def get_start_urls():
    response = requests.get(url=url, headers=headers)
    print(response.text)


if __name__ == '__main__':
    get_start_urls()
