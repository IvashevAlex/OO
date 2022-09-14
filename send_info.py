import time
import datetime as dt
from WhiteList import *
import pypyodbc
import sql_queries

today = dt.date.today()


def time_checker():
    # Проверка на день недели. По выходным сообщения не рассылаем. 7(Вс) пока стоит для тестирования
    # Неравенства так же для тестирования
    if dt.datetime.today().isoweekday() in (1,2,3,4,5):
        if time.localtime()[3] != 10:
            if time.localtime()[4] != 10:
                if time.localtime()[5] % 15 == 0:
                    time.sleep(1)
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
    print('get_calendar_info:', answer)
    return answer
    # End SQL  


# Подфункция get_day_range_of_groups(). Добавляет последним элементом списка текущую дату
def make_list_of_date_ranges(answer):
    list_of_date_ranges = list()
    for _ in range(len(answer)):
        list_of_date_ranges.append(answer[_][0])
    list_of_date_ranges.append(str(today))
    print('make_list_of_date_ranges:', list_of_date_ranges)
    return list_of_date_ranges


# Возвращает список из дат регистрации групп. Для последней группы датой окончания набора считается текущий день
def get_day_range_of_groups():
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.get_full_list_of_dates()
    cursor.execute(SQLQuery)
    answer = cursor.fetchall()
    first_and_last_day_list = make_list_of_date_ranges(answer)
    print('get_day_range_of_groups:', first_and_last_day_list)
    return first_and_last_day_list
    # End SQL  


# Возвращает список пар дат в формате (первый день набора, последний день набора). 
# Для последней группы датой окончания набора считается текущий день
def make_lists_of_dates(dates):
    answer = list()
    for _ in range(len(dates) - 1):
        answer.append((dates[_], dates[_ + 1]))
    print('make_lists_of_dates:', answer)
    return answer


# Подфункция make_dict_of_groups() запрашивающая из БД WhiteList список id по дате регистрацц 
def make_dict_of_groups_sql(first_day, last_day):
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.get_list_of_users(first_day, last_day)
    cursor.execute(SQLQuery)
    answer = cursor.fetchall()
    return answer
    # End SQL  


# Обращаемся к БД и формируем словарь, где ключи - это списки из make_lists_of_dates, а значения - это
# id пользователей зарегистрировавшихся в указанный временной интервал, включая крайние даты 
def make_dict_of_groups(lists_of_dates):
    dict_of_groups = {}
    for _ in range(len(lists_of_dates)):
        list_of_groups = make_dict_of_groups_sql(lists_of_dates[_][0], lists_of_dates[_][1])
        dict_of_groups[lists_of_dates[_]] = list_of_groups
    print('make_dict_of_groups:', dict_of_groups)

    return dict_of_groups


# Считает в диапазоне дат число будних дней
def weekdays_minus_sundays(pre_answer_int, first_day_format):
    answer = 0
    for _ in range(pre_answer_int):
        if first_day_format.isoweekday() in (1,2,3,4,5):
            answer += 1
            first_day_format += dt.timedelta(days=1)


# Рассчет прошедших дней со дня начала обучения за вычетом выходных
# Суббота и воскресенье всегда считаются выходными. Возможно стоит добавить список выходных через БД
def weekday_calc(today, lists_of_dates_pair):
    print('IN weekday_calc')
    print(lists_of_dates_pair[0])
    first_day = lists_of_dates_pair[0]
    first_day_format = dt.datetime.strptime(first_day, '%Y-%m-%d').date()
    pre_answer = today - first_day_format
    pre_answer_int = int(pre_answer.days)
    print('pre_answer', pre_answer, type(pre_answer))
    answer = weekdays_minus_sundays(pre_answer_int, first_day_format)
    return answer


while True:
    if time_checker() == True:
        calendar_list = get_calendar_info()
        print('calendar_list:', calendar_list)
        dates_range = get_day_range_of_groups()
        print('dates_range:', dates_range)
        lists_of_dates = make_lists_of_dates(dates_range)
        print('lists_of_dates:', lists_of_dates)
        dict_of_groups = make_dict_of_groups(lists_of_dates)
        print('dict_of_groups:', dict_of_groups)

        for _ in range(len(lists_of_dates)):
            print('Набор №', _)
            print('lists_of_dates[_]:', lists_of_dates[_])
            send_day_number = weekday_calc(today, lists_of_dates[_][0]) # Число будних дней 
            print('send_day_number:', send_day_number)
            print('-' * 100)
        
    else:
        pass

        # Делаем запрос на число записсей для рассылки
        # Получаем список id подходящих для рассылки
        # Получаем тело рассылки
        # Запускаем цикл рассылки
        # Для каждого id из списка
        #     bot.send_message(id, body)
