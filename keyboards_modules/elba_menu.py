import modul_for_bot
import keyboards
from telebot import types
from WhiteList import bot


def Elba_menu(name, bot):
    @bot.message_handler(func=lambda message: message.text == name)
    def Elb_m(message):
        modul_for_bot.tests_data[message.chat.id] = 'ELB'
        modul_for_bot.sql_user(bot, message)
        keyboards.test_menu(bot, message)


def test_elb(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

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
    bot.edit_message_text("Выбери тему: ", chat_id=callback_query.from_user.id,
                          message_id=callback_query.message.message_id, reply_markup=markup)


def prk_elb(bot, callback_query):
    modul_for_bot.sql_user(bot, callback_query)

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
