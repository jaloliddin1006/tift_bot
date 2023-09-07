from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "🏃 Botni ishga tushurish"),
            types.BotCommand("help", "ℹ️ Yordam"),
            # types.BotCommand("login", "➕ LMS tizimiga ulanish"),
            # types.BotCommand("logout", "➖ LMS tizimidan chiqish"),
            # types.BotCommand("off", "🔕 Bildirishnomalarni o'chirish"),
            # types.BotCommand("on", "🔔 Bildirishnomalarni yoqish"),
        ]
    )
