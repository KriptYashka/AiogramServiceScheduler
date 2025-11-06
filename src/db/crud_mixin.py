# src/db/crud_mixin.py
from functools import wraps

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.db.session_manager import AsyncSessionManager


def session_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = AsyncSessionManager.get_session()
        kwargs["session"] = session
        result = await func(*args, **kwargs)
        return result
    return wrapper


class CRUDMixin:
    @classmethod
    @session_required
    async def create(cls, session: AsyncSession, **kwargs):
        """Создание записи в таблице."""
        instance = cls(**kwargs)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @classmethod
    @session_required
    async def get_all(cls, session: AsyncSession, limit: int = 10, offset: int = 0):
        """Получение всех записей с учетом offset и limit."""
        results = await session.execute(
            select(cls).limit(limit).offset(offset)
        )
        return results.scalars().all()

    @classmethod
    @session_required
    async def get_by_id(cls, session: AsyncSession, object_id: int):
        """Получение записи по ID."""
        instance = await session.get(cls, object_id)
        return instance

    @classmethod
    @session_required
    async def update(cls, session: AsyncSession, object_id: int, **kwargs):
        """Обновление записи по ID."""
        instance = await session.get(cls, object_id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            await session.commit()
            await session.refresh(instance)
        return instance

    @classmethod
    @session_required
    async def delete_by_id(cls, session: AsyncSession, object_id: int):
        """Удаление записи по ID."""
        instance = await session.get(cls, object_id)
        if instance:
            await session.delete(instance)
            await session.commit()
            return True
        return False
