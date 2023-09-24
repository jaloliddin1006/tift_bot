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


homiylar_btn = InlineKeyboardMarkup(
	inline_keyboard=[
	[
		InlineKeyboardButton(text="⚙️ Homiylarni kamaytirish", callback_data="minus_list"),
		
	],
 	[
		InlineKeyboardButton(text="🔼 Bosh menu", callback_data="main_menu"),
		
	],
])


homiy_data = CallbackData('vote', 'action', 'id')  # post:<action>:<language>

def delete_homiylar(channels):
    
    channels_check = InlineKeyboardMarkup(row_width=1)
    tr = 1
    for channel in channels:
        channels_check.insert(InlineKeyboardButton(text=f"{tr}. {channel[1]}", callback_data=homiy_data.new(action='delete', id=f'{channel[0]}')))
        tr += 1
    channels_check.add(InlineKeyboardButton(text=f"🔙 Ortga", callback_data=f"back_btn"))
        
    return channels_check



# def show_books_categories_btn(books_category):
    
#     channels_check = InlineKeyboardMarkup(row_width=2)
#     tr = 1
#     for channel in channels:
#         channels_check.insert(InlineKeyboardButton(text=f"{tr}. {channel[1]}", callback_data=homiy_data.new(action='delete', id=f'{channel[0]}')))
#         tr += 1
#     channels_check.add(InlineKeyboardButton(text=f"🔙 Ortga", callback_data=f"back_btn"))
        
#     return channels_check