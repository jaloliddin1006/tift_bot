from aiogram import types
from handlers.users.start import IsTiftUser

from loader import dp, db

from keyboards.default.defoult_btn import login_menu

# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    user_id = message.from_user.id
    await message.answer(message.text, reply_markup=login_menu(user=IsTiftUser(user_id)))
