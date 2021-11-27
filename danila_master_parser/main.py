import requests
import csv
import os

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver

print('Скрипт запущен...')

csv_headers = (
    'Название товара',
    'Цена товара',
    'Опимание товара',
)


class Parser:
    """ Основной класс """
    def __init__(self):
        self.useragent = UserAgent().random
        self.session = requests.session()
        self.session.headers = {
            'user-agent': f'{self.useragent}',
            'accept': '*/*'
        }
        options = self.options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={self.useragent}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--headless')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.driver = webdriver.Chrome(executable_path='/home/neuroo/github/python-parsers/danila_master_parser/chromedriver', options=options)
        if not os.path.exists('data'):
            os.mkdir('data')
        with open('data/all_data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)

    def get_start_links(self):
        """ Сбор ссылок на товары и пагенация страниц. """
        url = 'https://www.danilamaster.net/catalog/oboi/'
        response = self.session.get(url).text
        soup = BeautifulSoup(response, 'lxml')
        last_page = soup.find('ul', class_='pagination').find_all('li')[-1].find('a').get('href').split('=')[1]
        for i in range(1, int(last_page) + 1):
            all_start_links_list = []
            pagen_url = url + f'?PAGEN_1={i}'
            response = self.session.get(url=pagen_url).text
            soup = BeautifulSoup(response, 'lxml')
            link = soup.find_all('div', class_ = 'name-inner-wrap')
            print(f'Обрабатывается страница{i}/{last_page}')
            for i in link:
                links = i.find('a').get('href')
                all_start_links = 'https://www.danilamaster.net' + links
                all_start_links_list.append(all_start_links)
                self.get_product_data(all_start_links)

    def get_product_data(self, all_start_links):
        self.driver.get(all_start_links)
        self.driver.implicitly_wait(5)
        # Название.
        try:
            name = self.driver.find_element_by_xpath('//*[@id="isolation"]/main/div[2]/h1').text.strip()
        except:
            name = 'Название товара не указано.'
        # Цена.
        try:
            price = self.driver.find_element_by_xpath('//*[@id="current_price"]').text.strip()
        except:
            price = 'Цена товара не указана.'
        # Описание.
        try:
            description = self.driver.find_element_by_xpath('//*[@id="product-desc"]').text.strip()
        except:
            description = 'Описание товара не указано.'
        with open('data/all_data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                name,
                price,
                description,
            ))

    def close_driver(self):
        """ Закрывает процессы хрома. """
        self.driver.close()
        self.driver.quit()

    def run(self):
        """ Собс-но запускатор. """
        self.get_start_links()
        self.close_driver()


if __name__ == '__main__':
    parser = Parser()
    parser.run()
    print('Сбор данных завершен!')
