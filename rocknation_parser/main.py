import os
import time

from database import MusicDbManager, find_all_groups
from parser import parse


music_manager_instance = MusicDbManager()


if __name__ == '__main__':
    # uncomment find_all_groups() if data base not exist (music.db)
    find_all_groups()

    music_manager_instance.show_all_groupnames()

    GROUP_NAME = input('Enter group name: ')

    if not os.path.exists(GROUP_NAME):
        os.mkdir(GROUP_NAME)

    LINK_TO_SELECTED_GROUP = music_manager_instance.group_selection(GROUP_NAME)

    ANSWER = (input('Do you need LIVE albums?  (enter yes / no) ')).lower()

    print('OK, Start parsing music...')
    try:
        parse(
                LINK_TO_SELECTED_GROUP=LINK_TO_SELECTED_GROUP,
                ANSWER=ANSWER, GROUP_NAME=GROUP_NAME
                )
    except ConnectionResetError:
        print('ConnectionResetError, Trying reconnect...')
        time.sleep(5)
        parse(LINK_TO_SELECTED_GROUP=LINK_TO_SELECTED_GROUP,
            ANSWER=ANSWER, GROUP_NAME=GROUP_NAME)

    input('END.\nEnter some key for exit.')
