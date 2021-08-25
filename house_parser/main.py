import requests
import os
import csv
import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from openpyxl import Workbook


csv_headers = (
    'Имя категории', 
    'Объявление', 
    'Ссылка на объявление', 
    'Автор объявления', 
    'Номер телефона'
)


class Parser:
    """
    Парсит данные с сайта по продаже недвижимости.
    """
    def __init__(self):
        self.input_url = input('Введите название города: (АНГЛИЙСКИМИ БУКВАМИ)')
        self.useragent = UserAgent().random
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': f'{self.useragent}', 
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 
            'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7'
        }
        if not os.path.exists('data'):
            os.mkdir('data')
        with open(f'data/CSV_table_to_{self.input_url}_.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(csv_headers)



    def get_start_links(self):
        """
        Собирает ссылки на нужные разделы недвижимости.
        """
        self.domain = f'https://{self.input_url}.n1.ru'
        url = f'https://{self.input_url}.n1.ru/sitemap'
        response = self.session.get(url=url).text
        soup = BeautifulSoup(response, 'lxml')
        all_start_links_list = []
        start_links = soup.find_all('ul', class_ = 'site-map-item__children')[1]
        print('Скрипт запущен. Ожидайте завершения сбора данных. Это займет время...')
        for item in start_links:
            all_start_links = self.domain + item.find('a', class_ = 'site-map-item__link').get('href')
            self.start_category_names = item.find('a', class_ = 'site-map-item__link').get_text().strip()
            all_start_links_list.append(all_start_links)
            self.get_links_to_products(all_start_links)



    def get_links_to_products(self, pagen_links):
        """
        Собирает ссылки уже на сами позиции.
        HTML код на некоторых страницах отличатся,
        блок 'try, except' режает эту проблему.
        Цикл 'while' отвечает за пагинацию страниц.
        """
        self.i = 1
        while True:
            response = self.session.get(url=pagen_links, params={'page': self.i}).text
            soup = BeautifulSoup(response, 'lxml')
            all_product_links_list = []
            print(f'Этап обработки: тип недвижимости -- {self.start_category_names} / страница № {self.i}')
            try:
                links = soup.find('div', class_ = 'search-content__results').find_all('a', class_ = 'link')
                for item in links:
                    self.all_product_links = self.domain + item.get('href')
                    all_product_links_list.append(self.all_product_links)
                    self.all_datad_from_pcoduct(self.all_product_links)
            except:
                links = soup.find_all('div', class_ = 'content-entry')
                for item in links:
                    self.all_product_links = self.domain + item.find('a').get('href')
                    all_product_links_list.append(self.all_product_links)
                    self.all_datad_from_pcoduct(self.all_product_links)
            self.i += 1
            if soup.find('span', text = re.compile('Следующая')) == None:
                break


    def all_datad_from_pcoduct(self, all_product_links):
        """
        Осноаная функция скрипта.
        Собирает со страницы объявления все нужные данные.
        """
        response = self.session.get(url=all_product_links).text
        soup = BeautifulSoup(response, 'lxml')
        self.all_phone_list = []
        # Название объявления.
        try:
            self.product_name = soup.find('span', class_ = 'title').get_text()
        except:
            self.product_name = 'Название объявления не указано.'
        # Тип автора(собственник, агенство недвижимости, и т.д.).
        ad_author_block = soup.find('div', class_ = 'offer-card-contacts__wrapper _published').find('div', class_ = 'offer-card-contacts__block')
        try:
            self.author_type = ad_author_block.find('div', class_ = 'offer-card-contacts__person _type').get_text().strip()
        except:
            self.author_type = 'Тип автора объявления не указан.'
        # Имя автора объявления.
        try:
            self.author_name = ad_author_block.find('span', class_ = 'ui-kit-link__inner').get_text().strip()
        except:
            self.author_name = 'Имя автора объявления не указано.'
        # Номер телефона автора объявления.
        try:
            author_phone = soup.find_all('a', class_ = 'offer-card-contacts-phones__phone')
            for item in author_phone:
                phone = item.get('href')
                self.all_phone_list.append(phone)
        except:
            phone = 'Номер телефона не указан.'
        self.save_to_csv()


    def save_to_csv(self):
        """
        Пишет все собраные данные в таблицу CSV формата.
        """
        with open(f'data/CSV_table_to_{self.input_url}_.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(
                (
                    self.start_category_names, 
                    self.product_name, 
                    self.all_product_links, 
                    self.author_type, 
                    str(self.all_phone_list).replace('[', '').replace(']', '').replace("'", ''), 
                )
            )


    def convert_csv_to_excel(self):
        """
        Конвертирует CSV файл в XLSX, оставляя при этом и то и то.
        """
        wb = Workbook()
        ws = wb.active
        with open(f'data/CSV_table_to_{self.input_url}_.csv', 'r', encoding='utf-8') as file:
            for row in csv.reader(file):
                ws.append(row)
        wb.save(f'data/EXCEL_table_to_{self.input_url}_.xlsx')



    def run(self):
        """
        Функция собирает весь скрипт воедино.
        Проверят правописание / наличие города на сайте.
        """
        try:
            self.get_start_links()
            self.convert_csv_to_excel()
        except Exception:
            os.remove(f'data/CSV_table_to_{self.input_url}_.csv')
            print('Произошла ошибка!!!\nЛибо данного города на сайте нет, либо вы не правельно написали название города.\nПопробуйте еще раз.')
            parser = Parser()
            parser.run()




if __name__ == '__main__':
    parser = Parser()
    parser.run()
    print('Сбор данных завершен.\nCSV и XLSX файлы лежат в директории со скриптом.')
    input('Нажмите любую клавишу затем Enter чтобы закрыть консоль...')