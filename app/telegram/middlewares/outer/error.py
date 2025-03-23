from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import TelegramObject


class ErrorHandlingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        # print('event', event)
        if event.callback_query:
            print('callback_query_id', event.callback_query.id)
        try:
            return await handler(event, data)
        except TelegramBadRequest as e:
            logger.error(f'Something went wrong: {str(e)}')
