import sqlite3

class MusicDbManager:
    """
    Some desctiption.
    """
    def __init__(self):
        self.connect = sqlite3.connect('database/music.db')
        self.cursor = self.connect.cursor()

    def __del__(self):
        self.connect.commit()
        self.connect.close()

        print(self.__dict__)

    def create_db(self):
            create_table = """
                CREATE TABLE IF NOT EXISTS music(
                    id INTEGER PRIMARY KEY,
                    group_name TEXT,
                    group_link TEXT,
                    genre TEXT
                )
            """
            self.cursor.execute(create_table)

    def write_all_data_to_db(self, group_name: str, group_link: str, genre: str):
            self.cursor.execute(
                """INSERT INTO music(group_name, group_link, genre)
                   VALUES(?, ?, ?)
                """,
                (group_name, group_link, genre)
                )

    def show_all_groupnames(self):
            print_all_data = self.cursor.execute(
                """
                SELECT group_name FROM music
                """
            ).fetchall()
            for i in print_all_data:
                print(*i)

    def group_selection(self, choice_of_user: str) -> str:
            user_selected_group = self.cursor.execute(
                """
                SELECT group_link FROM music WHERE group_name = ?
                """,
                (choice_of_user,)
            ).fetchone()
            return user_selected_group[0]

