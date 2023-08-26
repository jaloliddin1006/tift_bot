import sqlite3

from aiogram import types
from data.api import login_user

from data.config import ADMINS
from loader import dp, db, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.defoult_btn import login_menu, about_btn, user_menu_func
from keyboards.inline.inline_btn import language_btn, lang_code



@dp.message_handler(text = "🔙 Ortga")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    if user:
        isUser = True  
    else:
        isUser = False
    await message.answer("Asosiy menu", reply_markup=login_menu(isUser))


@dp.message_handler(text = "👤 User menu")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    await message.answer("👤 User menu bo'limi", reply_markup=user_menu_func(user=user[5]))
    

@dp.message_handler(text = "📚 Meni Fanlarim")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    await message.answer("📚 Meni Fanlarim bo'limi")
    

@dp.message_handler(text = "📆 Dars jadvalim")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    await message.answer("📆 Dars jadvalim bo'limi")
    

@dp.message_handler(text = "⚠️ Topshirilmagan vazifalarim")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    await message.answer("⚠️ Topshirilmagan vazifalarim bo'limi")
    

@dp.message_handler(text = "🎓 Individual shaxsiy reja")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    await message.answer("🎓 Individual shaxsiy reja bo'limi")
    

@dp.message_handler(text = "⚖️ GPA")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    await message.answer("⚖️ GPA bo'limi")
    
