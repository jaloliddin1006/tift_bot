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

# def shahar_btn_yasash(shaharlar_data):
# 	# print(call_1)


# 	shaharlar_btn = InlineKeyboardMarkup(row_width=2)

# 	for key, value in shaharlar_data.items():
# 	    shaharlar_btn.insert(InlineKeyboardButton(text=key, callback_data=value))
#     return shaharlar_btn



