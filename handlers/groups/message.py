from aiogram import types
from data.config import ADMINS
from loader import dp, db, bot
from filters.group_chat import IsGroup

# Group_id = -1001704364861 # new bot tester
Group_id = -1001583537353

# create thread group with command /thread_group
@dp.message_handler(text = "/thread", user_id=ADMINS)
async def thread_group(message: types.Message):
    print("/thread")
    print(message.chat.id)
    print(message.chat.type)
    print(message.chat.title)
    print(message.chat.username)
    print(message.chat.full_name)
    await message.answer("Creating thread group...")
    topic = await bot.create_forum_topic(chat_id=-1001583537353, name="new topic 5")
    print("ok")
    await message.answer(f"Thread group created: {topic}")
    threads = bot.get_forum_threads(chat_id=Group_id)
    await message.answer(f"Threads: {threads}")
    
    # await message.answer("Sending message to thread group...")
    # await topic.send_message("Hello from thread group!")
    # await message.answer("Message sent!")
    # await message.answer("Deleting thread group...")
    # await topic.leave()
    # await message.answer("Thread group deleted!")



@dp.message_handler(chat_type=[types.ChatType.SUPERGROUP, types.ChatType.GROUP])
async def answer_message(message: types.Message):
  
    if message.reply_to_message:
        # await message.answer(f"reply message: {message}")
        if message.reply_to_message.message_thread_id == 2702:
            print("ok 2702")
            pass
            
        elif message.reply_to_message.message_thread_id == 2:
            
            answer = message.text
            msg_id = message.reply_to_message.text.split("#")[1]
            user_id = db.select_message(msg_id=msg_id)[1]
            # txt = f"ID: #{msg_id}\n"
            txt = f"Answer: {answer}"
            await bot.send_message(chat_id=user_id, text=txt)
            await message.reply("Answer sent!")
        
        elif not message.reply_to_message.message_thread_id:
            # print(message.reply_to_message)
            print("general group reply")
        else:
            print("ok otheer topics reply ")
    else:
        print("no reply message")
