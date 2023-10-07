import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from handlers.users.echo import subscribe_channel_func
from keyboards.inline.inline_btn import check_member_button
from aiogram.types import ReplyKeyboardRemove
from data.config import ADMINS
# from data.config import CHANNELS
from utils.misc import subscription
from loader import bot, db

class AuthMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: types.Message, data: dict):
        # Bu joyda foydalanuvchi haqida ma'lumotlar olish kerak.
        user_id = message.from_user.id
        CHANNELS = db.select_all_channels()[0]

        # Foydalanuvchi haqida olingan ma'lumotlar bilan majburiy a'zo qilishingizni tekshirish kerak.
        is_member = await  subscription.check(user_id=user_id,
                                                channel=CHANNELS[0])

        if not is_member:
            await message.answer("Siz kanallarga majburiy a'zo emasligingiz uchun bu botni ishlatishingiz mumkin emas.")
            return await bot.leave_chat(message.chat.id)
    

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):  
        
        try: 
                
            CHANNELS = db.select_all_channels()
            
            if update.message:
                user = update.message.from_user.id
                # if update.message.text in ['/start', '/help']:
                #     return
            elif update.callback_query:
                user = update.callback_query.from_user.id
                if update.callback_query.data == "check_subs":
                    return
            else:
                return
            join_channel = []

            result = "Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:\n"
            final_status = True
            for channel_id in CHANNELS:
                # print(channel_id)
                # print(await bot.get_chat(channel_id[0]))
                status = await subscription.check(user_id=user,
                                                channel=channel_id[0])
                # print(status)
                final_status *= status
                channel = await bot.get_chat(channel_id[0])
                    
                # status = await bot.get_chat_member(channel, update.message.from_user.id)
                invite_link = await channel.export_invite_link()
                
                if not status:
                    channel_info = [invite_link, channel.title, 0]
                else:
                    channel_info = [invite_link, channel.title, 1]
                    # aa += 1
                join_channel.append(channel_info)
                
                if not status:
                    # invite_link = await channel.export_invite_link()
                    result += (f"       👉 <a href='{invite_link}'>{channel.title}</a>\n")

            if not final_status:
                await subscribe_channel_func(update.message, result, join_channel)
                return await bot.leave_chat(update.message.chat.id)
            
                # await update.message.answer("Kanallarga to'liq obuna bo'ling", reply_markup=ReplyKeyboardRemove())
                # await update.message.answer(result, disable_web_page_preview=True, reply_markup=check_member_button(join_channel))
            
                # raise CancelHandler()
        except Exception as err:
            print("=======================", err)
            # await db.delete_channels()
            
            await bot.send_message(ADMINS[0], f"Error:  {err}")