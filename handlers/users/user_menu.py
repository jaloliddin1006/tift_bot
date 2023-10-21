import datetime
import sqlite3

from aiogram import types
from data.api import get_notifications, get_student_schedule, get_student_sciences, get_teacher_groups, get_teacher_schedule, login_user, get_student, get_rating_notebook, get_video_source

from data.config import ADMINS
from loader import dp, db, bot
from handlers.users.help import IsTiftUser

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default.defoult_btn import login_menu, about_btn, user_menu_func
from keyboards.inline.inline_btn import language_btn, lang_code



@dp.message_handler(text = "🔙 Ortga")
async def bot_start(message: types.Message):
    user_id = message.from_user.id
    await message.answer("Asosiy menu", reply_markup=login_menu(user=IsTiftUser(user_id)))


@dp.message_handler(text = "👤 User menu")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    await message.answer("Kerakli bo'limni tanlang", reply_markup=user_menu_func(user=user[5]))
    
@dp.message_handler(text = "🎞 Video Qo'llanma")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)
    await message.answer(f"<b>{user[5]}</b> roliga tegishli video qo'llanma hozirda mavjud emas.")    
    # if user:
    #     video = get_video_source(user[8])
    #     # 
        
    #     await message.answer(video)
    

@dp.message_handler(text = "📚 Meni Fanlarim")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    token = user[8]
    data = get_student_sciences(token)
    
    if data:
        try:
            txt = f"🎓 <b>Talaba:</b> {data['student']}\n"
            sciences = "\n"
            for science in data['sciences']:
                part = f"\n📗<b>  Fan: {science['name']}</b>\n"
                part += f"🧮<b>  NB: </b>{science['nb_count']}\n"
                for group in science['groups']:
                    gr = f"     👥 <b>Guruh:</b> {group['name']}\n"
                    gr += f"     ✍🏻 <b>Turi:</b> {group['science_type']}\n"
                    gr += f"     👩‍🏫 <b>O'qituvchi:</b> {group.get('teacher')}\n\n"
                    part += gr
                sciences += part
                sciences += "\n"
            await message.answer("      📚 Meni Fanlarim\n"+txt+sciences)
        except:
            await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi(error)")
    else:
        await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi...")


@dp.message_handler(text = "📆 Dars jadvalim")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id) 
    token = user[8]
    data = get_student_schedule(token)
    # print("data: ", data)
    # sorted_data = sorted(data, key=lambda x: x['start'])
    
    if data:
        
        # Define a dictionary to map weekdays to their respective names in your language
        dayys = {
            'Monday': 'Dushanba',
            'Tuesday': 'Seshanba',
            'Wednesday': 'Chorshanba',
            'Thursday': 'Payshanba',
            'Friday': 'Juma',
            'Saturday': 'Shanba',
            'Sunday': 'Yakshanba'
        }

        ddy = {
            
            'Monday': {},
            'Tuesday': {},
            'Wednesday': {},
            'Thursday': {},
            'Friday': {},
            'Saturday': {},
            'Sunday': {}
            
        }

        # Initialize a dictionary to store lessons for Monday
        lessons_by_day = ddy.copy()
        for para in data['results']:
            
            for day in para['timetable']:
                # if day['weekday'] == 'Monday':
                lessons_by_day[day['weekday']][para['name']] = day['groups']

        # Print the formatted schedule for Monday
        # print("Dushanba kuniga tegishli fanlar:")
        week_schedule = ""
        for i,j in lessons_by_day.items():
            # if j['groups']:
            # print(f"{i} kuniga tegishli fanlar:")
            # print(j)
            daily_lesson = ""
            for para_num, groups in j.items():
                lesson = ""
                if groups:
                    start_time = next((para['start_time'] for para in data['results'] if para['name'] == para_num), '')
                    end_time = next((para['end_time'] for para in data['results'] if para['name'] == para_num), '')
                    
                    lesson += f"{para_num} - para : {start_time} - {end_time}\n"
                    for group in groups:
                        name = group['group']
                        room = group['room']
                        science = group['science']
                        group_type = group['group_type']
                        lesson += f"👥 <b>Patok:</b> {name}\n"
                        lesson += f"🏢 <b>Xona:</b> {room}\n"
                        lesson += f"📗 <b>Fan:</b> {science}\n"
                        lesson += f"✍🏻 <b>Turi:</b> {group_type}\n\n"
                    # print(lesson)
                if lesson:
                    daily_lesson += lesson
            if daily_lesson:
                week_schedule += f"{dayys[i]} kuniga tegishli fanlar:\n{daily_lesson}\n"
        await message.answer("       📆 Dars jadvalim \n\n"+week_schedule)

    else:
        await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi...")

