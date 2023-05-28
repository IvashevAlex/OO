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
from keyboards_modules.focus_menu import *

import text
import sql_queries

# Функция отрисовки кнопок в начальном меню
def question(bot, message):
    print('IN question')
    print(message.chat.id)
    modul_for_bot.sql_user(bot, message)

    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Диaдoк')
    itembtn2 = types.KeyboardButton('Pитейл')
    itembtn3 = types.KeyboardButton('Экстeрн')
    itembtn4 = types.KeyboardButton('Maркет')
    itembtn12 = types.KeyboardButton('Удостов. центр')
    itembtn13 = types.KeyboardButton('Устaнoвка')
    itembtn14 = types.KeyboardButton('WIС')
    itembtn15 = types.KeyboardButton('Вн. сервисы')
    itembtn5 = types.KeyboardButton('OФД')
    itembtn6 = types.KeyboardButton('ФMС')
    itembtn7 = types.KeyboardButton('Бухгaлтерия')
    itembtn8 = types.KeyboardButton('Эльбa')
    itembtn9 = types.KeyboardButton('Фокус')
    itemhelp = types.KeyboardButton('Пoмощь')

    markup.row(itembtn14, itembtn13, itembtn15)
    markup.row(itembtn1, itembtn2, itembtn3)
    markup.row(itembtn12, itembtn4, itembtn5)
    markup.row(itembtn6, itembtn7, itembtn8)
    markup.row(itembtn9, itemhelp)

    try:
        bot.send_message(message.chat.id, text.hello_mes, reply_markup=markup)
    except Exception as EX:
        print('Ошибка в формировании меню функцией question')


# Клавиатура выбора типа обучения
def test_menu(bot, message):
    print('IN test_menu')
    try:
        del modul_for_bot.practicks_data[message.from_user.id]
    except Exception as EX:
        print('Ошибка очистки practicks_data в test_menu')

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as EX:
        print('Ошибка редактирования сообщения в test_menu')

    markup_1 = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Тесты', callback_data='Тесты')
    itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='Кейсы')
    itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup_1.add(itembtn1, itembtn2)
    markup_1.add(itembtn12)

    try:
        bot.send_message(message.from_user.id, text.education_type, reply_markup=markup_1)
    except Exception as EX:
        print('Ошибка отправки сообщения в test_menu')

# Меню админа, вызываемое по команде "/admin"
def Admin_menu(message, bot): #Описание функций для меню поместил в конец кода
    print('IN Admin_menu')
    modul_for_bot.callback_check[message.from_user.id] = 'admin'
    markup = types.InlineKeyboardMarkup()
    
    itembtn1 = types.InlineKeyboardButton('Обновить таблицы', callback_data='Обновить таблицы')
    itembtn2 = types.InlineKeyboardButton('Зарегистрировать пользователя', callback_data='Зарегистрировать пользователя')
    itembtn3 = types.InlineKeyboardButton('Удалить пользователя', callback_data='Удалить пользователя')
    itembtn4 = types.InlineKeyboardButton('Рассылка', callback_data='Рассылка')

    itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup.add(itembtn1)
    markup.add(itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn9)

    try:
        bot.send_message(message.from_user.id, text.admin_mes, reply_markup=markup)
    except Exception as EX:
        print('Ошибка отправки сообщения в основном разделе Admin_menu')

# Отдельное меню для продукта Установка. Тут только тесты
def Inst_menu(name, bot):
    print('IN Inst_menu')
    @bot.message_handler(func=lambda message: message.text == name)
    def in_menu(message):
        try:
            del modul_for_bot.practicks_data[message.chat.id]
        except:
            print('Ошибка очистки practicks_data в Inst_menu')

        modul_for_bot.tests_data[message.chat.id] = 'INST'
        modul_for_bot.sql_user(bot, message)
        test_INST(bot, message)  # <--- тут будет отправка и меню с выбором


