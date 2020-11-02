from telebot import types
import random
import requests
import time
import openpyxl
import pypyodbc
import re
from WhiteList import *
from telebot.types import CallbackQuery

alex_id = 233770916 #ID телеграма Лёхи, для обработки сообщений об ошибке
toha_id = 391368365 #ID Антохи, для обработки технической ошибки

data_base = {'BotUsers': {},
             'UserQuestions': {},
             }

mySQLServer = "K1606047"
myDatabase = "UsersDB"

sheet = 0
count = 0
rand = 0

a = {}
save_check = {'wic_search':{}
              }
tests_data = {}
practicks_data = {'check_attempt':{}}
ans = {'lower': {}}
callback_check = {'text': {}}
file_id = {}
file_dir = 'Data/screens/'  # Указываем путь до папок отделов с скринами и файлами
save_message_id = {'check_answer': {},
                   'message_id': {},
                   'message_text':{},
                   'message_id_answer':{}
                   }

rand_question = {} #<-- тут мы держим номера вопросов, которые нужно задать

db_data = {}  # <-- тут мы для храним файл ексель для каждого отдела

# -----------------------   Загружаем все эксели в базу -------------------------#
db_data['all'] = openpyxl.load_workbook('./Data/УЦ.xlsx', read_only=True)
db_data['UC'] = openpyxl.load_workbook('./Data/УЦ.xlsx', read_only=True)
db_data['FMS'] = openpyxl.load_workbook('./Data/ФМС.xlsx', read_only=True)
db_data['MK'] = openpyxl.load_workbook('./Data/Маркет.xlsx', read_only=True)
db_data['EDI'] = openpyxl.load_workbook('./Data/Ритейл.xlsx', read_only=True)
db_data['DD'] = openpyxl.load_workbook('./Data/Диадок.xlsx', read_only=True)
db_data['KE'] = openpyxl.load_workbook('./Data/KE.xlsx', read_only=True)
db_data['BH'] = openpyxl.load_workbook('./Data/Бухгалтерия.xlsx', read_only=True)
db_data['ELB'] = openpyxl.load_workbook('./Data/Эльба.xlsx', read_only=True)
db_data['OFD'] = openpyxl.load_workbook('./Data/ОФД.xlsx', read_only=True)
db_data['INST'] = openpyxl.load_workbook('./Data/Установка.xlsx', read_only=True)
db_data['WIC'] = openpyxl.load_workbook('./Data/WIC.xlsx', read_only=True)
db_data['OTHER'] = openpyxl.load_workbook('./Data/Вн. сервисы.xlsx', read_only=True)

# ------------ Функция обработки нажатия кнопок ---------- #
def quest(theme, number_of_page, bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == theme)
    def name_def(callback_query):
        try:
            bot.edit_message_text(text='Подготавливаю вопросы, это займёт некоторое время.',
                                  chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
            bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id)
        except Exception as Abc:
            pass

        a[callback_query.from_user.id] = number_of_page  # <--- Запоминаем номер страницы с продуктом (Ехель)
        save_check['wic_search'][callback_query.from_user.id] = False #Отвечает за нажатие кнопки Wic поиск знаний. Для того чтобы формируя кейс влиять на сообщение

        if practicks_data.get(callback_query.from_user.id) == 'PR':  # <---- находимся ли мы в кейсах
            if tests_data[callback_query.from_user.id] == 'extrn':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1 #из Екселя берем number_of_page + 1, ибо в файле 1ая табла тесты а следующая кейсы
            elif tests_data[callback_query.from_user.id] == 'BUH':
                a[callback_query.from_user.id] = 7 #В продукте КБ кейсы всегда на 7 индексе
            elif tests_data[callback_query.from_user.id] == 'ELB':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'OFD':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'EDI':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'FMS':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'UC':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'MK':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'DD':
                a[callback_query.from_user.id] = int(a[callback_query.from_user.id]) + 1
            elif tests_data[callback_query.from_user.id] == 'WIC':
                if callback_query.data == 'WIC.Поиск_знаний': #Проверяем нажата ли кнопка поиск знаний раздела ВИК
                    save_check['wic_search'][callback_query.from_user.id] = True #Если нажата то активируем переменную, для формирования определенного сообщения в кейсах
            elif tests_data[callback_query.from_user.id] == 'OTHER':
                pass # нам не нужно присваивать новые номера для внутр сервисов

            answers_prk(bot, callback_query) #Запускаем цикл вопрос\ответ по кейсам
        else:
            answers(bot, callback_query) #Если выбрали не кейсы, то запускаем цикл вопрос\ответ по тестам


def back_to_menu(bot, message):
    test_menu(bot, message)


