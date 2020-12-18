import openpyxl
import pypyodbc
import re
import telebot
from telebot import types
from telebot.types import CallbackQuery
import random

bot = telebot.TeleBot('1174261024:AAEfPd9lElQbGXvRST8t9e2YAhwAPWlOLGs',  threaded=False)
# bot = telebot.TeleBot('1253732018:AAESPvgR9YfmnTAHtHRMWJ8tjOmApA_qSyI',  threaded=False) #OOHelper

mySQLServer = "K1606047"
myDatabase = "UsersDB"

mes = ['233770916', '391368365']

mes_pas = ("У тебя нет прав на использования данного бота!\n\n"
           # "За доступом обратись к @fenix073 или @lexxxekb .\n\n"
           "Отправь @lexxxekb ссылку своей страницы на Стаффе и этот телеграмм ID: ")


def echo(callback_query):
    return True
    # connection = pypyodbc.connect('Driver={SQL Server};'
    #                               'Server=' + mySQLServer + ';'
    #                                                         'Database=' + myDatabase + ';'
    #                               )

    # cursor = connection.cursor()

    # SQLQuery = ("""SELECT top(1) iif(UserChat = """ + str(callback_query.from_user.id) + """, convert(varchar(max), UserChat), 'False') as res
    #                     FROM dbo.WhiteList order by res""")
    # cursor.execute(SQLQuery)
    # count = cursor.fetchall()
    # userid = str(count[0][0])
    # print('uID = ', userid, type(userid))

    # if str(callback_query.from_user.id) == userid:
    #     SQLQuery = ("""select UserMark from dbo.WhiteList where UserChat = """ + str(callback_query.from_user.id) + """;""")

    #     cursor.execute(SQLQuery)

    #     result = cursor.fetchall()

    #     print(result[0][0])

    #     if (result[0][0] == False):
    #         bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
    # else:
    #     SQLQuery = ("""insert into dbo.WhiteList (UserChat, UserId, UserFIO)
    #                     values (""" + str(callback_query.from_user.id) + """, '@' + '""" + str(
    #         callback_query.from_user.username) + """', '""" + str(callback_query.from_user.first_name) + ' ' + str(
    #         callback_query.from_user.last_name) + """');"""
    #                 )
    #     cursor.execute(SQLQuery)
    #     bot.send_message(callback_query.from_user.id, mes_pas + str(callback_query.from_user.id) + ".")
    #     connection.commit()
    #     connection.close()

    # return result[0][0]


def add_user(message, data_base):
    connection = pypyodbc.connect('Driver={SQL Server};'
                                  'Server=' + mySQLServer + ';'
                                                            'Database=' + myDatabase + ';'
                                  )

    cursor = connection.cursor()

    if str(message.from_user.id) in mes:
        res = data_base['BotUsers'][message.from_user.id]['UserAnswer']
    else:
        return

    print('----------')
    print(res)
    SQLQuery = """update dbo.WhiteList
    set UserMark = 1 where UserChat = """ + str(res) + """;"""

    cursor.execute(SQLQuery)

    bot.send_message(chat_id=message.from_user.id, text=f'Пользователь с id {str(res)} добавлен.')

    connection.commit()
    connection.close()



def rm_user(message, data_base):
    connection = pypyodbc.connect('Driver={SQL Server};'
                                  'Server=' + mySQLServer + ';'
                                                            'Database=' + myDatabase + ';'
                                  )

    cursor = connection.cursor()

    if str(message.from_user.id) in mes:
        res = data_base['BotUsers'][message.from_user.id]['UserAnswer']
    else:
        return

    SQLQuery = """delete dbo.WhiteList where UserChat = """ + str(res) + """;
                  delete dbo.BotUsers where UserChat = """ + str(res) + """;
                  delete dbo.UserQuestions where UserChat = """ + str(res) + """;"""

    cursor.execute(SQLQuery)

    bot.send_message(chat_id=message.from_user.id, text=f"Пользователь с id {str(res)} удален.")

    connection.commit()
    connection.close()
