import sqlite3

from lessons.lesson_6.app.db_connections.db_connection import DBConnection
from variables import LESSON_6_DB_PATH


class SQLiteConnection(DBConnection):
    def __init__(self, db_path: str = LESSON_6_DB_PATH):
        super().__init__()
        self.db_path = db_path
        self.connection = self.create_connection()

    def create_connection(self, db_path=None, **kwargs):
        return sqlite3.connect(db_path or self.db_path)

    def get_connection(self, new=False, **kwargs):
        if new or not self.connection:
            self.connection = self.create_connection()
        return self.connection

    def execute_query(self, query):
        connection = self.get_connection()
        try:
            cursor = connection.cursor()
        except Exception as ex:  # pylint: disable=broad-exception-caught
            print(f'Exception occurred during query execution: {ex}')
            connection = self.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()

        result = cursor.execute(query).fetchall()
        connection.commit()
        return result
