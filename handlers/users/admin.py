import asyncio
from aiogram.dispatcher.filters.builtin import CommandStart
from keyboards.default.defoult_btn import login_menu, back_btn, admin_menu
from keyboards.inline.inline_btn import homiylar_btn, homiy_data, delete_homiylar
from aiogram import types, utils

from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from datetime import datetime
import os
from aiogram.dispatcher import FSMContext


@dp.message_handler(CommandStart(), user_id=ADMINS)
async def bot_start(message: types.Message):
    user_id = message.from_user.id    
    await message.answer("Xush kelibsiz Admin!", reply_markup=login_menu(user='admin',tg_id=user_id))

@dp.message_handler(state="*",text ="🔙 Ortga", user_id=ADMINS)
async def input_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id   
    await state.finish()
    await message.answer(f"Asosiy sahifa",reply_markup=login_menu(user="admin",tg_id=user_id))
    

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
    users = db.select_all_users()
    await message.answer(f"Bot foydalanuvchilari ma'lumotlari: {len(users)}")



@dp.message_handler(text="⚜️ All Channels (Groups)", user_id=ADMINS)
async def bot_homiylari_func(message: types.Message):
    await message.answer("Majburiy a'zolik kanallari", reply_markup=types.ReplyKeyboardRemove())
    channels = db.select_all_channels()
    if channels:
            
        text = "<b>📣 Homiylar  ro'yxati:</b>\n\n"
        tr = 1
        for chanel in channels:
            text += f"<b>📣 {tr} - {chanel[1]}</b>\n"
            text += f"<b>ID:</b> {chanel[0]}\n"
            text += f"<b>Username:</b> {chanel[2]}\n"
            text += f"<b>Link:</b> {chanel[3]}\n\n"
            text += f"<b>Join users:</b> {chanel[4]}\n\n"
            tr += 1
        await message.answer(text, reply_markup=homiylar_btn)
    else:
        await message.answer("Homiy kanallar mavjud emas", reply_markup=admin_menu)
        
@dp.callback_query_handler(text="main_menu", user_id=ADMINS)
async def change_lang_(query: types.CallbackQuery):     
    await query.message.delete()
    await query.message.answer("Admin Panel", reply_markup=admin_menu)
     
        
@dp.callback_query_handler(text="minus_list", user_id=ADMINS)
async def delete_homiylar_list(query: types.CallbackQuery):
    await query.message.delete()
    channels = db.select_all_channels()
    if channels:
        text = "<b>📣 Homiylar  ro'yxati:</b>\n\n"
        tr = 1
        for chanel in channels:
            text += f"{tr}. {chanel[1]}\n"
            tr += 1
        text += "\nO'chirmoqchi bo'lgan homiylarni tanlang."
        await query.message.answer(text=text, reply_markup=delete_homiylar(channels))
    else:
        await query.message.answer("Homiy kanallar mavjud emas", reply_markup=admin_menu)
        
        
  
@dp.callback_query_handler(text="back_btn", user_id=ADMINS)
async def change_lang_(query: types.CallbackQuery):     
    await query.message.delete()
    await bot_homiylari_func(query.message)

@dp.callback_query_handler(homiy_data.filter(action='delete'), user_id=ADMINS)
async def change_lang_(query: types.CallbackQuery, callback_data: dict):
    del_id = callback_data['id']
    
    db.delete_channel(channel_id=del_id)
    await query.answer("Homiylar ro'yxatidan o'chirildi ")
    
    await query.message.answer("Homiylar ro'yxatidan o'chirildi ✅", reply_markup=admin_menu)
    await delete_homiylar_list(query)

    

