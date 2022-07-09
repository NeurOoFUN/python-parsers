import re
import os

from bs4 import BeautifulSoup

from conf import url, session


def main():
    if not os.path.exists('data'):
        os.mkdir('data')
    response = session.get(url=url)
    soup = BeautifulSoup(response.text, 'lxml')
    album_name_list = soup.find('div', id='clips') \
        .find('ol', class_='list').find_all('li')
    for i in album_name_list:
        album_refs = 'http://rocknation.su' + i.find('a').get('href')
        album_name = i.get_text()
        download_songs(album_refs=album_refs, album_name=album_name)


def download_songs(album_refs, album_name):
    response1 = session.get(url=album_refs).text
    os.mkdir(f'data/{album_name}')
    pattern_of_ref = re.findall(
        r'http://rocknation\.su/upload/mp3/.+?\.mp3',
        response1
    )
    # pattern_of_name = re.findall(
    #     r'\"(\w{1,2}\. .+?)\"',
    #     response1
    # )
    b = 1
    for i in pattern_of_ref:
        response2 = session.get(url=i).content
        with open(f'data/{album_name}/{b}', 'wb') as file:
            file.write(response2)
        b += 1


if __name__ == '__main__':
    main()
