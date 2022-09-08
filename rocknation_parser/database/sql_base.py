import sqlite3


class SqliteBase:
    def __init__(self):
        with sqlite3.connect('database/music.db') as db:
            cursor = db.cursor()
            create_table = """
                CREATE TABLE IF NOT EXISTS music(id INTEGER PRIMARY KEY,
                group_name TEXT,
                group_link TEXT, genre TEXT)
            """
            cursor.execute(create_table)

    def write_group_name(self, group_name, group_link, genre):
        with sqlite3.connect('database/music.db') as db:
            cursor = db.cursor()
            cursor.execute(
                """INSERT INTO music(group_name, group_link, genre)
                VALUES(?, ?, ?)""",
                (group_name, group_link, genre)
            )
