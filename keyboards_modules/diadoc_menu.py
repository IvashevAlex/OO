import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def DD_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def menu(message):
        modul_for_bot.tests_data[message.chat.id] = 'DD'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)  # <--- тут будет отправка и меню с выбором

# --------------------------------------- ТЕСТЫ ----------------------------------------------------

# Функция отрисовки кнопок меню выброва тестов для Диадок
def test_DD(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Web', callback_data='Диадок.Тесты.Web')
    itembtn6 = types.InlineKeyboardButton('Интеграция', callback_data='Диадок.Тесты.Интеграция')
    itembtn5 = types.InlineKeyboardButton('Геракл', callback_data='DD.Tests.Геракл')
    itembtn3 = types.InlineKeyboardButton('Роуминг', callback_data='Диадок.Тесты.Роуминг')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn6)
    markup.add(itembtn3, itembtn5)
    markup.add(itembtn12)

    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


# DD.Test.Web
def test_diadoc_web(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)
    markup_test_web = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Общие', callback_data='DD.Tests.Web.Общее')
    itembtn2 = types.InlineKeyboardButton('Документы', callback_data='DD.Tests.Web.Документы')
    itembtn3 = types.InlineKeyboardButton('Настройки и реквизиты', callback_data='DD.Tests.Web.Настройки')
    itembtn4 = types.InlineKeyboardButton('Маршруты', callback_data='DD.Tests.Web.Маршруты')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup_test_web.add(itembtn1, itembtn2)
    markup_test_web.add(itembtn3, itembtn4)
    markup_test_web.add(itembtn10)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери подраздел:",
                        message_id=callback_query.message.message_id, reply_markup=markup_test_web)
    except Exception as e:
        print(e.args)

# DD.Test.Integrtion
def test_diadoc_integrtion(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)
    markup_test_int = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Общие', callback_data='DD.Tests.Int.Общие')
    itembtn2 = types.InlineKeyboardButton('Документы', callback_data='DD.Tests.Int.Документы')
    itembtn3 = types.InlineKeyboardButton('Настройки и компоненты', callback_data='DD.Tests.Int.Настройки')
    itembtn4 = types.InlineKeyboardButton('Ошибки', callback_data='DD.Tests.Int.Ошибки')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup_test_int.add(itembtn1, itembtn2)
    markup_test_int.add(itembtn3, itembtn4)
    markup_test_int.add(itembtn10)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери подраздел:",
                        message_id=callback_query.message.message_id, reply_markup=markup_test_int)
    except Exception as e:
        print(e.args)

# DD.Test.Roaming
def test_diadoc_roaming(bot, callback_query):
    print('IN test_diadoc_roaming')
    modul_for_bot.sql_user(bot, callback_query)
    markup_test_roam = types.InlineKeyboardMarkup()

    itembtn1 = types.InlineKeyboardButton('Общие', callback_data='DD.Tests.Roam.Общие')
    itembtn2 = types.InlineKeyboardButton('Мониторинг роуминга', callback_data='DD.Tests.Roam.Mon')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup_test_roam.add(itembtn1, itembtn2)
    markup_test_roam.add(itembtn10)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери подраздел:",
                        message_id=callback_query.message.message_id, reply_markup=markup_test_roam)
    except Exception as e:
        print(e.args)

# ---------------------------------- КЕЙСЫ --------------------------------------------------

# Функция отрисовки кнопок меню выброва кейсов для Диадок
def prk_diadoc(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn4 = types.InlineKeyboardButton('Админка и вн. сервисы', callback_data='DD.Case.Admin')
    itembtn5 = types.InlineKeyboardButton('Web', callback_data='DD.Case.Web')
    itembtn7 = types.InlineKeyboardButton('Роуминг', callback_data='DD.Case.Roam')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn7, itembtn5)
    markup.add(itembtn4)
    markup.add(itembtn12)
    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери подраздел:",
                            message_id=callback_query.message.message_id, reply_markup=markup)
        print('IN prk_diadoc callback_query.message.message_id:', callback_query.message.message_id)
    except Exception as e:
        print(e.args)


# DD.Case.Admin
def prk_diadoc_admin(bot, callback_query):
    print('IN prk_diadoc_admin')
    modul_for_bot.sql_user(bot, callback_query)

    markup_diadoc_adminka = types.InlineKeyboardMarkup()
    itembtn4 = types.InlineKeyboardButton('Аминка Диадока', callback_data='DD.Case.Admin.АдминкаДД')    
    itembtn5 = types.InlineKeyboardButton('Админка Портала', callback_data='DD.Case.Admin.АдминкаПР')
    itembtn6 = types.InlineKeyboardButton('Билли', callback_data='DD.Case.Admin.Билли')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup_diadoc_adminka.add(itembtn4, itembtn5)
    markup_diadoc_adminka.add(itembtn6)
    # markup.add(itembtn8) Коннекторы диадок
    markup_diadoc_adminka.add(itembtn12)
    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                              text="Выбери тему: ", reply_markup=markup_diadoc_adminka)
    except Exception as e:
        print(e.args)


# DD.Case.Web
def prk_diadoc_web(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Пользователи', callback_data='DD.Case.Web.Пользователи')
    itembtn2 = types.InlineKeyboardButton('Контрагенты', callback_data='DD.Case.Web.Контрагенты')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2)
    markup.add(itembtn10)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                            message_id=callback_query.message.message_id, reply_markup=markup)   
    except Exception as e:
        print(e.args)    

def prk_diadoc_roam(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Заявки', callback_data='DD.Case.Web.Заявки')
    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')
    
    markup.add(itembtn1)
    markup.add(itembtn10)

    try:
        bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                            message_id=callback_query.message.message_id, reply_markup=markup)   
    except Exception as e:
        print(e.args)   

DD_menu("Диaдoк", bot)
