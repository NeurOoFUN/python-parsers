import re

import requests
from bs4 import BeautifulSoup

from conf import url, headers


def get_album_refs():
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    album_name = soup.find('div', id='clips') \
        .find('ol', class_='list').find_all('li')
    for i in album_name:
        ref = 'http://rocknation.su' + i.find('a').get('href')
        # name = i.get_text()
        get_song_links(ref=ref)


def get_song_links(ref):
    response = requests.get(url=ref, headers=headers).text
    pattern = re.findall(
        r'http://rocknation\.su/upload/mp3/.+?\.mp3',
        response
    )
    print(pattern)


if __name__ == '__main__':
    get_album_refs()
