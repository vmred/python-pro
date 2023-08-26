"""Create table books

Revision ID: 5f4635e1bce4
Revises: 
Create Date: 2023-08-26 11:58:21.577992

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '5f4635e1bce4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        '''CREATE TABLE books (
            id UUID NOT NULL,
            name VARCHAR,
            author VARCHAR,
            date_of_release DATE,
            description VARCHAR,
            genre VARCHAR,
            PRIMARY KEY (id)
        );'''
    )


def downgrade() -> None:
    op.execute('DROP TABLE IF EXISTS books;')
