import requests
import json
import config

def staff_api_users(token):
    value_auth = 'Bearer ' + token
    url = config.staff_api_users_url
    method = config.staff_api_users_method
    payload = config.staff_api_users_payload
    headers = {'Authorization': value_auth, 'Cookie': config.staff_api_users_Cookie}
    params = config.staff_api_users_params

    link = url + method + params
        
    try:
        response = requests.request("GET", link, headers=headers, data=payload)
        data = json.loads(response.text)
        file = open('data.json', 'a+', encoding='utf-8')
        file.write(data)
        file.close()
        print('Запрос к АПИ выполнен успешно.')

    except Exception as EX:
        print('Ошибка запроса данных по АПИ!')
        print(EX.args)

file = open('token.txt','r')
token = file.read()
file.close()

staff_api_users(token)
