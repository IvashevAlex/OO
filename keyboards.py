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


def question(bot, message):
    print(message.chat.id)

    modul_for_bot.sql_user(bot, message)

    # bot.send_message(message.chat.id, 'Диадок \nEDI \nЭкстерн \nУЦ \nУстановка')
    markup = types.ReplyKeyboardMarkup(row_width=4, resize_keyboard=True, one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('Диaдoк')
    itembtn2 = types.KeyboardButton('Pитейл')
    itembtn3 = types.KeyboardButton('Экстeрн')
    itembtn4 = types.KeyboardButton('Maркет')
    itembtn12 = types.KeyboardButton(' УЦ  ')
    itembtn13 = types.KeyboardButton('Устaнoвка')
    itembtn14 = types.KeyboardButton('WIС')
    itembtn15 = types.KeyboardButton('Bнутренние сервисы')
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
    bot.send_message(message.chat.id, "Привет :) Это бот Отдела Обучения.\n"
                                      "Выбери нужную тему с помощью кнопок внизу.", reply_markup=markup)


def test_menu(bot, message):
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
    itembtn12 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')

    markup_1.add(itembtn1, itembtn2)
    markup_1.add(itembtn12)

    try:
        bot.send_message(
            message.from_user.id, "Какой вид обучения тебя интересует?", reply_markup=markup_1)
    except Exception as E:
        pass


def Admin_menu(message, bot): #Описание функций для меню поместил в конец кода
    modul_for_bot.callback_check[message.from_user.id] = 'admin'
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
            del modul_for_bot.practicks_data[message.chat.id]
        except:
            pass
        modul_for_bot.tests_data[message.chat.id] = 'INST'
        modul_for_bot.sql_user(bot, message)
        test_INST(bot, message)  # <--- тут будет отправка и меню с выбором

def WIC_menu(name, bot):
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
    itembtn9 = types.InlineKeyboardButton('Отмена', callback_data='Cancel')


    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5, itembtn6)
    markup.add(itembtn7, itembtn8)
    markup.add(itembtn9)

    bot.send_message(message.chat.id, "Выбери тему: ", reply_markup=markup)

# ------------  Клавиатура кейсов для каждого отдела -----------------#
def prk_wic(bot, message):
    modul_for_bot.sql_user(bot, message)

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
    modul_for_bot.sql_user(bot, message)

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


def back_to_menu(bot, message):
    test_menu(bot, message)


def tests(bot):
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


Other_srvice_menu("Внутренние сервисы", bot)
WIC_menu("WIС", bot)
Inst_menu("Устaнoвка", bot)
tests(bot)
praktics(bot)
