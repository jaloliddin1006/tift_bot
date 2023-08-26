from aiogram import types

from loader import dp, db

from keyboards.default.defoult_btn import login_menu

# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    if user:
        isUser = True  
    else:
        isUser = False
    await message.answer(message.text, reply_markup=login_menu(user=isUser))
