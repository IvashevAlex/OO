import time
import datetime as dt
from WhiteList import *
import pypyodbc
import sql_queries

today = dt.date.today()
print('Today:', today)

def time_checker():
    # Проверка на день недели. По выходным сообщения не рассылаем. 7(Вс) пока стоит для тестирования
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

def make_list_of_date_ranges(answer):
    list_of_date_ranges = list()
    for _ in range(len(answer)):
        print('ANS:', answer[_])
        list_of_date_ranges.append(answer[_][0])
    list_of_date_ranges.append(str(today))
    return list_of_date_ranges

def get_day_range_of_groups():
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.get_full_list_of_dates()
    cursor.execute(SQLQuery)
    answer = cursor.fetchall()
    first_and_last_day_list = make_list_of_date_ranges(answer)
    return first_and_last_day_list
    # End SQL  


def make_lists_of_dates(dates):
    answer = list()
    for _ in range(len(dates) - 1):
        answer.append((dates[_], dates[_ + 1]))
    print('make_lists_of_dates: ', answer)
    return answer

# Рассчет прошедших дней со дня начала обучения за вычетом выходных
# Суббота и воскресенье всегда считаются выходными. Возможно стоит добавить список выходных через БД
def weekday_calc(today):
    pass

# Обращаемся к БД и формируем группы для рассылок
def get_sending_groups(today):
    pass

while True:
    if time_checker() == True:
        print('Time')
        calendar_list = get_calendar_info()
        dates = get_day_range_of_groups()
        
        lists_of_dates = make_lists_of_dates(dates)

        print('DATES:', dates)

        for i in range(len(calendar_list)):
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

