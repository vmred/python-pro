"""Create ingex on books (genre)

Revision ID: b4a94b12af4f
Revises: 5f4635e1bce4
Create Date: 2023-08-26 11:58:38.169846

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b4a94b12af4f'
down_revision: Union[str, None] = '5f4635e1bce4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute('CREATE INDEX idx_genre ON books (genre);')


def downgrade() -> None:
    op.execute('DROP INDEX idx_genre;')