def sql_user(bot, callback_query):
    userid = str(callback_query.from_user.id)
    print('ID = ', userid, type(userid))

    if str(callback_query.from_user.id) == userid:
        print('user - ', callback_query.from_user.id)
        data_base['BotUsers'][callback_query.from_user.id] = {'UserChat': str(callback_query.from_user.id),
                                                              'UserRand': '0',
                                                              'UserPage': 'None',
                                                              'UserAnswer': 'None',
                                                              'UserRowQuestions': '0',
                                                              'UserCounterTrueAns': '0'}

        rand_question[callback_query.from_user.id] = []
        try:
            del callback_check[callback_query.from_user.id]
        except:
            pass


    else:
        data_base['BotUsers'][callback_query.from_user.id] = {'UserChat': str(callback_query.from_user.id),
                                                              'UserRand': '0',
                                                              'UserPage': 'None',
                                                              'UserAnswer': 'None',
                                                              'UserRowQuestions': '0',
                                                              'UserCounterTrueAns': '0'}
        rand_question[callback_query.from_user.id] = []

    try:
        del data_base['UserQuestions'][callback_query.from_user.id]
    except:
        pass

    try:
        del callback_check[callback_query.from_user.id]
    except:
        pass

    results = data_base['BotUsers'][callback_query.from_user.id]['UserChat'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

    print(results)


def question(bot, message):
    print(message.chat.id)

    sql_user(bot, message)

    # bot.send_message(message.chat.id, 'Диадок \nEDI \nЭкстерн \nУЦ \nУстановка')
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Диaдoк')
    itembtn2 = types.KeyboardButton('Ритейл')
    itembtn3 = types.KeyboardButton('Экстерн')
    itembtn4 = types.KeyboardButton('Maркет')
    itembtn12 = types.KeyboardButton('УЦ')
    itembtn13 = types.KeyboardButton('Устанoвка')
    itembtn14 = types.KeyboardButton('WIC')
    itembtn15 = types.KeyboardButton('Внутренние сервисы')
    itembtn5 = types.KeyboardButton('OФД')
    itembtn6 = types.KeyboardButton('ФMС')
    itembtn7 = types.KeyboardButton('Бухгалтерия')
    itembtn8 = types.KeyboardButton('Эльба')
    itemhelp = types.KeyboardButton('Помощь')

    markup.row(itembtn14, itembtn13, itembtn15)
    markup.row(itembtn1, itembtn2, itembtn3)
    markup.row(itembtn12, itembtn4, itembtn5)
    markup.row(itembtn6, itembtn7, itembtn8)
    markup.row(itemhelp)
    bot.send_message(message.chat.id, "Привет :) Это бот Отдела Обучения.\n"
                                      "Выбери нужную тему с помощью кнопок внизу.", reply_markup=markup)

def Admin_menu(message, bot): #Описание функций для меню поместил в конец кода
    callback_check[message.from_user.id] = 'admin'
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Обновить таблицы', callback_data='Обновить таблицы')
    itembtn2 = types.InlineKeyboardButton('Зарегистрировать пользователя', callback_data='Зарегистрировать пользователя')
    itembtn3 = types.InlineKeyboardButton('Удалить пользователя', callback_data='Удалить пользователя')

    itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')

    markup.add(itembtn1)
    markup.add(itembtn2, itembtn3)
    markup.add(itembtn9)
    bot.send_message(message.from_user.id, 'Привет! Если ты видишь это сообщение, то у тебя чуть больше прав чем у других))\n'
                                           'Выбирай необходимое действие.', reply_markup=markup)

def Inst_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def in_menu(message):
        try:
            del practicks_data[message.chat.id]
        except:
            pass
        tests_data[message.chat.id] = 'INST'
        sql_user(bot, message)
        test_INST(bot, message)  # <--- тут будет отправка и меню с выбором

def WIC_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def wic_menu(message):
        try:
            del practicks_data[message.chat.id]
        except:
            pass

        practicks_data[message.from_user.id] = 'PR'
        tests_data[message.chat.id] = 'WIC'
        prk_wic(bot, message)  # <--- тут будет отправка и меню с выбором

def Other_srvice_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def in_menu(message):
        try:
            del practicks_data[message.chat.id]
        except:
            pass
        practicks_data[message.from_user.id] = 'PR'
        tests_data[message.chat.id] = 'OTHER'
        other_service_prk(bot, message)  # <--- тут будет отправка и меню с выбором

def DD_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def menu(message):
        tests_data[message.chat.id] = 'DD'
        sql_user(bot, message)
        test_menu(bot, message)  # <--- тут будет отправка и меню с выбором


def ext_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Extern_menu(message):
        tests_data[message.chat.id] = 'extrn'
        sql_user(bot, message)
        test_menu(bot, message)  # <--- тут будет отправка и меню с выбором


def EDI_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def menu(message):
        tests_data[message.chat.id] = 'EDI'
        sql_user(bot, message)
        test_menu(bot, message)  # <--- тут будет отправка и меню с выбором


def UC_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def UC(message):
        tests_data[message.chat.id] = 'UC'
        sql_user(bot, message)
        test_menu(bot, message)


def FMS_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def FMS_menu_start(message):
        tests_data[message.chat.id] = 'FMS'
        sql_user(bot, message)
        test_menu(bot, message)


def OFD_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def OFD_KKT_menu(message):
        tests_data[message.chat.id] = 'OFD'
        sql_user(bot, message)
        test_menu(bot, message)


def M_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Market_m(message):
        tests_data[message.chat.id] = 'MK'
        sql_user(bot, message)
        test_menu(bot, message)


def Buh_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Buh_m(message):
        tests_data[message.chat.id] = 'BUH'
        sql_user(bot, message)
        test_menu(bot, message)


def Elba_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Buh_m(message):
        tests_data[message.chat.id] = 'ELB'
        sql_user(bot, message)
        test_menu(bot, message)


# ----------------------------- Обрабатываем если выбрали "тесты" ---------------------------------- #
def tests(bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Тесты')
    def tests_hm(callback_query: CallbackQuery):

        bot.answer_callback_query(callback_query.id)
        if tests_data[callback_query.from_user.id] == 'DD':
            test_DD(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'EDI':
            test_EDI(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'extrn':
            test_ext(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'UC':
            test_uc(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'MK':
            test_mk(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'FMS':
            test_fms(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'OFD':
            test_ofd(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'BUH':
            test_buh(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'ELB':
            test_elb(bot, callback_query)
        

# ----------------------------- функции с клавиатурами после выбора отдела, тесты ---------------------------------- #
def test_menu(bot, message):
    try:
        del practicks_data[message.from_user.id]
    except:
        pass

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as Abc:
        pass

    markup_1 = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Тесты', callback_data='Тесты')
    itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='Кейсы')
    itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')

    markup_1.add(itembtn1, itembtn2)
    markup_1.add(itembtn12)

    try:
        bot.send_message(message.from_user.id, "Какой вид обучения тебя интересует?", reply_markup=markup_1)
    except Exception as E:
        pass


def test_INST(bot, message):
    sql_user(bot, message)

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
    itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')


    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn7, itembtn8)
    markup.add(itembtn9)

    bot.send_message(message.chat.id, "Выбери тему: ", reply_markup=markup)


def test_DD(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Web', callback_data='Web.Диадок')
    itembtn2 = types.InlineKeyboardButton('Модуль', callback_data='Модуль.Диадок')
    itembtn3 = types.InlineKeyboardButton('Роуминг', callback_data='Роуминг.Диадок')
    itembtn4 = types.InlineKeyboardButton('Коннекторы', callback_data='Коннекторы.Диадок')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn12)

    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_EDI(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('EDI Web', callback_data='EDI Web')
    itembtn2 = types.InlineKeyboardButton('EDI 1C', callback_data='EDI 1C')
    itembtn4 = types.InlineKeyboardButton('Меркурий', callback_data='Меркурий')
    itembtn3 = types.InlineKeyboardButton('Поставки', callback_data='Поставки')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_ext(bot, callback_query):  # <--- формируем меню с тестами для КЭ
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()

    itembtn3 = types.InlineKeyboardButton('Интерфейс', callback_data='Интерфейс')
    itembtn4 = types.InlineKeyboardButton('Режим работы', callback_data='Режим работы')
    itembtn5 = types.InlineKeyboardButton('ФНС', callback_data='ФНС')
    itembtn6 = types.InlineKeyboardButton('ИОН', callback_data='ИОН')
    itembtn7 = types.InlineKeyboardButton('Таблица отчетности', callback_data='Таблица отчетности')
    itembtn8 = types.InlineKeyboardButton('Письма ФНС', callback_data='Письма ФНС')
    itembtn9 = types.InlineKeyboardButton('ПФР', callback_data='ПФР')
    itembtn10 = types.InlineKeyboardButton('НДС и требования', callback_data='НДС и требования')
    itembtn11 = types.InlineKeyboardButton('НДФЛ', callback_data='НДФЛ')
    itembtn13 = types.InlineKeyboardButton('Росстат', callback_data='Росстат')
    itembtn14 = types.InlineKeyboardButton('РСВ', callback_data='РСВ')
    itembtn15 = types.InlineKeyboardButton('Заполнение ПФР', callback_data='Заполнение ПФР')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4, itembtn5)
    markup.add(itembtn6, itembtn7, itembtn8)
    markup.add(itembtn9, itembtn10, itembtn11)
    markup.add(itembtn13, itembtn14, itembtn15)
    markup.add(itembtn12)

    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_uc(bot, callback_query):  # <--- формируем меню с тестами для УЦ
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Проекты УЦ', callback_data='Проекты УЦ')
    itembtn2 = types.InlineKeyboardButton('ЭТП', callback_data='ЭТП')
    itembtn3 = types.InlineKeyboardButton('ИС', callback_data='ИС')
    itembtn4 = types.InlineKeyboardButton('Закупки', callback_data='Закупки')
    itembtn5 = types.InlineKeyboardButton('Реестро', callback_data='Реестро')
    itembtn6 = types.InlineKeyboardButton('Контур.Торги', callback_data='Контур.Торги')
    itembtn7 = types.InlineKeyboardButton('Декларант', callback_data='Декларант')
    itembtn8 = types.InlineKeyboardButton('Школа', callback_data='Школа')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn7, itembtn8)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_fms(bot, callback_query):  # <--- формируем меню с тестами для ФМС
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn3 = types.InlineKeyboardButton('ФМС', callback_data='ФМС')
    itembtn4 = types.InlineKeyboardButton('Отель', callback_data='Отель')
    itembtn5 = types.InlineKeyboardButton('Фокус', callback_data='Фокус')
    itembtn6 = types.InlineKeyboardButton('Фокус API', callback_data='Фокус API')
    itembtn7 = types.InlineKeyboardButton('Компас', callback_data='Компас')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4, itembtn5)
    markup.add(itembtn6, itembtn7)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_ofd(bot, callback_query):  # <--- формируем меню с тестами для ОФД
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('API', callback_data='API')
    itembtn2 = types.InlineKeyboardButton('1C', callback_data='1C')
    itembtn3 = types.InlineKeyboardButton('ОФД', callback_data='ОФД')
    itembtn4 = types.InlineKeyboardButton('ККТ', callback_data='ККТ')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4)
    markup.add(itembtn1, itembtn2)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_mk(bot, callback_query):  # <--- формируем меню с тестами для Маркета
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Маркет', callback_data='Маркет')
    itembtn2 = types.InlineKeyboardButton('ЕГАИС', callback_data='ЕГАИС')
    itembtn3 = types.InlineKeyboardButton('КМК', callback_data='КМК')
    itembtn4 = types.InlineKeyboardButton('Меркурий в Маркете', callback_data='Меркурий в Маркете')
    itembtn5 = types.InlineKeyboardButton('Маркировка в Маркете', callback_data='Маркировка в Маркете')
    itembtn6 = types.InlineKeyboardButton('РАР', callback_data='РАР')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5)
    markup.add(itembtn6)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_buh(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('ОСНО', callback_data='ОСНО')
    itembtn2 = types.InlineKeyboardButton('ЕНВД', callback_data='ЕНВД')
    itembtn3 = types.InlineKeyboardButton('УСН', callback_data='УСН')
    itembtn4 = types.InlineKeyboardButton('ОПФ. Реквизиты. Взносы ИП', callback_data='ОПФ. Реквизиты. Взносы ИП')
    itembtn5 = types.InlineKeyboardButton('Сотрудники', callback_data='Сотрудники')
    itembtn6 = types.InlineKeyboardButton('БО и бухучет', callback_data='БО и бухучет')
    itembtn7 = types.InlineKeyboardButton('Работа в сервисе', callback_data='Работа в сервисе')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5)
    markup.add(itembtn6, itembtn7)

    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


def test_elb(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn4 = types.InlineKeyboardButton('Реквизиты и ОПФ', callback_data='Реквизиты и ОПФ')
    itembtn5 = types.InlineKeyboardButton('Налоги и взносы', callback_data='Налоги и взносы')
    itembtn6 = types.InlineKeyboardButton('Сотрудники', callback_data='Сотрудники.Эльба')
    itembtn7 = types.InlineKeyboardButton('Работа в сервисе', callback_data='Работа в сервисе.Эльба')
    itembtn8 = types.InlineKeyboardButton('БО', callback_data='БО.Эльба')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn4, itembtn5, itembtn8)
    markup.add(itembtn6, itembtn7)
    markup.add(itembtn12)
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, reply_markup=markup)


# ----------------------------- Главное меню - "кейсы" ---------------------------------- #
def praktics(bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Кейсы')
    def tests_h(callback_query: CallbackQuery):
        bot.answer_callback_query(callback_query.id)

        practicks_data[callback_query.from_user.id] = 'PR'  # <-- Ставим метку что мы нажали кнопку "Кейсы"
        if tests_data[callback_query.from_user.id] == 'DD':
            prk_diadoc(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'EDI':
            prk_edi(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'extrn':
            prk_ext(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'UC':
            prk_uc(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'MK':
            prk_mk(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'FMS':
            prk_fms(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'OFD':
            prk_ofd(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'BUH':
            prk_buh(bot, callback_query)

        elif tests_data[callback_query.from_user.id] == 'ELB':
            prk_elb(bot, callback_query)


# ------------  Клавиатура кейсов для каждого отдела -----------------#
def prk_wic(bot, message):
    sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as Abc:
        pass

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Поиск знаний', callback_data='WIC.Поиск_знаний')
    itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='WIC.Кейсы')


    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')

    markup.add(itembtn1, itembtn2)
    markup.add(itembtn3)

    bot.send_message(chat_id=message.from_user.id, text="Выбери тему: ", reply_markup=markup)

def other_service_prk(bot, message):
    sql_user(bot, message)

    try:
        bot.edit_message_reply_markup(message.from_user.id, message.message_id - 1)
    except Exception as Abc:
        pass

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Билли', callback_data='Билли')
    itembtn2 = types.InlineKeyboardButton('КабУЦ', callback_data='КабУЦ')
    itembtn4 = types.InlineKeyboardButton('Клиент-Сервис', callback_data='Клиент-Сервис')


    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')

    markup.add(itembtn1, itembtn2, itembtn4)
    markup.add(itembtn3)

    bot.send_message(chat_id=message.from_user.id, text="Выбери тему: ", reply_markup=markup)


def prk_ext(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()

    itembtn3 = types.InlineKeyboardButton('Интерфейс', callback_data='Интерфейс')
    itembtn4 = types.InlineKeyboardButton('Режим работы', callback_data='Режим работы')
    itembtn5 = types.InlineKeyboardButton('ФНС', callback_data='ФНС')
    itembtn6 = types.InlineKeyboardButton('ИОН', callback_data='ИОН')
    itembtn7 = types.InlineKeyboardButton('Таблица отчетности', callback_data='Таблица отчетности')
    itembtn8 = types.InlineKeyboardButton('Письма ФНС', callback_data='Письма ФНС')
    itembtn9 = types.InlineKeyboardButton('ПФР', callback_data='ПФР')
    itembtn10 = types.InlineKeyboardButton('НДС и требования', callback_data='НДС и требования')
    itembtn11 = types.InlineKeyboardButton('НДФЛ', callback_data='НДФЛ')
    itembtn13 = types.InlineKeyboardButton('Росстат', callback_data='Росстат')
    itembtn14 = types.InlineKeyboardButton('РСВ', callback_data='РСВ')
    itembtn15 = types.InlineKeyboardButton('Заполнение ПФР', callback_data='Заполнение ПФР')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4, itembtn5)
    markup.add(itembtn6, itembtn7, itembtn8)
    markup.add(itembtn9, itembtn10, itembtn11)
    markup.add(itembtn13, itembtn14, itembtn15)
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_buh(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn8 = types.InlineKeyboardButton('Работа в сервисе', callback_data='Работа в сервисе')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn8)

    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_diadoc(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn5 = types.InlineKeyboardButton('Web', callback_data='Web.Диадок')
    itembtn6 = types.InlineKeyboardButton('Модуль', callback_data='Модуль.Диадок')
    itembtn7 = types.InlineKeyboardButton('Роуминг', callback_data='Роуминг.Диадок')
    itembtn8 = types.InlineKeyboardButton('Коннекторы', callback_data='Коннекторы.Дидаок')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn5, itembtn6, itembtn7)
    markup.add(itembtn8)
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_elb(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn5 = types.InlineKeyboardButton('Налоги и взносы', callback_data='Налоги и взносы')
    itembtn6 = types.InlineKeyboardButton('Сотрудники', callback_data='Сотрудники.Эльба')
    itembtn7 = types.InlineKeyboardButton('Работа в сервисе', callback_data='Работа в сервисе.Эльба')
    itembtn8 = types.InlineKeyboardButton('БО', callback_data='БО.Эльба')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn5, itembtn8)
    markup.add(itembtn6, itembtn7)
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_ofd(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn5 = types.InlineKeyboardButton('ОФД', callback_data='ОФД')
    itembtn1 = types.InlineKeyboardButton('API', callback_data='API')
    itembtn6 = types.InlineKeyboardButton('ККТ', callback_data='ККТ')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn5, itembtn6, itembtn1)

    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_edi(bot, callback_query):
    sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('EDI Web', callback_data='EDI Web')
    itembtn2 = types.InlineKeyboardButton('EDI 1C', callback_data='EDI 1C')
    itembtn4 = types.InlineKeyboardButton('Меркурий', callback_data='Меркурий')
    itembtn3 = types.InlineKeyboardButton('Поставки', callback_data='Поставки')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4)
    markup.add(itembtn12)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_fms(bot, callback_query):
    markup = types.InlineKeyboardMarkup()
    itembtn3 = types.InlineKeyboardButton('ФМС', callback_data='ФМС')
    itembtn4 = types.InlineKeyboardButton('Отель', callback_data='Отель')
    itembtn5 = types.InlineKeyboardButton('Фокус', callback_data='Фокус')
    itembtn6 = types.InlineKeyboardButton('Фокус API', callback_data='Фокус API')
    itembtn7 = types.InlineKeyboardButton('Компас', callback_data='Компас')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn3, itembtn4, itembtn5)
    markup.add(itembtn6, itembtn7)
    markup.add(itembtn12)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_uc(bot, callback_query):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Проекты УЦ', callback_data='Проекты УЦ')
    itembtn2 = types.InlineKeyboardButton('ЭТП', callback_data='ЭТП')
    itembtn3 = types.InlineKeyboardButton('ИС', callback_data='ИС')
    itembtn4 = types.InlineKeyboardButton('Закупки', callback_data='Закупки')
    itembtn5 = types.InlineKeyboardButton('Декларант', callback_data='Декларант')
    itembtn6 = types.InlineKeyboardButton('Школа', callback_data='Школа')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_mk(bot, callback_query):
    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Маркет', callback_data='Маркет')
    itembtn2 = types.InlineKeyboardButton('ЕГАИС', callback_data='ЕГАИС')
    itembtn3 = types.InlineKeyboardButton('КМК', callback_data='КМК')
    itembtn4 = types.InlineKeyboardButton('Меркурий в Маркете', callback_data='Меркурий в Маркете')
    itembtn5 = types.InlineKeyboardButton('Маркировка в Маркете', callback_data='Маркировка в Маркете')
    itembtn6 = types.InlineKeyboardButton('РАР', callback_data='РАР')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


# ---------------------------------------------------#
# ------ Проверяем по какому продукту сейчас проходит тестирование ------------#
def check_product(callback_query):
    if tests_data[callback_query.from_user.id] == 'DD':
        db = db_data['DD']
    elif tests_data[callback_query.from_user.id] == 'EDI':
        db = db_data['EDI']
    elif tests_data[callback_query.from_user.id] == 'extrn':
        db = db_data['KE']
    elif tests_data[callback_query.from_user.id] == 'UC':
        db = db_data['UC']
    elif tests_data[callback_query.from_user.id] == 'MK':
        db = db_data['MK']
    elif tests_data[callback_query.from_user.id] == 'FMS':
        db = db_data['FMS']
    elif tests_data[callback_query.from_user.id] == 'OFD':
        db = db_data['OFD']
    elif tests_data[callback_query.from_user.id] == 'BUH':
        db = db_data['BH']
    elif tests_data[callback_query.from_user.id] == 'ELB':
        db = db_data['ELB']
    elif tests_data[callback_query.from_user.id] == 'INST':
        db = db_data['INST']
    elif tests_data[callback_query.from_user.id] == 'WIC':
        db = db_data['WIC']
    elif tests_data[callback_query.from_user.id] == 'OTHER':
        db = db_data['OTHER']
    else:
        db = db_data['all']

    return db


def get_max_row(sheet):  # <--- Функция для получения максимального числа вопросов
    number_A = 1  # <--- Это число для ячейки в столбике А
    max_row = 0  # <--- Максимальное число вопросов

    while sheet[f'{chr(65) + str(number_A)}'].value != 'stop':
        if sheet[f'{chr(65) + str(number_A)}'].value != None:
            max_row += 1
            number_A += 1
        else:
            break

    return max_row

def random_question(id_user, max_row):

    if len(rand_question[id_user]) < 1:
        for i in range(2, max_row + 1):
            rand_question[id_user].append(i)

    number = random.choice(rand_question[id_user])  # <--- получаем случайное число из списка
    rand_question[id_user].remove(number)

    return number


def answers(bot, callback_query):  # <--- Функция отвечающая за поиск и отправку вопросов по тестам
    print('1')
    db = check_product(callback_query)

    name_sheet = db.sheetnames[int(a[callback_query.from_user.id])]  # <--- Получаем название вкладки (продукта) в таблице
    sheet = db[name_sheet]  # <--- Загружаем все вопросы во вкладке, имя которой узнали выше

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    if str(results[1]) == 'None':
        data_base['BotUsers'][callback_query.from_user.id]['UserPage'] = str(a[callback_query.from_user.id])
        data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'] = get_max_row(sheet)

    data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'] = 'None'

    results = int(data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'])

    try:
        ress = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand']) + 1  # смотрим сколько всего вопросов было и добавляем 1
    except:
        ress = 0 + 1

    print('ress = ', ress)

    if ress == results:  # <--- Если ответил на все вопросы
        print('Task complete!')

        results_cmpl = data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
                       data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

        sc = results_cmpl
        results_cmpl = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])
        ans_q = results_cmpl

        bot.send_message(callback_query.from_user.id, f'Ты ответил на все вопросы! \n'
                                                      f'\nКоличество вопросов, которые были заданы: {str(ans_q)}'
                                                      f'\nПравильных ответов: {int(sc[1])}')

        callback_check[callback_query.from_user.id] = 'end'

    else:  # <--- Если ответил не на все вопросы
        t = 0
        while t != 1:
            try:  # <--- Если номер вопроса получится тем же на который уже был ответ то получим исключение
                # --------------- Ниже мы получаем рандомное число вопроса, и записываем егов BotUsers UserRand ------- #
                max_row = get_max_row(sheet)
                number = random_question(callback_query.from_user.id, max_row) #Получаем случайный вопрос


                try:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                except:
                    data_base['UserQuestions'][callback_query.from_user.id] = {'UserChat': '0',
                                                                               'UserRand': []}

                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                try:
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']
                except:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserRand'] = []
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']

                if str(number) not in user_rand: #<-- Если сгенерированного вопроса нет в списке заданных вопросов, то его мы опубликуем
                    user_rand.append(str(number))
                else:
                    continue

                data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(number)

                t += 1
            except Exception as ty:
                print(ty)

        # --- Делаем запрос в БД с целью узнать число в BotUsers->UserRand, UserRowQuestions ------ #
        results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
                  data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions']

        fs = results  # <-- тут мы имеем сразу UserRand и UserRowQuestions
        # sc = re.findall(r'\b\d+\b', fs) #<--- распарсиваем их чтоб можно было выбрать, но надо ли?
        print('Номер вопроса =', int(fs[0]), type(fs), 'из', int(fs[1]), type(fs))

        # ----- формируем сообщение для отправки вопроса ------ #

        message_question = f'<b>Вопрос</b>: {sheet[chr(65) + str(fs[0])].value}'
        i = 1
        # Ниже уже делаем запрос к екселю через chr получаем букву столбика и смотрим что в строке (номер вопроса)
        while sheet[chr(65 + i) + str(fs[0])].value != 'stop':  # пока не натыкаемся на стоп продолжаем смотреть ячейки
            if sheet[chr(65 + i) + str(fs[0])].value != None:  # если наткнулись на пустую ячейку, то тормозим
                message_question += f'\n<b>{i}</b>. {sheet[chr(65 + i) + str(fs[0])].value}'
                i += 1
            else:
                break
        # ----------------------------------------------------- #

        markup = types.InlineKeyboardMarkup()
        #itembtn_test = types.InlineKeyboardButton('Ответить', callback_data='Ответить')
        itembtn1 = types.InlineKeyboardButton('Результаты', callback_data='Результаты')
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')

        markup.add(itembtn1)
        markup.add(itembtn2)

        message_question += '\n\nПиши правильные варианты ответа цифрами без дополнительных символов и пробелов. \n' \
                            'Помни! Вариантов ответов может быть несколько.\n' \
                            'Если уверен в правильности ответа → Нажми «Отправить».'

        message_id = bot.send_message(callback_query.from_user.id, message_question, parse_mode='HTML', reply_markup=markup)

        save_message_id['message_text'][callback_query.from_user.id] = message_id.text

        save_message_id['check_answer'][callback_query.from_user.id] = message_id.message_id  # сохраняем ID заданного вопроса
        callback_check[callback_query.from_user.id] = 'tests' # Указываем что тест еще выполняется (для обработки текстового сообщения)


    print('results[0][1] = ', results[1])


def answers_prk(bot, callback_query):  # <--- Функция отвечающая за поиск и отправку вопросов по кейсам
    practicks_data['check_attempt'][callback_query.from_user.id] = '1'

    db = check_product(callback_query)

    name_sheet = db.sheetnames[int(a[callback_query.from_user.id])]  # <--- Получаем название вкладки (продукта) в таблице
    sheet = db[name_sheet]  # <--- Загружаем все вопросы во вкладке, имя которой узнали выше

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    if str(results[1]) == 'None':
        data_base['BotUsers'][callback_query.from_user.id]['UserPage'] = str(a[callback_query.from_user.id])
        data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'] = get_max_row(sheet)

    data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'] = 'None'

    results = int(data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'])

    try:
        ress = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand']) + 1  # смотрим сколько всего вопросов было и добавляем 1
    except:
        ress = 0 + 1

    print('ress = ', ress)

    if ress == results:  # <--- Если ответил на все вопросы
        print('Task complete!')

        results_cmpl = data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
                       data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

        sc = results_cmpl
        results_cmpl = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])
        ans_q = results_cmpl

        bot.send_message(callback_query.from_user.id, f'Ты выполнил все кейсы! \n'
                                                      f'\nКоличество кейсов, которые были заданы: {str(ans_q)}'
                                                      f'\nПравильных ответов: {int(sc[1])}')
        callback_check[callback_query.from_user.id] = 'end'

    else:  # <--- Если ответил не на все вопросы
        t = 0
        while t != 1:
            try:  # <--- Если номер вопроса получится тем же на который уже был ответ то получим исключение
                # --------------- Ниже мы получаем рандомное число вопроса, и записываем егов BotUsers UserRand ------- #
                max_row = get_max_row(sheet)
                number = random_question(callback_query.from_user.id, max_row)  # <--- генерируем случайное число чтобы получить вопрос

                try:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                except:
                    data_base['UserQuestions'][callback_query.from_user.id] = {'UserChat': '0',
                                                                               'UserRand': []}

                    data_base['UserQuestions'][callback_query.from_user.id]['UserChat'] = str(callback_query.from_user.id)
                try:
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']
                except:
                    data_base['UserQuestions'][callback_query.from_user.id]['UserRand'] = []
                    user_rand = data_base['UserQuestions'][callback_query.from_user.id]['UserRand']

                if str(number) not in user_rand:
                    user_rand.append(str(number))
                else:
                    continue
                data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(number)

                t += 1
            except Exception as ty:
                print(ty)

        # --- Делаем запрос в БД с целью узнать число в BotUsers->UserRand, UserRowQuestions ------ #
        results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
                  data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions']

        fs = results  # <-- тут мы имеем сразу UserRand и UserRowQuestions
        print('Номер вопроса = ', int(fs[0]), type(fs), 'из ', int(fs[1]), type(fs))

        # ----- формируем сообщение для отправки вопроса ------ #
        mes_qv = f'{sheet[chr(65) + str(fs[0])].value}' #Формируем вопрос, чтобы дальше его проверить на недопустимые символы

        if save_check['wic_search'][callback_query.from_user.id] == True: #Смотрим активна ли переменная Поиск знаний
            message_question = '' #Задача убрать слово "Кейс" из сообщения в вопросе
        else:
            message_question = f'<b>Кейс</b>: '

        if '<' in mes_qv or '>' in mes_qv: #Ищем есть ли в вопросе знак <, он вызывает конфликт при parse_mode=HTML
            for i in mes_qv: #Пробегаем по каждому символу в вопросе
                if i == '<':
                    i = '&lt' #Если нашли этот знак то меняем его на &lt
                message_question += i #Добавляем каждую букву к итоговому сообщению
        else: #Если символа такого в вопросе нет, то к итоговому сообщению добавим сразу вопрос
            message_question += mes_qv

        message_question += f'\n\nПиши правильные ответы в соответствии с требованиями вопросов. ' \
                            f'\nТочку в конце не ставь.\n' \
                            f'Если уверен в правильности ответа → Нажми «Отправить».'

        # Ниже уже делаем запрос к екселю через chr получаем букву столбика и смотрим что в строке (номер вопроса)

        # ----------------------------------------------------- #

        markup = types.InlineKeyboardMarkup()
        #itembtn_test = types.InlineKeyboardButton('Ответить', callback_data='Ответить')
        itembtn1 = types.InlineKeyboardButton('Результаты', callback_data='Результаты')
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')

        markup.add(itembtn1)
        markup.add(itembtn2)

        if sheet[chr(67) + str(fs[0])].value != None:  # <-- Смотрим на столбик "С", ищем путь к файлу для отправки. Если есть то

            file_id[callback_query.from_user.id] = file_dir
            file_id[callback_query.from_user.id] = f'{file_id[callback_query.from_user.id]}{sheet[chr(67) + str(fs[0])].value}'

            try:
                with open(file_id[callback_query.from_user.id], 'rb') as file:
                    if file_id[callback_query.from_user.id].split('.')[-1] in ('png', 'jpg', 'jpeg', 'bmp'):
                        message_id = bot.send_photo(callback_query.from_user.id, file, reply_markup=markup, caption=message_question, parse_mode='HTML')
                    else:
                        message_id = bot.send_document(callback_query.from_user.id, file, reply_markup=markup, caption=message_question, parse_mode='HTML')

            except:
                pass

            del file_id[callback_query.from_user.id]
        else: #<--- Если файл не должен отправляться
            message_id = bot.send_message(callback_query.from_user.id, message_question, parse_mode='HTML', reply_markup=markup)

        save_message_id['message_text'][callback_query.from_user.id] = message_question
        save_message_id['check_answer'][callback_query.from_user.id] = message_id.message_id  # сохраняем ID заданного вопроса
        callback_check[callback_query.from_user.id] = 'practicks'



    print('results[0][1] = ', results[1])


def true_ans(callback_query):  # <--- Функция отвечает за запись правильных ответов по тестам, чтобы в дальнейшем сравнить с тем что написал пользователь
    i = 0
    ans[callback_query.from_user.id] = []

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    print('При проверке, номер вопроса =', int(results[0]), 'номер темы в экселе =', int(results[1]), 'ID пользователя =', str(callback_query.from_user.id))

    db = check_product(callback_query)
    sheet = db[db.sheetnames[int(results[1])]]

    try:
        while sheet[chr(83 + i) + str(results[0])].value != 'stop':
            if sheet[chr(83 + i) + str(results[0])].value != None:
                ans[callback_query.from_user.id].append(str(sheet[chr(83 + i) + str(results[0])].value))
                i += 1
            else:
                break
    except:
        if i >= 8:
            i = 0
            while sheet['A' + chr(65 + i) + str(results[0])].value != 'stop':
                if sheet['A' + chr(65 + i) + str(results[0])].value != None:
                    ans[callback_query.from_user.id].append(str(sheet['A' + chr(65 + i) + str(results[0])].value))
                    i += 1
                else:
                    break

    print('правильные ответы - ', ans[callback_query.from_user.id])
    return ans[callback_query.from_user.id]


def true_ans_prk(callback_query):  # <--- Функция отвечает за запись правильных ответов по тестам, чтобы в дальнейшем сравнить с тем что написал пользователь
    ans[callback_query.from_user.id] = []
    ans['lower'][callback_query.from_user.id] = []

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    print('При проверке, номер вопроса = ', int(results[0]), 'номер темы в экселе = ', int(results[1]))

    db = check_product(callback_query)
    sheet = db[db.sheetnames[int(results[1])]]
    sheet = (str(sheet[chr(66) + str(results[0])].value))
    for i in sheet.split(';'):
        ans['lower'][callback_query.from_user.id].append(i)
        ans[callback_query.from_user.id].append(i.strip().upper())

    print('правильные ответы - ', ans[callback_query.from_user.id])
    return ans[callback_query.from_user.id], ans['lower'][callback_query.from_user.id]


def continue_(bot, message):  # <--- функция обработки простых текстовых сообщений
    print("Ввод пользователя - ", message.text)

    if callback_check.get(message.chat.id) in ('tests', 'practicks', 'admin'):  # Если пользователь не нажимал "Сообщить об ошибке"
        try:
            data_base['BotUsers'][message.chat.id]['UserAnswer'] = str(message.text)
        except:
            data_base['BotUsers'][message.chat.id] = {'UserAnswer': 'None'}
            data_base['BotUsers'][message.chat.id]['UserAnswer'] = str(message.text)



    elif callback_check[message.chat.id] == '1':  # Если пользователь нажал на сообщить об ошибке
        bot.send_message(message.chat.id, 'Ты еще не выбрал о какой ошибке хочешь сообщить. Если не хочешь сообщать, нажми «Отмена».')

    elif callback_check[message.chat.id] == '2':  # Если пользователь нажал на сообщить об ошибке и выбрал "о технческой ошибке"
        text_error = 'Антоха, конс нашел техническую ошибку: '
        bot.send_message(toha_id, text=f'{text_error}{message.text}\nОб ошибке сообщил - @{message.from_user.username}')
        bot.send_message(message.chat.id, 'Спасибо! Информация передана ответственному.\nЕсли понадобится уточнение он с тобой свяжется.'
                                          '\nМожешь продолжить отвечать на вопросы.')
        callback_check[message.from_user.id] = save_check[message.from_user.id]

    elif callback_check[message.chat.id] == '3':  # Если пользователь нажал на сообщить об ошибке и выбрал "об ошибке в вопросе"
        if tests_data[message.chat.id] == 'DD':
            product = 'Диадок'

        elif tests_data[message.chat.id] == 'EDI':
            product = 'ЕДИ'

        elif tests_data[message.chat.id] == 'extrn':
            product = 'Экстерн'

        elif tests_data[message.chat.id] == 'UC':
            product = 'УЦ'

        elif tests_data[message.chat.id] == 'MK':
            product = 'МК'

        elif tests_data[message.chat.id] == 'FMS':
            product = 'ФМС'

        elif tests_data[message.chat.id] == 'OFD':
            product = 'ОФД'

        elif tests_data[message.chat.id] == 'BUH':
            product = 'Бухгалтерия'

        elif tests_data[message.chat.id] == 'ELB':
            product = 'Эльба'

        text_error = f'<b>Лёха, конс нашел ошибку в вопросе!</b>\nОтдел: {product}.\n\n{callback_check["text"][message.chat.id]}'
        bot.send_message(alex_id, text=f'{text_error}Комментарий: {message.text}\nОб ошибке сообщил - @{message.from_user.username}', parse_mode='HTML')

        bot.send_message(message.chat.id, 'Спасибо! Информация передана ответственному.\nЕсли понадобится уточнение он с тобой свяжется.'
                                          '\nМожешь продолжить отвечать на вопросы.')
        callback_check[message.from_user.id] = save_check[message.from_user.id]




def check_answer(bot, callback_query):  # Функция прооверяет правильность введённого ответа от пользователя по тестам
    print(callback_query.from_user.id)

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserPage']

    print('1 if')
    if results[1] == 'None':  # <---смотрим в БД пустой ли ответ
        bot.edit_message_text("Ты вводишь пустой ответ. Пока не напишешь варианты ответа, дальше не двинемся.",
                              chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id]
                              )
    else:
        print('2 if')

        markup = types.InlineKeyboardMarkup()
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')
        markup.add(itembtn2)
        bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=save_message_id['check_answer'][callback_query.from_user.id],
                              text=save_message_id['message_text'][callback_query.from_user.id], reply_markup=markup)

        check_true_ans = true_ans(callback_query)
        if sorted(set(map(str, results[1]))) == check_true_ans:
            bot.edit_message_text("Красава!", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
            data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'] = str(int(results[2]) + 1)

        else:
            check_true_ans_1 = ''
            for i in check_true_ans:
                check_true_ans_1 += f'{i}'
            if len(check_true_ans) == 1:
                bot.edit_message_text(f"Неправильно! Учи! \nПравильный вариант: {check_true_ans_1}.", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
            else:
                bot.edit_message_text(f"Неправильно! Учи! \nПравильные варианты: {check_true_ans_1}.", chat_id=callback_query.from_user.id,
                                      message_id=save_message_id['message_id'][callback_query.from_user.id])
        data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(int(results[0]) + 1)

        h = 0
        while h != 1:
            answers(bot, callback_query)
            h += 1


def check_answer_prk(bot, callback_query):  # Функция прооверяет правильность введённого ответа от пользователя по кейсам

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRand'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserPage']
    print('1 if')

    if results[1] == 'None':  # <---смотрим в БД пустой ли ответ
        bot.edit_message_text("Ты вводишь пустой ответ. Пока не напишешь варианты ответа, дальше не двинемся.",
                              chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
        return
    else:
        print('2 if')
        db_results = str(results[1])

        markup = types.InlineKeyboardMarkup()
        itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')
        markup.add(itembtn2)
        try:
            bot.edit_message_caption(chat_id=callback_query.from_user.id, message_id=save_message_id['check_answer'][callback_query.from_user.id],
                                  caption=save_message_id['message_text'][callback_query.from_user.id], reply_markup=markup, parse_mode='HTML')
        except:
            bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=save_message_id['check_answer'][callback_query.from_user.id],
                                     text=save_message_id['message_text'][callback_query.from_user.id], reply_markup=markup, parse_mode='HTML')

        # Проверям правильный ли ответ
        check_true_ans_prk, lower_ans_prk = true_ans_prk(callback_query)
        if db_results.upper() in check_true_ans_prk:
            bot.edit_message_text("Красава!", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])
            data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns'] = str(int(results[2]) + 1)
        else:
            if practicks_data['check_attempt'][callback_query.from_user.id] == '1':
                markup = types.InlineKeyboardMarkup()
                #itembtn_test = types.InlineKeyboardButton('Ответить', callback_data='Ответить')
                itembtn1 = types.InlineKeyboardButton('Результаты', callback_data='Результаты')
                itembtn2 = types.InlineKeyboardButton('Сообщить об ошибке', callback_data='Сообщить об ошибке')

                markup.add(itembtn1)
                markup.add(itembtn2)

                message_id = bot.edit_message_text("Неправильно! У тебя есть еще одна попытка.", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id], reply_markup=markup)
                practicks_data['check_attempt'][callback_query.from_user.id] = '0'
                data_base['BotUsers'][callback_query.from_user.id]['UserAnswer'] = 'None'
                save_message_id['check_answer'][callback_query.from_user.id] = message_id.message_id
                return
            else:
                bot.edit_message_text(f"Неправильно! Учи!\nПравильный ответ: {lower_ans_prk[0]}.", chat_id=callback_query.from_user.id, message_id=save_message_id['message_id'][callback_query.from_user.id])

        data_base['BotUsers'][callback_query.from_user.id]['UserRand'] = str(int(results[0]) + 1)
        h = 0
        while h != 1:
            answers_prk(bot, callback_query)
            h += 1


def lesten_res(bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Результаты')
    def les_res(callback_query: CallbackQuery):
        res(bot, callback_query)


def res(bot, callback_query):  # Функция публикует результат

    results = data_base['BotUsers'][callback_query.from_user.id]['UserRowQuestions'], \
              data_base['BotUsers'][callback_query.from_user.id]['UserCounterTrueAns']

    sc = results
    results = len(data_base['UserQuestions'][callback_query.from_user.id]['UserRand'])
    ans_q = results

    bot.send_message(text=f'Результаты! \nКоличество всех вопросов: {int(sc[0]) - 1} '
                          f'\nКоличество вопросов, которые были заданы: {str(ans_q)}'
                          f'\nПравильных ответов: {int(sc[1])}',
                     chat_id=callback_query.from_user.id)

    markup = types.ReplyKeyboardMarkup()
    itembtn_back = types.KeyboardButton('В меню')
    markup.add(itembtn_back)


# ------------------------------- Обработка Inline клавиатуры ---------------------------------------#
def send_error(bot, callback_query):  # <--- Меню Inline "Сообщить об ошибке"

    error_markup = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('О технической ошибке', callback_data='error_tehn')
    itembtn2 = types.InlineKeyboardButton('Об ошибке в вопросе', callback_data='error_txt')
    itembtn3 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')

    error_markup.add(itembtn1, itembtn2)
    error_markup.add(itembtn3)
    bot.send_message(callback_query.from_user.id, 'Выбери направление о какой ошибке хочешь сообщить?', reply_markup=error_markup)
    save_check[callback_query.from_user.id] = callback_check[callback_query.from_user.id]

    callback_check[callback_query.from_user.id] = '1'  # Присваиваем ИД переменную, чтобы дальше фильтровать
    callback_check['text'][callback_query.from_user.id] = callback_query.message.text.split('Пиши')[0]



def cancel_error(bot):  # <---  Обрабатываем если нажали "отмена"
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Cancel')  # <--- кнопка отмены
    def error_cancel(callback_query: CallbackQuery):
        bot.answer_callback_query(callback_query.id)
        bot.edit_message_text('Действие отменено', chat_id=callback_query.from_user.id,
                              message_id=callback_query.message.message_id)
        del callback_check[callback_query.from_user.id]


def tehn_error(bot):  # <---  Обрабатываем если нажали "о технической ошибке"
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'error_tehn')  # <--- кнопка о технической ошибке
    def error_tehn(callback_query: CallbackQuery):
        bot.answer_callback_query(callback_query.id)
        bot.edit_message_text('Опиши полностью техническую ошибку, которая у тебя произошла.', chat_id=callback_query.from_user.id,
                              message_id=callback_query.message.message_id)

        callback_check[callback_query.from_user.id] = '2'  # Присваиваем ИД переменную, чтобы дальше фильтровать


def txt_error(bot):  # <---  Обрабатываем если нажали "об ошибке в вопросе"
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'error_txt')  # <--- кнопка "об ошибке в вопросе"
    def error_txt(callback_query: CallbackQuery):
        bot.answer_callback_query(callback_query.id)
        bot.edit_message_text('Опиши полностью ошибку в вопросе.', chat_id=callback_query.from_user.id,
                              message_id=callback_query.message.message_id)

        callback_check[callback_query.from_user.id] = '3'  # Присваиваем ИД переменную, чтобы дальше фильтровать


def btn_back_menu(bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Назад')  # <--- кнопка "об ошибке в вопросе"
    def btn_back(callback_query: CallbackQuery):
        try:
            del practicks_data[callback_query.from_user.id]
        except:
            pass

        markup_1 = types.InlineKeyboardMarkup()

        itembtn1 = types.InlineKeyboardButton('Тесты', callback_data='Тесты')
        itembtn2 = types.InlineKeyboardButton('Кейсы', callback_data='Кейсы')
        itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')

        markup_1.add(itembtn1, itembtn2)
        markup_1.add(itembtn12)

        try:
            bot.edit_message_text(chat_id=callback_query.from_user.id, text="Какой вид обучения тебя интересует?",
                                  message_id=callback_query.message.message_id, reply_markup=markup_1)
        except Exception as E:
            print(E.args)

        bot.answer_callback_query(callback_query.id)

def update_tables(bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Обновить таблицы')  # <--- кнопка "об ошибке в вопросе"
    def upd_tb(callback_query: CallbackQuery):
        db_data['all'] = openpyxl.load_workbook('./Data/УЦ.xlsx', read_only=True)
        db_data['UC'] = openpyxl.load_workbook('./Data/УЦ.xlsx', read_only=True)
        db_data['FMS'] = openpyxl.load_workbook('./Data/ФМС.xlsx', read_only=True)
        db_data['MK'] = openpyxl.load_workbook('./Data/Маркет.xlsx', read_only=True)
        db_data['EDI'] = openpyxl.load_workbook('./Data/Ритейл.xlsx', read_only=True)
        db_data['DD'] = openpyxl.load_workbook('./Data/Диадок.xlsx', read_only=True)
        db_data['KE'] = openpyxl.load_workbook('./Data/KE.xlsx', read_only=True)
        db_data['BH'] = openpyxl.load_workbook('./Data/Бухгалтерия.xlsx', read_only=True)
        db_data['ELB'] = openpyxl.load_workbook('./Data/Эльба.xlsx', read_only=True)
        db_data['OFD'] = openpyxl.load_workbook('./Data/ОФД.xlsx', read_only=True)
        db_data['INST'] = openpyxl.load_workbook('./Data/Установка.xlsx', read_only=True)

        bot.answer_callback_query(callback_query.id)

        bot.send_message(chat_id=callback_query.from_user.id, text='Таблицы успешно обновлены!')

def reg_user(bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Зарегистрировать пользователя')  # <--- кнопка "об ошибке в вопросе"
    def add_u(callback_query: CallbackQuery):
        add_user(callback_query, data_base)
        bot.answer_callback_query(callback_query.id)

def del_user(bot):
    @bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Удалить пользователя')  # <--- кнопка "об ошибке в вопросе"
    def dell_user(callback_query: CallbackQuery):
        rm_user(callback_query, data_base)
        bot.answer_callback_query(callback_query.id)