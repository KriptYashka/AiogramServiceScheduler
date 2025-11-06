# src/db/manager.py
import asyncio

from sqlalchemy.orm import Session
from src.db.models import *
from src.db.models import create_tables
from src.db.session_manager import AsyncSessionManager


class DBManager:
    def __init__(self, session: Session):
        self.session = session


def setup_db():
    database_url = "sqlite+aiosqlite:///./test.db"
    AsyncSessionManager.set_engine(database_url)


async def main():
    setup_db()
    await create_tables()

    new_user = await User.create(phone='1234567891', name='John Doe', tg_username='johndoe1')
    new_user = await User.create(phone='1234567892', name='John Doe1', tg_username='johndoe2')
    new_user = await User.create(phone='1234567893', name='John Doe2', tg_username='johndoe3')
    users = await User.get_all(limit=5, offset=0)
    user = await User.get_by_id(object_id=new_user.id)
    updated_user = await User.update(object_id=new_user.id, name='Jane Doe')
    # deleted = await User.delete_by_id(object_id=new_user.id)


if __name__ == '__main__':
    asyncio.run(main())
