import sqlite3


def create_db():
    with sqlite3.connect('database/music.db') as db:
        cursor = db.cursor()
        create_table = """
            CREATE TABLE IF NOT EXISTS music(id INTEGER PRIMARY KEY,
            group_name TEXT,
            group_link TEXT, genre TEXT)
        """
        cursor.execute(create_table)
        db.commit()


def write_all_data_to_db(group_name, group_link, genre):
    with sqlite3.connect('database/music.db') as db:
        cursor = db.cursor()
        cursor.execute(
            """INSERT INTO music(group_name, group_link, genre)
            VALUES(?, ?, ?)""",
            (group_name, group_link, genre)
            )
        db.commit()


def show_all_groupnames():
    with sqlite3.connect('database/music.db') as db:
        cursor = db.cursor()
        print_all_data = cursor.execute(
            """
            SELECT group_name FROM music
            """
        ).fetchall()
        for i in print_all_data:
            print(i)


def group_selection(choice_of_user):
    with sqlite3.connect('database/music.db') as db:
        cursor = db.cursor()
        user_selected_group = cursor.execute(
            """
            SELECT group_link FROM music WHERE group_name = ?
            """,
            (choice_of_user,)
        ).fetchone()
        return user_selected_group[0]
