from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

admin_btn = InlineKeyboardMarkup(
	inline_keyboard=[
	[
		InlineKeyboardButton(text="📞 Admin bilan bog'lanish", url="https://t.me/Jaloliddin_Mamatmusayev"),
		# InlineKeyboardButton(text="Namangan", callback_data="Namangan"),
	],
])


lang_code = CallbackData('vote', 'action', 'language')  # post:<action>:<language>

language_btn = InlineKeyboardMarkup(
	inline_keyboard=[
	[
		InlineKeyboardButton(text="🇺🇿 UZ", callback_data=lang_code.new(action='set', language='uz')),
		InlineKeyboardButton(text="🇷🇺 RU", callback_data=lang_code.new(action='set', language='ru')),
	],
])



def check_member_button(channels):
    
    channels_check = InlineKeyboardMarkup(row_width=1)
    for channel in channels:
        if channel[2]==0:
            channels_check.insert(InlineKeyboardButton(text=f"{channel[1]}", url=f"{channel[0]}"))
        else:
            channels_check.insert(InlineKeyboardButton(text=f"✅{channel[1]}", url=f"{channel[0]}"))
    channels_check.add(InlineKeyboardButton(text=f"✅ Obunani tekshirish ✅ ", callback_data=f"check_subs"))
        
    return channels_check


