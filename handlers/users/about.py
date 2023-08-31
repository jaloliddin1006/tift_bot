import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from data.api import login_user

from data.config import ADMINS
from handlers.users.help import IsTiftUser

from loader import dp, db, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.defoult_btn import login_menu, about_btn
from keyboards.inline.inline_btn import language_btn, lang_code


@dp.message_handler(text = "🔙 Ortga")
async def bot_start(message: types.Message):
    user_id = message.from_user.id

    await message.answer("Asosiy menu", reply_markup=login_menu(user=IsTiftUser(user_id)))





@dp.message_handler(text = "ℹ️ Ma'lumot olish")
async def bot_start(message: types.Message):

    await message.answer("Qanday ma'lumot olmoqchisiz", reply_markup=about_btn)


@dp.message_handler(text = "🏛 TIFT haqida")
async def bot_start(message: types.Message):

    await message.answer("🏛 TIFT haqida ma'lumotlar", reply_markup=about_btn)


@dp.message_handler(text = "⚙️ LMS Tizimi haqida")
async def bot_start(message: types.Message):

    await message.answer("⚙️ LMS Tizimi haqida ma'lumotlar", reply_markup=about_btn)


@dp.message_handler(text = "ℹ️ Qo'shimcha ma'lumot olish")
async def bot_start(message: types.Message):

    await message.answer("ℹ️ Qo'shimcha ma'lumot olish aloqa contactlari ", reply_markup=about_btn)


