import re
import os
import asyncio

from bs4 import BeautifulSoup
from faker import Faker
import requests

session = requests.Session()
f = Faker()
agent = f.firefox()
session.headers['User-Agent'] = agent


async def get_album_links_and_name():
    print(
                '''
                ________________________________________08¶88
        _____________________________________08¶¶¶¶8
        ___________________________________00¶¶¶¶¶0
        __________________________________08¶¶¶¶8
        ________________________________08¶¶¶¶¶0
        ______________________________0¶8¶¶¶¶¶0
        ______________________________08¶¶¶¶¶0
        ________________________________00000
        ________________________________8¶¶¶
        _______________________________08¶88
        _______________________________0¶8¶0
        _______________________________88880
        _______________________________8888
        ______________________________08888
        ______________________________088¶0
        ______________________________88880
        ______________________________88880
        _____________________________08888
        _____________________________08888
        _____________________________88880
        ____________________________088880
        ____________________________088880
        ____________________________88888
        ____________________________88888
        ___________________________088880
        ___________________________088880___________0080
        ___________________________888880________080__8
        __________________________08888¶0_____0880___80
        ______________________008¶¶8888¶¶800880___0_80
        ____________________0¶¶¶¶¶¶¶¶¶¶¶¶800_______80
        ____________________0¶¶¶¶¶¶¶¶¶¶¶¶_________¶0
        ____________________0¶¶¶¶¶00888¶0________80
        ____________________0¶¶¶¶¶______________80
        ____________________0¶¶¶¶8_____________88
        ____________________0¶¶¶¶¶¶¶8880______88
        ____________________8¶¶¶¶¶¶¶¶¶¶¶_____8¶                ------------------------------------ INFO------------------------------------
        __________________0¶¶¶¶¶¶¶¶¶¶¶¶8____8¶0
        _________________0¶¶¶¶¶¶¶¶¶¶¶¶¶8___8¶¶¶                This script parse MUSIC from this website - http://rocknation.su/
        ________________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶88¶¶¶¶¶0               For start parsing you'll necessary to enter a link on interesting group for you.
        ______________0¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶               Example: http://rocknation.su/mp3/band-37
        _____________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶0              ALL GROUPS -- http://rocknation.su/mp3
        ___________0¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶8
        __________8¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
        ________0¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶8
        _______8¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶
        _____0¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶800
        ____0¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶8800
        __0¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶8000
        _0¶¶¶¶¶¶¶¶¶8888000000
                '''
    )
    global group_name
    group_name = input('Enter folder name for save downloaded music: ')
    if not os.path.exists(group_name):
        os.mkdir(group_name)
    input_group_ref = input('Enter reference on group page: ')
    print('OK, Start parsing music...')
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
        print(response.status_code)


async def download_songs(album_refs, album_name):
    response = session.get(url=album_refs).text
    os.mkdir(os.path.normpath(f'{group_name}/{album_name}'))
    print(f'Album: {album_name}')
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
