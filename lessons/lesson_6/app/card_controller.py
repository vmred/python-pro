import sqlite3
from typing import Union

from lessons.lesson_6.app.card_model import Card
from variables import LESSON_6_DB_PATH


class DBConnection:
    connection = None

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


class CardController(DBConnection):
    def __init__(self):
        self.__connection = DBConnection.get_connection()

    def save_card(self, card: Card) -> None:
        self.execute_query(
            f'''
            INSERT INTO cards (pan, expiry_date, cvv, issue_date, owner_id, status)
            VALUES ('{card.pan}', '{card.expiry_date}', '{card.cvv}', '{card.issue_date}', '{card.owner_id}', 
            '{card.status}');'''
        )

    def get_card(self, pan: str) -> Union[None, Card]:
        result = self.execute_query(
            f'''
            SELECT * FROM cards WHERE pan = '{pan}';
            '''
        )
        if not result:
            return None

        return Card(
            pan=result[0][1],
            expiry_date=result[0][2],
            cvv=result[0][3],
            issue_date=result[0][4],
            owner_id=result[0][5],
            status=result[0][6],
        )
