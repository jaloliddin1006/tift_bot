from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from data.config import GroupID
from handlers.users.help import IsTiftUser
from keyboards.default.defoult_btn import message_phone, login_menu, back_btn
from loader import dp, db, bot
import uuid



    
@dp.message_handler(text = "❓ Bugalteriyaga oid savollar")
async def input_login(message: types.Message, state: FSMContext):
    await state.update_data(type="bugalteriya")
    
    user = db.select_new_message(telegram_id=message.from_user.id)
    if user:
        await message.answer("Bugalteriyaga oid qandaydir savollaringiz yoki bugalteriyaga bilan bo'g'liq muammoingiz bo'lsa yozishingiz mumkin. Xabaringizni to'liq qilib bitta xabarda ko'rsating \n\n<i>(ruxsat:  video, audio, rasm, matn)</i>", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("message")
    else:
        await message.answer("Ism Familiyangizni yuboring", reply_markup=back_btn)
        await state.set_state("full_name")

# @dp.message_handler(state="bugalteriya_message", content_types=types.ContentType.ANY)
# async def get_bugalteriya_message(message: types.Message, state: FSMContext):
#     user_id = message.from_user.id
#     await message.forward(chat_id='-1002087698683')
#     await message.answer(f"Xabaringiz bugalteriya xodimlariga yuborildi ✅, \nXabaringizga tez orada javob beramiz.", reply_markup=login_menu(user=IsTiftUser(user_id)))
#     await state.finish()

@dp.message_handler(text = '📨 Xabar yozish')
async def message_write(message: types.Message, state: FSMContext):
    await state.update_data(type="message")
    user = db.select_new_message(telegram_id=message.from_user.id)
    if user:
        await message.answer("Murojaatingizni bitta xabarda to'liq aks ettiring(rasm, audio, video, matn)", reply_markup=types.ReplyKeyboardRemove())
        await state.set_state("message")
    else:
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
    nick_name = message.from_user.full_name
    # await state.update_data(phone=phone)
    data = await state.get_data()
    full_name = data['full_name']
    db.add_new_message(telegram_id=message.from_user.id, full_name=full_name, nick_name=nick_name, phone=phone)
    # phone = data['phone']
    await message.answer(f"Xabar/Ariza matningizni kiriting\n (Xabaringizni to'liq qilib bitta xabarda yoritib bering):", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state("message")

@dp.message_handler(state="phone")
async def get_phone(message: types.Message, state: FSMContext):
    await message.answer("Quidagi tugma yordamida telefon raqamingizni yuboring👇", reply_markup=message_phone)
    await state.set_state("phone")
    


@dp.message_handler(state="message", content_types=types.ContentType.ANY)
async def send_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id  
    type_ = await state.get_data()
    type_ = type_['type']
    if type_ == "message":
        await message.forward(chat_id=GroupID, message_thread_id=828)
    else:
        await message.forward(chat_id='-1002087698683')
        
    db.update_new_message(nick_name=message.from_user.full_name, user_id=user_id)
    
    await message.answer(f"Xabaringiz yuborildi ✅, \nXabaringizga tez orada javob beramiz.", reply_markup=login_menu(user=IsTiftUser(user_id)))
    await state.finish()