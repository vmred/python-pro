from datetime import date

from models import Book


def test_create_book(session):
    book = Book(
        name="Sample Book",
        author="John Doe",
        date_of_release=date(2020, 1, 1),
        description="A sample book description.",
        genre="Fiction",
    )

    session.add(book)
    session.commit()

    stored_book = session.query(Book).filter_by(name="Sample Book").first()
    assert stored_book.author == "John Doe"
    assert stored_book.genre == "Fiction"
    assert stored_book.date_of_release