# {'results': {'monday': [{'id': 3, 'group': 'INM-001', 'room': 'A-302', 'group_type': 'lecture', 'group_science': 'Iqtisodiyot nazariyasi', 'updated_at': '2023-08-25T16:48:50.670631+05:00', 'created_at': '2023-08-25T16:48:50.670678+05:00', 'weekday': 'monday', 'types': 'full', 'para': 3, 'semester': 2}], 'tuesday': [], 'wednesday': [], 'thursday': [], 'friday': [{'id': 4, 'group': 'IUMM-001-L1', 'room': 'A-300', 'group_type': 'practical', 'group_science': 'Iqtisodchilar uchun matematika', 'updated_at': '2023-08-25T20:23:44.791512+05:00', 'created_at': '2023-08-25T20:23:44.791549+05:00', 'weekday': 'friday', 'types': 'full', 'para': 1, 'semester': 2}], 'saturday': []}}
@dp.message_handler(text = "⚠️ Topshirilmagan vazifalarim")
async def student_dedline(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    token = user[8]
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
        txt = "Vazifalar hali mavjud emas."
    await message.answer("⚠️ Topshirilmagan vazifalarim: \n\n"+txt)
    

@dp.message_handler(text = "🎓 Individual shaxsiy reja")
async def bot_start(message: types.Message):
    await message.answer("🎓 Individual shaxsiy reja bo'limi", reply_markup=user_menu_func("student"))
    user = db.select_tift_user(user_id=message.from_user.id)  
    token = user[8]
    raiting_notebook = get_rating_notebook(token)
    if raiting_notebook:
        txt = f"🎓 <b>Talaba:</b> {raiting_notebook['student']}\n"
        semesters = ""
        for semester in raiting_notebook['sciences']:
            sciences = f"\n<b>   {semester['semester']} - Semester</b>\n\n"
        
            for science in semester['sciences']:
                part = f"📗<b>  Fan: </b>{science['science']}\n"
                part += f"💳<b>  Kredit: </b>{science['credit']}\n"
                part += f"📈<b>  Baho: </b>{science['gpa'] if science['gpa'] else 0}\n\n"
                sciences += part
            # semesters += sciences
            await message.answer(txt+sciences)
        # await message.answer(txt+semesters)
    
    else:
        await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi...")



@dp.message_handler(text = "⚖️ GPA")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  

    token = user[8]
    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkyMjc3MDkwLCJpYXQiOjE2OTIxOTA2OTAsImp0aSI6IjMwZmI3NzRjMmJkYTQzN2M4MGU0N2M3MDY5MThmYWQ1IiwidXNlcl9pZCI6Nn0.JONI2_lkAZ2NJ2jIVH5MqFiGBn2cPugHAkurYLOdmgQ"

    data = get_student(token=token)
    if data: 
        txt = f"🎓 <b>Talaba:</b> {data['full_name']}\n"
        txt += f"🏛 <b>Yo'nalish:</b> {data['direction']}\n"
        txt += f"⚖️ <b>GPA:</b> {data['gpa']}"
        await message.answer(f"<b>⚖️ GPA bo'limi:</b>\n\n{txt}", reply_markup=user_menu_func("student"))
    else:
        await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi...")


@dp.message_handler(text = "ℹ️ Ma'lumotlarim")
async def bot_start(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    token = user[8]
    data = get_student(token=token)
    if data:
        txt = f"🎓 <b>Talaba:</b> {data['full_name']}\n"
        txt += f"🏛 <b>Yo'nalish:</b> {data['direction']}\n"
        txt += f"💲 <b>Kontrak miqdori:</b> {data['direction_contract']}\n"
        txt += f"🔺 <b>Kurs:</b> {data['course_number']}\n"
        txt += f"👥  <b>Guruh:</b> {data['academic_group']}\n"
        txt += f"⚖️ <b>GPA:</b> {data['gpa']}"
        await message.answer(f"<b>🎓 Talaba haqida ma'lumot:</b>\n\n{txt}", reply_markup=user_menu_func("student"))
    else:
        await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi...")



######################################################
###############  teacher  ############################
######################################################

@dp.message_handler(text = "👥 Meni Guruhlarim")
async def teacher_groups(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    token = user[8]
    data = get_teacher_groups(token=token)
    if data:
        groups = ''
        for group in data:
            txt = f"<b>👥 Guruh:</b> {group['name']}\n"
            txt += f"<b>🎓 Talabalar:</b> {group['students']}\n"
            txt += f"<b>📓 Fan:</b> {group['science']}\n"
            txt += f"<b>✍🏻 Turi:</b> {group['science_type']}\n\n"
            groups += txt
        await message.answer(groups)
        
    else:
        await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi...")
    
@dp.message_handler(text = "📅 Dars jadvalim")
async def bot_start(message: types.Message):    
    user = db.select_tift_user(user_id=message.from_user.id) 
    token = user[8]
    data = get_teacher_schedule(token)
    sorted_data = sorted(data, key=lambda x: x['start'])

    if data:
        dayys = {
            'Monday': 'Dushanba',
            'Tuesday': 'Seshanba',
            'Wednesday': 'Chorshanba',
            'Thursday': 'Payshanba',
            'Friday': 'Juma',
            'Saturday': 'Shanba',
            'Sunday': 'Yakshanba'
        }
        day = ""
        week = ""
        for table in sorted_data:
            today = datetime.datetime.strptime(str(table['start']), "%Y-%m-%dT%H:%M:%S" )
            
            weekday = dayys[today.strftime('%A')]
            room = table['title'].split()[-1]
            group = table['title'].split()[-2]
            para = table['para']
            science = " ".join(table['title'].split(" ")[0:-3])
            
            schedule_table = ""
            
            if week == weekday:
                pass
            else:
                week = weekday
                schedule_table += f"              <b> ||    {week}     ||</b>\n"
            schedule_table += f"⏲ <b>Para:</b> {para}\n"
            schedule_table += f"🏢 <b>Xona:</b> {room}\n"
            schedule_table += f"👥 <b>Patok:</b> {group}\n"
            schedule_table += f"📗 <b>Fan:</b> {science}\n\n"
            
            day += schedule_table 
        
        
        await message.answer("       📆 Dars jadvalim \n\n"+day)
    else:
        await message.answer("Biroz kuting tez orada ma'lumotlar qo'shiladi...")
        

@dp.message_handler(text = "⚠️ Tekshirilmagan vazifalarim")
async def teacher_groups(message: types.Message):
    user = db.select_tift_user(user_id=message.from_user.id)  
    token = user[8]
    noti = get_notifications(token=token)
    txt = ""
    if noti:
        for no in noti:
            time_ = no['time_']
             
            n = f"<b>👥 Patok:</b> {no['patok_name']}\n"
            n += f"<b>📗 Fan:</b> {no['science']}\n"
            n += f"<b>📝 Topshiriq:</b> {no['title']}\n"
            n += f"<b>🕔 Deadline:</b> {time_}\n"
            n += f"<b>⏳ Qoldi:</b> {no['deadline']['day']} kun {no['deadline']['hours']} soat\n"
            txt += n
            txt += "----------\n"
    else:
        txt += "vazifalar hali mavjud emas"
    await message.answer("⚠️ Tekshirilmagan vazifalarim: \n\n"+txt)
    