# Отдельное меню ВИК. Тут только кейсы
def WIC_menu(name, bot):
    print('IN WIC_menu')
    @bot.message_handler(func=lambda message: message.text == name)
    def wic_menu(message):
        try:
            del modul_for_bot.practicks_data[message.chat.id]
        except:
            print('Ошибка очистки practicks_data в WIC_menu')

        modul_for_bot.practicks_data[message.from_user.id] = 'PR'
        modul_for_bot.tests_data[message.chat.id] = 'WIC'
        prk_wic(bot, message)  # <--- тут будет отправка и меню с выбором


# Отдельное меню для Внутренних сервисов. Тут только кейсы
def Other_srvice_menu(name, bot):
    print('IN Other_service_menu')
    @bot.message_handler(func=lambda message: message.text == name)
    def in_menu(message):
        try:
            del modul_for_bot.practicks_data[message.chat.id]
        except Exception as EX:
            print('Ошибка очистки practicks_data в Other_srvice_menu')
       
        modul_for_bot.practicks_data[message.from_user.id] = 'PR'
        modul_for_bot.tests_data[message.chat.id] = 'OTHER'
        other_service_prk(bot, message)  # <--- тут будет отправка и меню с выбором


# Установка - Тесты - Клавиатура
def test_INST(bot, message):
    print('IN test_INST')
    modul_for_bot.sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as EX:
        print('Ошибка редактирования сообщения practicks_data в test_INST')

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Сертификаты и носители', callback_data='Сертификаты и носители')
    itembtn2 = types.InlineKeyboardButton('Работа с электронной подписью', callback_data='Работа с электронной подписью')
    itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup.add(itembtn1)
    markup.add(itembtn2)
    markup.add(itembtn9)

    try:
        bot.send_message(message.chat.id, "Выбери тему: ", reply_markup=markup)
    except Exception as EX:
        print('Ошибка редактирования сообщения practicks_data в test_INST')

# ------------  Клавиатура кейсов для каждого отдела -----------------#

# Отдельная клавиатура для кейсов по ВИК
def prk_wic(bot, message):
    print('IN prk_wic')
    modul_for_bot.sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as EX:
        print('Ошибка редактирования сообщения в prk_wic')

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Поиск знаний', callback_data='WIC.Поиск_знаний')
    itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='WIC.Кейсы')

    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup.add(itembtn1, itembtn2)
    markup.add(itembtn3)

    try:
        bot.send_message(chat_id=message.from_user.id, text="Выбери тему: ", reply_markup=markup)
    except Exception as EX:
        print('Ошибка отправки сообщения в prk_wic')

# Отдельная клавиатура для кейсов по Внутренним сервисам
def other_service_prk(bot, message):
    print('IN other_service_prk')
    modul_for_bot.sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as EX:
        print('Ошибка редактирования сообщения в other_service_prk')

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Билли', callback_data='Билли')
    itembtn2 = types.InlineKeyboardButton('КабУЦ', callback_data='КабУЦ')

    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Отмена')

    markup.add(itembtn1, itembtn2)
    markup.add(itembtn3)

    try:
        bot.send_message(chat_id=message.from_user.id, text="Выбери тему: ", reply_markup=markup)
    except Exception as EX:
        print('Ошибка отправки сообщения в other_service_prk')

# Возвращает к меню выбора тест/кейс для продуктов без индивидуальной схемы кнопок
def back_to_menu(bot, message):
    print('IN back_to_menu')
    test_menu(bot, message)


# Запускает функцию меню тестов продукта, ранее записанного в modul_for_bot.tests_data[callback_query.from_user.id]
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
        
        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'KF':
            test_focus(bot, callback_query)

# Запускает функцию меню кейсов продукта, ранее записанного в modul_for_bot.tests_data[callback_query.from_user.id]
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

        elif modul_for_bot.tests_data[callback_query.from_user.id] == 'KF':
            prk_focus(bot, callback_query)

