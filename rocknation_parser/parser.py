import re

from bs4 import BeautifulSoup

from tools import session
from writer import download_songs


class Parser:
    '''

    This class parses music.
    '''
    link_to_selected_group = str()
    answer = str()
    group_name = str()

    def parse(self):
        for page_count in range(1, 10):  # pagenation.
            album_number = 1
            response = session.get(
                self.link_to_selected_group + f'/{str(page_count)}'
            )

            soup = BeautifulSoup(response.text, 'lxml')
            # 'li' tags with album links, and album names.
            album_data = soup.find('div', id='clips').find('ol', class_='list').find_all('li')

            for li in album_data:
                album_refs = 'http://rocknation.su' + li.find('a').get('href')
                album_name = li.get_text()

                if self.answer == 'no' and re.search(r'(?i)\blive\b', album_name):
                    continue
                print(
                    f'Page: {page_count}, ' +
                    f'Album: {album_number} / {len(album_data)}'
                )

                album_number += 1

                try:
                    download_songs(
                        album_refs=album_refs, album_name=album_name, GROUP_NAME=self.group_name
                    )
                except FileExistsError:
                    print('We have this album, next...')

