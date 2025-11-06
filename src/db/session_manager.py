from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


class AsyncSessionManager:
    engine = None
    _Session = None

    @classmethod
    def set_engine(cls, database_url: str):
        cls.engine = create_async_engine(database_url, echo=True)
        cls._Session = sessionmaker(bind=cls.engine, class_=AsyncSession, expire_on_commit=False)

    @classmethod
    def get_session(cls):
        async_session = cls._Session()
        return async_session
