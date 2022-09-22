import time
import datetime as dt
from WhiteList import *
import pypyodbc
import sql_queries

today = dt.date.today()

def time_checker():
    # Проверка на день недели. По выходным сообщения не рассылаем. Отправка в 12:05:05 по локальному времени
    if dt.datetime.today().isoweekday() in (1,2,3,4,5):
        if time.localtime()[3] == 12:
            if time.localtime()[4] == 5:
                if time.localtime()[5] == 5:
                    time.sleep(1) # Что-бы случайно не отправить дважды
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False
    else:
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
# ? Как будет вести себя функция еслидата сегодняшняя? 
# ? Пока есть ощущение, что выгядеть это будет как (2022-09-15, 2022-09-14) и приведет к ошибке
# todo По факту ошибка действительно возникает, но фиксится добавлением в dbo.Settable
# todo строки для рассылки нулевого дня
def make_lists_of_dates(dates):
    answer = list()
    for _ in range(len(dates) - 1):
        # dates_minus - коррректировака именно на последний день, а не на первый день следующего набора
        dates_minus = str(dt.datetime.strptime(dates[_ + 1], '%Y-%m-%d').date() - dt.timedelta(days=1))
        answer.append((dates[_], dates_minus))
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
    return dict_of_groups


# ! Исправить подсчет дней так, что бы нулевой день отсутствовал.
# Считает в диапазоне дат число будних дней
def weekdays_minus_sundays(pre_answer_int, first_day_format):
    answer = 0
    for _ in range(pre_answer_int):
        if first_day_format.isoweekday() in (1,2,3,4,5):
            print(first_day_format, first_day_format.isoweekday(), first_day_format.isoweekday() in (1,2,3,4,5))
            answer += 1
            first_day_format += dt.timedelta(days=1)
        else:
            print(first_day_format, first_day_format.isoweekday(), first_day_format.isoweekday() in (1,2,3,4,5))
            first_day_format += dt.timedelta(days=1)
    return answer

# ! Когда число прошедших дней привысит число дней в календаре будут сыпаться обшибки
# Рассчет прошедших дней со дня начала обучения за вычетом выходных
# Суббота и воскресенье всегда считаются выходными. Возможно стоит добавить список выходных через БД
def weekday_calc(today, lists_of_dates_pair):
    print('IN weekday_calc')
    print(lists_of_dates_pair[0])
    first_day = lists_of_dates_pair[0]
    first_day_format = dt.datetime.strptime(first_day, '%Y-%m-%d').date()
    pre_answer = today - first_day_format
    pre_answer_int = int(pre_answer.days)
    print('Всего прошло дней:', pre_answer)
    answer = weekdays_minus_sundays(pre_answer_int, first_day_format)
    return answer

# ! Когда число прошедших дней привысит число дней в календаре будут сыпаться обшибки
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

# ! Когда число прошедших дней привысит число дней в календаре будут сыпаться обшибки
# Получить текст сообщения по его номеру
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

print('Программа рассылки запущена!')

# Основной цикл
while True:
    if time_checker() == True:
        print('Начало отправки:', time.localtime()[3], time.localtime()[4], time.localtime()[5])
        dates_range = get_day_range_of_groups() # Получение списка дней начал обучения. Последний элемент - текущая дата
        lists_of_dates = make_lists_of_dates(dates_range) # Получение пар дат (начало-окончание) для каждой группы
        dict_of_groups = make_dict_of_groups(lists_of_dates) # Полученеи словоря {(начало-окончание):(список id пользователей за период)}

        # Запускаем цикл для каждой пары даты отдельно
        for _ in range(len(lists_of_dates)):
            print('Набор №', _ + 1)
            print('Пара дат:', lists_of_dates[_])
            send_day_number = weekday_calc(today, lists_of_dates[_]) # Число будних дней 
            number_of_message_by_date = get_message_number_by_day_number(send_day_number) # Номер сообщения для числа дней

            # Если для указанног дня есть сообщение
            if number_of_message_by_date != None:
                message_by_number = get_message_by_day_number(number_of_message_by_date) # Получение по номеру текста сообщения
                print('Текст отправляемого сообщения:', message_by_number)
                print('-' * 50)
                for i in range(len(dict_of_groups.get(lists_of_dates[_]))):
                    users_id = dict_of_groups.get(lists_of_dates[_])[i][0]
                    print('Отправка', users_id)
                    try:
                        bot.send_message(users_id, message_by_number)
                    except:
                        print('Ошибка отправки ', users_id)
            else:
                pass
            print('-' * 100)
        print('Конец отправки:', time.localtime()[3], time.localtime()[4], time.localtime()[5])
        time.sleep(150) # Защита от спамных отправок при сбоях.
    else:
        pass
