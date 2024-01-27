import pypyodbc
import telebot
from telebot import types
from telebot.types import CallbackQuery

from config import DB_name
import test_mode_check
import sql_queries

import text
import time

# Переменная, хранящая информацию об активации тестового режима
test_mode = test_mode_check.test_mode()

mes = test_mode_check.get_admins(test_mode)
mySQLServer = test_mode_check.get_server(test_mode)
bot = test_mode_check.get_token(test_mode)
myDatabase = DB_name

if test_mode == False:
    mes_pas = text.no_access
elif test_mode == True:
    mes_pas = text.no_access_test_mode
else:
    print('Что-то пошло не так')

# Проверяет наличие доступа у пользователя
def echo(callback_query):
    print('start echo')
    try:
        # Проверяем наличие id юзера в столбце UserChat таблицы WhiteList
        connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = """ SELECT TOP(1) 
                        IIF(UserChat = """ + str(callback_query.from_user.id) + """, 
                            CONVERT(VARCHAR(max), UserChat), 
                            'False') as res
                        FROM dbo.WhiteList ORDER BY res"""

        cursor.execute(SQLQuery)
        count = cursor.fetchall()
        userid = str(count[0][0])

    except:
        print('Ошибка запроса к базе данных!')

    # Если юзер уже есть в списке, то проверяем флаг доступа из UserMark
    if str(callback_query.from_user.id) == userid:
        print('if userid')
        try:
            print('start')
            SQLQuery = """SELECT UserMark 
                        FROM dbo.WhiteList 
                        WHERE UserChat = """ + str(callback_query.from_user.id) + """;"""

            cursor.execute(SQLQuery)
            result = cursor.fetchall()
            print(result[0][0])
            print('end')
        except:
            print('Ошибка проверки флага доступа')

        # Если флаг 0, то сообщаем юзеру об остутствии прав на использование
        if (result[0][0] == None):
            print('result[0][0] == None')
            SQLQuery = sql_queries.check_in_email_user_name(str('@' + callback_query.from_user.username))
            cursor = connection.cursor()
            cursor.execute(SQLQuery)
            count = cursor.fetchall()

            if count is False:
                print('Нет данных')
            else:
                print(count)
            #todo 
            """
            Перед отрпавкой юзера к админу мы делаем запрос к БД и проверяем есть ли юзернейм в списке [EmailUserName].
            Если его нет мы делаем запрос к АПИ и записываем новые данные в [EmailUserName], если такие есть, то
            после получения ответа повторно запращиваемданные [EmailUserName] и если ответа нет - посылаем к админу.

            Также из ответа АПИ записываем данные в [FiredUserEmail] и если такие есть в [WhiteList], то удаляем запись.
            Если юзер есть в списке [EmailUserName], то проставляем ему флаг доступа и перезапускаем echo.
            Каждое добавление/удаление логируем в отдельный файл. Файлы логов в определенное время отправляем себе в ТГ.
            
            Нужно добавлять дату создания записи на подобии той, что в [WhiteList] чтобы автоматически чистить информацию 
            которая страше двух недель, чтобы избежать разрастания файликов. Добавить автоочистку наборов из [Settable] для
            всех записей которые страше 4 недель
            """


            try:
                bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
            except:
                print('Ошибка отправки сообщения об отсутствии доступа пользователю!')
    
    # Если юзера нет в списке, то вносим его данные из Телеграм. 
    # Флаг остается нулевым. Изменение значения флага производит админ через меню бота
    else:
        print('else userid')
        try:
            SQLQuery = """ INSERT INTO dbo.WhiteList (UserChat, UserId, UserFIO, AddUserDate)
                            VALUES (""" + str(callback_query.from_user.id) + """, 
                            '@' + '""" + str(callback_query.from_user.username) + """', 
                            '""" + str(callback_query.from_user.first_name) + ' ' + str(callback_query.from_user.last_name) + """',
                            '""" + str(time.strftime('%Y-%m-%d')) + """');"""

            cursor.execute(SQLQuery)
            bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
            connection.commit()
            connection.close()
        
        except:
            try:
                SQLQuery = """ INSERT INTO dbo.WhiteList (UserChat, UserId, UserFIO, AddUserDate)
                            VALUES (""" + str(callback_query.from_user.id) + """, 
                            '@' + '""" + str(callback_query.from_user.username) + """', 
                            '""" + str('Ошибка') + ' ' + str('Ошибка') + """',
                            '""" + str(time.strftime('%Y-%m-%d')) + """');"""

                cursor.execute(SQLQuery)
                bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
                connection.commit()
                connection.close()
                print('Запись выполнена, но данные first_name и last_name указаны как Ошибка!')

            except:
                print('Ошибка записи данных в БД!')


    return result[0][0]


# Добавляет пользователю маркер о разрешении на доступ
def add_user(message, data_base):
    try:
        connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
        cursor = connection.cursor()
        
        # Если запрос получен от админа, то формируем переменную res со значением id добовляемого пользователя
        if str(message.from_user.id) in mes:
            res = data_base['BotUsers'][message.from_user.id]['UserAnswer']
        else:
            return

        print('Добавляем пользователя с номером', res)

        # SQL запрос на смену флага доступа для пользователя с id указанным в переменной res
        SQLQuery = """UPDATE dbo.WhiteList
                    SET UserMark = 1
                    WHERE UserChat = """ + str(res) + """;"""

        cursor.execute(SQLQuery)
        bot.send_message(chat_id=message.from_user.id, text=f'Пользователь с id {str(res)} добавлен.')

        connection.commit()
        connection.close()
    except:
        print('Ошибка добавления пользователя!')
        bot.send_message(chat_id=message.from_user.id, text='Ошибка добавления. Попробуй еще раз.')

# Удаляет всю информацию о пользователе из БД
def rm_user(message, data_base):
    try:
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
    except:
        print('Ошибка удаления пользователя!')
        bot.send_message(chat_id=message.from_user.id, text='Ошибка удаления. Попробуй еще раз.')
