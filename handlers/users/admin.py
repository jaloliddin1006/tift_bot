import asyncio
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.defoult_btn import login_menu, back_btn, admin_menu

from aiogram import types

from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from datetime import datetime
import os


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start(message: types.Message):
    user_id = message.from_user.id    
    await message.answer("Xush kelibsiz Admin!", reply_markup=login_menu(user='admin'))



@dp.message_handler(text="👤 Admin menu", user_id=ADMINS)
async def get_all_users(message: types.Message):
    await message.answer("👤 Admin Menu", reply_markup=admin_menu)



@dp.message_handler(text="📊 Statistika", user_id=ADMINS)
async def get_all_users(message: types.Message):
    usersBOT = db.select_all_users("BotUsers")
    usersTIFT = db.select_all_users("TiftUsers")
    txt = f"Bot foydalanuvchilari:  <b>{len(usersBOT)}</b> nafar\n"
    txt += f"Shundan TIFT userlari: <b>{len(usersTIFT)}</b> nafar \n"
    await message.answer(txt)


@dp.message_handler(text="👯‍♂️ All Users", user_id=ADMINS)
async def get_all_users(message: types.Message):
    # usersBOT = db.select_all_users("BotUsers")
    # usersTIFT = db.select_all_users("TiftUsers")
    
    # df = pd.DataFrame(usersBOT, columns=['id', 'telegram_id', 'name', 'user_name', 'language', 'join_date'])
    # excel_filename = f"Bot_Users.xlsx"
    # excel_writer = pd.ExcelWriter(excel_filename)
    # df.to_excel(excel_writer, sheet_name='Sheet1', index=False)
    # # excel_writer.save()
    # # excel_writer.close()
    # await message.answer(df)
    # df2 = pd.DataFrame(usersTIFT, columns=['id', 'lms_id', 'user_id', 'username', 'full_name', 'role', 'join_date', 'update_date', 'token'])
    # excel_filename2 = f"Tift_Users.xlsx"
    # excel_writer2 = pd.ExcelWriter(excel_filename, engine='xlsxwriter')
    # df2.to_excel(excel_writer2, sheet_name='Sheet1', index=False)
    # # excel_writer2.save()
    # # excel_writer2.close()

    # with open(excel_filename, 'rb') as excel_file:
    #     await bot.send_document(message.chat.id, excel_file)

    # # with open(excel_filename2, 'rb') as excel_file:
    # #     await bot.send_document(message.chat.id, excel_file)

    # # # Faylni o'chirish
    # # os.remove(excel_filename)
    # # os.remove(excel_filename2)
    await message.answer("Bot foydalanuvchilari ma'lumotlari")



@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@SariqDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)   

@dp.message_handler(text="/cleandb", user_id=ADMINS)
async def get_all_users(message: types.Message):
    db.delete_users()
    await message.answer("Baza tozalandi!")