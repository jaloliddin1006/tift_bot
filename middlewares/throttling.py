import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from data.api import check_user
from keyboards.default.defoult_btn import login_menu
from loader import db
import sqlite3

class ThrottlingMiddleware(BaseMiddleware):
    """
    Simple middleware
    """

    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        # print(message.from_user.full_name)
        
        user = message.from_user
        old = db.select_bot_user(telegram_id = user.id)
        if not old:
            if user.username:
                username = user.username
            else:
                username = None

            try:
                db.add_bot_user(telegram_id=user.id, name=user.full_name, user_name=username, language="uz")
            except sqlite3.IntegrityError as err:
                pass
        else:
            user = db.select_tift_user(user_id = message.from_user.id)
            if user:
                token = user[8]
                # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyNDUxNjA4LCJpYXQiOjE2OTIzNjUyMDgsImp0aSI6IjY3ZjE1NmI1NzA3ZTRmMDZiNjg5NmY0YjdhMWE0ZjhkIiwidXNlcl9pZCI6NH0.WZwuayZdLJ1Au2c-XBoF_e-2sgSJHIouO9uisaw8T6g"
                if token:
                    get_user = check_user(token)
                    if get_user != 200:
                        db.logout_token(user_id=message.from_user.id, token=None)
                        await message.answer("LMS bilan aloqa uzuldi, qaytadan login qiling. 👉 /login", reply_markup=login_menu(user=False))
            
            

        handler = current_handler.get()
        dispatcher = Dispatcher.get_current()
        if handler:
            limit = getattr(handler, "throttling_rate_limit", self.rate_limit)
            key = getattr(handler, "throttling_key", f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_message"
        try:
            await dispatcher.throttle(key, rate=limit)
        except Throttled as t:
            await self.message_throttled(message, t)
            raise CancelHandler()

    async def message_throttled(self, message: types.Message, throttled: Throttled):

        handler = current_handler.get()

        dispatcher = Dispatcher.get_current()

        if handler:

            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")

        else:

            key = f"{self.prefix}_message"


        # Calculate how many time is left till the block ends

        delta = 1


        # Prevent flooding

        if throttled.exceeded_count <= 2:

            await message.reply('Too many requests! ')


        # Sleep.

            await asyncio.sleep(delta)


        # Check lock status

        thr = await dispatcher.check_key(key)


        # If current message is not last with current key - do not send message

        if thr.exceeded_count == throttled.exceeded_count:

            await message.reply('Unlocked.')