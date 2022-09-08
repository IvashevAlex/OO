# ----------------------------- dbo.Messages -------------------------------

# Получение общего числа записей в dbo.Messages
""" SELECT COUNT(*)
    FROM [dbo].[Messages]
"""


# Выбор конкретного сообщения из dbo.Messages
"""SELECT [Message]
   FROM [dbo].[Messages]
   WHERE [Number] = """ + str() + """;
"""


# Указание нового текста сообщения по номеру (изменить запись)
""" UPDATE [dbo].[Messages]
    SET [Message] = '""" + str() + """'
    WHERE [Number] = """ + str() + """;
"""


# Добавление новой строки в dbo.Messages (новая запись)
"""INSERT INTO [dbo].[Messages] (Number, Message)
   VALUES ((SELECT COUNT(*) FROM [dbo].[Messages]) + 1, """ + str() + """);   
"""

# Удаление не предусмотрено

# ----------------------------- dbo.Settable -------------------------------

# Получение общего числа записей в dbo.Settable
""" SELECT COUNT(*)
    FROM [dbo].[Settable]
"""


# Выбор всех сообщений из dbo.Settable
"""SELECT *
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


# Выбор всех сообщений из dbo.Calendar
"""SELECT *
   FROM [dbo].[Calendar]
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
