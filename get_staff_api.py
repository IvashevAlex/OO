import requests
import json
import config

# Метод получающий значение токена из файла
def get_token():
    try:
        file = open('token.txt','r')
        token = file.read()
        file.close()
    except:
        token = str('Ошибка чтения файла токена!')
        print('Ошибка чтения файла токена!')

    return token


# Метод отправляющий запрос в АПИ
def staff_api_users(token):
    value_auth = 'Bearer ' + token
    url = config.staff_api_users_url
    method = config.staff_api_users_method
    payload = {}
    headers = {'Authorization': value_auth, 'Cookie': config.staff_api_users_Cookie}
    params = config.staff_api_users_params

    link = url + method + params
        
    try:
        response = requests.request("GET", link, headers=headers, data=payload)
        data = response.text
        file = open('data.json', 'w', encoding='utf-8')
        file.write(data)
        file.close()
        print('Запрос к АПИ выполнен успешно')

    except Exception as EX:
        print('Ошибка запроса данных по АПИ')
        print(EX.args)

# Метод отправляющий POST запрос для получения нового токена 
def checking_request():

    url = config.checking_request_url
    payload = config.checking_request_payload
    headers = {'Authorization': config.checking_request_authorization,
                'Content-Type': config.checking_request_content_type,
                'Cookie': config.checking_request_cookie}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)

        data = json.loads(response.text).get("access_token")
        file = open('token.txt','w')
        file.write(data)
        file.close()
        print('Новый токен успешно получен')
        token = get_token()
        staff_api_users(token)
    
       
    except Exception as EX:
        print('Ошибка запроса нового токена')
        print(EX.args)

# Метод отправляющий короткий GET запрос для проверки работоспособности токена и при необходимости вызывающий метод его обновления
def check_token(token):

    value_auth = 'Bearer ' + token
    url = config.check_token_url
    payload={}
    headers = {'Authorization': value_auth,'Cookie': config.check_token_headers_cookie}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)

        if response.status_code == 401:
            print('Запрос нового токена')
            checking_request()
        else:
            print('Код ответа:', response.status_code)
            staff_api_users(token)

    except Exception as EX:
        print('Ошибка проверки доступа по токену')
        print(EX.args)


token = get_token()
check_token(token)
