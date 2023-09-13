from aiogram import executor
from handlers.users.notifications import scheduler
from loader import dp, db
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)
    # scheduler.start()

    # Ma'lumotlar bazasini yaratamiz:
    try:
        db.create_table_users()
        db.create_table_tiftusers()
        # db.drop_message()
        db.create_table_messages()
        # db.drop_channels()
        db.create_table_channels()
        pass
    except Exception as err:
        print(err)
        # pass


    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
