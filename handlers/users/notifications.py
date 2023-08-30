from aiogram import types
from aiogram.dispatcher import FSMContext
from data.api import check_user
from handlers.users.start import IsTiftUser
from keyboards.default.defoult_btn import message_phone, login_menu, back_btn
from loader import dp, db, bot
import asyncio
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from data.api import get_notifications


scheduler = AsyncIOScheduler()

async def send_notifications(token ):
    noti = get_notifications(token=token)
    txt = ""
    if noti:
        for no in noti:
            # time_ = datetime.datetime.strptime(str(no['time_']), "%Y-%m-%dT%H:%M:%S" )
            n = f"<b>👥 Patok:</b> {no['patok_name']}\n"
            n += f"<b>📗 Fan:</b> {no['science']}\n"
            n += f"<b>📝 Topshiriq:</b> {no['title']}\n"
            n += f"<b>🕔 Deadline:</b> {no['time_']}\n"
            n += f"<b>⏳ Qoldi:</b> {no['deadline']['day']} kun {no['deadline']['hours']} soat\n"
            txt += n
            txt += "----------\n"
    else:
        return []
    # await message.answer("⚠️ Topshirilmagan vazifalarim: \n\n"+txt)
    notification = "⚠️ Topshirilmagan vazifalarim: \n\n"+txt
    return notification
    

async def get_and_send_notifications():
    users = db.select_all_users("TiftUsers")
    
    for user in users:
        token = user[8]
        user_id = user[2]
        if token:
            if token == "disable":
                # print("bildirishnoma o'chirilgan", user_id)
                pass 
            else:
                get_user = check_user(token)
                if get_user != 200:
                    db.logout_token(user_id=user_id, token=None)
                    await bot.send_message(chat_id=user_id,text = "LMS bilan aloqa uzuldi, endi siz bildirishnomalarni boshqa ololmaysiz. \nIltimos qaytadan tizimga kiring. 👉 /login", reply_markup=login_menu(user=False))
                else:
                    send_data = await send_notifications(token)
                    if send_data:
                        await bot.send_message(chat_id=user_id, text=send_data)
                        await asyncio.sleep(0.01)
                        # print("yuboriladi")
                    else:
                        # print("data bo'sh")
                        pass
        else:
            await bot.send_message(chat_id=user_id,text = "LMS bilan aloqa uzuldi, endi siz bildirishnomalarni boshqa ololmaysiz. \nIltimos qaytadan tizimga kiring. 👉 /login", reply_markup=login_menu(user=False))
        


scheduler.add_job(get_and_send_notifications, CronTrigger(hour=8, minute=00)) 
scheduler.add_job(get_and_send_notifications, CronTrigger(hour=18, minute=00))  


@dp.message_handler(text = "1")
async def input_password(message: types.Message, state: FSMContext):
    await get_and_send_notifications()






