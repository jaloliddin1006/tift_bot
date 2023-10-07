from aiogram import Dispatcher

from loader import dp
from .throttling import ThrottlingMiddleware
from .checksub import BigBrother, AuthMiddleware


if __name__ == "middlewares":
    dp.middleware.setup(ThrottlingMiddleware())
    # dp.middleware.setup(AuthMiddleware())
    dp.middleware.setup(BigBrother())

