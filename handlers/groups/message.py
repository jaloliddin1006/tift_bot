from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from filters.group_chat import IsGroup

# Group_id = -1001704364861 # new bot tester

@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def answer_message(message: types.Message):
    # print(message)
    if message.reply_to_message:
        if message.reply_to_message.message_id == 2702:
            print("ok")
            
        elif message.reply_to_message.message_id == 2704:
            print("858585858")
        else:
            print(message.reply_to_message)
        # answer = message.text
        # msg_id = message.reply_to_message.text.split("#")[1]
        # user_id = db.select_message(msg_id=msg_id)[1]
        # txt = f"ID: #{msg_id}\n"
        # txt += f"Answer: {answer}"
        # await bot.send_message(chat_id=user_id, text=txt)
        
