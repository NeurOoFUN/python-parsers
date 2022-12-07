import os
import re

from tools import session


def download_songs(album_refs: str, album_name: str, GROUP_NAME: str) -> None:
    """
    Download and save all albums with .mp3 songs.
    """
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
        # Get the name of the song from song link.
        pattern_of_name = re.findall(r'\d\.(.+)\.mp3', i)[0]
        # Cleaning the name of the song.
        song_name = re.sub(r'[\d %]', r'', pattern_of_name)
        music_recording(
            GROUP_NAME=GROUP_NAME,album_name=album_name,
            song_name=song_name, pattern_of_ref=pattern_of_ref,
            download=download, song_count=song_count
        )
        song_count += 1


def music_recording(
    GROUP_NAME: str, album_name: str, song_name: str,
    pattern_of_ref: str, download: bytes, song_count: int
) -> None:
        music_path = os.path.normcase(
            f'{GROUP_NAME}/{album_name}/{song_count}. {song_name}.mp3'
        )
        with open(music_path, 'wb') as file:
            file.write(download)
            print(
                f'Song: {song_name} {song_count} / {len(pattern_of_ref)}'
            )
