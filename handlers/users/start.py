import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.api import login_user

from data.config import ADMINS
from loader import dp, db, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):    
    await message.answer("Xush kelibsiz!")




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
        
        if not user:
            username = req['username']
            full_name = req['full_name']
            token = req['token']
            role = req['role']
            db.add_tift_user(user_id=user_id, username=username, full_name=full_name, role=role, token=token)
            await message.answer(f"{req['full_name']} - tizimga muvaffaqiyatli bog'landingiz ✅")
        else:
            username = req['username']
            full_name = req['full_name']
            token = req['token']
            role = req['role']
            db.update_tift_user(user_id=user_id, username=username, full_name=full_name, role=role, token=token)
            await message.answer(f"{req['full_name']} - sifatida tizimga kirdingiz ✅")
            


@dp.message_handler(Command("logout"))
async def logout_user(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = db.select_tift_user(user_id=user_id)
    db.logout_token(token=None, user_id=user_id)
    await message.answer(f"{user[3]} -  tizimdan muvaffaqiyatli chiqdingiz")
    