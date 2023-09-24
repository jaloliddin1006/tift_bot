import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.api import login_user

from data.config import ADMINS
from loader import dp, db, bot
from data.api import get_book
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.defoult_btn import login_menu, back_btn  
from keyboards.inline.inline_btn import language_btn, lang_code, check_member_button
from handlers.users.help import IsTiftUser



@dp.message_handler(CommandStart(), state="*")
async def bot_start(message: types.Message, state=FSMContext):
    if message.text == "/start":
        user_id = message.from_user.id    
        await message.answer("Xush kelibsiz!", reply_markup=login_menu(user=IsTiftUser(user_id)))
    else:
        book_slug = message.text.split(" ")[-1]
        book = get_book(book_slug)
      
        if book[1]:
            await message.answer_photo(types.InputFile.from_url(book[0]+book[1]['photo']), caption=f"<b>{book[1]['title']}</b>\n\n{book[1]['description']}", reply_markup=login_menu(user=IsTiftUser(message.from_user.id)))
            await message.answer_document(types.InputFile.from_url(book[0]+book[1]['file']), caption=f"<b>{book[1]['title']}</b>\n\n{book[1]['description']}", reply_markup=login_menu(user=IsTiftUser(message.from_user.id)))
    await state.finish()
    
    # all = db.select_user_all_data(telegram_id=message.from_user.id)
    # await message.answer(all)



# @dp.message_handler()
# async def bot_start(message: types.Message):
#     msgs = await message.answer("OK!")
#     msg = message
#     await bot.pin_chat_message(chat_id=msgs.chat.id, message_id=msgs.message_id, disable_notification=True)
#     # user_id = message.from_user.id 
    
#     # await bot.send_message(chat_id="@new_bot_test_group", text=message.text)
#     # await bot.send_message(chat_id="-1001704364861", message_thread_id="2704", text=message.text)
#     # await bot.send_message(chat_id="-1001704364861/2704", text="🔵🔵🔵sdfsdfsd🌀🌀🌀🌀sdfsdf🎮🎮🎮sdf    🔔")
#     # # await bot.send_message
    
#     await message.answer("OK!")
#     # all = db.select_user_all_data(telegram_id=message.from_user.id)
#     # await message.answer(all)


@dp.message_handler(Command("off"))
async def input_login(message: types.Message, state: FSMContext):
    try:
        db.logout_token(user_id=message.from_user.id, token="disable")
        await message.answer("LMS tizimidan keladigan bildirishnomalar o'chirildi va tizim bilan bo'g'lanish uzildi.\n\n Bildirishnomalarni yoqish uchun qaytadan 👉 /login qiling", reply_markup=login_menu(user=False))
    except:
        await message.answer("Bu funksiya faqat universitet xodimlari va talabalari uchun ishlaydi.")
    
@dp.message_handler(Command("on"))
async def input_login(message: types.Message, state: FSMContext):
    try:
        db.logout_token(user_id=message.from_user.id, token=None)
        await message.answer("Bildirishnomalarni yoqish uchun tizimga kiring. 👉 /login ", reply_markup=login_menu(user=False))
    except:
        await message.answer("Bu funksiya faqat universitet xodimlari va talabalari uchun ishlaydi.")
    
    
    
@dp.message_handler(Command("login"))
async def input_login(message: types.Message, state: FSMContext):
    await message.answer("LMS tizimiga kirishingiz uchun LOGIN yuboring\n", reply_markup=back_btn)
    await state.set_state("login")



@dp.message_handler(state="login", text ="🔙 Ortga")
async def input_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id   
    await state.finish()
    await message.answer(f"Asosiy sahifa",reply_markup=login_menu(user=IsTiftUser(user_id)))
    
    

@dp.message_handler(state="login")
async def input_password(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Parol: ")
    await state.set_state("password")




@dp.message_handler(state="password")
async def login_user_func(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.delete()
    data = await state.get_data()
    req = login_user(data['login'], data['password'])
    await state.finish()
    
    user_id = message.from_user.id   
    if req == 500:
        await message.answer("❌ Login yoki Parol noto'g'ri kiritilgan.", reply_markup=login_menu(user=IsTiftUser(user_id)))
    else:     
        user_id = message.from_user.id   
        user = db.select_tift_user(user_id = user_id)
    
        if req['role'] in ["teacher", "student", "tutor"]:
            lms_id = req['id']
            username = req['username']
            full_name = req['full_name']
            token = req['token']
            role = req['role']
            txt = f"Login: <b>{username} </b>\n"
            txt += f"Name: <b>{full_name}</b> \n"
            txt += f"Role: <b>{role} </b> "

            if not user:
            
                db.add_tift_user(lms_id=lms_id, user_id=user_id, username=username, full_name=full_name, role=role, token=token)
                msg = await message.answer(f"{txt} - sifatida tizimga muvaffaqiyatli bog'landingiz ✅",reply_markup=login_menu(user=IsTiftUser(user_id)))
            else:
                db.update_tift_user(lms_id=lms_id, user_id=user_id, username=username, full_name=full_name, role=role, token=token)
                msg = await message.answer(f"{txt} - sifatida tizimga kirdingiz ✅",reply_markup=login_menu(user=IsTiftUser(user_id)))

            await bot.pin_chat_message(chat_id=msg.chat.id, message_id=msg.message_id, disable_notification=False)
        else:
            await message.answer("Siz uchun ushbu botning vazifalari to'g'ri kelmaydi. ", reply_markup=login_menu())


@dp.message_handler(Command("logout"))
async def logout_user(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.select_tift_user(user_id=user_id)
    if not user or user[8] == "disable" or not user[8]:
        await message.answer("Siz tizimga ulanmagansiz.")
    else:
        db.logout_token(token=None, user_id=user_id)
        msg = await message.answer(f"{user[3]} -  tizimdan muvaffaqiyatli chiqdingiz",reply_markup=login_menu(user=False))
        await bot.pin_chat_message(chat_id=msg.chat.id, message_id=msg.message_id, disable_notification=False)
    
    
    
    
    
    
@dp.message_handler(text="🌐 Tilni o'zgartirish")
async def change_lang(message: types.Message):
    await message.answer("O'zingizga qulay tilni tanglang \n  //"+"-"*15+"\nВыберите язык, который вам удобен\n", reply_markup=language_btn)
 


@dp.callback_query_handler(lang_code.filter(action='set'))
async def change_lang_(query: types.CallbackQuery, callback_data: dict):
    lang = callback_data['language']
    db.update_lang(lang, query.from_user.id)
    await query.answer("til o'zgartirildi ")
    
    user_id = query.from_user.id
    await query.message.answer("til o'zgartirildi", reply_markup=login_menu(user=IsTiftUser(user_id)))
    await query.message.delete()


