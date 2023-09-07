import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from data.api import get_contract, login_user
from aiogram.types import InputFile
from data.config import ADMINS
from handlers.users.help import IsTiftUser
import aiohttp

from loader import dp, db, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.defoult_btn import login_menu, about_btn
from keyboards.inline.inline_btn import language_btn, lang_code
from keyboards.default.defoult_btn import student_part_btn


@dp.message_handler(text = "🔙 Ortga")
async def bot_start(message: types.Message):
    user_id = message.from_user.id

    await message.answer("Asosiy menu", reply_markup=login_menu(user=IsTiftUser(user_id)))





@dp.message_handler(text = "ℹ️ Ma'lumot olish")
async def bot_start(message: types.Message):

    await message.answer("Qanday ma'lumot olmoqchisiz", reply_markup=about_btn)

about_uni = """

TOSHKENT XALQARO MOLIYAVIY BOSHQARUV VA TEXNOLOGIYALAR UNIVERSITETI

2022-yilda tashkil etilgan Toshkent Xalqaro moliyaviy boshqaruv va texnologiyalar universiteti yuqori sifatli taʼlim mutaxassislarini tayyorlashga yoʻnaltirilgan nodavlat oliy ta’lim muassasasi hisoblanadi. Universitet Vazirlar Mahkamasi huzuridagi Ta’lim sifatini nazorat qilish davlat inspeksiyasi tomonidan oliy ta’lim sohasida faoliyat yuritish huquqini beruvchi 046621-sonli litsenziyaga ega. Bizning oliy maqsadimiz, bu - ta'lim jarayonining barcha talabalariga innovatsion ta’lim dasturlarini taqdim etish hisoblanadi. Universitet bitiruvchilari kelajakda innovator, tadbirkor, ijodkor va ishbilarmon bo‘lib yetishadilar. Oliy ta’lim sohasida katta tajribaga ega bo’lgan professor-o‘qituvchilar tarkibi boy va zamonaviy bilim beradilar. Toshkent xalqaro moliyaviy boshqaruv va texnologiyalar universiteti talabalar uchun talabgir, keng ta’lim yo’nalishlarini taklif qiladi.
"""
@dp.message_handler(text = "🏛 TIFT haqida")
async def bot_start(message: types.Message):

    await message.answer(about_uni, reply_markup=about_btn)


@dp.message_handler(text = "⚙️ LMS Tizimi haqida")
async def bot_start(message: types.Message):

    await message.answer("⚙️ LMS Tizimi haqida ma'lumotlar", reply_markup=about_btn)


@dp.message_handler(text = "ℹ️ Qo'shimcha ma'lumot olish")
async def bot_start(message: types.Message):

    await message.answer("ℹ️ Qo'shimcha ma'lumot olish aloqa contactlari\n\n+998 78 113 29 99 \n\nhttps://t.me/tiftuzbot ", reply_markup=about_btn)





@dp.message_handler(text ="🎓 Talabalar bo'limi")
async def input_password(message: types.Message):
    await message.answer(f"Talabalar bo'limi. Talabalar tuchun kerakli hujjatlar.",reply_markup=student_part_btn)
    
    

