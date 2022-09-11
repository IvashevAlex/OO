import time
import datetime as dt
from WhiteList import *
import pypyodbc
import sql_queries

today = dt.date.today()
print('Today:', today)

def time_checker():
    if time.localtime()[3] == 14:
        if time.localtime()[4] == 16:
            if time.localtime()[5] < 5:
                time.sleep(5)
                return True
            else:
                return False
    return False


# Обращаемся к БД и получаем словарь формата {число дней:номер рассылки}
def get_calendar_info():
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.get_all_info_from_calendar()
    cursor.execute(SQLQuery)
    print('INFO: ', cursor)
    # End SQL  

# Обращаемся к БД и формируем группы для рассылок
def get_sending_groups(today):
    pass



while True:
    if time_checker() == True:
        print('Time')
        get_calendar_info()
        
    else:
        pass

        # Делаем запрос на число записсей для рассылки
        # Получаем список id подходящих для рассылки
        # Получаем тело рассылки
        # Запускаем цикл рассылки
        # Для каждого id из списка
        #     bot.send_message(id, body)

