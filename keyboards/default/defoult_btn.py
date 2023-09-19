from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from handlers.users.help import IsTiftUser

def login_menu(user=False, tg_id=None):
    loginusermenu = []
    if user == "admin":
        if IsTiftUser(tg_id) and IsTiftUser(tg_id) != "disable":
            loginusermenu =   [
                    KeyboardButton(text="👤 Admin menu"), 
                    KeyboardButton(text="👤 User menu"), 
                ]
        else:
            loginusermenu =   [
                    KeyboardButton(text="👤 Admin menu"), 
                ]
    elif user: 
        loginusermenu =   [
                KeyboardButton(text="👤 User menu"), 
            ]
        
    menu_btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="ℹ️ Ma'lumot olish"), 
                KeyboardButton(text="🎓 Talabalar bo'limi"),           
            ],
            [
                KeyboardButton(text="📨 Xabar yozish"), 
            ],
            loginusermenu,
            [
                # KeyboardButton(text="🌐 Tilni o'zgartirish"),           
                
            ],
            [
                # KeyboardButton(text="👨🏻‍💻️ Muallif"), 
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limlardan birini tanlang"

    )
    return menu_btn


about_btn = ReplyKeyboardMarkup(
    keyboard=[
        
        [
            KeyboardButton(text="🏛 TIFT haqida"),              
            ],
        [
            KeyboardButton(text="⚙️ LMS Tizimi haqida"), 
             ],
        [
            KeyboardButton(text="ℹ️ Qo'shimcha ma'lumot olish"), 
            ],
        [
            KeyboardButton(text="🔙 Ortga"), 
            ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Ma'lumot olish uchun"

)


def user_menu_func(user):
    if user == "student":
        user_menu = ReplyKeyboardMarkup(
            keyboard=[
                
                [
                    KeyboardButton(text="📚 Meni Fanlarim"),              
                    KeyboardButton(text="📆 Dars jadvalim"), 
                    ],
                [
                    KeyboardButton(text="⚠️ Topshirilmagan vazifalarim"), 
                    ],
                [
                    KeyboardButton(text="🎓 Individual shaxsiy reja"), 
                    KeyboardButton(text="⚖️ GPA"), 
                    ],
                 [
                    KeyboardButton(text="ℹ️ Ma'lumotlarim"), 
                    KeyboardButton(text="🎞 Video Qo'llanma"), 
                    ],
                
                [
                    KeyboardButton(text="🔙 Ortga"), 
                    ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Talaba Menusi"

        )
    elif user == "teacher":
         user_menu = ReplyKeyboardMarkup(
            keyboard=[
                
                [
                    KeyboardButton(text="🎞 Video Qo'llanma"), 
                    ],
                [
                    KeyboardButton(text="👥 Meni Guruhlarim"),              
                    KeyboardButton(text="📅 Dars jadvalim"), 
                    ],
                [
                    KeyboardButton(text="⚠️ Tekshirilmagan vazifalarim"), 
                    ],
                [
                    KeyboardButton(text="🔙 Ortga"), 
                    ],
            ],
            resize_keyboard=True,
            input_field_placeholder="O'qituvchi Menusi"

        )
    elif user == "tutor":
         user_menu = ReplyKeyboardMarkup(
            keyboard=[
                
                [
                    KeyboardButton(text="👥 Meni Guruhlarim"),              
                    ],
                [
                    KeyboardButton(text="🔙 Ortga"), 
                    ],
            ],
            resize_keyboard=True,
            input_field_placeholder="O'qituvchi Menusi"

        )
    else:
                 user_menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="🔙 Ortga"), 
                    ],
            ],
            resize_keyboard=True,
            input_field_placeholder="O'qituvchi Menusi"

        )
        
    return user_menu

admin_menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="✍🏻 Xabar yozish"), 
                    KeyboardButton(text="⏩ Reklama (Forward)"), 
                    ],
                  [
                    KeyboardButton(text="👯‍♂️ All Users"), 
                    KeyboardButton(text="📊 Statistika"), 
                    ],
                [
                    KeyboardButton(text="⚜️ All Channels (Groups)"), 
                    KeyboardButton(text="➕ Add Channels (Groups)"), 
                    ],
                [
                    KeyboardButton(text="🔙 Ortga"), 
                    ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Admin Menusi"

        )
message_phone = ReplyKeyboardMarkup(
        keyboard=[
            
            [
                KeyboardButton(text="☎️ Telefon raqamni ulashish", request_contact=True),              
                ],
            [
                KeyboardButton(text="🔙 Ortga"), 
                ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Phone number is required"

    )
back_btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🔙 Ortga"), 
                ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Your full name ..."

    )
# https://t.me/eduuz/10199
student_part_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📃 Shartnomani yuklab olish"), 
        ],
        [
            KeyboardButton(text="💳 Ta'lim kreditlari"), 
        ],
        
        [
            KeyboardButton(text="ℹ️ Ichki tartib qoidalar"),           
            KeyboardButton(text="👨🏻‍🎓 Iqtidorli talabalar bo'limi"),           
            
        ],
         [
                KeyboardButton(text="🔙 Ortga"), 
                ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Talabalar bo'limi"

)

student_contract = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📂 Excel faylni yuklash"), 
        ],
         [
                KeyboardButton(text="🔙 Ortga"), 
                ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Shartnoma olish uchun"

)


message_type_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📁 Userlarni Exceldan yuklash"), 
        ],
        
        [
            KeyboardButton(text="👥 To All Users"),           
            KeyboardButton(text="🏛 To TIFT Users"),           
            
        ],
         [
                KeyboardButton(text="🔙 Ortga"), 
                ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Kimga xabar yozmoqchisiz?"

)



def eslatmani_yoqish(aa):
    eslatma = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=f"{aa}")   
            ],
            [
                KeyboardButton(text="🔙 Ortga"), 
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Eslatmani to'g'irlash bo'limi"
    )
    return eslatma
