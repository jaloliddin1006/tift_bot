import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.api import login_user

from data.config import ADMINS
from loader import dp, db, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.defoult_btn import login_menu
from keyboards.inline.inline_btn import language_btn, lang_code



@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    if user:
        isUser = True  
    else:
        isUser = False
    await message.answer("Xush kelibsiz!", reply_markup=login_menu(user=isUser))
    # all = db.select_user_all_data(telegram_id=message.from_user.id)
    # await message.answer(all)



@dp.message_handler(Command("login"))
async def input_login(message: types.Message, state: FSMContext):
    await message.answer("LMS tizimiga kirishingiz uchun LOGIN yuboring\n")
    await state.set_state("login")


@dp.message_handler(state="login")
async def input_password(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text)
    await message.answer("Parol: ")
    await state.set_state("password")




@dp.message_handler(state="password")
async def login_user_func(message: types.Message, state: FSMContext):
    await state.update_data(password=message.text)
    
    data = await state.get_data()
    req = login_user(data['login'], data['password'])
    await state.finish()
    
    if req == 500:
        await message.answer("❌ Login yoki Parol noto'g'ri kiritilgan.")
    else:     
        user_id = message.from_user.id   
        user = db.select_tift_user(user_id = user_id)
        if req['role'] in ["teacher", "student", "admin"]:
            lms_id = req['id']
            username = req['username']
            full_name = req['full_name']
            token = req['token']
            role = req['role']
            
            if not user:
            
                db.add_tift_user(lms_id=lms_id, user_id=user_id, username=username, full_name=full_name, role=role, token=token)
                await message.answer(f"{req['full_name']} - tizimga muvaffaqiyatli bog'landingiz ✅",reply_markup=login_menu(user=True))
            else:
                db.update_tift_user(lms_id=lms_id, user_id=user_id, username=username, full_name=full_name, role=role, token=token)
                await message.answer(f"{req['full_name']} - sifatida tizimga kirdingiz ✅",reply_markup=login_menu(user=True))
        else:
            await message.answer("Siz uchun ushbu botning vazifalari to'g'ri kelmaydi. ", reply_markup=login_menu())


@dp.message_handler(Command("logout"))
async def logout_user(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.select_tift_user(user_id=user_id)
    db.logout_token(token=None, user_id=user_id)
    await message.answer(f"{user[3]} -  tizimdan muvaffaqiyatli chiqdingiz")
    
    
    
    
    
    
@dp.message_handler(text="🌐 Tilni o'zgartirish")
async def change_lang(message: types.Message):
    await message.answer("O'zingizga qulay tilni tanglang \n  //"+"-"*15+"\nВыберите язык, который вам удобен\n", reply_markup=language_btn)
 


@dp.callback_query_handler(lang_code.filter(action='set'))
async def change_lang_(query: types.CallbackQuery, callback_data: dict):
    lang = callback_data['language']
    db.update_lang(lang, query.from_user.id)
    await query.answer("til o'zgartirildi ")
    await query.message.answer("til o'zgartirildi", reply_markup=login_menu(1))
    await query.message.delete()


