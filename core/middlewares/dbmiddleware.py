from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from core.database import DBConnection


class DbMiddleware(BaseMiddleware):
    def __init__(self,
                 db: DBConnection):
        self.__db = db

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        data['db'] = self.__db
        return await handler(event, data)

