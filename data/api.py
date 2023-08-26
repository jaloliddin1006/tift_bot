import requests
import json

# BASE_URL = "http://jaloliddin1006.jprq.live/api/v1"
# BASE_URL = "http://husanibragimov.jprq.live/api/v1"

BASE_URL = "http://127.0.0.1:8000/api/v1"
# http://127.0.0.1:8000/api/v1/users/me/
# login/?username=dekan1&password=Pass!123
def login_user(username, password):
    url = f"{BASE_URL}/login/"
    data = {
                "username": username,
                "password": password,
                # "is_bot": True,
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

    # data_ = json.loads(response.text)[0]
    # is_user = False
    # for i in data_:
    #     if i["user_id"] == user_id:
    #         is_user = True
    #         break
    #
    # if not is_user:
    #     data = {
    #         "username": username,
    #         "name": name,
    #         "user_id": user_id,
    #     }
    #     post = requests.post(url=url, data=data)
    #     return "Bazaga qo'shildi"
    # return "Foydalanuvchi mavjud"

# def get_me_func(token):
#     url = f"{BASE_URL}/users/me/"
   


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