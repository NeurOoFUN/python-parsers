import requests
import json

from bs4 import BeautifulSoup




def get_data():
    url = f'https://albico.ru/products/fartuki/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67'
    }
    print('Парсер запущен, идет сбор данных...')
    page_count = 24
    for i in range(1, 25):
        r = requests.get(url=url + f'?PAGEN_1={i}', headers=headers)
        with open('html.html', 'w', encoding='utf-8') as file:
            file.write(r.text)
        with open('html.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        link_class = soup.find_all('div', class_ = 'apron_list_item')
        all_links_list = []
        for item in link_class:
            all_links = 'https://albico.ru' + item.find('a').get('href')
            all_links_list.append(all_links)
        for link in all_links_list:
            req = requests.get(url=link, headers=headers)
            with open('data/pages.html', 'w', encoding='utf-8') as file:
                file.write(req.text)
            with open('data/pages.html', encoding='utf-8') as file:
                src = file.read()

            soup = BeautifulSoup(src, 'lxml')
            all_datas = soup.find_all(class_ = 'wrapper')
            all_datas_list = []
            for datas in all_datas:
                name = datas.find(class_ = 'apron_detail_top').find('h1').text
                params = datas.find(class_ = 'apron_detail_tabs_panel').text.strip()
                all_datas_list.append(
                    {
                        'Название': name, 
                        'Характеристики': params
                    }
                )
                with open('data/all_datas.json', 'a', encoding='utf-8') as file:
                    json.dump(all_datas_list, file, indent=4, ensure_ascii=False)
        page_count -= 1
        print(f'Спаршено страниц: {page_count} из 24')
        if page_count == 0:
            print('Сбор данных успешно завершен!')










get_data()