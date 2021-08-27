import requests
import pickle
import csv
import re
import os

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from fake_useragent import UserAgent
from authorization_datas import account_login, account_password


print('СКРИПТ ЗАПУЩЕН.\nСЕЙЧАС НАЧНЕТСЯ СБОР ДАННЫХ.\nЭТО ЗАЙМЕТ ВРЕМЯ...')

csv_headers = (
    'Категория', 
    'Подкатегория', 
    'Ссылки на изображения', 
    'Название', 
    'Артикул (id товара)', 
    'Описание', 
    'Световой поток', 
    'Мощность', 
    'Цветовая температура', 
    'Двойной угол половинной яркости', 
    'Тип кривой силы света', 
    'Тип рассеивателя', 
    'Коэф. пульсации', 
    'Индекс цветопередачи', 
    'Производитель светодиодов', 
    'Напряжение питания', 
    'Коэффициент мощности', 
    'Тип питания', 
    'Частота напряжения', 
    'Класс защиты', 
    'Температура эксплуатации', 
    'Степень защиты от пыли и влаги', 
    'Климатическое исполнение', 
    'Рекомендуемая высота установки', 
    'Срок службы светильника', 
    'Срок службы светодиодов', 
    'Гарантийный срок', 
    'Габаритные размеры', 
    'Масса', 
    'Тип крепления', 
    'Материал корпуса', 
    'Материал рассеивателя', 
    'Наличие гальванической развязки', 
    'РРЦ (рекомендуемая цена)', 
    'МРЦ (минимальная розничная цена)', 
    'наша цена (партнерская)'
)



