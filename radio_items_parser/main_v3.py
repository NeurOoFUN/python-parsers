import re
import time
import math
import os
import csv

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

csv_headers_tuple = (
    'url',
    'lot_name',
    'current_price',
    'buy_now_price'
)

start_time = time.time()
url = 'http://japanparcel.com/catalogv2/Audio__video_equipment/Amplifiers?=&n=100&min=&max=&scroll=1&pg=2'
headers = {
    'user-agent': f'{UserAgent()}',
    'accept': '*/*'
}
response = requests.get(url=url, headers=headers)
pattern = re.findall(r'href=\\"\\/ylot\\/(\w+)\\"', response.text)
datas = set()


class Saver:
    def __init__(self):
        """ Created directory for collected datas. """
        if not os.path.exists('datas'):
            os.mkdir('datas')

    @staticmethod
    def create_csv_table(csv_headers: tuple):
        with open('datas/table.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(
                file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(csv_headers)

    @staticmethod
    def save_to_csv(fields: tuple):
        with open('datas/table.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(
                file, dialect='excel', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(fields)


def parse():
    Saver()
    print('The start parsing...')
    counter = 0
    Saver.create_csv_table(csv_headers_tuple)
    for i in pattern:
        datas.add('http://japanparcel.com/ylot/' + i)
    print('Total lots: ', len(datas))
    for urls in datas:
        counter += 1
        print(f'Current lot: {counter} / {len(datas)}')
        response2 = requests.get(url=urls, headers=headers)
        soup = BeautifulSoup(response2.text, 'lxml')
        try:
            lot_name = soup.find('div', class_='item_name').find('h1', itemprop='name').get_text()
        except AttributeError:
            lot_name = 'Not found'
        try:
            current_price = soup.find('div', class_='current_price_block')\
                .find('span', class_='current_price_value').get_text().strip()
        except AttributeError:
            current_price = 'Not found'
        try:
            buy_now_price = soup.find('div', class_='blits_price_block')\
                .find('span', class_='blits_price_value').get_text().strip()
        except AttributeError:
            buy_now_price = 'Not found'
        Saver.save_to_csv((
            urls,
            lot_name,
            current_price,
            buy_now_price
        ))


if __name__ == '__main__':
    parse()
    finish_time = time.time()
    print('Elapsed time: ', abs(math.floor(start_time - finish_time)), 'seconds.')
    print('.csv file the data file is located in the folder with the script.')
