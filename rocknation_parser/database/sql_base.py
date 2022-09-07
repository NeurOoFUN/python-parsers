import sqlite3


class SqliteBase:
    def __init__(self):
        with sqlite3.connect('database/music.db') as db:
            cursor = db.cursor()
            create_table = """
                CREATE TABLE IF NOT EXISTS music(group_name TEXT)
            """
            cursor.execute(create_table)
            cursor.execute(
                """INSERT INTO music(group_name) VALUES('Test')"""
            )

    def write_group_name(self):
        pass
