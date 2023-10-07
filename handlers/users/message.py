from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from data.config import GroupID
from handlers.users.help import IsTiftUser
from keyboards.default.defoult_btn import message_phone, login_menu, back_btn
from loader import dp, db, bot
import uuid


@dp.message_handler(text = '📨 Xabar yozish')
async def message_write(message: types.Message, state: FSMContext):
    await message.answer("Ism Familiyangizni yuboring", reply_markup=back_btn)
    await state.set_state("full_name")


@dp.message_handler(state="full_name", text ="🔙 Ortga")
async def input_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id   
    await state.finish()
    await message.answer(f"Asosiy sahifa",reply_markup=login_menu(user=IsTiftUser(user_id)))
    
    
@dp.message_handler(state="full_name")
async def get_full_name(message: types.Message, state: FSMContext):
    full_name = message.text
    await state.update_data(full_name=full_name)
    await message.answer(f"Telefon raqamingizni yuboring", reply_markup=message_phone)
    await state.set_state("phone")
    

@dp.message_handler(state="phone", text ="🔙 Ortga")
async def input_password(message: types.Message, state: FSMContext):
    user_id = message.from_user.id   
    await state.finish()
    await message.answer(f"Asosiy sahifa",reply_markup=login_menu(user=IsTiftUser(user_id)))
    

@dp.message_handler(state="phone", content_types=types.ContentType.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number    
    await state.update_data(phone=phone)
    await message.answer(f"Xabar/Ariza matningizni kiriting\n (Xabar matningizni to'liq qilib metta xabarda yoritib berin):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("message")

@dp.message_handler(state="phone")
async def get_phone(message: types.Message, state: FSMContext):
    await message.answer("Quidagi tugma yordamida telefon raqamingizni yuboring👇", reply_markup=message_phone)
    await state.set_state("phone")
    


@dp.message_handler(state="message")
async def send_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    data = await state.get_data()
    full_name = data['full_name']
    phone = data['phone']
    msg = message.text
    msg_id = uuid.uuid4().hex[:16]
    
    txt = f"User: {full_name}\n"
    txt += f"Phone: <code>{phone}</code>\n"
    txt += f"Message: {msg}\n"
    msg = db.add_message(user_id, full_name, msg_id)
    await message.answer(txt)
    if message.from_user.username:
        txt = f"Username: @{message.from_user.username}\n" + txt
    txt1 = f"ID: #{msg_id}#\n" + txt
    
    
    await bot.send_message(chat_id=GroupID, message_thread_id=2, text=txt1)
    await message.answer(f"Xabaringiz yuborildi ✅, \nXabaringizga tez orada javob beramiz.", reply_markup=login_menu(user=IsTiftUser(user_id)))
    await state.finish()