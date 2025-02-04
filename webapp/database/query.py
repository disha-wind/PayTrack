from typing import Type, Union

from sqlalchemy.ext.asyncio import AsyncSession

from database.model import Base
from database.session import connect


@connect
async def add(session: AsyncSession, obj: Base) -> None:
    try:
        session.add(obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        raise exc

@connect
async def get_by_id(session: AsyncSession, obj_type: Type[Base], obj_id: int) -> Union[Type[Base], None]:
    try:
        obj = await session.get(obj_type, obj_id)
        return obj
    except Exception as exc:
        raise exc

@connect
async def remove_by_id(session: AsyncSession, obj_type: Type[Base], obj_id: int) -> None:
    try:
        obj = await session.get(obj_type, obj_id)
        await session.delete(obj)
        await session.commit()
    except Exception as exc:
        await session.rollback()
        raise exc


