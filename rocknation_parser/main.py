import re
import os
import time

from bs4 import BeautifulSoup

# from info import INFO
from tools import session
from database.getting_data_for_db import find_all_groups

# print(INFO)
find_all_groups()
group_name = input('Enter folder name for save downloaded music: ')

if not os.path.exists(group_name):
    os.mkdir(group_name)

input_group_ref = input('Enter reference on group page: ')

answer = (input('Need download LIVE albums?  (enter yes / no) ')).lower()

print('OK, Start parsing music...')


def main():
    """
    This triggered function.
    Get all album links and names.
    """
    try:
        for page_count in range(1, 10):  # pagenation.
            album_count = 1
            response = session.get(input_group_ref + f'/{str(page_count)}')
            soup = BeautifulSoup(response.text, 'lxml')
            # 'li' tags with album links, and album names.
            album_data = soup.find('div', id='clips') \
                .find('ol', class_='list').find_all('li')

            for li in album_data:
                album_refs = 'http://rocknation.su' + li.find('a').get('href')
                album_name = li.get_text()

                if answer == 'no' and re.search(r'(?i)\blive\b', album_name):
                    continue
                print(
                    f'Page: {page_count}, ' +
                    f'Album: {album_count} / {len(album_data)}'
                )
                album_count += 1

                download_songs(
                    album_refs=album_refs, album_name=album_name
                )

    except ConnectionResetError:
        print('ConnectionResetError, Trying reconnect...')
        time.sleep(5)
        main()


def download_songs(album_refs=None, album_name=None):
    """
    Download and save all albums with .mp3 songs.
    """
    try:
        response = session.get(url=album_refs).text
        # path of downloaded music
        os.mkdir(os.path.normpath(f'{group_name}/{album_name}'))
        # regex, parse links from JS.
        pattern_of_ref = re.findall(
            r'http://rocknation\.su/upload/mp3/.+?\.mp3',
            response
        )
        song_count = 1

        # download songs.
        for i in pattern_of_ref:
            download = session.get(url=i).content
            # Get song name from song link.
            pattern_of_name = re.findall(r'\d\.(.+)\.mp3', i)[0]
            # Washing song name.
            song_name = re.sub(r'[\d %]', r'', pattern_of_name)
            music_path = os.path.normcase(
                f'{group_name}/{album_name}/{song_count}. {song_name}.mp3'
            )
            with open(music_path, 'wb') as file:
                file.write(download)
                print(
                    f'Song: {song_name} {song_count} / {len(pattern_of_ref)}'
                )
                song_count += 1

    except FileExistsError:
        print('We have this album, next...')


if __name__ == '__main__':
    main()
    input('END.\nEnter any key for exit.')
