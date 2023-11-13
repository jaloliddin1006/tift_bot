from aiogram import types
from data.config import ADMINS
from handlers.users.help import IsTiftUser
from keyboards.inline.inline_btn import check_member_button


from loader import dp, db, bot

from keyboards.default.defoult_btn import login_menu

# Echo bot
@dp.message_handler(state='*', user_id=ADMINS)
async def bot_echo(message: types.Message):
    user_id = message.from_user.id
    await message.answer(message.text, reply_markup=login_menu(user="admin", tg_id=user_id))
    
    
@dp.message_handler(state='*')
async def bot_echo(message: types.Message):
    user_id = message.from_user.id
    await message.answer(message.text, reply_markup=login_menu(IsTiftUser(user_id)))

async def subscribe_channel_func(message, result, join_channel):
    await message.answer("Kanallarga to'liq obuna bo'ling", reply_markup=types.ReplyKeyboardRemove())
    await message.answer(result, disable_web_page_preview=True, reply_markup=check_member_button(join_channel))
    return
    # chat = await bot.get_chat('@new_bot_test_group')
    #    user = await bot.get_chat_member(chat_id="@new_bot_test_group", user_id=message.from_user.id)
    # isuser = await bot.get_chat_member(chat_id="-1001704364861", user_id=message.from_user.id) #status owner, administrator, member
    # invite_link = await chat.export_invite_link()
    # invite_link = chat['invite_link']
    # print(chat)
    # # await message.answer(isuser)
    # status = await bot.get_chat_member("-1001704364861", message.from_user.id)
    # member_count = await bot.get_chat_member_count(chat_id=chat.id) ## member count
    
    
    # await message.answer(message.text)
    # if status['status'] == 'left':
    #     channel_info = [invite_link, chat.title, 0]
    # else:
    #     channel_info = [invite_link, chat.title, 1]
    #             aa += 1
    #         join_channel.append(cha
    # user_id = message.from_user.id
    # await message.answer(message.text, reply_markup=login_menu(user=IsTiftUser(user_id)))





async def check_membership(user_id):
    # Foydalanuvchi haqida ma'lumotlarni olish va majburiy a'zo bo'lishini tekshirish
    # Ma'lumotlar bazasidan yoki Telegram API orqali tekshirish mumkin

    # Masalan, agar foydalanuvchi kanalga majburiy a'zo bo'lsa True qaytaring,
    # aks holda False qaytaring.
    return True  # Bu o'rniga tegishli kodni yozing