# ------------------------------------ МЕНЮ АДМИНА-РАССЫЛКА----------------------------------------------

# Меню рассылки
def sending_menu(bot, callback_query):
    print('IN sending_menu')
    markup_send = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('База сообщений', callback_data='База сообщений')
    itembtn2 = types.InlineKeyboardButton('Календарь рассылок', callback_data='Календарь рассылок')
    itembtn3 = types.InlineKeyboardButton('Начать новый набор', callback_data='Начать новый набор')
    # itembtn12 = types.InlineKeyboardButton('Вернуться в Меню админа', callback_data='Вернуться в Меню админа')

    markup_send.add(itembtn1, itembtn2)
    markup_send.add(itembtn3)
    # markup_send.add(itembtn12)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text=text.send_actions, 
                              message_id=callback_query.message.message_id, reply_markup=markup_send,
                              parse_mode='Markdown')
    except:
        pass

# ---------------------------------МЕНЮ АДМИНА-РАССЫЛКИ-БАЗА СООБЩЕНИЙ--------------------------------

# Меню Рассылки - База сообщений (dbo.Messages)
def sending_menu_base(bot, callback_query):
    print('IN sending_menu_base')
    markup_base = types.InlineKeyboardMarkup()

    itembtn2 = types.InlineKeyboardButton('Создать сообщение', callback_data='Создать сообщение')
    itembtn3 = types.InlineKeyboardButton('Просмотреть все сообщения', callback_data='Просмотреть все сообщения')
    itembtn4 = types.InlineKeyboardButton('Изменить сообщение', callback_data='Изменить сообщение')

    itembtn12 = types.InlineKeyboardButton('Вернуться в Рассылки', callback_data='Вернуться в Рассылки')

    markup_base.add(itembtn2)
    markup_base.add(itembtn3, itembtn4)
    markup_base.add(itembtn12)

    # Start SQL
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.number_of_values_in_messages()
        cursor.execute(SQLQuery)
        number_of_messages = cursor.fetchall()[0][0]
    except Exception as EX:
        print('Ошибка работы с БД в sending_menu_base:', end='')
        print(EX.args)
    # End SQL

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, 
                              text=text.sending_base + str(number_of_messages), 
                              message_id=callback_query.message.message_id, 
                              reply_markup=markup_base)
    except:
        pass


# Добавление новой записи в dbo.Messages
def sending_menu_base_add_to_sql(message):
    print('IN sending_menu_base_add_to_sql')

    # Start SQL
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        print('TEXT: ', message.text)
        SQLQuery = sql_queries.add_new_value_in_messages(message.text)
        print(SQLQuery)
        cursor.execute(SQLQuery)
        connection.commit()
        connection.close()
        print('Запись успешно добавлена')
    except Exception as EX:
        print('Ошибка работы с БД в sending_menu_base_add_to_sql:', end='')
        print(EX.args)        
    # End SQL


# Изменить текст записи в dbo.Messages
def sending_menu_base_change(message):
    print('IN sending_menu_base_change')
    number_text = str(message.text).split('*')
    print(number_text)
    print(number_text[0])
    print(number_text[1])
    
    # Start SQL
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.select_message_for_change(number_text[0], number_text[1])
        cursor.execute(SQLQuery)
        connection.commit()
        connection.close()
        print('Текст успешно изменен')
    except Exception as EX:
        print('Ошибка работы с БД в sending_menu_base_change:', end='')
        print(EX.args)          

    # End SQL 
    try:
        bot.send_message(chat_id=message.from_user.id,  text='Сообщение изменено!', message_id=message.message_id)
    except:
        pass

# ---------------------------------МЕНЮ АДМИНА-РАССЫЛКИ-КАЛЕНДАРЬ РАССЫЛОК--------------------------------

