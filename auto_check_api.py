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
print('\n')

while True:
    time.sleep(30) # давжды в минуту проверяем не настало ли время
    if auto_checker() == True:
        try:
            get_staff_api.get_start() # получение файла data.json
            print('Данные успешно получены в', str(time.localtime()[3]) + ':' + str(time.localtime()[4]))
        except:
            print(str(time.localtime()[3]) + ':' + str(time.localtime()[4]), 'Ошибка обращения к АПИ')
        
        try:
            parsing_json.parsing()
            print('Данные успешно обработаны в', str(time.localtime()[3]) + ':' + str(time.localtime()[4]))
        except:
            print(str(time.localtime()[3]) + ':' + str(time.localtime()[4]), 'Ошибка обработки ответа АПИ')
        
        
        time.sleep(6600) # После обновления данных в течение 1,5 часов нет смысла проверять время
        