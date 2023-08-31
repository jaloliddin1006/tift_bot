from loader import dp, db, bot
from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from keyboards.inline.inline_btn import check_member_button
from keyboards.default.defoult_btn import login_menu
from handlers.users.help import IsTiftUser

from data.config import ADMINS



@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    try:
        CHANNELS = db.select_all_channels()
        
        await call.message.delete()
        join_channel = []
        aa = 0
        for channel in CHANNELS:
            chat = await bot.get_chat(channel[0])
            invite_link = await chat.export_invite_link()
            status = await bot.get_chat_member(channel[0], call.from_user.id)
            
            if status['status'] == 'left':
                channel_info = [invite_link, chat.title, 0]
            else:
                channel_info = [invite_link, chat.title, 1]
                aa += 1
            join_channel.append(channel_info)
                
        if aa != len(CHANNELS):   
            await call.message.answer(f"""{call.from_user.full_name} kanallarga to'liq obuna bo'ling""", reply_markup=ReplyKeyboardRemove())
            await call.message.answer(f"Quyidagi kanallarga obuna bo'ling: \n",
                            
                            reply_markup=check_member_button(join_channel),
                            disable_web_page_preview=True)
        else:
            await call.message.answer("Xush kelibsiz! Botdan foydalanishingiz mumkin", reply_markup=login_menu(user=IsTiftUser(call.from_user.id)))
    except Exception as err:
        print(err,"=============================================")


        # db.delete_channels()
        
        await bot.send_message(ADMINS[0], "Ushbu bot qaysidir kanaldan chiqarib yuborildi, Botning kanalda adminligiga to'laqonli ishonch hosil qiling. Xavfsizlik uchun barcha ulangan kanallar majburiy a'zolik ro'yxatidan o'chirildi. ")
