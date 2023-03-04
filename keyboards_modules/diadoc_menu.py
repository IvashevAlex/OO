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


# Функция отрисовки кнопок меню выброва тестов для Диадок
def test_DD(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Web', callback_data='Web.Диадок')
    # itembtn2 = types.InlineKeyboardButton('Модуль', callback_data='Модуль.Диадок')
    itembtn6 = types.InlineKeyboardButton('Интеграции', callback_data='Интеграции.Диадок')
    # itembtn4 = types.InlineKeyboardButton('Коннекторы', callback_data='Коннекторы.Диадок')
    itembtn5 = types.InlineKeyboardButton('Геракл', callback_data='Геракл.Диадок')
    itembtn3 = types.InlineKeyboardButton('Роуминг', callback_data='Роуминг.Диадок')
    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn6)
    markup.add(itembtn3, itembtn5)
    markup.add(itembtn12)

    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


# Функция отрисовки кнопок меню выброва кейсов для Диадок
def prk_diadoc(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn4 = types.InlineKeyboardButton('Админка и вн. сервисы', callback_data='Админка.Диадок.Кейсы')    
    itembtn5 = types.InlineKeyboardButton('Web', callback_data='Web.Диадок.Кейсы')
    itembtn6 = types.InlineKeyboardButton('Интеграции', callback_data='Интеграции.Диадок.Кейсы')
    itembtn7 = types.InlineKeyboardButton('Роуминг', callback_data='Роуминг.Диадок.Кейсы')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn4, itembtn5)
    markup.add(itembtn6, itembtn7)
    # markup.add(itembtn8) Коннекторы диадок
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


# Админка.Диадок.Кейсы
def prk_diadoc_admin(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn4 = types.InlineKeyboardButton('Аминка Диадока', callback_data='Админка.Диадок.Кейсы.Аминка Диадока')    
    itembtn5 = types.InlineKeyboardButton('Админка Портала', callback_data='Админка.Диадок.Кейсы.Админка Портала')
    itembtn6 = types.InlineKeyboardButton('Билли', callback_data='Админка.Диадок.Кейсы.Билли')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn4, itembtn5)
    markup.add(itembtn6)
    # markup.add(itembtn8) Коннекторы диадок
    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)    


# Web.Диадок.Кейсы
def prk_diadoc_web(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Пользователи', callback_data='WEB.Диадок.Кейсы.Пользователи')
    itembtn2 = types.InlineKeyboardButton('Контрагенты', callback_data='WEB.Диадок.Кейсы.Контрагенты')
    itembtn3 = types.InlineKeyboardButton('Документы', callback_data='WEB.Диадок.Кейсы.Документы')
    itembtn4 = types.InlineKeyboardButton('Настройки и реквизиты', callback_data='WEB.Диадок.Кейсы.Настройки и реквизиты')
    itembtn5 = types.InlineKeyboardButton('Маршруты', callback_data='WEB.Диадок.Кейсы.Маршруты')


    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn4, itembtn5)
    markup.add(itembtn10)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)   


# Интеграции.Диадок.Кейсы
def prk_diadoc_integration(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Документы', callback_data='Интеграции.Диадок.Кейсы.Документы')
    itembtn2 = types.InlineKeyboardButton('Настройки и контрагенты', callback_data='Интеграции.Диадок.Кейсы.Настройки и контрагенты')
    itembtn3 = types.InlineKeyboardButton('Ошибки', callback_data='Интеграции.Диадок.Кейсы.Ошибки')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2, itembtn3)
    markup.add(itembtn10)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)   


# Роуминг.Диадок.Кейсы
def prk_diadoc_roaming(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn1 = types.InlineKeyboardButton('Заявки', callback_data='Роуминг.Диадок.Кейсы.Заявки')
    itembtn2 = types.InlineKeyboardButton('Мониторинг роуминга', callback_data='Роуминг.Диадок.Кейсы.Мониторинг роуминга')

    itembtn10 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn1, itembtn2)
    markup.add(itembtn10)

    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)   

DD_menu("Диaдoк", bot)
