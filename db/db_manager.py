import sqlite3


class DBManager:
    @classmethod
    def generate_schema(cls):
        connection = sqlite3.connect("game.db")
        cursor = connection.cursor()

        # cursor.execute("DROP TABLE game_save")
        cursor.execute("CREATE TABLE IF NOT EXISTS game_save (id INTEGER NOT NULL PRIMARY KEY, name TEXT)")
        cursor.execute("INSERT INTO game_save (name) VALUES ('first save')")
        connection.commit()
