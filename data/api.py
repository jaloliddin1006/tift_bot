import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1"


def create_user(username, name, user_id):
    url = f"{BASE_URL}/bot-users"
    response = requests.get(url=url)
    data_ = json.loads(response.text)[0]
    is_user = False
    for i in data_:
        if i["user_id"] == user_id:
            is_user = True
            break

    if not is_user:
        data = {
            "username": username,
            "name": name,
            "user_id": user_id,
        }
        post = requests.post(url=url, data=data)
        return "Bazaga qo'shildi"
    return "Foydalanuvchi mavjud"


def create_feedback(body, user_id):
    url = f"{BASE_URL}/feedbacks"
    if body and user_id:
        post = requests.post(url=url, data={
            "user_id": user_id,
            "body": body
        })
        return "Adminga yuborildi"
    return "Nimadir xato ketdi"


# create_user("jaloliddin1006", "Jaloliddin", "234234234")
print(create_feedback("yaxshi cabar keldi", "132133"))