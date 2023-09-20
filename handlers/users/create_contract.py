from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from keyboards.default.defoult_btn import student_part_btn
from data.api import create_contract
import time
import requests
import pandas as pd



@dp.message_handler(text ="📂 Excel faylni yuklash", state="passport")
async def input_password(message: types.Message, state: FSMContext):
    users = [2079362883, 6225306577, 827825058]
    user_id = message.from_user.id
    if user_id in users or message.from_user.username and message.from_user.username == "te1monov":
        with open("CreateContractTemplate.xlsx", "rb") as file:
            await message.answer_document(document=file)
        await message.answer("Excel faylni yuklang.", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("contract_excel")
    else:
        await message.answer("Sizga ruxsat mavjud emas", reply_markup=student_part_btn)
        await state.finish()
        
        
        
async def create_student_contract_func(file_name):
    df = pd.read_excel(f"excel/{file_name}", engine='openpyxl', header=0) 
    students = []
    for i, row in df.iterrows():
        student={
            "ID":row["ID"],
            "F.I.Sh.":row["F.I.Sh."],
            "pasport":row["pasport"],
            "Ta'lim yo'nalishi":row["speciality"],
            "Ta'lim turi":row["study_type"],
            "edu_level_uz":row["degree"],
            "period":row["period"],
            "kurs":row["kurs"],
            "Kontraktning umumiy summasi":row["Kontraktning umumiy summasi"],
            "Tug'ilgan sana va yil":str(row["Tug'ilgan sana va yil"]),
            "address":row["address"],
            "Telefoni":row["Telefoni"],
            
        }
        students.append(student)
        # print(student)
        
        
    contracts = create_contract(students)
    return contracts



@dp.message_handler(state="contract_excel", content_types=types.ContentTypes.DOCUMENT)
async def send_message(message: types.Message, state: FSMContext):
    try:      
        file_id = message.document.file_id
        file_name = "studentContract.xlsx"
        file = await bot.get_file(file_id=file_id)
        file_path = file.file_path
        await bot.download_file(file_path=file_path, destination=f"excel/{file_name}")
        await message.answer(f"Excel fayl yuklandi ✅")
        
        time_msg = await message.answer("Biroz kutib turing ...  ⏳ ")
        
        contracts = await create_student_contract_func(file_name)
        
        # for i in range(2):
        #     if i == 0:
        #         pass
                
        #     time_msg = await bot.edit_message_text(f"Biroz kutib turing ...  ⌛️ ", chat_id=message.from_user.id, message_id=time_msg.message_id)
        #     time.sleep(0.5)
        #     time_msg = await bot.edit_message_text(f"Biroz kutib turing ...  ⏳ ", chat_id=message.from_user.id, message_id=time_msg.message_id)
        
        await time_msg.delete()
            
        try:
            if contracts:
                base_url = contracts["url"]
                await message.answer("Shartnomangizni quidagi link orqali yuklab olishingiz mumkin\n\n")

            
                for contract in contracts["data"]:
                
                    doc = f"{base_url[0:-7]}{contract['file']}"
                   
                    if requests.get(doc).status_code == 200:
                        text = f"          [📂 Yuklab olish | {contract['file'].split('/')[-1]}]({doc}) \n\n" 
                        await message.answer(text, parse_mode=types.ParseMode.MARKDOWN) 
                    else:
                        await message.answer("Shartnoma hozircha mavjud emas.")
            else:
                await message.answer("Passport seria raqami topilmadi. ")
        except Exception as err:
            await message.answer(f"Error: {err}")
        await state.finish()
        
    except Exception as err:
        await message.answer(f"Excel faylni yuklashda xatolik: {err}")
        await state.finish()
    await message.answer(f"Talabalar bo'limi. Talabalar tuchun kerakli hujjatlar.",reply_markup=student_part_btn)
        
        