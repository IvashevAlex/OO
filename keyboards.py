from WhiteList import *
import modul_for_bot
from keyboards_modules.fms_menu import *
from keyboards_modules.diadoc_menu import *
from keyboards_modules.extern_menu import *
from keyboards_modules.buh_menu import *
from keyboards_modules.edi_menu import *
from keyboards_modules.elba_menu import *
from keyboards_modules.market_menu import *
from keyboards_modules.ofd_menu import *
from keyboards_modules.uc_menu import *

import text
import sql_queries

def question(bot, message):
    print('IN question')
    print(message.chat.id)
    modul_for_bot.sql_user(bot, message)

    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Диaдoк')
    itembtn2 = types.KeyboardButton('Pитейл')
    itembtn3 = types.KeyboardButton('Экстeрн')
    itembtn4 = types.KeyboardButton('Maркет')
    itembtn12 = types.KeyboardButton('УЦ′')
    itembtn13 = types.KeyboardButton('Устaнoвка')
    itembtn14 = types.KeyboardButton('WIС')
    itembtn15 = types.KeyboardButton('Внутренние сервисы')
    itembtn5 = types.KeyboardButton('OФД')
    itembtn6 = types.KeyboardButton('ФMС')
    itembtn7 = types.KeyboardButton('Бухгaлтерия')
    itembtn8 = types.KeyboardButton('Эльбa')
    itemhelp = types.KeyboardButton('Пoмощь')

    markup.row(itembtn14, itembtn13, itembtn15)
    markup.row(itembtn1, itembtn2, itembtn3)
    markup.row(itembtn12, itembtn4, itembtn5)
    markup.row(itembtn6, itembtn7, itembtn8)
    markup.row(itemhelp)
    bot.send_message(message.chat.id, text.hello_mes, reply_markup=markup)


def test_menu(bot, message):
    print('IN test_menu')
    try:
        del modul_for_bot.practicks_data[message.from_user.id]
    except:
        pass

    try:
        bot.edit_message_reply_markup(
            message.from_user.id, message.message_id - 1)
    except Exception as Abc:
        pass

    markup_1 = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Тесты', callback_data='Тесты')
    itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='Кейсы')
    itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup_1.add(itembtn1, itembtn2)
    markup_1.add(itembtn12)

    try:
        bot.send_message(
            message.from_user.id, text.education_type, reply_markup=markup_1)
    except Exception as E:
        pass


def Admin_menu(message, bot): #Описание функций для меню поместил в конец кода
    print('IN Admin_menu')
    modul_for_bot.callback_check[message.from_user.id] = 'admin'
    markup = types.InlineKeyboardMarkup()
    
    itembtn1 = types.InlineKeyboardButton('Обновить таблицы', callback_data='Обновить таблицы')
    itembtn2 = types.InlineKeyboardButton('Зарегистрировать пользователя', callback_data='Зарегистрировать пользователя')
    itembtn3 = types.InlineKeyboardButton('Удалить пользователя', callback_data='Удалить пользователя')
    itembtn4 = types.InlineKeyboardButton('Рассылки', callback_data='Рассылки')

    itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup.add(itembtn1)
    markup.add(itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn9)
    bot.send_message(message.from_user.id, text.admin_mes, reply_markup=markup)

def Inst_menu(name, bot):
    print('IN Inst_menu')
    @bot.message_handler(func=lambda message: message.text == name)
    def in_menu(message):
        try:
            del modul_for_bot.practicks_data[message.chat.id]
        except:
            pass
        modul_for_bot.tests_data[message.chat.id] = 'INST'
        modul_for_bot.sql_user(bot, message)
        test_INST(bot, message)  # <--- тут будет отправка и меню с выбором

def WIC_menu(name, bot):
    print('IN WIC_menu')
    @bot.message_handler(func=lambda message: message.text == name)
    def wic_menu(message):
        try:
            del modul_for_bot.practicks_data[message.chat.id]
        except:
            pass

        modul_for_bot.practicks_data[message.from_user.id] = 'PR'
        modul_for_bot.tests_data[message.chat.id] = 'WIC'
        prk_wic(bot, message)  # <--- тут будет отправка и меню с выбором

