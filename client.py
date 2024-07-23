import requests
#
# response = requests.post("http://127.0.0.1:5000/user/",
#                          json={'name': 'user_2'},
#                          )
# print(response.status_code)
# print(response.json())

# response = requests.post("http://127.0.0.1:5000/adv/",
#                          json={'title': 'adv_5', 'content': 'asdfg', 'user_id': 5},
#                          )
# print(response.status_code)
# print(response.json())


# response = requests.get("http://127.0.0.1:5000/user/5/")
#
# print(response.status_code)
# print(response.json())


# response = requests.patch("http://127.0.0.1:5000/user/5/",
#                           json={"name": "user_5"})
#
# print(response.status_code)
# print(response.json())

# response = requests.patch("http://127.0.0.1:5000/adv/15/",
#                           json={"title": "adv_5", "content": "content", "user_id": 5})
#
# print(response.status_code)
# print(response.json())

# response = requests.get("http://127.0.0.1:5000/adv/11/")
#
# print(response.status_code)
# print(response.json())

response = requests.delete("http://127.0.0.1:5000/adv/13/")

print(response.status_code)
print(response.json())


# response = requests.get("http://127.0.0.1:5000/user/1/")
#
# print(response.status_code)
# print(response.json())


# response = requests.post(
#     "http://127.0.0.1:5000/user/",
#     json={"password": "1234"},
# )
# print(response.status_cod