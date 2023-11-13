from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from filters.group_chat import IsGroup


@dp.message_handler(text="/about", chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], )
async def get_about(message: types.Message):
    try:
        if message.reply_to_message:
            if message.reply_to_message.forward_sender_name:
                user_ = db.select_bot_user(name=message.reply_to_message.forward_sender_name)
                user = db.select_new_message(nick_name=message.reply_to_message.forward_sender_name)
            else:
                user_ = db.select_bot_user(telegram_id=message.reply_to_message.forward_from.id)
                user = db.select_new_message(telegram_id=message.reply_to_message.forward_from.id)
            await message.reply(f"User haqida ma'lumotlar:\n\nTelegram ID: {user[0]}\nNick Name: {user[2]}\nFull Name: {user[1]}\nUsername: @{user_[3]}\nTelefon: {user[3]}")
        else:
            await message.reply("Biror xabarni 'reply' qilib /about buyrug'ini kiriting:")
    except Exception as err:
        # await message.reply(f"Xatolik: {err}")
        pass

@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP], content_types=types.ContentTypes.ANY)
async def answer_message(message: types.Message):
    if message.reply_to_message:
        try:
            if message.reply_to_message.forward_sender_name:
                user = db.select_new_message(nick_name=message.reply_to_message.forward_sender_name)
            else:
                user = db.select_new_message(telegram_id=message.reply_to_message.forward_from.id)
            await bot.send_message(chat_id=user[0], text="Sizga javob keldi:")
            await message.send_copy(chat_id=user[0])
            await message.reply("Xabar yuborildi ✅")
        except Exception as err:
            pass
            # await message.reply(f"Xabar yuborilmadi: {err}")
            
        
      
# # Group_id = -1001704364861 # new bot tester
# Group_id = -1001583537353

# # create thread group with command /thread_group
# @dp.message_handler(text = "/thread", user_id=ADMINS)
# async def thread_group(message: types.Message):
#     print("/thread")
#     print(message.chat.id)
#     print(message.chat.type)
#     print(message.chat.title)
#     print(message.chat.username)
#     print(message.chat.full_name)
#     await message.answer("Creating thread group...")
#     topic = await bot.create_forum_topic(chat_id=-1001583537353, name="new topic 5")
#     print("ok")
#     await message.answer(f"Thread group created: {topic}")
#     threads = bot.get_forum_threads(chat_id=Group_id)
#     await message.answer(f"Threads: {threads}")
    
#     # await message.answer("Sending message to thread group...")
#     # await topic.send_message("Hello from thread group!")
#     # await message.answer("Message sent!")
#     # await message.answer("Deleting thread group...")
#     # await topic.leave()
#     # await message.answer("Thread group deleted!")



# @dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
# async def answer_message(message: types.Message):
  
#     if message.reply_to_message:
#         # await message.answer(f"reply message: {message}")
#         if message.reply_to_message.message_thread_id == 2702:
#             print("ok 2702")
#             pass
            
#         elif message.reply_to_message.message_thread_id == 2:
            
#             answer = message.text
#             msg_id = message.reply_to_message.text.split("#")[1]
#             user_id = db.select_message(msg_id=msg_id)[1]
#             # txt = f"ID: #{msg_id}\n"
#             txt = f"Answer: {answer}"
#             await bot.send_message(chat_id=user_id, text=txt)
#             await message.reply("Answer sent!")
        
#         elif not message.reply_to_message.message_thread_id:
#             # print(message.reply_to_message)
#             print("general group reply")
#         else:
#             print("ok otheer topics reply ")
#     else:
#         print("no reply message")
