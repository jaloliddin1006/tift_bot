# import sqlite


# def test():
#     db = sqlite.Database(path_to_db='../../data/main.db')
#     user = db.select_tift_user(user_id=973108256, role='student')
#     print(user)
#     # db.create_table_users()
#     # db.add_user(1, "One", "email", 'ru')
#     # db.add_user(2, "olim", "olim@gmail.com", 'uz')
#     # db.add_user(3, 1, 1)
#     # db.add_user(4, 1, 1)
#     # db.add_user(5, "John", "john@mail.com")

#     # users = db.select_all_users()
#     # print(f"Barcha fodyalanuvchilar: {users}")

#     # user = db.select_user(Name="John", id=5)
#     # print(f"Bitta foydalanuvchini ko'rish: {user}")



# test()


list_ = ['13000217417', '13000285018', '13000307587', '3000056707', '13000256412',
    '13000004510', '13000252319', '13000231839', '13000100782', '3000056794',]

from selenium import webdriver
driver = webdriver.Chrome()
import requests
for i in list_:
    response = requests.get(f"https://api.triumf-express.uz/media/pdfs/133/{i}.pdf")
    file_name = f'{i}.pdf'
    with open(file_name, 'wb') as f:
        f.write(response.content)