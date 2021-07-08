import requests
import json
import time
import random

from bs4 import BeautifulSoup


def main():
    url = 'https://www.ldsp-market.ru/catalog/kromochnye_materialy/kromka_mebelnaya/filter/proizvoditel-is-ecb2f6b1-33c4-11e6-80d5-00155d006309/apply/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.64'
    }
    iteration_count = 22
    print('Идет сбор данных...')
    print(f'Всего итераций: {iteration_count}')
    for item in range(1, 23):
        r = requests.get(url=url + f'?PAGEN_1={item}', headers=headers)
        with open('link_datas.html', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'lxml')
        links = soup.find_all('div', class_ = 'image_wrapper_block')
        all_links_list = []
        for product_link in links:
            all_links = 'https://www.ldsp-market.ru' + product_link.find('a').get('href')
            all_links_list.append(all_links)

            for item in all_links_list:
                r = requests.get(url=all_links, headers=headers)
                
                with open(f'data/{iteration_count}.html', 'w', encoding='utf-8') as file:
                    file.write(r.text)
                
                with open(f'data/{iteration_count}.html', encoding='utf-8') as file:
                    src = file.read()

                soup = BeautifulSoup(src, 'lxml')
                product_data = soup.find_all(class_ = 'container')
                all_product_info_list = []
                for item in product_data:
                    name = item.find('h1').text
                    article = item.find('div', class_ = 'article iblock').find('span', class_ = 'value').text
                    info = item.find('table', class_ = 'props_list').find_all('tr')
                    characteristics_dict = {}
                    for characteristics in info:
                        characteristics_key = characteristics.find_all('td')[0].text.strip()
                        characteristics_value = characteristics.find_all('td')[1].text.strip()
                        characteristics_dict[characteristics_key] = characteristics_value.strip()
                    all_product_info_list.append(
                        {
                            'Название': name, 
                            'Артикул': article, 
                            'Характеристики': characteristics_dict
                        }
                    )
            with open('data/files.json', 'a', encoding='utf-8') as file:
                json.dump(all_product_info_list, file, indent=4, ensure_ascii=False)
        iteration_count -=1
        print('Идет сбор данных...')
        print(f'Осталось итераций: {iteration_count} / 22')
        if iteration_count == 0:
            print('Сбор данных завершен!')
        time.sleep(random.randrange(2, 4))

main()