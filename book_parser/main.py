import json
import math
import requests
import fake_useragent
import os
import time

from bs4 import BeautifulSoup


start_time = time.time()


class Parser:
    def __init__(self):
        self.session = requests.Session()
        self.user = fake_useragent.UserAgent().random
        self.session.headers = {
            'User-Agent': self.user,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'accept-language': 'ru'
        }
        if not os.path.exists('data'):
            os.mkdir('data')

    def main(self):
        self.pagenation_count = 1
        while True:
            url = 'https://book24.ru/catalog/'
            req = self.session.get(url=url + f'page-{self.pagenation_count}')
            if req.status_code == 404:
                print('Сбор данных завершен!!!')
                break
            self.parse_pages(req.text)
            self.pagenation_count += 1
            time.sleep(1)

    def parse_pages(self, text):
        all_links_list = []
        soup = BeautifulSoup(text, 'lxml')
        link = soup.find_all(class_ = 'product-card__image-holder')
        books_count = 0
        for all_links in link:
            self.all_books_list = []
            book = 'https://book24.ru' + all_links.find('a').get('href')
            all_links_list.append(book)
            req = self.session.get(url=book)
            with open('data/pages.html', 'w', encoding='utf-8') as file:
                file.write(req.text)
            with open('data/pages.html', encoding='utf-8') as file:
                src = file.read()
            soup = BeautifulSoup(src, 'lxml')
            all_content_from_page = soup.find_all(class_ = 'product-detail-page')
            for iteration_content in all_content_from_page:
                # Название.
                name = iteration_content.find(class_ = 'product-detail-page__title').text.strip()
                # Ссылка на картинку.
                img_link = iteration_content.find('img', class_ = 'product-poster__main-image').get('src')
                # Описание.
                about_the_book = iteration_content.find(class_ = 'product-about__text').get_text().strip().replace('\t', '').replace('\"', '')
                # Характеристики.
                characteristics = iteration_content.find(class_ = 'product-characteristic__list').get_text().strip().split()
                mod_characteristics = ' '.join(characteristics)
                # Цена.
                try:
                    price = iteration_content.find(class_ = 'app-price product-sidebar-price__price').get_text().strip()
                except Exception:
                    price = 'Цена товара не указана'
                # Наличие на складе.
                if iteration_content.find(class_ = 'product-preorder-info product-sidebar__preorder-date'):
                    presence = iteration_content.find(class_ = 'product-preorder-info product-sidebar__preorder-date').get_text().strip()
                elif iteration_content.find(class_ = 'product-availability-holder product-sidebar__availability-holder'):
                    presence = iteration_content.find(class_ = 'product-availability-holder product-sidebar__availability-holder').get_text().strip()
                elif iteration_content.find(class_ = 'product-availability-holder _little product-sidebar__availability-holder'):
                    presence = iteration_content.find(class_ = 'product-availability-holder _little product-sidebar__availability-holder').get_text().strip()
                elif iteration_content.find(class_ = 'product-available product-sidebar__availability-holder'):
                    presence = iteration_content.find(class_ = 'product-available product-sidebar__availability-holder').get_text().strip()
                else:
                    presence = 'Нет в наличии'
                # Скидка.
                if iteration_content.find(class_ = 'product-sidebar-price__discount'):
                    discount = iteration_content.find(class_ = 'product-sidebar-price__discount').get_text().strip()
                else:
                    discount = 'Скидки нет'
                self.all_books_list.append(
                    {
                        'Название книги': name,
                        'Ссылка на книгу': book,
                        'Ссылка на постер': img_link,
                        'Про что книга': about_the_book,
                        'Описание товара': mod_characteristics,
                        'Цена товара': price,
                        'Наличие на складе': presence,
                        'Скидка': discount
                    }
                )
                self.save_to_json()
                time.sleep(0.3)
                books_count += 1
                print(f'Обрабатывается страница № {self.pagenation_count} / 6265 \n Товар № {books_count} / 30')

    def save_to_json(self):
        with open('data/books.json', 'a', encoding='utf-8') as file:
            json.dump(self.all_books_list, file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    parser = Parser()
    parser.main()
    finish_time = time.time() - start_time
    math_time = math.floor(finish_time)
    print(f'Затраченое на работу скрипта время -- {math_time} секунд.')
