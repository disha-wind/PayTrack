import functools
import os
from typing import Type, Union, Any

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from database.model import *

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

if not all([POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB]):
    raise EnvironmentError("Database environment variables are not set properly.")

class Database:
    def __init__(self):
        self.engine = create_async_engine(f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@database/{POSTGRES_DB}")
        self.async_session = async_sessionmaker(self.engine)
        self.last_session = None

    async def init(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def close(self):
        await self.engine.dispose()
    
    async def get_by_id_with_session(self, obj_type: Type[Base], obj_id: int) -> Union[Type[Base], None]:
        try:
            self.last_session = self.async_session()
            obj = await self.last_session.get(obj_type, obj_id)
            return obj
        except Exception as exc:
            raise exc
    
    async def commit(self):
        try:
            if self.last_session:
                await self.last_session.commit()
                self.last_session = None
        except Exception as exc:
            await self.last_session.rollback()
            self.last_session = None
            raise exc
    
    @staticmethod
    def connect(function) -> Any:
        @functools.wraps(function)
        async def wrapper(self, *args, **kwargs):
            try:
                async with self.async_session() as session:
                    result = await function(self, session, *args, **kwargs)
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
    async def get_all(self, session: AsyncSession, obj_type: Type[Base]) -> list[Base]:
        try:
            result = await session.execute(select(obj_type))
            objs = []
            objs.extend(result.scalars().all())
            return objs
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
    
    @connect
    async def get_by_email(self, session: AsyncSession, email: str) -> Union[User, None]:
        try:
            result = await session.execute(select(User).where(User.email == email))
            user = result.scalars().first()
            return user
        except Exception as exc:
            raise exc
    
    @connect
    async def get_accounts(self, session: AsyncSession, user_id: int) -> list[Account]:
        try:
            result = await session.execute(select(Account).where(Account.user_id == user_id))
            accounts = []
            accounts.extend(result.scalars().all())
            return accounts
        except Exception as exc:
            raise exc
        
    @connect
    async def get_payments(self, session: AsyncSession, user_id: int) -> list[Payment]:
        try:
            result = await session.execute(select(Account).where(Account.user_id == user_id))
            accounts = []
            accounts.extend(result.scalars().all())
            payments = []
            for account in accounts:
                result = await session.execute(select(Payment).where(Payment.account_id == account.id))
                payments.extend(result.scalars().all())
            return payments
        except Exception as exc:
            raise exc
    
    @connect
    async def update_user(self, session: AsyncSession, user_id: int, updated_data: dict) -> None:
        try:
            user = await session.get(User, user_id)
    
            if not user:
                return None

            for key, value in updated_data.items():
                if hasattr(user, key):
                    setattr(user, key, value)
    
            await session.commit()
            
        except Exception as exc:
            await session.rollback()
            raise exc
