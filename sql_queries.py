import datetime as dt
import time

today = dt.date.today()

# ----------------------------- dbo.Messages -------------------------------

# Получение общего числа записей в dbo.Messages
def number_of_values_in_messages():
    return """ SELECT COUNT(*)
               FROM [dbo].[Messages]
           """


# Выбор конкретного сообщения из dbo.Messages
def select_message_by_number(number):
    return """SELECT [Message]
              FROM [dbo].[Messages]
              WHERE [Number] = """ + str(number) + """;
           """


# Выбор ВСЕХ сообщений
def get_all_info_from_messages():
    return """SELECT * 
              FROM [dbo].[Messages]
           """


# Указание нового текста сообщения по номеру (изменить запись)
def select_message_for_change(message_number, new_message_body):
    return """ UPDATE [dbo].[Messages]
                SET [Message] = '""" + str(new_message_body) + """'
                WHERE [Number] = """ + str(message_number) + """;
            """


# Добавление новой строки в dbo.Messages (новая запись)
def add_new_value_in_messages(new_messages_text):
    # print('IN add_new_value_in_messages')
    return """INSERT INTO [dbo].[Messages] (Number, Message)
              VALUES ((SELECT COUNT(*) FROM [dbo].[Messages]), '""" + str(new_messages_text) + """');
           """


# Удаление не предусмотрено
# ----------------------------- dbo.Settable -------------------------------

# Получение общего числа записей в dbo.Settable
""" SELECT COUNT(*)
    FROM [dbo].[Settable]
"""


# Выбор всех сообщений из dbo.Settable
def get_full_list_of_dates():
    return """SELECT *
    FROM [dbo].[Settable]
    ORDER BY [StartDate] ASC
    """


# Создать новый набор с сегодняшнего дня
def create_new_wave():
    return """INSERT INTO [dbo].[Settable] (StartDate)
              VALUES ('""" + str(dt.date.today()) + """'); 
            """

# Проверяет наличие сегодняшнего дня в списке дат начала набора 
def check_wave_duplicates():
    return """SELECT COUNT (*)
                FROM [dbo].[Settable]
                WHERE [StartDate] = ('""" + str(dt.date.today()) + """'); 
            """

# Удаление не предусмотрено 
# Редактирование через скрипт для SSMS непостредственно на сервере

# ----------------------------- dbo.Calendar -------------------------------

# Получение общего числа записей в dbo.Calendar
""" SELECT COUNT(*)
    FROM [dbo].[Calendar]
"""

# Получение общего числа не пустых записей в dbo.Calendar
def number_of_values_in_calendar():
    return """ SELECT COUNT(*), 
    SUM(CASE WHEN QuestionNumber IS NOT NULL THEN 1 ELSE 0 END)
    FROM [dbo].[Calendar]
    """


# Выбор всех сообщений из dbo.Calendar
def get_all_info_from_calendar():
    return """SELECT *
              FROM [dbo].[Calendar]
              WHERE [QuestionNumber] IS NOT NULL
            """


# Получить сообщение по его номеру записи
def get_message_by_number_by_sql(send_day_number):
    if send_day_number != None:
        return """ SELECT [QuestionNumber]
                    FROM [dbo].[Calendar]
                    WHERE [DayAfterStart] = """ + str(send_day_number) + """;"""
    else:
        return None


# Задать значение по номеру записи
def select_calendar_for_change(day_number, message_number):
    return """ UPDATE [dbo].[Calendar]
               SET [QuestionNumber] = """ + str(message_number) + """
               WHERE [DayAfterStart] = """ + str(day_number) + """;
           """


# Очистить значение по номеру записи
def clear_value_in_callendar(number):
    return """ UPDATE [dbo].[Calendar]
               SET [QuestionNumber] = NULL
               WHERE [DayAfterStart] = """ + str(number) + """;
           """

# ----------------------------- dbo.WhiteList ------------------------------- 

# Запрос списка id пользователей зарегистрированных в указанный диапазон
def get_list_of_users(lists_one, lists_two):
    return """SELECT [UserChat]
              FROM [dbo].[WhiteList]
              WHERE AddUserDate BETWEEN '""" + str(lists_one) + """' AND '""" + str(lists_two) + """'"""


# ----------------------------- dbo.TrueAccess ------------------------------- 

# Проверка наличия юзернейма ТГ в таблице TrueAccess БД UsersDB
def check_in_true_access(UsersName):
    return str("""SELECT COUNT (*)
              FROM [dbo].[TrueAccess]
              WHERE [UserNameTG] = '""" + str(UsersName) + """'""")


def check_in_true_access_mail(UsersMail):
    return str("""SELECT COUNT (*)
              FROM [dbo].[TrueAccess]
              WHERE [Email] = '""" + str(UsersMail) + """'""")

# Запрос на удаление записи из TrueAccess по почте
def remove_true_access(mail):
    return """DELETE 
                FROM [dbo].[TrueAccess]
                WHERE Email = '""" + str(mail) + """'"""