class Parser:
    """
    Основной класс парсера.
    """
    def __init__(self):
        self.useragent = UserAgent().random
        options = self.options = webdriver.ChromeOptions()
        options.add_argument(f'user-agent={self.useragent}')
        options.add_argument('--headless')
        options.add_argument('--disable-blink-features=AutomationControlled')
        self.driver = webdriver.Chrome(executable_path=r'D:\Programs\python_progs\parsers\market_parser_4\chromedriver.exe', options=options)
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': f'{self.useragent}', 
            'Accept': '*/*'
        }
        # Авторизация на сайте.
        # Цены на товары становятся видны только после авторизации.
        try:
            # Логин.
            self.driver.get('https://promled.com/login/')
            login = self.driver.find_element_by_id('input-email')
            login.clear()
            login.send_keys(account_login)
            self.driver.implicitly_wait(10)
            # Пароль.
            password = self.driver.find_element_by_id('input-password')
            password.clear()
            password.send_keys(account_password)
            self.driver.implicitly_wait(10)
            # Ввод.
            password.send_keys(Keys.ENTER)
            self.driver.implicitly_wait(10)
            #Получаем cookies
            pickle.dump(self.driver.get_cookies(), open('cookies', 'wb'))
        except Exception as ex:
            print(ex)
        finally:
            self.driver.quit()
        # Передаем сохраненные печеньки в сессию requests.
        for cookie in pickle.load(open('cookies', 'rb')):
            self.session.cookies.set(cookie['name'], cookie['value'])
        if not os.path.exists('data'):
            os.mkdir('data')
        with open('data/all_data_table.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)


    def get_start_category_pages(self):
        """
        Собирает ссылки на стартовые категории, их всего 3.
        В них в свою очередь лежат ссылки на подкатегории.
        """
        url = 'https://promled.com/'
        response = self.session.get(url=url).text
        soup = BeautifulSoup(response, 'lxml')
        start_category_pages = soup.find_all('a', style='padding: 0px;')
        start_category_pages_list = []
        for item in start_category_pages:
            link = 'https://promled.com/' + item.get('href')
            start_category_pages_list.append(link)
        for all_start_category_links in start_category_pages_list:
            self.get_subcategory_pages(all_start_category_links)


    def get_subcategory_pages(self, all_start_category_links):
        """
        Принемает ссылки из функции 'get_start_category_pages'.
        Получает из них ссылки на подкатегории всех товаров.
        """
        response = self.session.get(url=all_start_category_links).text
        soup = BeautifulSoup(response, 'lxml')
        category_links = soup.find_all(class_ = 'relatedproduct-thumb transition')
        category_links_list = []
        for item in category_links:
            link = item.find('h4').find('a').get('href')
            self.category_name = item.find('h4').find('a').get_text().strip()
            category_links_list.append(link)
            for all_category_links in category_links_list:
                self.get_product_links(all_category_links)


    def get_product_links(self, all_category_links):
        """
        Принемает ссылки из функции 'get_subcategory_pages'.
        Получает из них ссылку на страницу с товаром.
        """
        response = self.session.get(url=all_category_links).text
        soup = BeautifulSoup(response, 'lxml')
        product_links = soup.find_all(class_ = 'relatedproduct-thumb transition')
        all_product_links_list = []
        for item in product_links:
            product_link = item.find('h4').find('a').get('href')
            self.product_name = item.find('h4').find('a').get_text().strip()
            all_product_links_list.append(product_link)
        for all_product_links in all_product_links_list:
            self.get_pagenation_from_modifications(all_product_links)


    def get_pagenation_from_modifications(self, all_product_links):
        """
        Тут пагенация страниц модификаций товара если есть, 
        и сбор описания товара.
        Если страница одна, ссылка просто летит дальше.
        """
        response = self.session.get(url=all_product_links).text
        soup = BeautifulSoup(response, 'lxml')
        if soup.find('ul', class_ = 'pagination'):
            last_block = soup.find('ul', class_ = 'pagination').find_all('li')[-1].find('a').get('href')
            req = self.session.get(url=last_block).text
            soup_2 = BeautifulSoup(req, 'lxml')
            pagenation_count = soup_2.find('li', class_ = 'active').get_text()
            for count in range(1, int(pagenation_count) + 1):
                processed_links = all_product_links + f'?page={count}'
                self.get_data_from_product(processed_links)
        else:
            self.get_data_from_product(all_product_links)



    def get_data_from_product(self, processed_links):
        """
        Забирает со страниц с товарами имя товара, имя модификации,
        ссылку на модификацию.
        Так как данные на страницах отличаются, напсан блок try, except
        """
        response = self.session.get(url=processed_links).text
        soup = BeautifulSoup(response, 'lxml')   # НЕ ЗАБЫТЬ ПРО ССЫЛКИ НА ИЗОБРАЖЕНИЯ!!!
        product_modification_links_list = []
        try:
            self.product_name = soup.find('h1', class_ = 'prohead').get_text()
            self.product_modification_name = soup.find_all('tr', class_ = 'product-layout')[0].find('a').get_text().strip()
            product_modification_links = soup.find_all('tr', class_ = 'product-layout')
            for item in product_modification_links:
                mod_product_modification_links = item.find('a').get('href')
                product_modification_links_list.append(mod_product_modification_links)
        except:
            another_links = soup.find_all('div', class_ = 'relatedproduct-thumb transition')
            for item in another_links:
                links = item.find('h4').find('a').get('href')
                req = self.session.get(url=links).text
                soup = BeautifulSoup(req, 'lxml')
                self.product_name = soup.find('h1', class_ = 'prohead').get_text()
                self.product_modification_name = soup.find_all('tr', class_ = 'product-layout')[0].find('a').get_text().strip()
                product_modification_links = soup.find_all('tr', class_ = 'product-layout')
                for item in product_modification_links:
                    mod_product_modification_links = item.find('a').get('href')
                    product_modification_links_list.append(mod_product_modification_links)
        for all_product_modification_links in product_modification_links_list:
            self.get_all_datas_from_products(all_product_modification_links)


    def get_all_datas_from_products(self, all_product_modification_links):
        """
        Парсинг всех необходимых данных со страниц модификаций.
        """
        response = self.session.get(url=all_product_modification_links).text
        soup = BeautifulSoup(response, 'lxml')
        # Ссылки на изображения.
        self.img_link_list = []
        img = soup.find('div', class_ = 'thumbnails slider-main').find_all('img')
        for item in img:
            img_link = item.get('src')
            self.img_link_list.append(img_link)
        # Имя модификации товара.
        try:
            self.name = soup.find('h1', itemprop = 'name').get_text().strip()
        except:
            self.name = 'Название не указано.'
        # ID модимикации товара.
        try:
            self.id = soup.find('div', class_ = 'prodmodeL').get_text().split('ID товара:')[1].strip()
        except:
            self.id = 'id не указан'
        # Рекомендуемая розничная цена (РРЦ).
        try:
            self.rrc = soup.find_all('span', class_ = 'prodprice')[0].get_text().strip()
        except:
            self.rrc = 'РРЦ не указана.'
        # Минимальная розничная цена (МРЦ).
        try:
            self.mrc = soup.find_all('span', class_ = 'prodprice')[1].get_text().strip()
        except:
            self.mrc = 'МРЦ не указана.'
        # Ваша цена.
        try:
            self.you_prace = soup.find('span', class_ = 'urprice').get_text().strip()
        except:
            self.you_prace = 'Ваша цена не указана.'
        # Описание модификации товара.
        try:
            self.description = soup.find(itemtype = 'http://schema.org/description').get_text().strip()
        except:
            self.description = 'Нет описания.'
        # Таблица с характеристиками.
        # 1.Световой поток, [лм].
        try:
            self.light_flow = soup.find('td', text = re.compile('Световой поток')).find_next_sibling().get_text().strip()
        except:
            self.light_flow = 'Информация о световом потоке не указана.'
        # 2.Мощность, [Вт].
        try:
            self.power = soup.find('td', text = re.compile('Мощность')).find_next_sibling().get_text().strip()
        except:
            self.power = 'Информация о мощности не указана.'
        # 3.Цветовая температура, [К].
        try:
            self.colour_temp = soup.find('td', text = re.compile('Цветовая температура')).find_next_sibling().get_text().strip()
        except:
            self.colour_temp = 'Информация о цветовой температуре не указана.'
        # 4.Двойной угол половинной яркости, [°].
        try:
            self.brightness_angle = soup.find('td', text = re.compile('Двойной угол половинной яркости')).find_next_sibling().get_text().strip()
        except:
            self.brightness_angle = 'Информация о двойном угле половинной яркости не указана.'
        # 5.Тип кривой силы света.
        try:
            self.luminous_type = soup.find('td', text = re.compile('Тип кривой силы света')).find_next_sibling().get_text().strip()
        except:
            self.luminous_type = 'Информация о типе кривой силы света не указана.'
        # 6.Тип рассеивателя.
        try:
            self.diffuser_type = soup.find('td', text = re.compile('Тип рассеивателя')).find_next_sibling().get_text().strip()
        except:
            self.diffuser_type = 'Информация о типе рассеивателя не указана.'
        # 7.Коэффициент пульсации (Кп), не более, [%].
        try:
            self.ripple_factor = soup.find('td', text = re.compile('Коэффициент пульсации')).find_next_sibling().get_text().strip()
        except:
            self.ripple_factor = 'Информация о коэффициенте пульсации не указана.'
        # 8.Индекс цветопередачи (CRI), не менее.
        try:
            self.color_rendering_index = soup.find('td', text = re.compile('Индекс цветопередачи')).find_next_sibling().get_text().strip()
        except:
            self.color_rendering_index = 'Информация о индексе цветопередачи не указана.'
        # 9.Производитель светодиодов.
        try:
            self.manufacturer = soup.find('td', text = re.compile('Производитель светодиодов')).find_next_sibling().get_text().strip()
        except:
            self.manufacturer = 'Информация о производителе светодиодов не указана.'
        # 10.Напряжение питания, [В].
        try:
            self.voltage = soup.find('td', text = re.compile('Напряжение питания')).find_next_sibling().get_text().strip()
        except:
            self.voltage = 'Информация о напряжении питания не указана.'
        # 11.Коэффициент мощности (Pf), не менее.
        try:
            self.power_factor = soup.find('td', text = re.compile('Коэффициент мощности')).find_next_sibling().get_text().strip()
        except:
            self.power_factor = 'Информация о коэффициенте мощности не указана.'
        # 12.Тип питания.
        try:
            self.type_of_food = soup.find('td', text = re.compile('Тип питания')).find_next_sibling().get_text().strip()
        except:
            self.type_of_food = 'Информация о типе питания не указана.'
        # 13.Частота напряжения электропитания, [Гц].
        try:
            self.voltage_frequency =  soup.find('td', text = re.compile('Частота напряжения электропитания')).find_next_sibling().get_text().strip()
        except:
            self.voltage_frequency = 'Информация о частоте напряжения не указана.'
        # 14.Класс защиты от поражения электрическим током (по ГОСТ Р МЭК 60598-1-2011)
        try:
            self.protection_class = soup.find('td', text = re.compile('Класс защиты')).find_next_sibling().get_text().strip()
        except:
            self.protection_class = 'Информация о классе защиты не указана.'
        # 15.Температура эксплуатации, [°С].
        try:
            self.operating_temp = soup.find('td', text = re.compile('Температура эксплуатации')).find_next_sibling().get_text().strip()
        except:
            self.operating_temp = 'Информация о температуре эксплуатации не указана.'
        # 16.Степень защиты от пыли и влаги (по ГОСТ Р МЭК 60598-1-2011).
        try:
            self.dust_protection = soup.find('td', text = re.compile('Степень защиты от пыли и влаги')).find_next_sibling().get_text().strip()
        except:
            self.dust_protection = 'Информация о защите от влаги и пыли не указана.'
        # 17.Климатическое исполнение (по ГОСТ 15150-69).
        try:
            self.climatic_performance = soup.find('td', text = re.compile('Климатическое исполнение')).find_next_sibling().get_text().strip()
        except:
            self.climatic_performance = 'Информация о климатическом исполнении не указана.'
        # 18.Рекомендуемая высота установки, [м].
        try:
            self.installation_height = soup.find('td', text = re.compile('Рекомендуемая высота установки')).find_next_sibling().get_text().strip()
        except:
            self.installation_height = 'Информация о рекомендуемой высоте установки не указана.'
        # 19.Срок службы светильника, не менее, [лет].
        try:
            self.lamp_life = soup.find('td', text = re.compile('Срок службы светильника')).find_next_sibling().get_text().strip()
        except:
            self.lamp_life = 'Информация о сроке службы светилька не указана.'
        # 20.Срок службы светодиодов, не менее, [ч].
        try:
            self.led_life = soup.find('td', text = re.compile('Срок службы светодиодов')).find_next_sibling().get_text().strip()
        except:
            self.led_life = 'Информация о сроке службы светодиодов не указана.'
        # 21.Гарантийный срок, [лет].
        try:
            self.guarantee_period = soup.find('td', text = re.compile('Гарантийный срок')).find_next_sibling().get_text().strip()
        except:
            self.guarantee_period = 'Информация о гарантийном сроке не указана.'
        # 22.Габаритные размеры, [мм].
        try:
            self.size = soup.find('td', text = re.compile('Габаритные размеры')).find_next_sibling().get_text().strip()
        except:
            self.size = 'Информация о габаритных размерах не указана.'
        # 23.Масса, [кг].
        try:
            self.weight = soup.find('td', text = re.compile('Масса')).find_next_sibling().get_text().strip()
        except:
            self.weight = 'Информация о массе не указана.'
        # 24.Тип крепления.
        try:
            self.mount_type = soup.find('td', text = re.compile('Тип крепления')).find_next_sibling().get_text().strip()
        except:
            self.mount_type = 'Информация о типе крепления не указана.'
        # 25.Материал корпуса.
        try:
            self.body_material = soup.find('td', text = re.compile('Материал корпуса')).find_next_sibling().get_text().strip()
        except:
            self.body_material = 'Информация о материале корпуса не указана.'
        # 26.Материал рассеивателя.
        try:
            self.diffuser_material = soup.find('td', text = re.compile('Материал рассеивателя')).find_next_sibling().get_text().strip()
        except:
            self.diffuser_material = 'Информация о материале рассеивателя не указана.'
        # 27.Наличие гальванической развязки.
        try:
            self.galvanic_isolation = soup.find('td', text = re.compile('Наличие гальванической развязки')).find_next_sibling().get_text().strip()
        except:
            self.galvanic_isolation = 'Информация о наличии гальванической развязки не указана.'
        self.save_datas_to_csv()
        print(f'Этап обработки:\nКатегория --  {self.category_name}\nТовар -- {self.product_name}\nМодификация -- {self.name}')



    def save_datas_to_csv(self):
        """
        Запись данных в csv файл.
        """
        with open('data/all_data_table.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            writer.writerow((
                self.category_name, 
                self.product_name, 
                str(self.img_link_list).replace(',', '\n').replace('[', '').replace(']', '').replace("'", ''), 
                self.name, 
                self.id, 
                self.description, 
                self.light_flow, 
                self.power, 
                self.colour_temp, 
                self.brightness_angle, 
                self.luminous_type, 
                self.diffuser_type, 
                self.ripple_factor, 
                self.color_rendering_index, 
                self.manufacturer, 
                self.voltage, 
                self.power_factor, 
                self.type_of_food, 
                self.voltage_frequency, 
                self.protection_class, 
                self.operating_temp, 
                self.dust_protection, 
                self.climatic_performance, 
                self.installation_height, 
                self. lamp_life, 
                self.led_life, 
                self.guarantee_period, 
                self.size, 
                self.weight, 
                self.mount_type, 
                self.body_material, 
                self.diffuser_material, 
                self.galvanic_isolation, 
                self.rrc, 
                self.mrc, 
                self.you_prace
            ))




if __name__ == '__main__':
    parser = Parser()
    parser.get_start_category_pages()
    print('Сбор данных завершен.\nCSV таблица с данными лежит в директории со скриптом.')