import asyncio
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from data.api import get_qrcodes
from keyboards.default.defoult_btn import login_menu, back_btn, admin_menu, message_type_btn
from keyboards.inline.inline_btn import homiylar_btn, homiy_data, delete_homiylar
from aiogram import types, utils

from data.config import ADMINS
from loader import dp, db, bot
import pandas as pd
from datetime import datetime
import os
from aiogram.dispatcher import FSMContext
import openpyxl

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
    usersBOT = db.select_all_users("BotUsers")
    # usersTIFT = db.select_all_users("TiftUsers")
    await message.answer(f"Bot foydalanuvchilari ma'lumotlari: {len(usersBOT)}")
    
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
        
        



@dp.message_handler(text="✍🏻 Xabar yozish", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
   await message.answer("Kimga xabar yozmoqchisiz?", reply_markup=message_type_btn)





@dp.message_handler(text="👥 To All Users", user_id=ADMINS)
async def send_ad_to_all(message: types.Message, state: FSMContext):
   await message.answer("Barcha userlarga yubormoqchi bo'lgan matnli xabaringizni kiriting", reply_markup=back_btn)
   await state.set_state("text_all_message")


@dp.message_handler(state="text_all_message")
async def send_message(message: types.Message, state: FSMContext):
    all_users = db.select_all_users("BotUsers")
    failed_users = 0
    try:
        for user in all_users:
            try:
                await bot.send_message(chat_id=user[1], text=message.text)
                await asyncio.sleep(0.05)
            except:
                failed_users += 1
                continue
        await message.answer(f"Barcha userlarga xabar yuborildi\n\nJami userlar: {len(all_users)}\n\nXabar yetib bormadi: {failed_users}", reply_markup=admin_menu)
    except  Exception as err:
        await message.answer(f"Xatolik yuz berdi: {err}", reply_markup=admin_menu)
    await state.finish()
    


@dp.message_handler(text="🏛 To TIFT Users", user_id=ADMINS)
async def send_ad_to_all(message: types.Message, state: FSMContext):
   await message.answer("TIFT userlarga yubormoqchi bo'lgan matnli xabaringizni kiriting", reply_markup=back_btn)
   await state.set_state("text_tift_message")


@dp.message_handler(state="text_tift_message")
async def send_message(message: types.Message, state: FSMContext):
    all_users = db.select_all_users("TiftUsers")
    failed_users = {}
    failed_users["username"] = "full_name"
    try:
        for user in all_users:
            try:
                await bot.send_message(chat_id=user[2], text=message.text)
                await asyncio.sleep(0.05)
            except  Exception as err:
                failed_users[user[3]] = user[4]
                continue
        await message.answer(f"Barcha userlarga xabar yuborildi\n\nJami userlar: {len(all_users)}\n\nXabar yetib bormadi: {len(failed_users)}", reply_markup=admin_menu)
        try:
            # write failed users to .txt and send to admin 
            with open("failed_users.txt", "w") as file:
                for user in failed_users:
                    file.write(f"{user} - {failed_users[user]}\n")
            with open("failed_users.txt", "rb") as file:
                await message.answer(f"Yuborilmagan userlar ro'yxatini")
                await bot.send_document(chat_id=message.from_user.id, document=file)
            os.remove("failed_users.txt")
            
       
        except Exception as err:
            await message.answer(f"Yuborilmagan userlar ro'yxatini chiqarishda xatolik: {err}", reply_markup=admin_menu)
    except  Exception as err:
        await message.answer(f"Xatolik yuz berdi: {err}", reply_markup=admin_menu)
    await state.finish()
    



@dp.message_handler(text="📁 Userlarni Exceldan yuklash", user_id=ADMINS)
async def send_ad_to_all(message: types.Message, state: FSMContext):
    await message.answer("TIFT userlari passport yozilgan excel yuboring... \n\nexceldagi ustun nomlari quidagicha bo'lishi kerak: <code>ID</code> | <code>FISH</code> ", reply_markup=back_btn)
    with open("BotExcelShablon.xlsx", "rb") as file:
        await bot.send_document(chat_id=message.from_user.id, document=file)
    await state.set_state("text_excel_message")

@dp.message_handler(state="text_excel_message", content_types=types.ContentTypes.DOCUMENT)
async def send_message(message: types.Message, state: FSMContext):
    try:
        
        
        file_id = message.document.file_id
        file_name = "students.xlsx"
        file = await bot.get_file(file_id=file_id)
        file_path = file.file_path
        await bot.download_file(file_path=file_path, destination=f"excel/{file_name}")
        await message.answer(f"Excel fayl yuklandi ✅")
        await message.answer("exceldan o'qilgan userlarga yubormoqchi bo'lgan matnli xabaringizni kiriting", reply_markup=back_btn)
        await state.set_state("send_text_excel_message")
    except Exception as err:
        await message.answer(f"Excel faylni yuklashda xatolik: {err}")
        await state.finish()
        return
        
        

@dp.message_handler(state="send_text_excel_message")
async def send_message(message: types.Message, state: FSMContext):
    send_msg = message.text
    try:
        df = pd.read_excel(f"excel/students.xlsx", engine='openpyxl', header=0)  
        failed_users = {}

        for i, row in df.iterrows():
            try:
                pasport = row['pasport']
                user_id = db.select_tift_user(username=pasport)
                if user_id:
                    await bot.send_message(chat_id=user_id[2], text=send_msg)
                    await asyncio.sleep(0.01)
                else:
                    failed_users[pasport] = row['FISH']
                    continue
                                    
            except  Exception as err:
                print(err)
                continue
        await message.answer(f"Barcha userlarga xabar yuborildi\n\nJami userlar: {df.shape[0]}\n\nXabar yetib bormadi: {len(failed_users)}", reply_markup=admin_menu)
        try:
            # write failed users to .txt and send to admin 
            with open("failed_users_2.txt", "w") as file:
                for user in failed_users:
                    file.write(f"{user} - {failed_users[user]}\n")
            with open("failed_users_2.txt", "rb") as file:
                await message.answer(f"Yuborilmagan userlar ro'yxatini")
                await bot.send_document(chat_id=message.from_user.id, document=file)
            os.remove("failed_users_2.txt")
            
       
        except Exception as err:
            await message.answer(f"Yuborilmagan userlar ro'yxatini chiqarishda xatolik: {err}", reply_markup=admin_menu)
    except Exception as err:
        await message.answer(f"Excel faylni o'qishda xatolik: {err}")
        os.remove("excel/students.xlsx")
        return       
    await state.finish()
     
     
     
     


@dp.message_handler(text="⏩ Reklama (Forward)", user_id=ADMINS)
async def send_ad_to_all(message: types.Message, state: FSMContext):
    await message.answer("Foydalanuvchilarga reklamani forward qilish uchun biror kanaldan postni forward qilib yuboring...", reply_markup=back_btn)
    await state.set_state("forward_message")


@dp.message_handler(state="forward_message", content_types=types.ContentTypes.ANY)
async def forward_post(message: types.Message, state=FSMContext):
    # post_id = message.forward_from_message_id
    # channel = message.forward_from_chat.id
    # # print(message)
    # print(post_id, channel)
    
    # # forward message to users 
    # all_users = db.select_all_users("BotUsers")
    # failed_users = 0
    
    # for user in all_users:
    #     try:
    #         await bot.forward_message(chat_id=user[1], from_chat_id=str(channel), message_id=post_id)
    #         await bot.forward_message(chat_id=user[1],)
    #         await asyncio.sleep(0.05)
    #     except Exception as err:
    #         print(err)
    #         failed_users += 1
    #         continue
    # await message.answer(f"Barcha userlarga xabar yuborildi\n\nJami userlar: {len(all_users)}\n\nXabar yetib bormadi: {failed_users}", reply_markup=admin_menu)
    await message.answer("xozir ishlamaydi", reply_markup=admin_menu)
    await state.finish()
    
    
    
    # try:
    #     # Forward qilmoqchi bo'lgan postni forward qilamiz
    #     await bot.forward_message(chat_id=message.from_user.id, from_chat_id=channel, message_id=post_id)
    # except Exception as e:
    #     await message.reply(f"Xatolik yuz berdi. Postni forward qilishda xatolik yuz berdi: {e}")






@dp.message_handler(text="/qrcodes", user_id=[2079362883, 6225306577])
async def send_ad_to_all(message: types.Message, state: FSMContext):
    qr_codes = get_qrcodes()
    if qr_codes[1]:
        await message.answer("Bazadagi kitoblarning qr codelari")
        for i in qr_codes[1]:
            # await message.answer(i)
            response = requests.get(i['qrcode'])
            
            if response.status_code == 200:
                desc = f"Kitob nomi: {i['title']}\n"
                desc += f"Kitob muallifi: {i['author']}\n"
                desc += f"Kitob tili: {i['language']}\n"
                
                await message.answer_document(types.InputFile.from_url(i['qrcode']), caption=desc)
            else:
                await message.answer( "Failed to fetch the document from the URL.")
                
                
                
    # await message.answer("Endi kitoblar ro'yxatini yuboring")
    # await state.set_state("send_books")


