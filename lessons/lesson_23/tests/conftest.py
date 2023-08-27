import pytest
from core.config import config
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(config.main_database.connection_string())
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    session = None
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()
