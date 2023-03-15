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

# --------------------------------------- Тесты ----------------------------------------------------

# Функция отрисовки кнопок меню выброва тестов для Диадок
def test_DD(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Web', callback_data='Диадок.Тесты.Web')
    itembtn6 = types.InlineKeyboardButton('Интеграция', callback_data='Диадок.Тесты.Интеграция')
    itembtn5 = types.InlineKeyboardButton('Геракл', callback_data='Диадок.Тесты.Геракл')
    itembtn3 = types.InlineKeyboardButton('Роуминг', callback_data='Диадок.Тесты.Роуминг')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn6)
    markup.add(itembtn3, itembtn5)
    markup.add(itembtn12)

    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


# ---------------------------------- КЕЙСЫ --------------------------------------------------

# Функция отрисовки кнопок меню выброва кейсов для Диадок
def prk_diadoc(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn4 = types.InlineKeyboardButton('Админка и вн. сервисы', callback_data='DD.Case.Admin')
    itembtn5 = types.InlineKeyboardButton('Web', callback_data='DD.Case.Web')
    itembtn6 = types.InlineKeyboardButton('Интеграции', callback_data='DD.Case.Integrtion')
    itembtn7 = types.InlineKeyboardButton('Роуминг', callback_data='DD.Case.Roaming')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn4, itembtn5)
    markup.add(itembtn6, itembtn7)
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
    itembtn4 = types.InlineKeyboardButton('Аминка Диадока', callback_data='DD.Case.Admin.Админка Диадока')    
    itembtn5 = types.InlineKeyboardButton('Админка Портала', callback_data='DD.Case.Admin.Админка Портала')
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
    itembtn3 = types.InlineKeyboardButton('Документы', callback_data='DD.Case.Web.Документы')
    itembtn4 = types.InlineKeyboardButton('Настройки и реквизиты', callback_data='DD.Case.Web.Настройки и реквизиты')
    itembtn5 = types.InlineKeyboardButton('Маршруты', callback_data='DD.Case.Web.Маршруты')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5)
    markup.add(itembtn10)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)   


# DD.Case.Integrtion
def prk_diadoc_integration(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Документы', callback_data='DD.Case.Integrtion.Документы')
    itembtn2 = types.InlineKeyboardButton('Настройки и контрагенты', callback_data='DD.Case.Integrtion.Настройки и контрагенты')
    itembtn3 = types.InlineKeyboardButton('Ошибки', callback_data='DD.Case.Integrtion.Ошибки')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn10)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)   


# DD.Case.Roaming
def prk_diadoc_roaming(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Заявки', callback_data='DD.Case.Roaming.Заявки')
    itembtn2 = types.InlineKeyboardButton('Мониторинг роуминга', callback_data='DD.Case.Roaming.Мониторинг роуминга')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2)
    markup.add(itembtn10)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)   

DD_menu("Диaдoк", bot)