def Other_srvice_menu(name, bot):
    print('IN Other_service_menu')
    @bot.message_handler(func=lambda message: message.text == name)
    def in_menu(message):
        try:
            del modul_for_bot.practicks_data[message.chat.id]
        except:
            pass
        modul_for_bot.practicks_data[message.from_user.id] = 'PR'
        modul_for_bot.tests_data[message.chat.id] = 'OTHER'
        other_service_prk(bot, message)  # <--- тут будет отправка и меню с выбором


def test_INST(bot, message):
    print('IN test_INST')
    modul_for_bot.sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as Abc:
        pass

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Компоненты для работы с ЭП', callback_data='Компоненты для работы с ЭП')
    itembtn2 = types.InlineKeyboardButton('Запрос КЭП', callback_data='Запрос КЭП')
    itembtn3 = types.InlineKeyboardButton('Работа с ЭП', callback_data='Работа с ЭП')
    itembtn4 = types.InlineKeyboardButton('КЭП для ЕГАИС', callback_data='КЭП для ЕГАИС')
    itembtn5 = types.InlineKeyboardButton('Сертификаты УЦ', callback_data='Сертификаты УЦ')
    itembtn6 = types.InlineKeyboardButton('Работа с ЭП не на Windows', callback_data='Работа с ЭП не на Windows')
    itembtn7 = types.InlineKeyboardButton('DSS', callback_data='DSS')
    itembtn8 = types.InlineKeyboardButton('Установка общее', callback_data='Установка общее')
    itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')


    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn7, itembtn8)
    markup.add(itembtn9)

    bot.send_message(message.chat.id, "Выбери тему: ", reply_markup=markup)

# ------------  Клавиатура кейсов для каждого отдела -----------------#
def prk_wic(bot, message):
    print('IN prk_wic')
    modul_for_bot.sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as Abc:
        pass

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Поиск знаний', callback_data='WIC.Поиск_знаний')
    itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='WIC.Кейсы')


    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup.add(itembtn1, itembtn2)
    markup.add(itembtn3)

    bot.send_message(chat_id=message.from_user.id, text="Выбери тему: ", reply_markup=markup)


def other_service_prk(bot, message):
    print('IN other_service_prk')
    modul_for_bot.sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as Abc:
        pass

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Билли', callback_data='Билли')
    itembtn2 = types.InlineKeyboardButton('КабУЦ', callback_data='КабУЦ')
    itembtn4 = types.InlineKeyboardButton('Клиент-Сервис', callback_data='Клиент-Сервис')


    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup.add(itembtn1, itembtn2, itembtn4)
    markup.add(itembtn3)

    bot.send_message(chat_id=message.from_user.id, text="Выбери тему: ", reply_markup=markup)


def back_to_menu(bot, message):
    print('IN back_to_menu')
    test_menu(bot, message)


