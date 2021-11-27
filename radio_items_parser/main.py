import os
import requests
import time
import csv
import datetime

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook


csv_headers = (
    'Lot_name',
    'Lot_link',
    'Current_price',
    'Buy_now_price',
    'Start_time',
    'End_time'
)


class Parser:
    """
    Парсер лотов с биржи.
    """
    def __init__(self):
        self.useragent = UserAgent().random
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': f'{self.useragent}',
            'accept': 'image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8'
        }
        options = self.options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={self.useragent}')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(executable_path=r'/home/neuroo/github/python-parsers/radio_items_parser/chromedriver', options=options)
        if not os.path.exists('data'):
            os.mkdir('data')
        with open('data/all_data.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)

    def get_fool_page(self):
        """
        Прокрут страницы до самого конца.
        Сбор динамически подгружаемых ссылок на лоты.
        Запись кода в HTML файл.
        """
        try:
            print('Скрипт запущен...\nПрежде чем начать сбор данных, нужно собрать динамически подгружаемые ссылки...\nЭто займет 1-5 минут, зависит от текущей нагрузки на сайт...')
            self.driver.get('http://japanparcel.com/catalogv2/Audio__video_equipment/Amplifiers')
            page = self.driver.find_element_by_tag_name('html')
            page.send_keys(Keys.END)
            time.sleep(5)
            page.send_keys(Keys.END)
            time.sleep(5)
            page.send_keys(Keys.END)
            time.sleep(5)
            page.send_keys(Keys.END)
            time.sleep(5)
            page.send_keys(Keys.END)
            time.sleep(5)
            page.send_keys(Keys.END)
            time.sleep(5)
            page.send_keys(Keys.END)
            time.sleep(5)
            page.send_keys(Keys.END)
        finally:
            with open('data/fucking_page.html', 'w', encoding='utf-8') as file:
                file.write(self.driver.page_source)
            self.driver.close()
            self.driver.quit()

    def get_all_links(self):
        """
        Чтение ссылок из HTML файла.
        Наполнение функции 'get_datas_from_lots' ссылками на лоты в цикле.
        """
        self.link_count = 0
        with open('data/fucking_page.html', encoding='utf-8') as file:
            src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        self.links = soup.find_all('div', class_ = 'search_item')
        all_links_list = []
        for item in self.links:
            self.all_links = 'http://japanparcel.com' + item.find('a').get('href')
            all_links_list.append(self.all_links)
            self.get_datas_from_lots(self.all_links)

    def get_datas_from_lots(self, links):
        """
        Парсинг всех нужных данных.
        """
        response = self.session.get(url=links).text
        soup = BeautifulSoup(response, 'lxml')
        # Имя лота.
        try:
            self.lot_name = soup.find('div', class_ = 'item_name').find('h1').get_text().strip()
        except:
            self.lot_name = 'No_lot_name.'
        # Текущая цена.
        try:
            self.current_price = soup.find('span', class_ = 'current_price_value').get_text().strip()
        except:
            self.current_price = 'No_current_price.'
        # Бонусная цена(если купить сейчас).
        try:
            self.buy_now_price = soup.find('span', class_ = 'blits_price_value').get_text().strip()
        except:
            self.buy_now_price = 'No_buy_now_price .'
        # Начальное время.
        try:
            self.start_time = soup.find_all('div', class_ = 'item_data')[2].get_text().split('e:')[1].strip()
        except:
            self.start_time = 'No_start_time.'
        # Крайнее время.
        try:
            self.end_time = soup.find_all('div', class_ = 'item_data')[3].get_text().split('e:')[1].strip()
        except:
            self.end_time = 'No_end_time.'
        self.link_count += 1
        print(f'Обрабатывается лот: {self.link_count} из {len(self.links)}')
        self.save_to_csv()

    def save_to_csv(self):
        """
        Запись полученых данных в таблицу CSV формата.
        """
        with open('data/all_data.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow((
                self.lot_name,
                self.all_links,
                self.current_price,
                self.buy_now_price,
                self.start_time,
                self.end_time,
            ))

    def convert_csv_to_excel(self):
        """
        Конвертирует CSV файл в XLSX, оставляя при этом и то и то.
        """
        wb = Workbook()
        ws = wb.active
        with open(f'data/all_data.csv', 'r', encoding='utf-8') as file:
            for row in csv.reader(file):
                ws.append(row)
        wb.save(f'data/all_data.xlsx')

    def run(self):
        self.get_fool_page()
        self.get_all_links()
        self.convert_csv_to_excel()


if __name__ == '__main__':
    while True:
        parser = Parser()
        parser.run()
        print('Сбор данных завершен.')
        print('Время:', datetime.datetime.now())
        print('Следующий сбор данных начнется ровно через 1 час.')
        time.sleep(3600)
