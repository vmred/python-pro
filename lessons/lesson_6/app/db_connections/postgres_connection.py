import os

from dotenv import load_dotenv, find_dotenv
from psycopg2 import ProgrammingError
from psycopg2.pool import SimpleConnectionPool

from lessons.lesson_6.app.db_connections.db_connection import DBConnection
from variables import LESSON_6_ENV

load_dotenv(dotenv_path=LESSON_6_ENV)


class PostgresConnection(DBConnection):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 5432
        self.db_name = os.environ.get('DB_NAME')
        self.user = os.environ.get('DB_USER')
        self.password = os.environ.get('DB_PASSWORD')
        self.connection_pool = self.create_connection()

    def create_connection(self):
        return SimpleConnectionPool(
            1, 10, host=self.host, port=self.port, dbname=self.db_name, user=self.user, password=self.password
        )

    def get_connection(self, **kwargs):
        return self.connection_pool.getconn()

    def execute_query(self, query):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute(query)
        try:
            result = cursor.fetchall()
        except ProgrammingError:
            result = None
        cursor.close()
        connection.commit()
        return result
