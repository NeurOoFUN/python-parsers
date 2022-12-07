import re

from bs4 import BeautifulSoup

from tools import session
from writer import download_songs


def parse(LINK_TO_SELECTED_GROUP: str, ANSWER: str, GROUP_NAME: str) -> None:
    """
    This triggered function.
    Get all album links and names.
    """
    for page_count in range(1, 10):  # pagenation.
        album_count = 1
        response = session.get(
            LINK_TO_SELECTED_GROUP + f'/{str(page_count)}'
        )

        soup = BeautifulSoup(response.text, 'lxml')
        # 'li' tags with album links, and album names.
        album_data = soup.find('div', id='clips').find('ol', class_='list').find_all('li')

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
            try:
                download_songs(
                    album_refs=album_refs, album_name=album_name, GROUP_NAME=GROUP_NAME
                )
            except FileExistsError:
                print('We have this album, next...')
