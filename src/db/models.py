from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

__all__ = [
    "User",
    "Location",
    "Master",
    "Service",
    "Admin"
]

from src.db.crud_mixin import CRUDMixin, session_required
from src.db.session_manager import AsyncSessionManager

Base = declarative_base()


class User(Base, CRUDMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    phone = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    tg_username = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', phone='{self.phone}', tg_username='{self.tg_username}')>"


class Location(Base, CRUDMixin):
    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    address = Column(String, nullable=False)

    def __repr__(self):
        return f"<Location(id={self.id}, name='{self.name}', address='{self.address}')>"


class Master(Base, CRUDMixin):
    __tablename__ = 'masters'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location_id = Column(Integer)
    services_offered = Column(String)

    def __repr__(self):
        return f"<Master(id={self.id}, name='{self.name}', location_id={self.location_id})>"


class Service(Base, CRUDMixin):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    price = Column(Integer)
    duration = Column(Integer)

    def __repr__(self):
        return f"<Service(id={self.id}, name='{self.name}', price={self.price}, duration={self.duration})>"


class Appointment(Base, CRUDMixin):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    service_id = Column(Integer)
    master_id = Column(Integer)
    date_time = Column(String)

    def __repr__(self):
        return f"<Appointment(id={self.id}, user_id={self.user_id}, service_id={self.service_id}, master_id={self.master_id}, date_time='{self.date_time}')>"


class Admin(Base, CRUDMixin):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    tg_username = Column(String, unique=True, nullable=False)
    name = Column(String)

    def __repr__(self):
        return f"<Admin(id={self.id}, name='{self.name}', tg_username='{self.tg_username}')>"


async def create_tables() -> None:
    async with AsyncSessionManager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
