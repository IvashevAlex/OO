import time
import datetime as dt
from WhiteList import *

def auto_checker():

    if time.localtime()[3] in [3, 9, 11, 13, 15, 17, 19, 21]:
        if time.localtime()[4] == 5:
            time.sleep(1)
            return True
        else:
            return False
    else:
        return False

print('Программа автодобавления пользователей запущена!')

while True:
    time.sleep(30) # давжды в минуту проверяем не настало ли время
    if auto_checker() == True:
        try:
            get_staff_api.get_start() # получение файла data.json
        except:
            print(str(time.localtime()[3]) + ':' + str(time.localtime()[4]), 'Ошибка обращения к АПИ')
        
        try:
            parsing_json.parsing()
        except:
            print(str(time.localtime()[3]) + ':' + str(time.localtime()[4]), 'Ошибка парсинга ответа АПИ')
        
        print('\n')
        print('Данные успешно обновлены в', str(time.localtime()[3]) + ':' + str(time.localtime()[4]))
        time.sleep(6600) # После обновления данных в течение 1,5 часов нет смысла проверять время
        