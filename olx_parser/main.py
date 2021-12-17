import requests
import re
import openpyxl
import csv
import os

from bs4 import BeautifulSoup
from fake_useragent import UserAgent

csv_headers = (
    'Заголовок',
    'Описание',
    'Фото',
    'Тип недвижимости',
    'Цена',
    'Этаж',
    'Этажность',
    'Адрес',
    'Кол-во комнат',
    'Площадь',
    'Имя собственника',
    'Номер телефона',
    'Ссылка на объявление',
    'Дата публикации',
    'ID'
)


class Parser:
    """
    Парсер сервиса объявлений OLX.
    """
    def __init__(self):
        self.useragent = UserAgent()
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': f'{self.useragent}',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
            'accept-encoding': 'gzip, deflate, br'
        }
        if not os.path.exists('data'):
            os.mkdir('data')
        with open('data/csv_table.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)

    def get_start_category_links(self):
        """
        Собирает с сайта ссылки и имена на стартовые категории.
        """
        response = self.session.get(url='https://www.olx.ua/nedvizhimost/').text
        soup = BeautifulSoup(response, 'lxml')
        all_start_category_links_list = []
        all_start_category = soup.find_all('li', class_ = 'visible')
        for item in all_start_category:
            start_category_links = item.find('a').get('href')
            self.start_category_names = item.find('span').get_text().strip()
            all_start_category_links_list.append(start_category_links)
            self.get_pagenation(start_category_links)

    def get_pagenation(self, start_category_links):
        """
        Отвечает за пагенацию страниц.
        """
        response = self.session.get(url=start_category_links).text
        soup = BeautifulSoup(response, 'lxml')
        last_page = soup.find('div', class_ = 'pager rel clr').find_all('span')[-3].get_text().strip()
        for i in range(1, int(last_page) + 1):
            pagen_links = start_category_links + f'?page={i}'
            self.get_all_ad(pagen_links)

    def get_all_ad(self, pagen_links):
        """
        Собирает ссылки и адреса на все обьявления.
        """
        response = self.session.get(url=pagen_links).text
        soup = BeautifulSoup(response, 'lxml')
        all_ads = soup.find_all('tr', class_ = 'wrap')
        all_ads_links_list = []
        for item in all_ads:
            self.ads_links = item.find('div', class_ = 'space rel').find('h3').find('a').get('href')
            self.ads_address = item.find_all('small', class_ = 'breadcrumb x-normal')[1].get_text().strip()
            all_ads_links_list.append(self.ads_links)
            self.get_all_datas(self.ads_links)

    def get_all_datas(self, ads_links):
        response = self.session.get(url=ads_links).text
        soup = BeautifulSoup(response, 'lxml')
        # Картинка.
        try:
            self.img = soup.find('div', class_ = 'swiper-zoom-container').find('img').get('src')
        except:
            self.img = 'Нет картинки.'
        # Дата публикации.
        try:
            self.date = soup.find('span', class_ = 'css-19yf5ek').get_text().strip()
        except:
            self.date = 'Информация не указана'
        # Заголовок объявления.
        try:
            self.ads_title = soup.find('h1', class_ = 'css-r9zjja-Text eu5v0x0').get_text().strip()
        except:
            self.ads_title = 'Заголовок объявления не указан.'
        # Цена.
        try:
            self.price = soup.find('h3', class_ = 'css-okktvh-Text eu5v0x0').get_text().strip()
        except:
            self.price = 'Цена не указана'
        # Описание.
        try:
            self.description = soup.find('div', class_ = 'css-g5mtbi-Text').get_text().strip()
        except:
            self.description = 'Нет описания'
        # Этаж.
        try:
            self.floor = soup.find('p', text = re.compile('Этаж:')).get_text().strip()
        except:
            self.floor = 'Информащия не указана.'
        # Этажность.
        try:
            self.number_of_storeys = soup.find('p', text = re.compile('Этажность:')).get_text().strip()
        except:
            self.number_of_storeys = 'Информащия не указана.'
        # Количество комнат.
        try:
            self.rooms_of_numbers = soup.find('p', text = re.compile('Количество комнат:')).get_text().strip()
        except:
            self.rooms_of_numbers = 'Информация не указана'
        # Площадь.
        try:
            if soup.find('p', text = re.compile('Общая площадь:')):
                self.square = soup.find('p', text = re.compile('Общая площадь:')).get_text().strip()
            elif soup.find('p', text = re.compile('Площадь участка:')):
                self.square = soup.find('p', text = re.compile('Площадь участка:')).get_text().strip()
        except:
            self.square = 'Информация не указана'
        # ID.
        try:
            self.id = soup.find('span', class_ = 'css-9xy3gn-Text eu5v0x0').get_text().strip()
        except:
            self.id = 'Информация не указана'
        # Имя собственника.
        try:
            self.name = soup.find('h2', class_ = 'css-u8mbra-Text eu5v0x0').get_text().strip()
        except:
            self.name = 'Информация не указана'
        # Номер телефона.
        # НЕ ЗАБЫТЬ!!!
        self.save_to_csv()

    def save_to_csv(self):
        """
        Пишет данные в CSV.
        """
        with open('data/csv_table.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                self.ads_title,
                self.description,
                self.img,
                self.start_category_names,
                self.price,
                self.floor,
                self.number_of_storeys,
                self.ads_address,
                self.rooms_of_numbers,
                self.square,
                self.name,
                '_____________',
                self.ads_links,
                self.date,
                self.id
            ))

    def run(self):
        self.get_start_category_links()


if __name__ == '__main__':
    parser = Parser()
    parser.run()
