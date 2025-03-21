from aiogram.types import Update
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from typing import Callable, Dict, Any, Awaitable
from src.database import get_db


class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
            self, handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: Dict[str, Any]
    ) -> Any:

        async for session in get_db():
            data["session"] = session
            return await handler(event, data)
