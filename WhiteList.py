import openpyxl
import pypyodbc
import re
import telebot
from telebot import types
from telebot.types import CallbackQuery
import random
import test_mode_check
import text
import time

test_mode = test_mode_check.test_mode()

mes = test_mode_check.get_admins(test_mode)
mySQLServer = test_mode_check.get_server(test_mode)
bot = test_mode_check.get_token(test_mode)
myDatabase = "UsersDB"

mes_pas = text.no_access

# Проверяет наличие доступа у пользователя
def echo(callback_query):
    # Проверяем наличие id юзера в столбце UserChat таблицы WhiteList
    # Если он есть, то он в виде строки передается в переменную userid
    # Если его нет, то в переменную userid подается значение False
    connection = pypyodbc.connect('Driver={SQL Server};'
                                  'Server=' + mySQLServer + ';'
                                  'Database=' + myDatabase + ';')

    cursor = connection.cursor()

    SQLQuery = (""" SELECT TOP(1) 
                    IIF(UserChat = """ + str(callback_query.from_user.id) + """, 
                        CONVERT(VARCHAR(max), UserChat), 
                        'False') as res
                    FROM dbo.WhiteList ORDER BY res""")

    cursor.execute(SQLQuery)
    count = cursor.fetchall()
    userid = str(count[0][0])
    print('uID = ', userid, type(userid))

    # Если юзер уже есть в списке, то проверяем флаг доступа из UserMark
    if str(callback_query.from_user.id) == userid:
        SQLQuery = ("""SELECT UserMark 
                       FROM dbo.WhiteList 
                       WHERE UserChat = """ + str(callback_query.from_user.id) + """;""")

        cursor.execute(SQLQuery)
        result = cursor.fetchall()
        print(result[0][0])

        # Если флаг 0, то сообаем юзеру об остутствии прав на использование
        if (result[0][0] == False):
            bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
    
    # Если юзера нет в списке, то вносим его данные из Телеграм. 
    # Флаг остается нулевым. Изменение значения флага производит админ через меню бота
    else:
    
        SQLQuery = (""" INSERT INTO dbo.WhiteList (UserChat, UserId, UserFIO)
                        VALUES (""" + str(callback_query.from_user.id) + """, 
                        '@' + '""" + str(callback_query.from_user.username) + """', 
                        '""" + str(callback_query.from_user.first_name) + ' ' + str(callback_query.from_user.last_name) + """',
                        '""" + str(time.strftime('%Y-%m-%d')) + """');""")

        cursor.execute(SQLQuery)
        bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
        connection.commit()
        connection.close()

    return result[0][0]


# Добавляет пользователю маркер о разрешении на доступ
def add_user(message, data_base):
    connection = pypyodbc.connect('Driver={SQL Server};'
                                  'Server=' + mySQLServer + ';'
                                  'Database=' + myDatabase + ';')
    cursor = connection.cursor()
    
    # Если запрос получен от админа, то формируем переменную res со значением id добовляемого пользователя
    if str(message.from_user.id) in mes:
        res = data_base['BotUsers'][message.from_user.id]['UserAnswer']
    else:
        return

    print(res)

    # SQL запрос на смену флага доступа для пользователя с id указанным в переменной res
    SQLQuery = """UPDATE dbo.WhiteList
                  SET UserMark = 1
                  WHERE UserChat = """ + str(res) + """;"""

    cursor.execute(SQLQuery)

    bot.send_message(chat_id=message.from_user.id, text=f'Пользователь с id {str(res)} добавлен.')

    connection.commit()
    connection.close()


# Удаляет всю информацию о пользователе из БД
def rm_user(message, data_base):
    connection = pypyodbc.connect('Driver={SQL Server};'
                                  'Server=' + mySQLServer + ';'
                                  'Database=' + myDatabase + ';')

    cursor = connection.cursor()

    if str(message.from_user.id) in mes:
        res = data_base['BotUsers'][message.from_user.id]['UserAnswer']
    else:
        return

    SQLQuery = """DELETE dbo.WhiteList 
                  WHERE UserChat = """ + str(res) + """;"""

    cursor.execute(SQLQuery)

    bot.send_message(chat_id=message.from_user.id, text=f"Пользователь с id {str(res)} удален.")

    connection.commit()
    connection.close()
