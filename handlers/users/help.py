from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish\n",
            "/help - Yordam\n",
            "/login - LMS tizimiga bo'g'lanib bildirishnomalarni bot orqali olish\n",
            "/logout - LMS tizimi bilan bo'g'lanishni uzish\n",
            "/off - LMS tizimidan keladigan bildirishnomalarni o'chirib qo'yish\n",
            "/on - LMS tizimidan keladigan bildirishnomalarni yoqish\n",
            )
    
    await message.answer("\n".join(text))