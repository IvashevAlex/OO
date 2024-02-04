import pypyodbc
from telebot import types
from telebot.types import CallbackQuery

from config import DB_name
import test_mode_check
import sql_queries
import get_staff_api
import parsing_json

import text
import time

# Переменная, хранящая информацию об активации тестового режима
test_mode = test_mode_check.test_mode()

# Переменные хранящие список админов, токен бота, имя SQL сервера и имя базы данных
mes = test_mode_check.get_admins(test_mode)
mySQLServer = test_mode_check.get_server(test_mode)
bot = test_mode_check.get_token(test_mode)
myDatabase = DB_name

# Выбор сообщения об отсутствии доступа в зависимости от режима работы тест/прод
if test_mode == False:
    mes_pas = text.no_access
elif test_mode == True:
    mes_pas = text.no_access_test_mode
else:
    print('Что-то пошло не так')


# Проверяет наличие доступа у пользователя
def echo(callback_query):

    # Проверяем наличие id юзера в столбце UserChat таблицы WhiteList
    try:
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
        
        try:
            SQLQuery = """SELECT COUNT (*) 
                        FROM dbo.WhiteList 
                        WHERE UserChat = """ + str(callback_query.from_user.id) + """ AND UserMark = '1';"""

            cursor.execute(SQLQuery)
            result = cursor.fetchall()
        
        except:
            print('Ошибка проверки флага доступа')


        # Если флаг 0, то проверяем наличие юзернейма в списке TrueAccess
        if result[0][0] == 0:
            try:
                SQLQuery = sql_queries.check_in_true_access(str('@' + callback_query.from_user.username))
                cursor = connection.cursor()
                cursor.execute(SQLQuery)
                count = cursor.fetchall()
            
            except:
                print()

            # Если информации в TrueAccess нет, то отправляем запрос к api для обновления данных
            if count == 0:
                get_staff_api # получение файла data.json
                parsing_json # добавление и удаление юзеров из TrueAccess

                print('Нет данных о пользователе')
                try:
                    bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
                    
                except:
                    print('Ошибка отправки сообщения об отсутствии доступа пользователю!')
            

            # Если запись есть, то добавляем юзеру флаг доступа автоматически
            else:

                try:
                    connection = pypyodbc.connect('Driver={SQL Server};'
                                    'Server=' + mySQLServer + ';'
                                    'Database=' + myDatabase + ';')
                    cursor = connection.cursor()

                    SQLQuery = """  UPDATE dbo.WhiteList
                                    SET UserMark = 1
                                    WHERE UserChat = """ + str(callback_query.from_user.id) + """;"""

                    cursor.execute(SQLQuery)
                    connection.commit()
                    connection.close()


                except:
                    print('Ошибка автодобваления пользователя!')
                    

                    try:
                        bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
                    
                    except:
                        print('Ошибка отправки сообщения об отсутствии доступа пользователю!')

    
    # Если юзера нет в списке, то вносим его данные из Телеграм. 
    # Флаг остается нулевым. Изменение значения флага производит админ через меню бота
    else:

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
