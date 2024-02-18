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
import log

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

    # time_info = str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5]) + ' '
    # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 1 def echo\n'
    # log.write_actions_log(log.actions_log_file, result_log_string)
    
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
        # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 2 Ошибка запроса к базе данных!\n'
        # log.write_actions_log(log.actions_log_file, result_log_string)

    # Если юзер уже есть в списке, то проверяем флаг доступа из UserMark
    if str(callback_query.from_user.id) == userid:

        # time_info = str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5]) + ' '
        try:
            SQLQuery = """SELECT COUNT (*) 
                        FROM dbo.WhiteList 
                        WHERE UserChat = """ + str(callback_query.from_user.id) + """ AND UserMark = '1';"""

            cursor.execute(SQLQuery)
            result = cursor.fetchall()
            # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 3 Маркер доступа = ', str(result[0][0]), '\n'
            # log.write_actions_log(log.actions_log_file, result_log_string)
        
        except Exception as EX:
            print(EX.args)
            print('Ошибка проверки флага доступа!')
            # result_log_string = str('    ' + time_info + str(callback_query.from_user.id) + ' --- 4 Ошибка проверки флага доступа!\n')
            # log.write_actions_log(log.actions_log_file, result_log_string)


        # Если флаг 0, то проверяем наличие юзернейма в списке TrueAccess
        if result[0][0] == 0:
            # time_info = str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5]) + ' '
            try:
                SQLQuery = sql_queries.check_in_true_access(str('@' + callback_query.from_user.username))
                cursor = connection.cursor()
                cursor.execute(SQLQuery)
                count = cursor.fetchall()[0][0]
                # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 5 Присутствие в TrueAcess = ', str(count), '\n'
                # log.write_actions_log(log.actions_log_file, result_log_string)
            
            except:
                pass
                # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 6 Ошибка проверки в TrueAcess!\n'
                # log.write_actions_log(log.actions_log_file, result_log_string)

            # Если информации в TrueAccess нет, то отправляем запрос к api для обновления данных
            if count == 0:
                # time_info = str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5]) + ' '
                # ! запрос обновления при каждом обращении незареганого юзера убрал для исключения возможного спама в АПИ
                # ! на замену сделал автозапрос данных кажжые 2 часа с 9 до 21 
                # get_staff_api.get_start() # получение файла data.json
                # parsing_json.parsing() # добавление и удаление юзеров из TrueAccess
                
                try:
                    SQLQuery = sql_queries.check_in_true_access(str('@' + callback_query.from_user.username))
                    cursor = connection.cursor()
                    cursor.execute(SQLQuery)
                    count_2 = cursor.fetchall()[0][0]
                    # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 7 Присутствие в TrueAcess = ', str(count_2), '\n'
                    # log.write_actions_log(log.actions_log_file, result_log_string)

                    if count_2 == 0:
                        bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
                        # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 8 Пользователь не подтвердил доступ!\n'
                        # log.write_actions_log(log.actions_log_file, result_log_string)
                    
                    if count_2 == 1:
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

                        # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 9 Установлен маркер доступа = 1 в результате запроса к АПИ\n'
                        # log.write_actions_log(log.actions_log_file, result_log_string)
                
                except:
                    pass
                    # print('Доступ предоставлен в результате запрос к АПИ!')
                    # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 10 Доступ предоставлен в результате запрос к АПИ!\n'
                    # log.write_actions_log(log.actions_log_file, result_log_string)

            
            elif count == 1:
                # time_info = str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5]) + ' '
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
                    print('Пользователь ', callback_query.from_user.id, 'успешно добавлен!')
                    bot.send_message(callback_query.from_user.id, 'Доступ к боту предоставлен автоматически. \nНажми /start чтобы начать работу.')
                    # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 11 Установлен маркер доступа = 1 без запроса к АПИ\n'
                    # log.write_actions_log(log.actions_log_file, result_log_string)

                except:
                    print('Ошибка автодобваления пользователя!')
                    
                    try:
                        bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
                    
                    except:
                        print('Ошибка отправки сообщения об отсутствии доступа пользователю!')
            else:
                pass

    
    # Если юзера нет в списке, то вносим его данные из Телеграм. 
    # Флаг остается нулевым. Изменение значения флага производит админ через меню бота
    else:
        # time_info = str(time.localtime()[3]) + ':' + str(time.localtime()[4]) + ':' + str(time.localtime()[5]) + ' '

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

            # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 12 Пользователь впервые обратился к боту. Создана новая запись.\n'
            # log.write_actions_log(log.actions_log_file, result_log_string)
        
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

                # result_log_string = '    ' + time_info + str(callback_query.from_user.id) + ' --- 13 Пользователь впервые обратился к боту. Создана новая запись. Ошибка!\n'
                # log.write_actions_log(log.actions_log_file, result_log_string)

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
