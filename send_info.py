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
    # print('make_dict_of_groups:', dict_of_groups)

    return dict_of_groups


# Считает в диапазоне дат число будних дней
def weekdays_minus_sundays(pre_answer_int, first_day_format):
    answer = 0
    for _ in range(pre_answer_int):
        if first_day_format.isoweekday() in (1,2,3,4,5):
            print('first_day_format.isoweekday()', first_day_format.isoweekday(), first_day_format.isoweekday() in (1,2,3,4,5))
            answer += 1
            first_day_format += dt.timedelta(days=1)
        else:
            print('PASS:', first_day_format.isoweekday())
            first_day_format += dt.timedelta(days=1)
            
    return answer

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


# Получение текста рассылки по ее дню из send_day_number
def get_message_number_by_day_number(send_day_number):
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.get_message_by_number_by_sql(send_day_number)
    print('get_message_number_by_day_number SQLQuery', SQLQuery)
    if SQLQuery != None:
        cursor.execute(SQLQuery)
        answer = cursor.fetchall()[0][0]
        return answer
    else:
        return None
    # End SQL  


def get_message_by_day_number(number_of_message_by_date):
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.select_message_by_number(number_of_message_by_date)
    print('get_message_by_day_number SQLQuery', SQLQuery)
    cursor.execute(SQLQuery)
    answer = cursor.fetchall()
    return answer
    # End SQL 


# Основной цикл
while True:
    if time_checker() == True:
        calendar_list = get_calendar_info() # Получение дня и номера рассылки. Возможно, не трбуется
        print('calendar_list:', calendar_list)
        dates_range = get_day_range_of_groups() # Получение списка дней начал обучения. Последний элемент - текущая дата
        print('dates_range:', dates_range)
        lists_of_dates = make_lists_of_dates(dates_range) # Получение пар дат (начало-окончание) для каждой группы
        print('lists_of_dates:', lists_of_dates)
        dict_of_groups = make_dict_of_groups(lists_of_dates) # Полученеи словоря {(начало-окончание):(список id пользователей за период)}

        # Запускаем цикл для каждой пары даты отдельно
        for _ in range(len(lists_of_dates)):
            print('Набор №', _ + 1)
            print('Пара дат:', lists_of_dates[_])
            send_day_number = weekday_calc(today, lists_of_dates[_]) # Число будних дней 
            print('send_day_number:', send_day_number)

            number_of_message_by_date = get_message_number_by_day_number(send_day_number) # Номер сообщения для числа дней
            print(number_of_message_by_date)

            # Если для указанног дня есть сообщение
            if number_of_message_by_date != None:
                message_by_number = get_message_by_day_number(number_of_message_by_date)
                print('message_by_number:', message_by_number)

                # for i in range():
                #     pass
                bot.send_message('5484457194', message_by_number)
            else:
                pass
            print('-' * 100)
        
    else:
        pass
