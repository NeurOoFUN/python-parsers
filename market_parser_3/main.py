import requests
import fake_useragent
import json
import time
import math

from bs4 import BeautifulSoup

start_time = time.time()
def get_data():
    print('Начался сбор данных, это займет какое-то время...')
    iteration_count = 320
    for i in range(1, 321):
        user = fake_useragent.UserAgent().random
        url = 'https://www.kolesa-darom.ru/catalog/avto/shiny/nav/'
        headers = {
            'User-Agent': user, 
            'Accept': '*/*'
        }
        response = requests.get(url=url + f'page-{i}/', headers=headers)
        
        with open('data/start_page.html', 'w', encoding='utf-8') as file:
            file.write(response.text)
        with open('data/start_page.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        links = soup.find_all(class_ = 'product-card__inner')
        all_links_list = []
        # Сбор ссылок и информации о наличии на каждый товар.
        for link in links:
            all_links = 'https://www.kolesa-darom.ru' + link.find(class_ = 'product-card__image').find('a').get('href')
            presence = link.find('span', class_ = 'product-availability__text').get_text().strip()
            all_links_list.append(all_links)
            
            # Запись каждой страницы в html фаил.
            req = requests.get(url=all_links, headers=headers)
            with open('data/pages.html', 'w', encoding='utf-8') as file:
                file.write(req.text)
            with open('data/pages.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            data = soup.find_all(class_ = 'page-wrapper')
            all_datas_list = []
            for all_datas in data:
                try:
                    code = all_datas.find(class_ = 'product-code').text.strip().split('Код: ')[1]
                except:
                    code = 'Код товара не указан.'
                
                try:
                    price = all_datas.find(class_ = 'product-price').find('span').text.strip() + ' Руб'
                except:
                    price = 'Цена товара не указана.'

                try:
                    img = 'https://www.kolesa-darom.ru' + all_datas.find(class_ = 'image-zoom kd-product-preview__zoom').find('img').get('src')
                except:
                    img = 'Нет ссылки на изображение'
                description = soup.find_all(class_ = 'dots-leaders-item')
                for description_datas in description:
                    text = description_datas.get_text().strip().split()
                    mod_text = ' '.join(text)
                    all_datas_list.append(mod_text.strip())
                all_datas_list.append({
                        'Наличие товара': presence, 
                        'Код товара': code, 
                        'Цена товара': price, 
                        'Ссылка на изображение': img, 
                        'Ссылка на товар': all_links
                    })
                with open('data/json_datas.json', 'a', encoding='utf-8') as file:
                    json.dump(all_datas_list, file, indent=4, ensure_ascii=False)
        iteration_count -= 1
        print(f'Осталось спарсить страниц: {iteration_count} / 320')
        if iteration_count == 0:
            print('Сбор данных завершен.')



def main():
    get_data()
    finish_time = time.time() - start_time
    math_time = math.floor(finish_time)
    print(f'Затраченое время: {math_time} секунд.')
if __name__ == '__main__':
    main()