# Меню рассылки - Календарь рассылок (dbo.Calendar)
def sending_menu_calendar(bot, callback_query):
    print('IN sending_menu_calendar')
    markup_calendar = types.InlineKeyboardMarkup()

    itembtn2 = types.InlineKeyboardButton('Задать день и номер рассылки', callback_data='Задать день и номер рассылки')
    itembtn3 = types.InlineKeyboardButton('Просмотреть расписание', callback_data='Просмотреть расписание')
    itembtn4 = types.InlineKeyboardButton('Очистить день от рассылки', callback_data='Очистить день от рассылки')

    itembtn12 = types.InlineKeyboardButton('Вернуться в Рассылки', callback_data='Вернуться в Рассылки')

    markup_calendar.add(itembtn2)
    markup_calendar.add(itembtn3, itembtn4)
    markup_calendar.add(itembtn12)

    # Start SQL
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.number_of_values_in_calendar()
        cursor.execute(SQLQuery)
        number_of_not_null_records = cursor.fetchall()[0][1]
    except Exception as EX:
        print('Ошибка работы с БД в sending_menu_calendar:', end='')
        print(EX.args)   
    # End SQL

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, 
                              text=text.sending_calendar + str(number_of_not_null_records), 
                              message_id=callback_query.message.message_id, 
                              reply_markup=markup_calendar)
    except:
        pass

# Изменяет в календаре номер рассылки для указанного дня
def edit_sending_menu_calendar(message):
    print('IN edit_sending_menu_calendar')
    number_text = str(message.text).split('*')
    print(number_text)
    print(number_text[0])
    print(number_text[1])
    
    # Start SQL
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.select_calendar_for_change(number_text[0], number_text[1])
        cursor.execute(SQLQuery)
        connection.commit()
        connection.close()
    except Exception as EX:
        print('Ошибка работы с БД в edit_sending_menu_calendar:', end='')
        print(EX.args)
    # End SQL

# Задает указанному дню рассылки значение NULL
def sending_menu_calendar_delete(message):
    print('IN sending_menu_calendar_delete')
    
    # Start SQL
    try:
        connection = pypyodbc.connect('Driver={SQL Server};''Server=' + mySQLServer + ';''Database=' + myDatabase + ';')
        cursor = connection.cursor()
        SQLQuery = sql_queries.clear_value_in_callendar(message.text)
        cursor.execute(SQLQuery)
        connection.commit()
        connection.close()
    except Exception as EX:
        print('Ошибка работы с БД в edit_sending_menu_calendar:', end='')
        print(EX.args)
    # End SQL
    
    try:
        bot.send_message(chat_id=message.from_user.id,  text='День очищен от рассылки!', message_id=message.message_id)
    except:
        pass

# ----------------------------МЕНЮ АДМИНА-РАССЫЛКИ-НАЧАТЬ НОВЫЙ НАБОР--------------------------

# Функция добавляет новую дату в dbo.Settable, дату начала нового набора
def sending_menu_start_new_wave(bot, callback_query):
    print('IN sending_menu_calendar')
    markup_new_wave = types.InlineKeyboardMarkup()

    itembtn2 = types.InlineKeyboardButton('Начать новый набор!', callback_data='Начать новый набор!')
    itembtn12 = types.InlineKeyboardButton('Вернуться в Рассылки', callback_data='Вернуться в Рассылки')

    markup_new_wave.add(itembtn2)
    markup_new_wave.add(itembtn12)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id,
                text="Нажми кнопку, для создания разделителя между старым и новым набором.\n"\
                "Старый набор будет ограничен вчерашней датой. Новый набор начнется с сегодняшней.\n"\
                "На данный момент перенос юзера из одного набора в другой можно сделать только  вручную.",
                message_id=callback_query.message.message_id, 
                reply_markup=markup_new_wave)
    except:
        pass

Other_srvice_menu("Вн. сервисы", bot)
WIC_menu("WIС", bot)
Inst_menu("Устaнoвка", bot)
tests(bot)
praktics(bot)
