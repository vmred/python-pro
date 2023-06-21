import sqlite3

from lessons.lesson_6.app.db_connections.db_connection import DBConnection
from variables import LESSON_6_DB_PATH


class SQLiteConnection(DBConnection):

    def __init__(self):
        pass

    @staticmethod
    def create_connection():
        return sqlite3.connect(LESSON_6_DB_PATH)

    @classmethod
    def get_connection(cls, new=False):
        if new or not cls.connection:
            cls.connection = cls.create_connection()
        return cls.connection

    @classmethod
    def execute_query(cls, query):
        connection = cls.get_connection()
        try:
            cursor = connection.cursor()
        except:
            connection = cls.get_connection(new=True)  # Create new connection
            cursor = connection.cursor()

        result = cursor.execute(query).fetchall()
        connection.commit()
        return result
