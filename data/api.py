import requests
import json

# BASE_URL = "http://jaloliddin1006.jprq.live/api/v1"
# BASE_URL = "http://husanibragimov.jprq.live/api/v1"
# BASE_URL = "http://oqdevpy.jprq.live/api/v1"
# BASE_URL = "http://127.0.0.1:8000/api/v1"
# BASE_URL = "https://api.lms-edu.uz/api/v1"
BASE_URL = "https://api.tift.uz/api/v1"


def login_user(username, password):
    url = f"{BASE_URL}/login/"
    data = {
                "username": username,
                "password": password,
                "is_bot": True,
            }
    response = requests.post(url=url, data=data)
    if response.status_code == 200:
        data = json.loads(response.text)
        token = data['data']['tokens']['access']


        get_me_url = f"{BASE_URL}/users/me/"
        get_me_header = {
            'Authorization': f"Bearer {token}",
        }
        get_me = requests.get(get_me_url, headers=get_me_header)
        get_data = json.loads(get_me.text)['data']
        id = get_data['id']
        username = get_data['username']
        role = get_data['role'][0]
        full_name = get_data['first_name']  + " " if get_data['first_name'] else " "
        full_name += get_data['last_name']  + " " if get_data['last_name'] else " "
        full_name += get_data['middle_name'] if get_data['middle_name'] else " "
        # print(full_name)
        
        return {'id':id, 'username':username, 'full_name':full_name, 'role':role, 'token':token} 
    else:
        return 500

def check_user(token):
    url = f"{BASE_URL}/users/me/"
    get_me_header = {
            'Authorization': f"Bearer {token}",
        }
    get_me = requests.get(url, headers=get_me_header)
    return get_me.status_code


def get_student(token):
    url = f"{BASE_URL}/student/student-detail/"
    get_me_header = {
            'Authorization': f"Bearer {token}",
        }
    try:
        get_me = requests.get(url, headers=get_me_header)
        get_data = json.loads(get_me.text)['result']
        full_name = get_data['full_name']
        direction = get_data['direction']
        birthday = get_data['birthday']
        course_number = get_data['course_number']
        academic_group = get_data['academic_group']
        tutor = get_data['tutor']
        rating_notebook = get_data['rating_notebook']
        try:
            gpa = get_data['gpa', 0] 
        except:
            gpa = 0
            
        context = {
            'full_name':full_name,
            'direction':direction,
            'birthday':birthday,
            'course_number':course_number,
            'academic_group':academic_group,
            'tutor':tutor,
            'rating_notebook':rating_notebook,
            'gpa':gpa,
        }
        return context
    except:
        return None


def get_rating_notebook(token):
    url = f"{BASE_URL}/student/rating-notebook/"
    get_me_header = {
            'Authorization': f"Bearer {token}",
        }
    get_me = requests.get(url, headers=get_me_header)
    get_data = json.loads(get_me.text)
    student = get_data['student']
    sciences = get_data['results']
    context = {
        'student':student,
        'sciences':sciences,
        
    }
    return context


def get_student_schedule(token):
    url = f"{BASE_URL}/student/schedule-table/"
    para_url = f"{BASE_URL}/bot/para/"
    get_header = {
            'Authorization': f"Bearer {token}",
        }
    get_ = requests.get(url, headers=get_header)
    get_data = json.loads(get_.text)
 
    return get_data



def get_student_sciences(token):
    url = f"{BASE_URL}/student/my-sciences" ## last semester
    get_me_header = {
            'Authorization': f"Bearer {token}",
        }
    get_me = requests.get(url, headers=get_me_header)
    get_data = json.loads(get_me.text)
    student = get_data['full_name']
    sciences = get_data['science']
    context = {
        'student':student,
        'sciences':sciences,
        
    }
    return context


def get_notifications(token):
    url = f"{BASE_URL}/student/notifications/" ## last 7 days
    get_me_header = {
            'Authorization': f"Bearer {token}",
        }
    get_me = requests.get(url, headers=get_me_header)
    if get_me.status_code == 200:
        get_data = json.loads(get_me.text)
        return get_data
    return []





def get_teacher_groups(token):
    url = f"{BASE_URL}/teacher/groups-list/" ## last semester
    get_me_header = {
            'Authorization': f"Bearer {token}",
        }
    get_me = requests.get(url, headers=get_me_header)
    get_data = json.loads(get_me.text)

    return get_data


def get_teacher_schedule(token):
    url = f"{BASE_URL}/teacher/schedule/" ## last semester
    get_me_header = {
            'Authorization': f"Bearer {token}",
        }
    get_me = requests.get(url, headers=get_me_header)
    get_data = json.loads(get_me.text)
    return get_data

def get_video_source(token):
    # url = f"{BASE_URL}/teacher/schedule/" ## last semester
    # get_me_header = {
    #         'Authorization': f"Bearer {token}",
    #     }
    # get_me = requests.get(url, headers=get_me_header)
    # get_data = json.loads(get_me.text)
    video = "https://www.youtube.com/watch?v=-penHWNfvVI"
    return video





def get_contract(passport):
    url = f"{BASE_URL}/bot/getstudentcontract/?passport={passport}"
    get_me = requests.get(url)
    if get_me.status_code == 200:
        get_data = json.loads(get_me.text)
        return {'data':get_data, "url":BASE_URL}
    return None



def create_contract(data):
    url = f"{BASE_URL}/bot/create-contract/"
    data = {
        "students":data
    }
    # print(data)
    get_me = requests.get(url, json=data)
    # print(get_me.text)
    if get_me.status_code == 200:
        get_data = json.loads(get_me.text)
        return {'data':get_data, "url":BASE_URL}
    return None





# def create_feedback(body, user_id):
#     url = f"{BASE_URL}/feedbacks"
#     if body and user_id:
#         post = requests.post(url=url, data={
#             "user_id": user_id,
#             "body": body
#         })
#         return "Adminga yuborildi"
#     return "Nimadir xato ketdi"


# create_user("jaloliddin1006", "Jaloliddin", "234234234")
# print(create_feedback("yaxshi cabar keldi", "132133"))

# a = login_user("admin", "123")
# print(a)




