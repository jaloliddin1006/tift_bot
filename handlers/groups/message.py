from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from filters.group_chat import IsGroup

# Group_id = -1001704364861 # new bot tester

@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def bot_start(message: types.Message):
 
    await message.reply("xabar")
    await message.answer(message)

