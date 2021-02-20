import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def Buh_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Buh_m(message):
        modul_for_bot.tests_data[message.chat.id] = 'BUH'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)


def test_buh(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

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
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_buh(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

    markup = types.InlineKeyboardMarkup()
    itembtn8 = types.InlineKeyboardButton(
        'Работа в сервисе', callback_data='Работа в сервисе')

    itembtn12 = types.InlineKeyboardButton('Назад', callback_data='Назад')

    markup.add(itembtn8)

    markup.add(itembtn12)
    bot.edit_message_text(chat_id=callback_query.from_user.id, text="Выбери тему: ",
                          message_id=callback_query.message.message_id, reply_markup=markup)


Buh_menu("Бухгaлтерия", bot)