@dp.message_handler(text="➕ Add Channels (Groups)", user_id=ADMINS)
async def get_all_users(message: types.Message, state=FSMContext):
    await message.answer("Birinchi navbatda botni kanalga qo'shing.")
    await message.answer("Kanaldan biror postni forward qiling, \nyoki kanal id sini yuboring (-100....) \nyoki username sini yuboring ( misol uchun:  @mychannel )", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("add_channel")
    
  
@dp.message_handler(state="add_channel", user_id=ADMINS, content_types=types.ContentTypes.ANY)
async def send_ad_to_all(message: types.Message, state = FSMContext):
    print(message)
    try:
        if message.text and message.entities and message.entities[0].type == "mention":
            channel_username = message.text
            channel = await bot.get_chat(channel_username)
            channel_id = channel['id']
            channel_name = channel['title']
            channel_link = await channel.export_invite_link()
            
            text = f"<b>ID:</b> {channel_id}\n"
            text += f"<b>Name:</b> {channel_name}\n"
            text += f"<b>Username:</b> {channel_username}\n"
            text += f"<b>Link:</b> {channel_link}\n"
            text += f"\n<code>Homiylar ro'yxatiga qo'shildi</code> ✅\n"
            db.add_channel(channel_id=channel_id, username=channel_username, channel_name=channel_name, channel_link=channel_link)
            await message.answer(text, reply_markup=admin_menu)
            
        elif message.text and message.text.startswith("-100") and message.text[1:].isdigit():
            channel = await bot.get_chat(message.text)
            channel_id = channel['id']
            channel_name = channel['title']
            channel_username = channel['username'] if channel['username'] else channel_id
            channel_link = channel['invite_link']
            
            text = f"<b>ID:</b> {channel_id}\n"
            text += f"<b>Name:</b> {channel_name}\n"
            text += f"<b>Username:</b> @{channel_username}\n"
            text += f"<b>Link:</b> {channel_link}\n"
            text += f"\n<code>Homiylar ro'yxatiga qo'shildi</code> ✅\n"
            db.add_channel(channel_id=channel_id, username=channel_username, channel_name=channel_name, channel_link=channel_link)
            await message.answer(text, reply_markup=admin_menu)

        elif message.forward_from_chat:
            channel_id = message.forward_from_chat.id
            channel_name = message.forward_from_chat.title
            channel_username = message.forward_from_chat.username if message.forward_from_chat.username else channel_id
            channel = await bot.get_chat(channel_id)
            channel_link = channel['invite_link']
            
            text = f"<b>ID:</b> {channel_id}\n"
            text += f"<b>Name:</b> {channel_name}\n"
            text += f"<b>Username:</b> @{channel_username}\n"
            text += f"<b>Link:</b> {channel_link}\n"
            text += f"\n<code>Homiylar ro'yxatiga qo'shildi</code> ✅\n"
            db.add_channel(channel_id=channel_id, username=channel_username, channel_name=channel_name, channel_link=channel_link)
            await message.answer(text, reply_markup=admin_menu)
            
        else:
            await message.answer("Nimadir xato ketti")
    except utils.exceptions.Unauthorized:
        await message.answer("Botni Kanal yoki guruhga qo'shilganligiga va admin ekanligiga ishonch hosil qiling", reply_markup= admin_menu)
    except Exception as err:
        await message.answer(f"Nomalum xatolik: {err}", reply_markup= admin_menu)
    
    await state.finish()
        
        

   
# @dp.message_handler(text="➖ Kanal o'chirish", user_id=ADMINS)
# async def send_ad_to_all(message: types.Message, state = FSMContext):
#     try:
#         await message.answer("Majburiy a'zolik kanallari", reply_markup=ReplyKeyboardRemove())
#         channels = db.select_all_channels()
#         text = "Qaysi kanallarni majburiy a'zolikdan olib tashlamoqchisiz:\n\n"
#         text += "📣 Kanallar ro'yxati:\n\n"
#         tr = 1
#         # print(channels)
#         for chanel in channels:
#             text += f"📣 {tr} - {chanel[1]}\n📣 Link: {chanel[2]}\n\n"
#             tr += 1
#         await message.answer(text, reply_markup=inline_channel_btn(channels))
            
        
    
#         await state.set_state("delete_channels")
#     except:
#         await message.answer("Majburiy a'zolik kanallari xatolik sodir boldi", reply_markup=admin_main_2)
        
    


# @dp.callback_query_handler(text="back_wars",state="delete_channels")
# async def change_(call: CallbackQuery, state=FSMContext):
#     await call.message.delete()
#     await state.finish()
#     await call.message.answer("Bosh menu 2", reply_markup=admin_main_2)
        
     
# @dp.callback_query_handler(state="delete_channels")
# async def golibni_aniqlash_war(call: CallbackQuery, state=FSMContext):
#     await call.message.delete()
#     try:
        
            
#         chanel = await bot.get_chat(call.data)
#         # print(chanel)
#         id = chanel.id
#         db.delete_channel(id)
#         invite_link = await chanel.export_invite_link()
#         name = chanel.full_name
        

#         text = f"Name: {name}\n"
#         text += f"Link: {invite_link}\n"
#         text += f"\nO'chirildi ✅ \n"
        
#         await call.message.answer(text)   
        
#     except Exception as err:
#         await call.message.answer(f"Nimadur xato ketti : {err}")  
         
#     await state.finish()
#     await call.message.answer("Bosh menu 2", reply_markup=admin_main_2)
#         ##################




@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    users = db.select_all_users()
    for user in users:
        user_id = user[0]
        await bot.send_message(chat_id=user_id, text="@SariqDev kanaliga obuna bo'ling!")
        await asyncio.sleep(0.05)   

# @dp.message_handler(text="/cleandb", user_id=ADMINS)
# async def get_all_users(message: types.Message):
#     db.delete_users()
#     await message.answer("Baza tozalandi!")