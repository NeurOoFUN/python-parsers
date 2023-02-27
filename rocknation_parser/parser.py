import re

from bs4 import BeautifulSoup

from tools import session
from writer import Saver


class Parser:
    '''

    This class parses music.
    '''
    link_to_selected_group = str()
    answer = str()
    group_name = str()

    def __init__(self):
        self.save = Saver()

    def parse(self):
        for self.page_count in range(1, 10):  # pagenation.
            album_number = 1
            response = session.get(
                self.link_to_selected_group + f'/{str(self.page_count)}'
            )

            soup = BeautifulSoup(response.text, 'lxml')
            # 'li' tags with album links, and album names.
            album_data = soup.find('div', id='clips').find('ol', class_='list').find_all('li')

            for li in album_data:
                self.album_refs = 'http://rocknation.su' + li.find('a').get('href')
                self.album_name = li.get_text()

                if self.answer == 'no' and re.search(r'(?i)\blive\b', self.album_name):
                    continue
                print(
                    f'Page: {self.page_count}, ' +
                    f'Album: {album_number} / {len(album_data)}'
                )

                album_number += 1

                self.save.album_refs, self.save.album_name, self.save.group_name = \
                        self.album_refs, self.album_name, self.group_name

                try:
                    self.save.download_songs()

                except FileExistsError:
                    print('We have this album, next...')

