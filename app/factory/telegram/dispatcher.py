from __future__ import annotations

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram_i18n import I18nMiddleware
from redis.asyncio import Redis

from app.models.config import AppConfig
from app.services.database.redis import RedisRepository
from app.telegram.handlers import admin, common, extra
from app.telegram.middlewares import UserMiddleware
from app.telegram.middlewares.outer.database import DBSessionMiddleware
from app.telegram.middlewares.outer.error import ErrorHandlingMiddleware
from app.telegram.middlewares.outer.throttling import ThrottlingMiddleware
from app.utils import mjson

from ..redis import create_redis
from ..session_pool import create_session_pool
from .i18n import create_i18n_middleware


def create_dispatcher(config: AppConfig) -> Dispatcher:
    """
    :return: Configured ``Dispatcher`` with installed middlewares and included routers
    """
    redis: Redis = create_redis(url=config.redis.build_url())
    i18n_middleware: I18nMiddleware = create_i18n_middleware(config)

    dispatcher: Dispatcher = Dispatcher(
        name="main_dispatcher",
        storage=RedisStorage(
            redis=redis,
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        config=config,
        session_pool=create_session_pool(config=config),
        redis=RedisRepository(client=redis),
    )

    dispatcher.include_routers(admin.router, common.router, extra.router)
    dispatcher.update.outer_middleware(UserMiddleware())
    dispatcher.update.outer_middleware(DBSessionMiddleware())
    dispatcher.update.outer_middleware(ErrorHandlingMiddleware())
    dispatcher.update.outer_middleware(ThrottlingMiddleware(client=redis))
    i18n_middleware.setup(dispatcher=dispatcher)
    dispatcher.callback_query.middleware(CallbackAnswerMiddleware())

    return dispatcher
