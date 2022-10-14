import re
import os
import time

from bs4 import BeautifulSoup

from tools import session
from database import find_all_groups, show_all_groupnames, group_selection


def parse():
    """
    This triggered function.
    Get all album links and names.
    """
    try:
        for page_count in range(1, 10):  # pagenation.
            album_count = 1
            response = session.get(
                LINK_TO_SELECTED_GROUP + f'/{str(page_count)}'
            )
            soup = BeautifulSoup(response.text, 'lxml')
            # 'li' tags with album links, and album names.
            album_data = soup.find('div', id='clips') \
                .find('ol', class_='list').find_all('li')

            for li in album_data:
                album_refs = 'http://rocknation.su' + li.find('a').get('href')
                album_name = li.get_text()

                if ANSWER == 'no' and re.search(r'(?i)\blive\b', album_name):
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
        parse()


def download_songs(album_refs=None, album_name=None):
    """
    Download and save all albums with .mp3 songs.
    """
    try:
        response = session.get(url=album_refs).text
        # path of downloaded music
        os.mkdir(os.path.normpath(f'{GROUP_NAME}/{album_name}'))
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
                f'{GROUP_NAME}/{album_name}/{song_count}. {song_name}.mp3'
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
    # find_all_groups()

    show_all_groupnames()

    GROUP_NAME = input('Enter group name: ')

    if not os.path.exists(GROUP_NAME):
        os.mkdir(GROUP_NAME)

    LINK_TO_SELECTED_GROUP = group_selection(GROUP_NAME)

    ANSWER = (input('Need download LIVE albums?  (enter yes / no) ')).lower()

    print('OK, Start parsing music...')

    parse()

    input('END.\nEnter any key for exit.')
