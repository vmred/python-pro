from uuid import uuid4

from sqlalchemy import Column, String, Date, UUID

from core.db.session import Base


class Book(Base):
    __tablename__ = 'books'

    id = Column(UUID, primary_key=True, default=uuid4())
    name = Column(String)
    author = Column(String)
    date_of_release = Column(Date)
    description = Column(String)
    genre = Column(String)
