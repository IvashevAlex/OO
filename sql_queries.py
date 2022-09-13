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


# Указание нового текста сообщения по номеру (изменить запись)
def select_message_for_change(new_message_body, message_number):
    return """ UPDATE [dbo].[Messages]
                SET [Message] = '""" + str(new_message_body) + """'
                WHERE [Number] = """ + str(message_number) + """;
            """


# Добавление новой строки в dbo.Messages (новая запись)
def add_new_value_in_messages(new_messages_text):
    print('IN add_new_value_in_messages')
    return """INSERT INTO [dbo].[Messages] (Number, Message)
              VALUES ((SELECT COUNT(*) FROM [dbo].[Messages]) + 1, '""" + str(new_messages_text) + """');
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
    """


# Создать новый набор с сегодняшнего дня
"""INSERT INTO [dbo].[Settable] (Data)
   VALUES ('""" + str() + """');   
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


# Указать значение по номеру записи
""" UPDATE [dbo].[Calendar]
    SET [QuestionNumber] = '""" + str() + """'
    WHERE [DayAfterStart] = """ + str() + """;
"""


# Очистить значение по номеру записи
""" UPDATE [dbo].[Calendar]
    SET [QuestionNumber] = NULL
    WHERE [DayAfterStart] = """ + str() + """;
"""

# ----------------------------- dbo.WhiteList ------------------------------- 

# Запрос списка id пользователей зарегистрированных в указанный диапазон
def get_list_of_users(lists_one, lists_two):
    return """SELECT [UserChat]
              FROM [dbo].[WhiteList]
              WHERE AddUserDate BETWEEN '""" + str(lists_one) + """' AND '""" + str(lists_two) + """'"""
