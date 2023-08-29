from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def login_menu(user=False):
    loginusermenu = []
    if user:
        loginusermenu =   [
                KeyboardButton(text="👤 User menu"), 
            ]
        
    menu_btn = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="ℹ️ Ma'lumot olish"), 
                KeyboardButton(text="🌐 Tilni o'zgartirish"),           
            ],
            [
                KeyboardButton(text="📨 Xabar yozish"), 
            ],
            loginusermenu,
            [
                KeyboardButton(text="👨🏻‍💻️ Muallif"), 
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
                    ],
                
                [
                    KeyboardButton(text="🔙 Ortga"), 
                    ],
            ],
            resize_keyboard=True,
            input_field_placeholder="Talaba Menusi"

        )
    else:
         user_menu = ReplyKeyboardMarkup(
            keyboard=[
                
                [
                    KeyboardButton(text="👥 Meni Guruhlarim"),              
                    ],
                [
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
    return user_menu


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
