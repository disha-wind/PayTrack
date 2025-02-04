import functools
from typing import Any

from sqlalchemy.exc import SQLAlchemyError

from database import async_session


def connect(function) -> Any:
    @functools.wraps(function)
    async def wrapper(*args, **kwargs):
        try:
            async with async_session() as session:
                result = await function(session, *args, **kwargs)
            return result
        except (OSError, SQLAlchemyError) as exc:
            raise ConnectionError("Database operation failed") from exc
    return wrapper