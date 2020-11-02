# Программа будет брать рандомную строку из xls файла и выводить в виде вопроса с 4 вариантами ответа.
# Нужно ответить однозначно верно на поставленный вопрос.
# Ставим ограничение на 20 вопросов на кейс, чтобы выяснить процент правильных ответов.
# Корректность ответов проверяются сразу.

import random
import telebot
import openpyxl
import Proxy_bot
from time import sleep
from telebot import types
from telebot import apihelper
from modul_for_bot import *
from WhiteList import *
from telebot.types import CallbackQuery

#ip_port = Proxy_bot.read_proxy()
#telebot.apihelper.proxy = {'https':'https://{}'.format(ip_port)}

#bot = telebot.TeleBot('935355674:AAFDc4BwAB4jQtugRIpcGiEPqyhKZqv3XSU',  threaded=False)
bot = telebot.TeleBot('1253732018:AAESPvgR9YfmnTAHtHRMWJ8tjOmApA_qSyI',  threaded=False) #OOHelper

# Открываем файл на чтение
#db = xlrd.open_workbook('111.xlsx')
#db = openpyxl.load_workbook('./Data/111.xlsx')

global a
a = 0
info = "Выбери тему и вид обучения для подготовки." \
       "\n\n*Тесты:* пиши правильные варианты ответа цифрами без пробелов и дополнительных символов. Вариантов может быть несколько." \
       "\n\n*Кейсы:* пиши правильные ответы в соответствии с требованиями вопросов. " \
       "\n\nДля того, чтобы ответить на вопрос:" \
       "\n1. Напиши ответ." \
       "\n2. Нажми «Отправить», если уверен в предоставленных вариантах." \
       "\n\nЕсли во время прохождения теста ты перейдешь в меню, то результат сбросится, помни об этом!"


@bot.message_handler(commands=["start"])
def greeting(message):
    if echo(message) == True:
        question(bot, message)


@bot.message_handler(commands=["help"])
def help(message):
    if echo(message) == True:
        bot.send_message(message.chat.id, info, parse_mode='Markdown')

@bot.message_handler(commands=["admin"]) #<---- Обновить таблицы в памяти, после изменений
def admin_menu(message):
    if message.chat.id in (233770916, 391368365):
        Admin_menu(message, bot)
    else:
        bot.send_message(message.from_user.id, 'У тебя нет доступа к данному функционалу.')


@bot.message_handler(func=lambda message: message.text == "В меню")
def back(message):
    if echo(message) == True:
        question(bot, message)

@bot.message_handler(func=lambda message: message.text == "Назад")
def back(message):
    if echo(message) == True:
        back_to_menu(bot, message) #Запускаем test_menu из modul_for_bot

@bot.message_handler(func=lambda message: message.text == "Помощь")
def help_text(message):
    if echo(message) == True:
        bot.send_message(message.chat.id, info, parse_mode='Markdown')

reg_user(bot)
del_user(bot)
update_tables(bot)
cancel_error(bot) #Кнопка Отмена
tehn_error(bot)
txt_error(bot)
lesten_res(bot)
btn_back_menu(bot) #Кнопка назад
#---- инициализируем меню тестов\кейсов -----#
tests(bot)
praktics(bot)

#----- Главное меню -------#
WIC_menu("WIC", bot)
Inst_menu("Установка", bot)
DD_menu("Диaдoк", bot)
EDI_menu("Ритейл", bot)
ext_menu("Экстерн", bot)
UC_menu("УЦ", bot)
M_menu("Maркет", bot)
OFD_menu("OФД", bot)
FMS_menu("ФMС", bot)
Buh_menu("Бухгалтерия", bot)
Elba_menu("Эльба", bot)

#--------------------------#

#------ Кнопки WIC ------#
quest('WIC.Поиск_знаний', 0, bot)
quest('WIC.Кейсы', 1, bot)

#------ Кнопки Установки -----#
quest('Компоненты для работы с ЭП', 0, bot)
quest('Запрос КЭП', 1, bot)
quest('Работа с ЭП', 2, bot)
quest('КЭП для ЕГАИС', 3, bot)
quest('Сертификаты УЦ', 4, bot)
quest('Работа с ЭП не на Windows', 5, bot)
quest('DSS', 6, bot)
quest('Установка общее', 7, bot)

#-----------Кнопки Диадок --------#
quest("Web.Диадок", 0, bot)
quest("Модуль.Диадок", 2,bot)
quest("Роуминг.Диадок", 4,bot)
quest("Коннекторы.Диадок", 6,bot)