def tests(bot):
    print('IN tests')
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Тесты')
    def tests_hm(callback_query: CallbackQuery):

        bot.answer_callback_query(callback_query.id)
        if modul_for_bot.tests_data[callback_query.from_user.id] == 'DD':
            test_DD(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'EDI':
            test_EDI(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'extrn':
            test_ext(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'UC':
            test_uc(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'MK':
            test_mk(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'FMS':
            test_fms(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'OFD':
            test_ofd(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'BUH':
            test_buh(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'ELB':
            test_elb(bot, callback_query)


def praktics(bot):
    print('IN praktics')
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Кейсы')
    def tests_h(callback_query: CallbackQuery):
        bot.answer_callback_query(callback_query.id)

        # <-- Ставим метку что мы нажали кнопку "Кейсы"
        modul_for_bot.practicks_data[callback_query.from_user.id] = 'PR'
        if modul_for_bot.tests_data[callback_query.from_user.id] == 'DD':
            prk_diadoc(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'EDI':
            prk_edi(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'extrn':
            prk_ext(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'UC':
            prk_uc(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'MK':
            prk_mk(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'FMS':
            prk_fms(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'OFD':
            prk_ofd(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'BUH':
            prk_buh(bot, callback_query)

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'ELB':
            prk_elb(bot, callback_query)



# ---------------------------------------------------------------------------------------------------


# Меню рассылки
def sending_menu(bot, callback_query):
    print('IN sending_menu')
    markup_send = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('База сообщений', callback_data='База сообщений')
    itembtn2 = types.InlineKeyboardButton('Календарь рассылок', callback_data='Календарь рассылок')
    itembtn3 = types.InlineKeyboardButton('Разделение групп', callback_data='Разделение групп')
    itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup_send.add(itembtn1, itembtn2)
    markup_send.add(itembtn3)
    markup_send.add(itembtn12)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text=text.send_actions, 
                              message_id=callback_query.message.message_id, reply_markup=markup_send)
    except:
        pass

# Меню рассылки - База сообщений (dbo.Messages)
def sending_menu_base(bot, callback_query):
    print('IN sending_menu_base')
    markup_base = types.InlineKeyboardMarkup()

    itembtn2 = types.InlineKeyboardButton('Создать сообщение', callback_data='Создать сообщение')
    itembtn3 = types.InlineKeyboardButton('Просмотреть сообщение', callback_data='Просмотреть сообщение')
    itembtn4 = types.InlineKeyboardButton('Удалить сообщение', callback_data='Удалить сообщение')

    itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup_base.add(itembtn2)
    markup_base.add(itembtn3, itembtn4)
    markup_base.add(itembtn12)

    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.number_of_values_in_messages()
    cursor.execute(SQLQuery)
    number_of_messages = cursor.fetchall()[0][0]
    # End SQL

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, 
                              text=text.sending_base + str(number_of_messages), 
                              message_id=callback_query.message.message_id, 
                              reply_markup=markup_base)
    except:
        pass

def sending_menu_calendar(bot, callback_query):
    print('IN sending_menu_calendar')
    markup_calendar = types.InlineKeyboardMarkup()

    itembtn2 = types.InlineKeyboardButton('Создать рассылку', callback_data='Создать рассылку')
    itembtn3 = types.InlineKeyboardButton('Просмотреть рассылку', callback_data='Просмотреть рассылку')
    itembtn4 = types.InlineKeyboardButton('Удалить рассылку', callback_data='Удалить рассылку')

    itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup_calendar.add(itembtn2)
    markup_calendar.add(itembtn3, itembtn4)
    markup_calendar.add(itembtn12)

    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.number_of_values_in_calendar()
    cursor.execute(SQLQuery)
    number_of_not_null_records = cursor.fetchall()[0][1]
    # End SQL

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, 
                              text=text.sending_calendar + str(number_of_not_null_records), 
                              message_id=callback_query.message.message_id, 
                              reply_markup=markup_calendar)
    except:
        pass


# def sending_menu_base_create(bot, callback_query):
#     print('IN sending_menu_base_create')

#     markup_calendar_create_message = types.InlineKeyboardMarkup()

#     itembtn2 = types.InlineKeyboardButton('Разместить рассылку', callback_data='Разместить рассылку')

#     itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

#     markup_calendar_create_message.add(itembtn2)
#     markup_calendar_create_message.add(itembtn12)

#     try:
#         bot.edit_message_text(chat_id=callback_query.from_user.id, 
#                               text=text.add_new_message_base, 
#                               message_id=callback_query.message.message_id, 
#                               reply_markup=markup_calendar_create_message)
#     except:
#         pass


def sending_menu_base_add_to_sql(message):
    print('IN sending_menu_base_add_to_sql')
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    print('TEXT: ', message.text)
    SQLQuery = sql_queries.add_new_value_in_messages(message.text)
    print(SQLQuery)
    cursor.execute(SQLQuery)
    connection.commit()
    connection.close()
    # End SQL

def sending_menu_base_look(bot, callback_query):
    print('IN sending_menu_base_look')
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.select_message_by_number(1)
    cursor.execute(SQLQuery)
    print('Сообщение номер **:')
    # End SQL    

def sending_menu_base_change(bot, callback_query):
    print('IN sending_menu_base_change')
    # Start SQL
    connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
    cursor = connection.cursor()
    SQLQuery = sql_queries.select_message_for_change(1)
    cursor.execute(SQLQuery)
    print('Введите новый текст для сообщения **:')
    # End SQL  

def sending_menu_calendar_create(bot, callback_query):
    bot.send_message(callback_query.from_user.id, 'Сообщает новую рассылку', parse_mode='Markdown')

def sending_menu_calendar_look(bot, callback_query):
    bot.send_message(callback_query.from_user.id, 'Показывает рассылки по дате', parse_mode='Markdown')

def sending_menu_calendar_delete(bot, callback_query):
    bot.send_message(callback_query.from_user.id, 'Удаляет рассылку по номеру', parse_mode='Markdown')


Other_srvice_menu("Внутренние сервисы", bot)
WIC_menu("WIС", bot)
Inst_menu("Устaнoвка", bot)
tests(bot)
praktics(bot)
