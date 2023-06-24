from typing import Union

from lessons.lesson_6.app.card_model import Card
from lessons.lesson_6.app.db_connections.postgres_connection import PostgresConnection
from lessons.lesson_6.app.db_connections.sqlite_connection import SQLiteConnection


class CardRepository:
    def __init__(self, connection_type: str):
        self.db = self.__init_db_connection(connection_type)

    @staticmethod
    def __init_db_connection(connection_type: str):
        connections = {'sqlite': SQLiteConnection, 'postgres': PostgresConnection}

        connection = connections.get(connection_type)
        if not connection:
            raise ValueError(f'Unknown connection: {connection_type}')
        return connection()

    def save_card(self, card: Card) -> str:
        result = self.db.execute_query(
            f'''
            INSERT INTO cards (pan, expiry_date, cvv, issue_date, owner_id, status)
            VALUES ('{card.pan}', '{card.expiry_date}', '{card.cvv}', '{card.issue_date}', '{card.owner_id}', 
            '{card.status}') returning id'''
        )
        return result[0][0]

    def get_card(self, pan: str = None, card_id: str = None) -> Union[dict, Card]:
        condition = f"pan = '{pan}'"
        if card_id:
            condition = f"id = '{card_id}'"
        result = self.db.execute_query(
            f'''
            SELECT * FROM cards WHERE {condition};
            '''
        )
        if not result:
            return {}

        return Card(
            card_id=result[0][0],
            pan=result[0][1],
            expiry_date=result[0][2],
            cvv=result[0][3],
            issue_date=result[0][4],
            owner_id=result[0][5],
            status=result[0][6],
        )