#---- Кнопки КЭ ------#
quest('Интерфейс', 0, bot)
quest('Режим работы', 2, bot)
quest('ФНС', 4, bot)
quest('ИОН', 6, bot)
quest('Таблица отчетности', 8, bot)
quest('Письма ФНС', 10, bot)
quest('ПФР', 12, bot)
quest('НДС и требования', 14, bot)
quest('НДФЛ', 16, bot)
quest('Росстат', 18, bot)
quest('РСВ', 20, bot)
quest('Заполнение ПФР', 22, bot)

#-----Кнопки Бухгалтерия -----#
quest('ОСНО', 0, bot)
quest('ЕНВД', 1, bot)
quest('УСН', 2, bot)
quest('ОПФ. Реквизиты. Взносы ИП', 3, bot)
quest('Сотрудники', 4, bot)
quest('БО и бухучет', 5, bot)
quest('Работа в сервисе', 6, bot)

#------Кнопки Эльба-------#
quest('Реквизиты и ОПФ', 0, bot)
quest('Налоги и взносы', 1, bot)
quest('Сотрудники.Эльба', 3, bot)
quest('Работа в сервисе.Эльба', 5, bot)
quest('БО.Эльба', 7, bot)

#----- Кнопки ОФД --------#
quest("ОФД", 0, bot)
quest("ККТ", 2, bot)
quest("API", 4, bot)
quest("1C", 6, bot)

#----- Кнопки EDI (Ритейл) -----#
quest("EDI Web", 0, bot)
quest("EDI 1C", 2, bot)
quest("Поставки", 4, bot)
quest("Меркурий", 6, bot)

#--- Кнопки ФМС -----#
quest("ФМС", 0, bot)
quest("Отель", 2, bot)
quest("Фокус", 4, bot)
quest("Фокус API", 6, bot)
quest("Компас", 8, bot)

#----- Кнопки УЦ -----#
quest("Проекты УЦ", 0, bot)
quest("ЭТП", 2, bot)
quest("ИС", 4, bot)
quest("Закупки", 6, bot)
quest("Реестро", 8, bot)
quest("Контур.Торги", 9, bot)
quest("Декларант", 10, bot)
quest("Школа", 12, bot)

#----- Кнопки Маркета -----#
quest("Маркет", 0, bot)
quest("ЕГАИС", 2, bot)
quest("КМК", 4, bot)
quest("Меркурий в Маркете", 6, bot)
quest("Маркировка в Маркете", 8, bot)
quest("РАР", 10, bot)
#--------------------#

@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Ответить')
def ans_true(callback_query: CallbackQuery):
    bot.answer_callback_query(callback_query.id)
    if echo(callback_query) == True:
        try:
            del callback_check[callback_query.from_user.id]
        except:
            pass

        try:
            check_answer_id = save_message_id['check_answer'][callback_query.from_user.id] #ПОлучаем ID сообщения заданного послений раз вопроса
        except:
            check_answer_id = 0 #Если вопрос не задавался то ставим 0

        if check_answer_id == callback_query.message.message_id: #Совпадает ли ID запомненного вопроса с ID где мы нажали кнопку "Ответить"

            message = bot.send_message(callback_query.from_user.id, "Проверяем ответ.\nПодожди немного.")
            save_message_id['message_id'][callback_query.from_user.id] = message.message_id

            if practicks_data.get(callback_query.from_user.id) == 'PR':
                check_answer_prk(bot, callback_query)
            else:
                check_answer(bot, callback_query)

        else: #Если нажали Ответить не в последнем заданном вопросе, то
            bot.edit_message_text("Ты пытаешься ответить на вопрос, который задавался гораздо раньше.",
                              chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)

@bot.message_handler(func=lambda message: message.text == "Результаты")
def res0(message):
    if echo(message) == True:
        res(bot, message)

@bot.callback_query_handler(func=lambda callback_query: callback_query.data == 'Сообщить об ошибке')
def error_send(callback_query):
    if echo(callback_query) == True:
        send_error(bot, callback_query)


@bot.message_handler(content_types=['text'])
def answer0(message):

    print(message.message_id)

    if callback_check.get(message.from_user.id) == 'tests':
        continue_(bot, message)
        messages = bot.send_message(message.from_user.id, "Проверяем ответ.\nПодожди немного.")
        save_message_id['message_id'][message.from_user.id] = messages.message_id
        check_answer(bot, message)
        return

    elif callback_check.get(message.from_user.id) == 'practicks':
        continue_(bot, message)
        messages = bot.send_message(message.from_user.id, "Проверяем ответ.\nПодожди немного.")
        save_message_id['message_id'][message.from_user.id] = messages.message_id
        check_answer_prk(bot, message)
        return

    elif callback_check.get(message.from_user.id) == None:
        if echo(message) == True:
            messages = bot.send_message(message.from_user.id, "Ты ещё не выбрал тему для прохождения тестов.")
            save_message_id['message_id'][message.from_user.id] = messages.message_id

    continue_(bot, message)

while True:

    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as e:
        print(e.args)
        sleep(0.7)