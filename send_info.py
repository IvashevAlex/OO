import time
import datetime as dt
from WhiteList import *
import pypyodbc
import sql_queries
import log

# today = dt.date.today() - положение в данном месте не позволяет оновлять переменную , т.к. она объявляетс только один раз

def time_checker():
    # Проверка на день недели. По выходным сообщения не рассылаем. Отправка в 12:05:05 по локальному времени
    if dt.datetime.today().isoweekday() in (1,2,3,4,5):
        if time.localtime()[3] == 12:
            if time.localtime()[4] == 50:
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
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.get_all_info_from_calendar()
        cursor.execute(SQLQuery)
        answer = cursor.fetchall()
        print('get_calendar_info:', answer)
        return answer
    except:
        pass


# Подфункция get_day_range_of_groups(). Добавляет последним элементом списка текущую дату
def make_list_of_date_ranges(answer):
    try:
        list_of_date_ranges = list()
        for _ in range(len(answer)):
            list_of_date_ranges.append(answer[_][0])
        list_of_date_ranges.append(str(dt.date.today()))
        print('make_list_of_date_ranges:', list_of_date_ranges)
        return list_of_date_ranges
    except:
        pass


# Возвращает список из дат регистрации групп. Для последней группы датой окончания набора считается текущий день
def get_day_range_of_groups():
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.get_full_list_of_dates()
        cursor.execute(SQLQuery)
        answer = cursor.fetchall()
        first_and_last_day_list = make_list_of_date_ranges(answer)
        print('get_day_range_of_groups:', first_and_last_day_list)
        return first_and_last_day_list
    except:
        pass


# Возвращает список пар дат в формате {первый день набора, последний день набора} 
# Для последней группы датой окончания набора считается текущий день
def make_lists_of_dates(dates):
    try:
        answer = list()
        for _ in range(len(dates) - 1):
            # dates_minus - коррректировака именно на последний день, а не на первый день следующего набора
            dates_minus = str(dt.datetime.strptime(dates[_ + 1], '%Y-%m-%d').date() - dt.timedelta(days=1))
            answer.append((dates[_], dates_minus))
        print('make_lists_of_dates:', answer)
        return answer
    except:
        pass


# Подфункция make_dict_of_groups(). Запрашивает из БД WhiteList список id по дате регистрацц 
def make_dict_of_groups_sql(first_day, last_day):
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.get_list_of_users(first_day, last_day)
        cursor.execute(SQLQuery)
        answer = cursor.fetchall()
        return answer
    except:
        pass

# Обращаемся к БД и формируем словарь, где ключи - это списки из make_lists_of_dates, а значения - это
# id пользователей зарегистрировавшихся в указанный временной интервал, включая крайние даты 
def make_dict_of_groups(lists_of_dates):
    try:
        dict_of_groups = {}
        for _ in range(len(lists_of_dates)):
            list_of_groups = make_dict_of_groups_sql(lists_of_dates[_][0], lists_of_dates[_][1])
            dict_of_groups[lists_of_dates[_]] = list_of_groups
        return dict_of_groups
    except:
        pass

# Считает в диапазоне дат число будних дней
def weekdays_minus_sundays(pre_answer_int, first_day_format):
    try:
        answer = 0
        for _ in range(pre_answer_int):
            if first_day_format.isoweekday() in (1,2,3,4,5):
                # print(first_day_format, first_day_format.isoweekday(), first_day_format.isoweekday() in (1,2,3,4,5))
                answer += 1
                first_day_format += dt.timedelta(days=1)
            else:
                # print(first_day_format, first_day_format.isoweekday(), first_day_format.isoweekday() in (1,2,3,4,5))
                first_day_format += dt.timedelta(days=1)
        return answer
    except:
        pass

# Рассчет прошедших дней со дня начала обучения за вычетом выходных
# Суббота и воскресенье всегда считаются выходными. Возможно, стоит добавить список выходных через БД
def weekday_calc(today, lists_of_dates_pair):
    try:
        print('IN weekday_calc')
        print(lists_of_dates_pair[0])
        first_day = lists_of_dates_pair[0]
        first_day_format = dt.datetime.strptime(first_day, '%Y-%m-%d').date()
        pre_answer = dt.date.today() - first_day_format
        pre_answer_int = int(pre_answer.days)
        print('Всего прошло дней:', pre_answer)
        answer = weekdays_minus_sundays(pre_answer_int, first_day_format)
        return answer
    except Exception as EX:
        print(EX.args)


# Получение текста рассылки по ее дню из send_day_number
# todo Учесть ситуацию, когда значение дня рассылки отсутствует
def get_message_number_by_day_number(send_day_number):
    try:
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
    except:
        pass

# Получить текст сообщения по его номеру
def get_message_by_day_number(number_of_message_by_date):
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.select_message_by_number(number_of_message_by_date)
        print('get_message_by_day_number SQLQuery', SQLQuery)
        cursor.execute(SQLQuery)
        answer = cursor.fetchall()
        return answer
    except:
        pass

print('Программа рассылки запущена!')

# Основной цикл
while True:
    if time_checker() == True:
        try:
            print('Начало отправки:', time.localtime()[3], time.localtime()[4], time.localtime()[5])
            dates_range = get_day_range_of_groups() # Получение списка дней начал обучения. Последний элемент - текущая дата
            lists_of_dates = make_lists_of_dates(dates_range) # Получение пар дат (начало-окончание) для каждой группы
            dict_of_groups = make_dict_of_groups(lists_of_dates) # Полученеи словаря {(начало-окончание):(список id пользователей за период)}

            # Запускаем цикл для каждой пары даты отдельно
            for _ in range(len(lists_of_dates)):
                print('Набор №', _ + 1)
                print('Пара дат:', lists_of_dates[_])
                today = dt.date.today()
                print('Сегодня: ', today)
                send_day_number = weekday_calc(today, lists_of_dates[_]) # Число будних дней 
                number_of_message_by_date = get_message_number_by_day_number(send_day_number) # Номер сообщения для числа дней

                # Если для указанного дня есть сообщение
                try:
                    if number_of_message_by_date != None:
                        message_by_number = get_message_by_day_number(number_of_message_by_date) # Получение текста сообщения по номеру дня
                        print('Текст отправляемого сообщения:', message_by_number)
                        print('-' * 50)
                        for i in range(len(dict_of_groups.get(lists_of_dates[_]))):
                            users_id = dict_of_groups.get(lists_of_dates[_])[i][0]
                            print('Отправка', users_id)
                            try:
                                bot.send_message(users_id, message_by_number, parse_mode='Markdown', disable_web_page_preview=True)
                                

                            except Exception as e:
                                # Фиксируем причину возникновения ошибки
                                print('----------')
                                print(e.args)
                                print('Ошибка отправки: ', users_id)
                                time.sleep(1)
                                try:
                                    bot.send_message(users_id, message_by_number, parse_mode='Markdown', disable_web_page_preview=True)
                                    print('Отправлено со второй попытки.')
                                except:
                                    print('Повторная отправка не удалась.')
                                    pass
                                print('----------')
                    else:
                        pass
                
                except Exception as ex:
                    print('----------')
                    print(ex.args)
                    print('Слишком старая дата отправки', users_id)
                    print('----------')
                    

                print('-' * 100)
            print('Конец отправки:', time.localtime()[3], time.localtime()[4], time.localtime()[5])
            print(' ')
            time.sleep(150) # Защита от спамных отправок при сбоях.
        except:
            pass
    else:
        pass
