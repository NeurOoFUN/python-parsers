import re
import os
import asyncio

from bs4 import BeautifulSoup
from faker import Faker
import requests

from info import INFO

# this request sessin.
session = requests.Session()
# fake user-agent
f = Faker()
agent = f.firefox()
session.headers['User-Agent'] = agent


async def get_album_links_and_name():
    print(INFO)
    global group_name
    group_name = input('Enter folder name for save downloaded music: ')
    if not os.path.exists(group_name):
        os.mkdir(group_name)
    input_group_ref = input('Enter reference on group page: ')
    print('OK, Start parsing music...')
    # pagenation.
    for x in range(1, 10):
        response = session.get(input_group_ref + f'/{str(x)}')
        soup = BeautifulSoup(response.text, 'lxml')
        album_name_list = soup.find('div', id='clips') \
            .find('ol', class_='list').find_all('li')
        for i in album_name_list:
            album_refs = 'http://rocknation.su' + i.find('a').get('href')
            album_name = i.get_text()
            await download_songs(
                album_refs=album_refs, album_name=album_name
            )


async def download_songs(album_refs, album_name):
    response = session.get(url=album_refs).text
    # path of downloaded music
    os.mkdir(os.path.normpath(f'{group_name}/{album_name}'))
    print(f'Album: {album_name}')
    # regex, parse links from JS.
    pattern_of_ref = re.findall(
        r'http://rocknation\.su/upload/mp3/.+?\.mp3',
        response
    )
    b = 1
    for i in pattern_of_ref:
        download = session.get(url=i).content
        music_path = os.path.normcase(f'{group_name}/{album_name}/{b}.mp3')
        with open(music_path, 'wb') as file:
            file.write(download)
            print(f'Song: №{b}')
            b += 1


async def main():
    await asyncio.gather(
        get_album_links_and_name()
    )


if __name__ == '__main__':
    asyncio.run(main())
    input('END.\nEnter any key for exit.')