@dp.message_handler(text ="📃 Shartnomani yuklab olish")
async def input_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user = IsTiftUser(tg_id=user_id)
    if user:
        # student = db.select_tift_user(user_id=user_id)
        # shartnoma = get_student_contract(student[-1])   #api chiqarilganda hujjatlarni api orqali olib keladi
        await message.answer("talaba shartnomasi yuboriladi, api chiqarilgandan so'ng...")
    else:
        # await message.answer(f"⚠️ Siz faqat TIFT talabasi bo'lgan taqdirda shartnomani yuklab olishingiz mumkin. Agar talaba bo'lsangiz tizim bilan bog'lanishingiz kerak: /login",reply_markup=student_part_btn)
        await message.answer("Shartnomani yuklab olish uchun Pasport seria va raqamingizni yuboring.", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("passport")
    
    

@dp.message_handler(state="passport")
async def input_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id   
    contracts = get_contract(message.text)
    if contracts:
        base_url = contracts["url"]
        await message.answer("Shartnomangizni quidagi link orqali yuklab olishingiz mumkin\n\n")
      
        for contract in contracts["data"]:

            doc = f"{base_url[0:-7]}{contract['file']}"
            if requests.get(doc).status_code == 200:
                text = f"          [📂 Yuklab olish  -  {contract['type']}]({doc}) \n\n" 
                await message.answer(text, parse_mode=types.ParseMode.MARKDOWN) 
            else:
                await message.answer("Shartnoma hozircha mavjud emas.")
    else:
        await message.answer("Passport seria raqami topilmadi. ")
    await state.finish()
    await message.answer(f"Asosiy sahifa",reply_markup=login_menu(user=IsTiftUser(user_id)))
    
    
    


@dp.message_handler(text ="💳 Ta'lim kreditlari")
async def input_password(message: types.Message):
    txt = """
    ❓Qaysi banklar taʼlim krediti ajratmoqda? Ular qanday shartlar asosida beriladi?

📹 Bu haqidagi batafsil maʼlumotni yuqoridagi videolavha orqali bilib olasiz.
"""
    # await bot.send_video(chat_id=message.from_user.id,  video="https://t.me/mamatmusayev_chat/19", caption=txt)
    await message.answer(f"https://t.me/eduuz/10199")
    
    
    
@dp.message_handler(text ="ℹ️ Ichki tartib qoidalar")
async def input_password(message: types.Message):
    # await bot.send_document(chat_id=message.from_user.id, document="https://t.me/mamatmusayev_uz/178")
    # await bot.send_document(chat_id=message.from_user.id, document="https://t.me/mamatmusayev_uz/180?single")
    await message.answer("Ma'lumotlar hozircha mavjud emas...")
    
    
    
@dp.message_handler(text ="👨🏻‍🎓 Iqtidorli talabalar bo'limi")
async def input_password(message: types.Message):
    txt = """
    📖Stipendiya turlari:

1️⃣ O‘zbekiston Respublikasi Prezidentining davlat stipendiyasi;
2️⃣ Abu Rayhon Beruniy;
3️⃣ Abu Ali ibn Sino;
4️⃣ Alisher Navoiy;
5️⃣ Mirzo Ulug‘bek;
6️⃣ Imom al-Buxoriy;
7️⃣ Islom Karimov nomidagi davlat stipendiyalari.

🇺🇿 Talabalarga tayinlash uchun belgilangan O‘zbekiston Respublikasi Prezidentining davlat stipendiyasi kvotasi (o‘n bitta) quyidagi ta’lim yo‘nalishlaridan har biri bo‘yicha bittadan stipendiya hisobidan bakalavriat va magistratura uchun alohida-alohida taqsimlanadi:

➖ qishloq va suv xo‘jaligi;
➖ texnika va informatika;
➖ sog‘liqni saqlash va ijtimoiy ta’minot;
➖ ijtimoiy-gumanitar va ijtimoiy fanlar;
➖ tabiiy fanlar;
➖ biznes va boshqaruv;
➖ pedagogika;
➖ madaniyat, san’at va sport;
➖ xorijiy tillar;
➖ huquq va xalqaro munosabatlar;
➖ jurnalistika.

🇺🇿 Nomdor davlat stipendiyalari
O‘zbekiston Respublikasi davlat oliy ta’lim muassasalarining bakalavriat bo‘yicha o‘qiyotgan oxirgi ikki kurs talabalariga tayinlanadi.
    """
    text = """
    ⚖️Huquqiy asos:
"O‘zbekiston iqtidorli yoshlarini taqdirlash va moddiy rag‘batlantirish to‘g‘risida" O‘zbekiston Respublikasi Vazirlar Mahkamasining
qarori
http://lex.uz//docs/-1399382

Rasmiy sayt: 
🌐 https://stipendiya.edu.uz/
Ariza yuborish: 
📩 https://stipendiya.edu.uz/login"""
    await message.answer(txt)
    await message.answer(text)
    await bot.send_document(chat_id=message.from_user.id, document="https://t.me/mamatmusayev_uz/181")
    
     