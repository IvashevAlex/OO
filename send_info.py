import time
import datetime as dt
from WhiteList import *
import pypyodbc
import sql_queries

today = dt.date.today()
print('Today:', today)

def time_checker():
    # Проверка на день недели. По выходным сообщения не рассылаем. 7(Вс) пока стоит для тестирования
    print(dt.datetime.today().isoweekday())
    print(dt.datetime.today().isoweekday() in (1,2,3,4,5,7))
    print(dt.datetime.today().isoweekday() in (1,2,3,4,5))
    
    if dt.datetime.today().isoweekday() in (1,2,3,4,5,7):
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
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.get_all_info_from_calendar()
    cursor.execute(SQLQuery)
    answer = cursor.fetchall()
    return answer
    # End SQL  

# Обращаемся к БД и формируем группы для рассылок
def get_sending_groups(today):
    pass


while True:
    if time_checker() == True:
        print('Time')
        calendar_list = get_calendar_info()

        for i in range(calendar_list):
            # Ответ формата (8, 13), где 
            # 8 - число рабочих дней прошедших с первого дня учебы текущего набора
            # 13 - номер рассылки, которую положено отправить в этот день
            calendar_list[i]
        
    else:
        pass

        # Делаем запрос на число записсей для рассылки
        # Получаем список id подходящих для рассылки
        # Получаем тело рассылки
        # Запускаем цикл рассылки
        # Для каждого id из списка
        #     bot.send_message(id, body)

