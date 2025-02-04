import functools
import os
from typing import Type, Union, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from database.model import *

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

class Database:
    def __init__(self):
        self.engine = create_async_engine(f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}")
        self.async_session = async_sessionmaker(self.engine)

    async def init(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def close(self):
        await self.engine.dispose()
    
    def connect(self, function) -> Any:
        @functools.wraps(function)
        async def wrapper(*args, **kwargs):
            try:
                async with self.async_session() as session:
                    result = await function(session, *args, **kwargs)
                return result
            except (OSError, SQLAlchemyError) as exc:
                raise ConnectionError("Database operation failed") from exc
        return wrapper

    @connect
    async def add(self, session: AsyncSession, obj: Base) -> None:
        try:
            session.add(obj)
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
    
    @connect
    async def get_by_id(self, session: AsyncSession, obj_type: Type[Base], obj_id: int) -> Union[Type[Base], None]:
        try:
            obj = await session.get(obj_type, obj_id)
            return obj
        except Exception as exc:
            raise exc
    
    @connect
    async def remove_by_id(self, session: AsyncSession, obj_type: Type[Base], obj_id: int) -> None:
        try:
            obj = await session.get(obj_type, obj_id)
            await session.delete(obj)
            await session.commit()
        except Exception as exc:
            await session.rollback()
            raise exc
